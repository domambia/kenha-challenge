import { useEffect, useState, lazy, Suspense } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  AlertCircle,
  CheckCircle2,
  Clock,
  TrendingUp,
  MapPin,
  Users,
  Camera,
  Activity,
  Calendar,
  Maximize2,
  Minimize2
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { incidentsAPI, Incident } from "@/lib/incidents-api";
import { analyticsAPI } from "@/lib/analytics-api";
import { useToast } from "@/hooks/use-toast";
import { formatDistanceToNow, format, startOfDay, endOfDay } from "date-fns";

// Dynamically import IncidentHeatmap to avoid SSR issues with Leaflet
const IncidentHeatmap = lazy(() => import("@/components/IncidentHeatmap"));

const Dashboard = () => {
  const { toast } = useToast();
  const navigate = useNavigate();
  const [recentIncidents, setRecentIncidents] = useState<Incident[]>([]);

  // Map filters
  const [mapDate, setMapDate] = useState<string>(format(new Date(), 'yyyy-MM-dd')); // Default to today
  const [mapStatus, setMapStatus] = useState<string>('all'); // all, in_progress, resolved, closed
  const [isMapMaximized, setIsMapMaximized] = useState(false);

  // Fetch incidents
  const { data: incidentsData, isLoading: incidentsLoading } = useQuery({
    queryKey: ['incidents', 'dashboard'],
    queryFn: () => incidentsAPI.getAll({ status: 'active' }),
  });

  const incidents = incidentsData?.results || [];

  // Show error toast if incidents fetch fails
  useEffect(() => {
    if (incidentsLoading === false && incidents.length === 0) {
      // Could optionally show a toast here, but let's not spam it
    }
  }, [incidents, incidentsLoading]);

  // Fetch dashboard stats (if endpoint exists)
  const { data: dashboardData, isLoading: statsLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      try {
        return await analyticsAPI.getDashboard();
      } catch (error) {
        // If analytics endpoint doesn't exist, return null and calculate from incidents
        return null;
      }
    },
    retry: false,
  });

  useEffect(() => {
    if (Array.isArray(incidents) && incidents.length > 0) {
      // Get recent 4 incidents, sorted by timestamp
      const sorted = [...incidents]
        .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
        .slice(0, 4);
      setRecentIncidents(sorted);
    } else {
      setRecentIncidents([]);
    }
  }, [incidents]);

  // Calculate stats from analytics API or incidents data
  const stats = dashboardData?.stats ? [
    {
      icon: <AlertCircle className="w-6 h-6" />,
      label: "Active Incidents",
      value: dashboardData.stats.active_incidents.toString(),
      change: undefined,
      color: "emergency"
    },
    {
      icon: <CheckCircle2 className="w-6 h-6" />,
      label: "Resolved Incidents",
      value: dashboardData.stats.resolved_incidents.toString(),
      change: undefined,
      color: "primary"
    },
    {
      icon: <Clock className="w-6 h-6" />,
      label: "Avg Response Time",
      value: dashboardData.stats.avg_response_time_minutes > 0
        ? `${dashboardData.stats.avg_response_time_minutes.toFixed(1)}min`
        : "N/A",
      change: undefined,
      color: "trust"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      label: "Total Incidents",
      value: dashboardData.stats.total_incidents.toString(),
      change: undefined,
      color: "warning"
    }
  ] : [
    {
      icon: <AlertCircle className="w-6 h-6" />,
      label: "Active Incidents",
      value: Array.isArray(incidents) ? incidents.filter(i => i.status !== 'closed').length.toString() : "0",
      change: undefined,
      color: "emergency"
    },
    {
      icon: <CheckCircle2 className="w-6 h-6" />,
      label: "Total Incidents",
      value: Array.isArray(incidents) ? incidents.length.toString() : "0",
      change: undefined,
      color: "primary"
    },
    {
      icon: <Clock className="w-6 h-6" />,
      label: "Recent Activity",
      value: recentIncidents.length > 0 ? formatDistanceToNow(new Date(recentIncidents[0]?.created_at || ''), { addSuffix: true }) : "No activity",
      change: undefined,
      color: "trust"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      label: "Verified Incidents",
      value: Array.isArray(incidents) ? incidents.filter(i => i.verification_status === 'verified').length.toString() : "0",
      change: undefined,
      color: "warning"
    }
  ];

  const iotDevices = dashboardData?.iot_status ? [
    { icon: <Camera className="w-5 h-5" />, label: "CCTV Cameras", value: dashboardData.iot_status.cctv_cameras.online.toString(), status: "Online" },
    { icon: <MapPin className="w-5 h-5" />, label: "RFID Readers", value: dashboardData.iot_status.rfid_readers.online.toString(), status: "Online" },
    { icon: <Activity className="w-5 h-5" />, label: "Traffic Sensors", value: dashboardData.iot_status.traffic_sensors.online.toString(), status: "Online" },
    { icon: <Users className="w-5 h-5" />, label: "Active Responders", value: dashboardData.iot_status.active_responders.toString(), status: "Active" }
  ] : [
    { icon: <Camera className="w-5 h-5" />, label: "CCTV Cameras", value: "0", status: "Offline" },
    { icon: <MapPin className="w-5 h-5" />, label: "RFID Readers", value: "0", status: "Offline" },
    { icon: <Activity className="w-5 h-5" />, label: "Traffic Sensors", value: "0", status: "Offline" },
    { icon: <Users className="w-5 h-5" />, label: "Active Responders", value: "0", status: "Inactive" }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "P1":
      case "critical":
        return "emergency";
      case "P2":
      case "high":
        return "warning";
      case "P3":
      case "medium":
        return "trust";
      case "low":
        return "muted";
      default: return "muted";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "in_progress":
      case "in progress":
        return "trust";
      case "assigned":
        return "primary";
      case "pending":
        return "warning";
      case "verified":
        return "primary";
      case "closed":
        return "muted";
      default: return "muted";
    }
  };

  const formatTimeAgo = (dateString: string) => {
    try {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true });
    } catch {
      return "Unknown";
    }
  };

  // Fetch incidents for map with date and status filters
  const getDateRange = (dateStr: string) => {
    const date = new Date(dateStr);
    const start = startOfDay(date).toISOString();
    const end = endOfDay(date).toISOString();
    return { start, end };
  };

  const { data: mapIncidentsData, isLoading: mapIncidentsLoading } = useQuery({
    queryKey: ['incidents', 'map', mapDate, mapStatus],
    queryFn: async () => {
      const { start, end } = getDateRange(mapDate);
      const params: { created_at__gte?: string; created_at__lte?: string; status?: string } = {
        created_at__gte: start,
        created_at__lte: end,
      };

      if (mapStatus !== 'all') {
        params.status = mapStatus;
      }

      // Fetch all pages for map
      return await incidentsAPI.getAllFlat(params);
    },
  });

  const mapIncidents = mapIncidentsData || [];

  const isLoading = incidentsLoading || statsLoading;

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 pt-20 pb-12">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
              Operations Dashboard
            </h1>
            <p className="text-muted-foreground">
              Real-time monitoring and incident management
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {stats.map((stat, index) => (
              <Card key={index} className="p-6 bg-card border-border hover:shadow-lg transition-all">
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 rounded-lg bg-${stat.color}/10 flex items-center justify-center text-${stat.color}`}>
                    {stat.icon}
                  </div>
                  {stat.change && (
                    <span className={`text-sm font-medium ${stat.change.startsWith('+') ? 'text-primary' : 'text-emergency'}`}>
                      {stat.change}
                    </span>
                  )}
                </div>
                <div className="text-2xl font-bold text-foreground mb-1">
                  {isLoading ? "..." : stat.value}
                </div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </Card>
            ))}
          </div>



          {/* Incident Heatmap */}
          <Card className="mt-6 p-6 bg-card border-border">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
              <div className="flex items-center gap-3">
                <h2 className="text-xl font-semibold text-foreground">Incident Heatmap</h2>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsMapMaximized(true)}
                  className="flex items-center gap-2"
                >
                  <Maximize2 className="w-4 h-4" />
                  <span className="hidden sm:inline">Maximize</span>
                </Button>
              </div>

              {/* Map Filters */}
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="flex items-center gap-2">
                  <Label htmlFor="map-date" className="text-sm whitespace-nowrap">
                    <Calendar className="w-4 h-4 inline mr-1" />
                    Date:
                  </Label>
                  <Input
                    id="map-date"
                    type="date"
                    value={mapDate}
                    onChange={(e) => setMapDate(e.target.value)}
                    className="w-[150px]"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <Label htmlFor="map-status" className="text-sm whitespace-nowrap">
                    Status:
                  </Label>
                  <Select value={mapStatus} onValueChange={setMapStatus}>
                    <SelectTrigger id="map-status" className="w-[150px]">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Status</SelectItem>
                      <SelectItem value="in_progress">In Progress</SelectItem>
                      <SelectItem value="assigned">Assigned</SelectItem>
                      <SelectItem value="pending">Pending</SelectItem>
                      <SelectItem value="resolved">Resolved</SelectItem>
                      <SelectItem value="closed">Closed</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setMapDate(format(new Date(), 'yyyy-MM-dd'));
                    setMapStatus('all');
                  }}
                >
                  Reset
                </Button>
              </div>
            </div>

            {mapIncidentsLoading ? (
              <div className="h-96 bg-muted rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                  <p className="text-muted-foreground">Loading incidents...</p>
                </div>
              </div>
            ) : (
              <div className="h-96 rounded-lg overflow-hidden border border-border">
                <Suspense fallback={
                  <div className="h-full flex items-center justify-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                  </div>
                }>
                  <IncidentHeatmap incidents={mapIncidents} />
                </Suspense>
              </div>
            )}

            {!mapIncidentsLoading && mapIncidents.length > 0 && (
              <p className="text-xs text-muted-foreground mt-2 text-center">
                Showing {mapIncidents.length} incident(s) for {format(new Date(mapDate), 'MMMM d, yyyy')}
                {mapStatus !== 'all' && ` with status: ${mapStatus}`}
              </p>
            )}
            {!mapIncidentsLoading && mapIncidents.length === 0 && (
              <p className="text-xs text-muted-foreground mt-2 text-center">
                No incidents found for {format(new Date(mapDate), 'MMMM d, yyyy')}
                {mapStatus !== 'all' && ` with status: ${mapStatus}`}
              </p>
            )}
          </Card>

          {/* Maximized Map Dialog */}
          <Dialog open={isMapMaximized} onOpenChange={setIsMapMaximized}>
            <DialogContent className="max-w-[95vw] w-[95vw] h-[95vh] p-0 flex flex-col translate-x-[-50%] translate-y-[-50%] left-[50%] top-[50%]">
              <DialogHeader className="px-6 pt-6 pb-4 border-b">
                <div className="flex items-center justify-between">
                  <DialogTitle className="text-2xl font-semibold">Incident Heatmap</DialogTitle>
                  <div className="flex items-center gap-3">
                    {/* Filters in maximized view */}
                    <div className="flex flex-col sm:flex-row gap-3">
                      <div className="flex items-center gap-2">
                        <Label htmlFor="map-date-max" className="text-sm whitespace-nowrap">
                          <Calendar className="w-4 h-4 inline mr-1" />
                          Date:
                        </Label>
                        <Input
                          id="map-date-max"
                          type="date"
                          value={mapDate}
                          onChange={(e) => setMapDate(e.target.value)}
                          className="w-[150px]"
                        />
                      </div>
                      <div className="flex items-center gap-2">
                        <Label htmlFor="map-status-max" className="text-sm whitespace-nowrap">
                          Status:
                        </Label>
                        <Select value={mapStatus} onValueChange={setMapStatus}>
                          <SelectTrigger id="map-status-max" className="w-[150px]">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="all">All Status</SelectItem>
                            <SelectItem value="in_progress">In Progress</SelectItem>
                            <SelectItem value="assigned">Assigned</SelectItem>
                            <SelectItem value="pending">Pending</SelectItem>
                            <SelectItem value="resolved">Resolved</SelectItem>
                            <SelectItem value="closed">Closed</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setMapDate(format(new Date(), 'yyyy-MM-dd'));
                          setMapStatus('all');
                        }}
                      >
                        Reset
                      </Button>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setIsMapMaximized(false)}
                      className="flex items-center gap-2"
                    >
                      <Minimize2 className="w-4 h-4" />
                      <span className="hidden sm:inline">Minimize</span>
                    </Button>
                  </div>
                </div>
              </DialogHeader>

              <div className="flex-1 relative min-h-0">
                {mapIncidentsLoading ? (
                  <div className="h-full bg-muted flex items-center justify-center">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                      <p className="text-muted-foreground">Loading incidents...</p>
                    </div>
                  </div>
                ) : (
                  <div className="h-full w-full">
                    <Suspense fallback={
                      <div className="h-full flex items-center justify-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                      </div>
                    }>
                      <IncidentHeatmap incidents={mapIncidents} key="maximized" />
                    </Suspense>
                  </div>
                )}
              </div>

              {!mapIncidentsLoading && (
                <div className="px-6 py-3 border-t bg-muted/50">
                  <p className="text-xs text-muted-foreground text-center">
                    {mapIncidents.length > 0 ? (
                      <>Showing {mapIncidents.length} incident(s) for {format(new Date(mapDate), 'MMMM d, yyyy')}
                        {mapStatus !== 'all' && ` with status: ${mapStatus}`}</>
                    ) : (
                      <>No incidents found for {format(new Date(mapDate), 'MMMM d, yyyy')}
                        {mapStatus !== 'all' && ` with status: ${mapStatus}`}</>
                    )}
                  </p>
                </div>
              )}
            </DialogContent>
          </Dialog>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Dashboard;
