import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Shield } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useAuthStore } from "@/store/auth-store";

const Register = () => {
  const { toast } = useToast();
  const navigate = useNavigate();
  const { register, isLoading, error, clearError, isAuthenticated } = useAuthStore();
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    role: "",
    password: "",
    password_confirm: "",
  });

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // Show error toast when error occurs
  useEffect(() => {
    if (error) {
      toast({
        title: "Registration Failed",
        description: error,
        variant: "destructive",
      });
      clearError();
    }
  }, [error, toast, clearError]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();

    // Validate passwords match
    if (formData.password !== formData.password_confirm) {
      toast({
        title: "Validation Error",
        description: "Passwords do not match",
        variant: "destructive",
      });
      return;
    }

    try {
      const response = await register({
        email: formData.email,
        phone: formData.phone,
        password: formData.password,
        password_confirm: formData.password_confirm,
        first_name: formData.first_name,
        last_name: formData.last_name,
        role: formData.role,
      });

      toast({
        title: "Registration Successful",
        description: response.message || "Please check your email to verify your account.",
      });

      // Redirect to login page
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      // Error is handled by the store and useEffect
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  const handleSelectChange = (value: string) => {
    setFormData({
      ...formData,
      role: value,
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/30 px-4 py-12">
      <Card className="w-full max-w-md p-8 bg-card border-border">
        {/* Logo */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center gap-2">
            <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center">
              <Shield className="w-7 h-7 text-primary-foreground" />
            </div>
            <div>
              <div className="text-xl font-bold text-foreground">KeNHA eSafety</div>
              <div className="text-xs text-muted-foreground">Road Safety Management</div>
            </div>
          </div>
        </div>

        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-foreground mb-2">Create Account</h1>
          <p className="text-sm text-muted-foreground">Register to report and track road incidents</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="first_name">First Name</Label>
              <Input
                id="first_name"
                type="text"
                placeholder="John"
                value={formData.first_name}
                onChange={handleChange}
                required
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="last_name">Last Name</Label>
              <Input
                id="last_name"
                type="text"
                placeholder="Doe"
                value={formData.last_name}
                onChange={handleChange}
                required
                disabled={isLoading}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="john.doe@example.com"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={isLoading}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="phone">Phone Number</Label>
            <Input
              id="phone"
              type="tel"
              placeholder="+254 700 000 000"
              value={formData.phone}
              onChange={handleChange}
              required
              disabled={isLoading}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="role">Account Type</Label>
            <Select required value={formData.role} onValueChange={handleSelectChange} disabled={isLoading}>
              <SelectTrigger id="role">
                <SelectValue placeholder="Select your role" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="road_user">Registered Road User</SelectItem>
                <SelectItem value="kenha_staff">KeNHA Staff</SelectItem>
                <SelectItem value="emergency_services">Emergency Services</SelectItem>
                <SelectItem value="police">Police Services</SelectItem>
                <SelectItem value="maintenance">Maintenance Crew</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="Create a strong password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={isLoading}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password_confirm">Confirm Password</Label>
            <Input
              id="password_confirm"
              type="password"
              placeholder="Re-enter your password"
              value={formData.password_confirm}
              onChange={handleChange}
              required
              disabled={isLoading}
            />
          </div>

          <div className="flex items-start gap-2">
            <input type="checkbox" id="terms" className="mt-1" required disabled={isLoading} />
            <Label htmlFor="terms" className="text-xs text-muted-foreground cursor-pointer">
              I agree to the Terms of Service and Privacy Policy
            </Label>
          </div>

          <Button type="submit" className="w-full" disabled={isLoading || !formData.role}>
            {isLoading ? "Creating account..." : "Create Account"}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link to="/login" className="text-primary font-medium hover:underline">
              Sign in here
            </Link>
          </p>
        </div>

        <div className="mt-6 pt-6 border-t border-border">
          <Link to="/">
            <Button variant="ghost" className="w-full">
              Back to Home
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default Register;
