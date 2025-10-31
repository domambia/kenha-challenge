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
  Minimize2,
  Gauge,
  Cloud,
  Radio,
  Thermometer,
  Droplets,
  Wind,
  Eye,
  Navigation
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

  // Fetch traffic flow data
  const { data: trafficFlowData, isLoading: trafficLoading } = useQuery({
    queryKey: ['traffic-flow'],
    queryFn: () => analyticsAPI.getTrafficFlow(24),
    enabled: !!dashboardData,
    retry: false,
  });

  // Fetch weather data
  const { data: weatherData, isLoading: weatherLoading } = useQuery({
    queryKey: ['weather'],
    queryFn: () => analyticsAPI.getWeather(),
    enabled: !!dashboardData,
    retry: false,
  });

  // Fetch road conditions
  const { data: roadConditionsData, isLoading: roadConditionsLoading } = useQuery({
    queryKey: ['road-conditions'],
    queryFn: () => analyticsAPI.getRoadConditions(),
    enabled: !!dashboardData,
    retry: false,
  });

  const iotDevices = dashboardData?.iot_status ? [
    {
      icon: <Camera className="w-5 h-5" />,
      label: "CCTV Cameras",
      value: `${dashboardData.iot_status.cctv_cameras.online}/${dashboardData.iot_status.cctv_cameras.total}`,
      status: dashboardData.iot_status.cctv_cameras.online > 0 ? "Online" : "Offline",
      total: dashboardData.iot_status.cctv_cameras.total,
      online: dashboardData.iot_status.cctv_cameras.online
    },
    {
      icon: <Radio className="w-5 h-5" />,
      label: "RFID Readers",
      value: `${dashboardData.iot_status.rfid_readers.online}/${dashboardData.iot_status.rfid_readers.total}`,
      status: dashboardData.iot_status.rfid_readers.online > 0 ? "Online" : "Offline",
      total: dashboardData.iot_status.rfid_readers.total,
      online: dashboardData.iot_status.rfid_readers.online
    },
    {
      icon: <Activity className="w-5 h-5" />,
      label: "Traffic Sensors",
      value: `${dashboardData.iot_status.traffic_sensors.online}/${dashboardData.iot_status.traffic_sensors.total}`,
      status: dashboardData.iot_status.traffic_sensors.online > 0 ? "Online" : "Offline",
      total: dashboardData.iot_status.traffic_sensors.total,
      online: dashboardData.iot_status.traffic_sensors.online
    },
    {
      icon: <Users className="w-5 h-5" />,
      label: "Active Responders",
      value: dashboardData.iot_status.active_responders.toString(),
      status: "Active"
    }
  ] : [
    { icon: <Camera className="w-5 h-5" />, label: "CCTV Cameras", value: "0/0", status: "Offline", total: 0, online: 0 },
    { icon: <Radio className="w-5 h-5" />, label: "RFID Readers", value: "0/0", status: "Offline", total: 0, online: 0 },
    { icon: <Activity className="w-5 h-5" />, label: "Traffic Sensors", value: "0/0", status: "Offline", total: 0, online: 0 },
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

          {/* Traffic & IoT Information Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Traffic Flow Summary */}
            <Card className="p-6 bg-card border-border">
              <div className="flex items-center gap-3 mb-4">
                <Gauge className="w-6 h-6 text-primary" />
                <h2 className="text-xl font-semibold text-foreground">Traffic Flow</h2>
              </div>
              {trafficLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                  <p className="text-muted-foreground">Loading traffic data...</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {dashboardData?.traffic_summary ? (
                    <>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <div className="text-sm text-muted-foreground mb-1">Vehicles (24h)</div>
                          <div className="text-2xl font-bold text-foreground">
                            {dashboardData.traffic_summary.total_vehicles_24h.toLocaleString()}
                          </div>
                        </div>
                        <div>
                          <div className="text-sm text-muted-foreground mb-1">Avg Speed</div>
                          <div className="text-2xl font-bold text-foreground">
                            {dashboardData.traffic_summary.avg_speed_kmh
                              ? `${dashboardData.traffic_summary.avg_speed_kmh} km/h`
                              : "N/A"}
                          </div>
                        </div>
                      </div>
                      {trafficFlowData?.timeline && trafficFlowData.timeline.length > 0 && (
                        <div className="pt-4 border-t">
                          <div className="text-sm text-muted-foreground mb-2">Recent Activity</div>
                          <div className="space-y-2 max-h-32 overflow-y-auto">
                            {trafficFlowData.timeline.slice(0, 5).map((item, idx) => (
                              <div key={idx} className="flex justify-between text-sm">
                                <span className="text-muted-foreground">
                                  {format(new Date(item.timestamp), 'HH:mm')}
                                </span>
                                <span className="font-medium">
                                  {item.vehicle_count} vehicles
                                  {item.avg_speed && ` @ ${item.avg_speed} km/h`}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">
                      No traffic data available
                    </div>
                  )}
                </div>
              )}
            </Card>

            {/* IoT Device Status */}
            <Card className="p-6 bg-card border-border">
              <div className="flex items-center gap-3 mb-4">
                <Activity className="w-6 h-6 text-primary" />
                <h2 className="text-xl font-semibold text-foreground">IoT Device Status</h2>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {iotDevices.map((device, index) => (
                  <div key={index} className="p-3 rounded-lg bg-muted/50">
                    <div className="flex items-center gap-2 mb-2">
                      <div className={`text-${device.status === 'Online' || device.status === 'Active' ? 'primary' : 'muted-foreground'}`}>
                        {device.icon}
                      </div>
                      <div className="text-sm font-medium text-foreground">{device.label}</div>
                    </div>
                    <div className="text-xl font-bold text-foreground mb-1">{device.value}</div>
                    <div className={`text-xs ${device.status === 'Online' || device.status === 'Active'
                        ? 'text-primary'
                        : 'text-muted-foreground'
                      }`}>
                      {device.status}
                      {device.total && device.total > 0 && (
                        <span className="ml-1">
                          ({Math.round((device.online / device.total) * 100)}%)
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Weather & Road Conditions Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Weather Conditions */}
            <Card className="p-6 bg-card border-border">
              <div className="flex items-center gap-3 mb-4">
                <Cloud className="w-6 h-6 text-primary" />
                <h2 className="text-xl font-semibold text-foreground">Weather Conditions</h2>
              </div>
              {weatherLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                  <p className="text-muted-foreground">Loading weather data...</p>
                </div>
              ) : weatherData && weatherData.conditions.length > 0 ? (
                <div className="space-y-4">
                  {weatherData.conditions.slice(0, 3).map((condition, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-muted/50">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-foreground">
                          Sensor {condition.sensor_id.split('-').pop()}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          {formatTimeAgo(condition.timestamp)}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        {condition.temperature !== null && (
                          <div className="flex items-center gap-2">
                            <Thermometer className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">{condition.temperature}°C</span>
                          </div>
                        )}
                        {condition.humidity !== null && (
                          <div className="flex items-center gap-2">
                            <Droplets className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">{condition.humidity}%</span>
                          </div>
                        )}
                        {condition.rainfall !== null && (
                          <div className="flex items-center gap-2">
                            <Cloud className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">{condition.rainfall}mm</span>
                          </div>
                        )}
                        {condition.wind_speed !== null && (
                          <div className="flex items-center gap-2">
                            <Wind className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">{condition.wind_speed} km/h</span>
                          </div>
                        )}
                        {condition.visibility !== null && (
                          <div className="flex items-center gap-2">
                            <Eye className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">{condition.visibility} km</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  {weatherData.conditions.length > 3 && (
                    <div className="text-center text-sm text-muted-foreground">
                      +{weatherData.conditions.length - 3} more sensors
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  No weather data available
                </div>
              )}
            </Card>

            {/* Road Conditions */}
            <Card className="p-6 bg-card border-border">
              <div className="flex items-center gap-3 mb-4">
                <Navigation className="w-6 h-6 text-primary" />
                <h2 className="text-xl font-semibold text-foreground">Road Conditions</h2>
              </div>
              {roadConditionsLoading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                  <p className="text-muted-foreground">Loading road conditions...</p>
                </div>
              ) : roadConditionsData && roadConditionsData.conditions.length > 0 ? (
                <div className="space-y-4">
                  {roadConditionsData.conditions.slice(0, 3).map((condition, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded-lg ${condition.anomaly_detected
                          ? 'bg-emergency/10 border border-emergency/20'
                          : 'bg-muted/50'
                        }`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-foreground">
                          Sensor {condition.sensor_id.split('-').pop()}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded ${condition.condition === 'dry'
                            ? 'bg-primary/20 text-primary'
                            : condition.condition === 'wet'
                              ? 'bg-trust/20 text-trust'
                              : 'bg-warning/20 text-warning'
                          }`}>
                          {condition.condition}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        {condition.temperature !== null && (
                          <div className="flex items-center gap-2">
                            <Thermometer className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">{condition.temperature}°C</span>
                          </div>
                        )}
                        {condition.surface_type && (
                          <div className="flex items-center gap-2">
                            <Navigation className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground capitalize">{condition.surface_type}</span>
                          </div>
                        )}
                        {condition.roughness !== null && (
                          <div className="flex items-center gap-2">
                            <Activity className="w-4 h-4 text-muted-foreground" />
                            <span className="text-foreground">Roughness: {condition.roughness}</span>
                          </div>
                        )}
                        {condition.anomaly_detected && (
                          <div className="col-span-2 flex items-center gap-2 text-emergency text-xs font-medium">
                            <AlertCircle className="w-4 h-4" />
                            Anomaly detected
                          </div>
                        )}
                      </div>
                      <div className="text-xs text-muted-foreground mt-2">
                        {formatTimeAgo(condition.timestamp)}
                      </div>
                    </div>
                  ))}
                  {roadConditionsData.conditions.length > 3 && (
                    <div className="text-center text-sm text-muted-foreground">
                      +{roadConditionsData.conditions.length - 3} more sensors
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  No road condition data available
                </div>
              )}
            </Card>
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
