import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authAPI, User, LoginCredentials, RegisterData } from '@/lib/auth-api';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<{ message: string; user_id: number }>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  clearError: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials: LoginCredentials) => {
        try {
          set({ isLoading: true, error: null });
          const response = await authAPI.login(credentials);

          // Store tokens in localStorage (also handled by persist middleware)
          localStorage.setItem('access_token', response.access);
          localStorage.setItem('refresh_token', response.refresh);
          localStorage.setItem('user', JSON.stringify(response.user));

          set({
            user: response.user,
            accessToken: response.access,
            refreshToken: response.refresh,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage =
            error.response?.data?.error ||
            error.response?.data?.message ||
            error.message ||
            'Login failed. Please try again.';
          set({
            error: errorMessage,
            isLoading: false,
            isAuthenticated: false,
          });
          throw error;
        }
      },

      register: async (data: RegisterData) => {
        try {
          set({ isLoading: true, error: null });
          const response = await authAPI.register(data);
          set({ isLoading: false, error: null });
          return response;
        } catch (error: any) {
          const errorMessage =
            error.response?.data?.error ||
            error.response?.data?.message ||
            error.message ||
            'Registration failed. Please try again.';
          set({
            error: errorMessage,
            isLoading: false,
          });
          throw error;
        }
      },

      logout: async () => {
        try {
          await authAPI.logout();
        } catch (error) {
          // Continue with logout even if API call fails
          console.error('Logout API error:', error);
        } finally {
          // Clear local storage
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');

          set({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
            error: null,
          });
        }
      },

      loadUser: async () => {
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            set({ isAuthenticated: false, user: null });
            return;
          }

          set({ isLoading: true, error: null });
          const user = await authAPI.getProfile();
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          // Token might be invalid, clear auth state
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          set({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      },

      clearError: () => {
        set({ error: null });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Initialize auth state on app load
if (typeof window !== 'undefined') {
  const storedToken = localStorage.getItem('access_token');
  const storedUser = localStorage.getItem('user');
  
  if (storedToken && storedUser) {
    useAuthStore.setState({
      accessToken: storedToken,
      refreshToken: localStorage.getItem('refresh_token'),
      user: JSON.parse(storedUser),
      isAuthenticated: true,
    });
  }
}

