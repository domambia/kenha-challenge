import { useEffect } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/auth-store';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const { isAuthenticated, isLoading, loadUser, accessToken } = useAuthStore();
    const location = useLocation();

    useEffect(() => {
        // If we have a token but user is not loaded, try to load it
        if (accessToken && !isAuthenticated && !isLoading) {
            loadUser();
        }
    }, [accessToken, isAuthenticated, isLoading, loadUser]);

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Loading...</p>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        // Redirect to login with return url
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    return <>{children}</>;
};

