import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AlertCircle, Camera, MapPin, Upload, CheckCircle2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { incidentsAPI, CreateIncidentData } from "@/lib/incidents-api";

const ReportIncident = () => {
  const { toast } = useToast();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [locationError, setLocationError] = useState<string | null>(null);
  const [coordinates, setCoordinates] = useState<{ latitude: number; longitude: number } | null>(null);
  const [formData, setFormData] = useState({
    type: "",
    severity: "",
    road_name: "",
    description: "",
    anonymous: false
  });

  // Format coordinate to ensure no more than 6 decimal places and 9 digits total
  const formatCoordinate = (coord: number): number => {
    // Backend requires maximum 6 decimal places
    // Round to 6 decimal places (which is standard precision for GPS coordinates)
    return parseFloat(coord.toFixed(6));
  };

  // Get user's current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCoordinates({
            latitude: formatCoordinate(position.coords.latitude),
            longitude: formatCoordinate(position.coords.longitude),
          });
          setLocationError(null);
        },
        (error) => {
          setLocationError("Unable to get your location. Please enter coordinates manually.");
          console.error("Geolocation error:", error);
        }
      );
    } else {
      setLocationError("Geolocation is not supported by your browser.");
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!coordinates) {
      toast({
        title: "Location Required",
        description: "Please enable location services or enter coordinates manually.",
        variant: "destructive",
      });
      return;
    }

    if (!formData.type || !formData.severity || !formData.description) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);

    try {
      // Format coordinates to ensure they meet the 9-digit requirement
      const formattedLat = formatCoordinate(coordinates.latitude);
      const formattedLng = formatCoordinate(coordinates.longitude);

      const incidentData: CreateIncidentData = {
        incident_type: parseInt(formData.type),
        severity: formData.severity,
        description: formData.description,
        latitude: formattedLat,
        longitude: formattedLng,
        road_name: formData.road_name || undefined,
        timestamp: new Date().toISOString(),
      };

      await incidentsAPI.create(incidentData);

      toast({
        title: "Incident Reported Successfully",
        description: "Your incident report has been received and is being processed.",
      });

      // Reset form
      setFormData({
        type: "",
        severity: "",
        road_name: "",
        description: "",
        anonymous: false
      });

      // Navigate to incidents list
      setTimeout(() => {
        navigate("/incidents");
      }, 1500);
    } catch (error: any) {
      toast({
        title: "Submission Failed",
        description: error.response?.data?.message || "Failed to submit incident report. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 pt-20 pb-12">
        <div className="container mx-auto px-4 max-w-4xl">
          {/* Header */}
          <div className="mb-8 text-center">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
              Report a Road Incident
            </h1>
            <p className="text-muted-foreground">
              Your report helps keep our roads safe. All reports are verified by AI and responded to promptly.
            </p>
          </div>

          {/* Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <Card className="p-4 bg-card border-border">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <div className="font-semibold text-foreground text-sm">Anonymous Reporting</div>
                  <div className="text-xs text-muted-foreground">Your privacy protected</div>
                </div>
              </div>
            </Card>
            <Card className="p-4 bg-card border-border">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-trust/10 flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-trust" />
                </div>
                <div>
                  <div className="font-semibold text-foreground text-sm">AI Verification</div>
                  <div className="text-xs text-muted-foreground">Instant validation</div>
                </div>
              </div>
            </Card>
            <Card className="p-4 bg-card border-border">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-warning/10 flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-warning" />
                </div>
                <div>
                  <div className="font-semibold text-foreground text-sm">Fast Response</div>
                  <div className="text-xs text-muted-foreground">&lt;5 min average</div>
                </div>
              </div>
            </Card>
          </div>

          {/* Report Form */}
          <Card className="p-6 md:p-8 bg-card border-border">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Incident Type */}
              <div className="space-y-2">
                <Label htmlFor="type">Incident Type *</Label>
                <Select
                  value={formData.type}
                  onValueChange={(value) => setFormData({ ...formData, type: value })}
                  required
                  disabled={isSubmitting}
                >
                  <SelectTrigger id="type">
                    <SelectValue placeholder="Select incident type" />
                  </SelectTrigger>
                  <SelectContent>
                    {/* Note: In a real app, these should be fetched from the backend */}
                    <SelectItem value="1">Traffic Accident</SelectItem>
                    <SelectItem value="2">Road Hazard</SelectItem>
                    <SelectItem value="3">Infrastructure Damage</SelectItem>
                    <SelectItem value="4">Vandalism</SelectItem>
                    <SelectItem value="5">Other</SelectItem>
                  </SelectContent>
                </Select>
                <p className="text-xs text-muted-foreground">
                  Note: Incident types are predefined in the system
                </p>
              </div>

              {/* Severity */}
              <div className="space-y-2">
                <Label htmlFor="severity">Severity Level *</Label>
                <Select
                  value={formData.severity}
                  onValueChange={(value) => setFormData({ ...formData, severity: value })}
                  required
                  disabled={isSubmitting}
                >
                  <SelectTrigger id="severity">
                    <SelectValue placeholder="Select severity" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="P1">P1 - Critical (Life threatening)</SelectItem>
                    <SelectItem value="P2">P2 - High (Major disruption)</SelectItem>
                    <SelectItem value="P3">P3 - Medium (Moderate impact)</SelectItem>
                    <SelectItem value="P4">P4 - Low (Minor issue)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Location */}
              <div className="space-y-2">
                <Label htmlFor="road_name">Location *</Label>
                <div className="relative">
                  <MapPin className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="road_name"
                    placeholder="Highway name, KM marker, or nearest landmark"
                    className="pl-10"
                    value={formData.road_name}
                    onChange={(e) => setFormData({ ...formData, road_name: e.target.value })}
                    required
                  />
                </div>
                {coordinates ? (
                  <p className="text-xs text-muted-foreground">
                    GPS: {coordinates.latitude.toFixed(6)}, {coordinates.longitude.toFixed(6)}
                  </p>
                ) : (
                  <p className="text-xs text-warning">
                    {locationError || "Requesting location..."}
                  </p>
                )}
              </div>

              {/* Description */}
              <div className="space-y-2">
                <Label htmlFor="description">Detailed Description *</Label>
                <Textarea
                  id="description"
                  placeholder="Describe what happened, number of vehicles involved, injuries, traffic conditions, etc."
                  rows={5}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  required
                  disabled={isSubmitting}
                />
              </div>

              {/* Photo Upload */}
              <div className="space-y-2">
                <Label htmlFor="photos">Photos / Videos (Optional)</Label>
                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer">
                  <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                  <p className="text-sm text-foreground mb-1">Click to upload or drag and drop</p>
                  <p className="text-xs text-muted-foreground">PNG, JPG, MP4 up to 10MB each</p>
                  <p className="text-xs text-muted-foreground mt-2">(Media upload will be implemented in a future update)</p>
                  <Button type="button" variant="outline" size="sm" className="mt-4" disabled>
                    <Camera className="w-4 h-4 mr-2" />
                    Choose Files
                  </Button>
                </div>
              </div>

              {/* Anonymous Toggle */}
              <div className="flex items-center gap-2 p-4 bg-muted/50 rounded-lg">
                <input
                  type="checkbox"
                  id="anonymous"
                  className="w-4 h-4"
                  checked={formData.anonymous}
                  onChange={(e) => setFormData({ ...formData, anonymous: e.target.checked })}
                  disabled={isSubmitting}
                />
                <Label htmlFor="anonymous" className="cursor-pointer">
                  Submit anonymously (your identity will be protected)
                </Label>
              </div>
              <p className="text-xs text-muted-foreground">
                Note: Anonymous reporting is handled automatically by the backend
              </p>

              {/* Submit Button */}
              <div className="flex gap-4">
                <Button
                  type="submit"
                  size="lg"
                  className="flex-1"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? "Submitting..." : "Submit Report"}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  size="lg"
                  onClick={() => setFormData({
                    type: "",
                    severity: "",
                    road_name: "",
                    description: "",
                    anonymous: false
                  })}
                  disabled={isSubmitting}
                >
                  Clear
                </Button>
              </div>
            </form>
          </Card>

          {/* Emergency Notice */}
          <Card className="mt-6 p-4 bg-emergency/10 border-emergency/20">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-emergency flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-emergency mb-1">Life-Threatening Emergency?</p>
                <p className="text-sm text-foreground">For immediate emergency assistance, call <span className="font-bold">999</span> or <span className="font-bold">112</span></p>
              </div>
            </div>
          </Card>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ReportIncident;
