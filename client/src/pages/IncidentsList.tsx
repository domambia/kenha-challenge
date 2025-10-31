import { useState, useMemo, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { AlertCircle, MapPin, Clock, Search, User, CheckCircle2, XCircle } from "lucide-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { incidentsAPI, Incident, IncidentComment } from "@/lib/incidents-api";
import { useToast } from "@/hooks/use-toast";
import { formatDistanceToNow, format } from "date-fns";

const IncidentsList = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [filterStatus, setFilterStatus] = useState(searchParams.get("status") || "all");
  const [selectedIncidentId, setSelectedIncidentId] = useState<string | null>(
    searchParams.get("incident")
  );
  const [assignDialogOpen, setAssignDialogOpen] = useState(false);
  const [incidentToAssign, setIncidentToAssign] = useState<string | null>(null);
  const [resolutionNotes, setResolutionNotes] = useState("");

  // Fetch selected incident details
  const { data: selectedIncident, isLoading: loadingDetails } = useQuery({
    queryKey: ['incident', selectedIncidentId],
    queryFn: () => incidentsAPI.getById(selectedIncidentId!),
    enabled: !!selectedIncidentId,
  });

  // Fetch comments for selected incident
  const { data: comments, isLoading: loadingComments } = useQuery({
    queryKey: ['incident-comments', selectedIncidentId],
    queryFn: () => incidentsAPI.getComments(selectedIncidentId!),
    enabled: !!selectedIncidentId,
  });

  // Update URL when selected incident changes
  useEffect(() => {
    if (selectedIncidentId) {
      const newParams = new URLSearchParams(searchParams);
      newParams.set('incident', selectedIncidentId);
      setSearchParams(newParams, { replace: true });
    } else {
      const newParams = new URLSearchParams(searchParams);
      newParams.delete('incident');
      setSearchParams(newParams, { replace: true });
    }
  }, [selectedIncidentId, searchParams, setSearchParams]);

  // Fetch incidents
  const { data: incidentsData, isLoading } = useQuery({
    queryKey: ['incidents', 'list', filterStatus],
    queryFn: () => {
      const params: { status?: string } = {};
      if (filterStatus !== 'all') {
        params.status = filterStatus;
      }
      return incidentsAPI.getAll(params);
    },
  });

  const incidents = incidentsData?.results || [];

  // Filter incidents based on search and filters
  const filteredIncidents = useMemo(() => {
    if (!Array.isArray(incidents)) return [];

    let filtered = [...incidents];

    // Filter by status
    if (filterStatus !== 'all') {
      filtered = filtered.filter(i => i.status.toLowerCase() === filterStatus.toLowerCase());
    }

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(i =>
        i.incident_type?.name.toLowerCase().includes(filterType.toLowerCase())
      );
    }

    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(i =>
        i.incident_id.toLowerCase().includes(query) ||
        i.description.toLowerCase().includes(query) ||
        i.road_name?.toLowerCase().includes(query) ||
        i.incident_type?.name.toLowerCase().includes(query)
      );
    }

    // Sort by most recent first
    return filtered.sort((a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    );
  }, [incidents, filterStatus, filterType, searchQuery]);

  const getSeverityColor = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case "p1":
      case "critical":
        return "emergency";
      case "p2":
      case "high":
        return "warning";
      case "p3":
      case "medium":
        return "trust";
      case "p4":
      case "low":
        return "muted";
      default: return "muted";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status?.toLowerCase()) {
      case "in_progress":
      case "in progress":
        return "trust";
      case "assigned":
        return "primary";
      case "pending":
        return "warning";
      case "verified":
        return "primary";
      case "resolved":
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

  const handleViewDetails = (incidentId: string) => {
    setSelectedIncidentId(incidentId);
  };

  const handleCloseDetails = () => {
    setSelectedIncidentId(null);
  };

  const handleOpenAssign = (incidentId: string) => {
    setIncidentToAssign(incidentId);
    setAssignDialogOpen(true);
  };

  const handleAssignResponder = async () => {
    if (incidentToAssign) {
      try {
        await incidentsAPI.assign(incidentToAssign);
        toast({
          title: "Success",
          description: "Incident assigned successfully",
        });
        // Refresh incidents list
        queryClient.invalidateQueries({ queryKey: ['incidents'] });
        // Refresh selected incident if it's the one being assigned
        if (selectedIncidentId === incidentToAssign) {
          queryClient.invalidateQueries({ queryKey: ['incident', selectedIncidentId] });
        }
        setAssignDialogOpen(false);
        setIncidentToAssign(null);
      } catch (error: any) {
        toast({
          title: "Error",
          description: error.response?.data?.message || "Failed to assign incident",
          variant: "destructive",
        });
      }
    }
  };

  const handleVerify = async (incidentId: string) => {
    try {
      await incidentsAPI.verify(incidentId);
      toast({
        title: "Success",
        description: "Incident verified successfully",
      });
      queryClient.invalidateQueries({ queryKey: ['incidents'] });
      if (selectedIncidentId === incidentId) {
        queryClient.invalidateQueries({ queryKey: ['incident', selectedIncidentId] });
      }
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.response?.data?.message || "Failed to verify incident",
        variant: "destructive",
      });
    }
  };

  const handleCloseIncident = async () => {
    if (!selectedIncidentId || !resolutionNotes.trim()) {
      toast({
        title: "Resolution Notes Required",
        description: "Please provide resolution notes before closing the incident",
        variant: "destructive",
      });
      return;
    }

    try {
      await incidentsAPI.close(selectedIncidentId, resolutionNotes);
      toast({
        title: "Success",
        description: "Incident closed successfully",
      });
      queryClient.invalidateQueries({ queryKey: ['incidents'] });
      queryClient.invalidateQueries({ queryKey: ['incident', selectedIncidentId] });
      setResolutionNotes("");
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.response?.data?.message || "Failed to close incident",
        variant: "destructive",
      });
    }
  };

  const getSeverityColorCode = (severity: string): string => {
    switch (severity?.toLowerCase()) {
      case "p1":
      case "critical":
        return "#FF0000";
      case "p2":
      case "high":
        return "#FF6600";
      case "p3":
      case "medium":
        return "#FFCC00";
      case "p4":
      case "low":
        return "#00CC00";
      default:
        return "#808080";
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 pt-20 pb-12">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-2">
              Active Incidents
            </h1>
            <p className="text-muted-foreground">
              Browse and track reported road incidents across the network
            </p>
          </div>

          {/* Filters */}
          <Card className="p-6 mb-6 bg-card border-border">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by ID, location, or description..."
                    className="pl-10"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                </div>
              </div>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="accident">Accident</SelectItem>
                  <SelectItem value="hazard">Road Hazard</SelectItem>
                  <SelectItem value="infrastructure">Infrastructure</SelectItem>
                  <SelectItem value="vandalism">Vandalism</SelectItem>
                </SelectContent>
              </Select>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="assigned">Assigned</SelectItem>
                  <SelectItem value="in-progress">In Progress</SelectItem>
                  <SelectItem value="resolved">Resolved</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </Card>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <Card className="p-4 bg-card border-border">
              <div className="text-2xl font-bold text-foreground">
                {isLoading ? "..." : filteredIncidents.length}
              </div>
              <div className="text-sm text-muted-foreground">Filtered Incidents</div>
            </Card>
            <Card className="p-4 bg-card border-border">
              <div className="text-2xl font-bold text-emergency">
                {isLoading ? "..." : Array.isArray(incidents) ? incidents.filter(i => i.severity?.level === "P1" || i.severity?.name?.toLowerCase() === "critical").length : 0}
              </div>
              <div className="text-sm text-muted-foreground">Critical</div>
            </Card>
            <Card className="p-4 bg-card border-border">
              <div className="text-2xl font-bold text-trust">
                {isLoading ? "..." : Array.isArray(incidents) ? incidents.filter(i => i.status?.toLowerCase() === "in_progress" || i.status?.toLowerCase() === "in progress").length : 0}
              </div>
              <div className="text-sm text-muted-foreground">In Progress</div>
            </Card>
            <Card className="p-4 bg-card border-border">
              <div className="text-2xl font-bold text-primary">
                {isLoading ? "..." : Array.isArray(incidents) ? incidents.filter(i => i.status?.toLowerCase() === "resolved" || i.status?.toLowerCase() === "closed").length : 0}
              </div>
              <div className="text-sm text-muted-foreground">Resolved</div>
            </Card>
          </div>

          {/* Incidents List */}
          {isLoading ? (
            <div className="text-center py-12 text-muted-foreground">Loading incidents...</div>
          ) : filteredIncidents.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground mb-4">No incidents found</p>
              <Button onClick={() => navigate("/report")}>Report New Incident</Button>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredIncidents.map((incident) => (
                <Card
                  key={incident.incident_id}
                  className={`p-6 bg-card border-border hover:border-primary/50 transition-all cursor-pointer ${selectedIncidentId === incident.incident_id ? 'ring-2 ring-primary' : ''}`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className={`px-3 py-1 rounded-full text-sm font-medium bg-${getSeverityColor(incident.severity?.level || incident.severity?.name || '')}/10 text-${getSeverityColor(incident.severity?.level || incident.severity?.name || '')} border border-${getSeverityColor(incident.severity?.level || incident.severity?.name || '')}/20`}>
                        {incident.severity?.level || incident.severity?.name || 'Unknown'}
                      </div>
                      <span className="font-bold text-foreground">{incident.incident_id}</span>
                      <Badge variant="outline">{incident.incident_type?.name || 'Unknown'}</Badge>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className={`px-3 py-1 rounded-full text-xs font-medium bg-${getStatusColor(incident.status)}/10 text-${getStatusColor(incident.status)}`}>
                        {incident.status}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                        <MapPin className="w-4 h-4" />
                        <span>{incident.road_name || `${Number(incident.latitude).toFixed(4)}, ${Number(incident.longitude).toFixed(4)}`}</span>
                      </div>
                      <p className="text-foreground">{incident.description}</p>
                    </div>
                    <div className="flex flex-col justify-between">
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Clock className="w-4 h-4" />
                        <span>{formatTimeAgo(incident.created_at)}</span>
                      </div>
                      {incident.ai_confidence_score !== undefined && (
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-muted-foreground">AI Confidence:</span>
                          <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                            <div
                              className="h-full bg-primary"
                              style={{ width: `${Number(incident.ai_confidence_score)}%` }}
                            />
                          </div>
                          <span className="text-xs font-medium text-foreground">
                            {Number(incident.ai_confidence_score).toFixed(1)}%
                          </span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button size="sm" variant="outline" onClick={() => handleViewDetails(incident.incident_id)}>
                      View Details
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => navigate(`/dashboard`)}>
                      View on Map
                    </Button>
                    {incident.status?.toLowerCase() === "pending" && (
                      <Button size="sm" onClick={() => handleOpenAssign(incident.incident_id)}>
                        Assign Responder
                      </Button>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          )}

          {/* Pagination placeholder */}
          <div className="mt-6 flex justify-center gap-2">
            <Button variant="outline" size="sm">Previous</Button>
            <Button variant="outline" size="sm">1</Button>
            <Button size="sm">2</Button>
            <Button variant="outline" size="sm">3</Button>
            <Button variant="outline" size="sm">Next</Button>
          </div>
        </div>
      </main>

      {/* Incident Details Dialog */}
      <Dialog open={!!selectedIncidentId} onOpenChange={(open) => !open && handleCloseDetails()}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          {loadingDetails ? (
            <div className="text-center py-8">Loading incident details...</div>
          ) : selectedIncident ? (
            <>
              <DialogHeader>
                <DialogTitle className="text-2xl font-bold">
                  Incident Details: {selectedIncident.incident_id}
                </DialogTitle>
                <DialogDescription>
                  Comprehensive information about this incident
                </DialogDescription>
              </DialogHeader>

              <div className="space-y-6 mt-4">
                {/* Header Info */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Card className="p-4">
                    <div className="text-xs text-muted-foreground mb-1">Severity</div>
                    <div
                      className="font-bold text-lg"
                      style={{ color: getSeverityColorCode(selectedIncident.severity?.level || selectedIncident.severity?.name || '') }}
                    >
                      {selectedIncident.severity?.level || selectedIncident.severity?.name || 'Unknown'}
                    </div>
                  </Card>
                  <Card className="p-4">
                    <div className="text-xs text-muted-foreground mb-1">Status</div>
                    <div className={`font-bold text-lg text-${getStatusColor(selectedIncident.status)}`}>
                      {selectedIncident.status}
                    </div>
                  </Card>
                  <Card className="p-4">
                    <div className="text-xs text-muted-foreground mb-1">Type</div>
                    <div className="font-bold text-lg">{selectedIncident.incident_type?.name || 'Unknown'}</div>
                  </Card>
                  <Card className="p-4">
                    <div className="text-xs text-muted-foreground mb-1">Verification</div>
                    <div className="font-bold text-lg capitalize">{selectedIncident.verification_status || 'Pending'}</div>
                  </Card>
                </div>

                {/* Description */}
                <Card className="p-4">
                  <h3 className="font-semibold mb-2">Description</h3>
                  <p className="text-sm text-foreground">{selectedIncident.description}</p>
                </Card>

                {/* Location & Metadata */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card className="p-4">
                    <h3 className="font-semibold mb-3 flex items-center gap-2">
                      <MapPin className="w-4 h-4" />
                      Location
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="text-muted-foreground">Road:</span>{" "}
                        <span className="font-medium">
                          {selectedIncident.road_name || 'Not specified'}
                        </span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Coordinates:</span>{" "}
                        <span className="font-mono">
                          {Number(selectedIncident.latitude).toFixed(6)}, {Number(selectedIncident.longitude).toFixed(6)}
                        </span>
                      </div>
                      {selectedIncident.weather && (
                        <div>
                          <span className="text-muted-foreground">Weather:</span>{" "}
                          <span className="font-medium capitalize">{selectedIncident.weather}</span>
                        </div>
                      )}
                    </div>
                  </Card>

                  <Card className="p-4">
                    <h3 className="font-semibold mb-3 flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      Timeline
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="text-muted-foreground">Reported:</span>{" "}
                        <span className="font-medium">
                          {format(new Date(selectedIncident.created_at), 'PPpp')}
                        </span>
                        <span className="text-muted-foreground ml-2">
                          ({formatDistanceToNow(new Date(selectedIncident.created_at), { addSuffix: true })})
                        </span>
                      </div>
                      {selectedIncident.timestamp && (
                        <div>
                          <span className="text-muted-foreground">Incident Time:</span>{" "}
                          <span className="font-medium">
                            {format(new Date(selectedIncident.timestamp), 'PPpp')}
                          </span>
                        </div>
                      )}
                      {selectedIncident.updated_at && selectedIncident.updated_at !== selectedIncident.created_at && (
                        <div>
                          <span className="text-muted-foreground">Last Updated:</span>{" "}
                          <span className="font-medium">
                            {format(new Date(selectedIncident.updated_at), 'PPpp')}
                          </span>
                        </div>
                      )}
                    </div>
                  </Card>
                </div>

                {/* AI Confidence & Metadata */}
                {selectedIncident.ai_confidence_score !== undefined && (
                  <Card className="p-4">
                    <h3 className="font-semibold mb-2">AI Analysis</h3>
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-3 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full bg-primary transition-all"
                          style={{ width: `${Number(selectedIncident.ai_confidence_score)}%` }}
                        />
                      </div>
                      <span className="font-semibold text-sm">
                        {Number(selectedIncident.ai_confidence_score).toFixed(1)}%
                      </span>
                    </div>
                  </Card>
                )}

                {/* Reporter Info */}
                {selectedIncident.reporter_email && (
                  <Card className="p-4">
                    <h3 className="font-semibold mb-2 flex items-center gap-2">
                      <User className="w-4 h-4" />
                      Reporter Information
                    </h3>
                    <div className="text-sm">
                      <div>
                        <span className="text-muted-foreground">Email:</span>{" "}
                        <span className="font-medium">{selectedIncident.reporter_email}</span>
                      </div>
                      {selectedIncident.is_anonymous && (
                        <div className="text-muted-foreground italic">Anonymous Report</div>
                      )}
                    </div>
                  </Card>
                )}

                {/* Comments Section */}
                <Card className="p-4">
                  <h3 className="font-semibold mb-4">Comments & Updates</h3>
                  {loadingComments ? (
                    <div className="text-center py-4 text-muted-foreground">Loading comments...</div>
                  ) : comments && comments.length > 0 ? (
                    <div className="space-y-3">
                      {comments.map((comment: IncidentComment) => (
                        <div key={comment.id} className="border-l-2 border-primary pl-4 py-2">
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-medium text-sm">
                              {comment.user_email || 'System'}
                            </span>
                            <span className="text-xs text-muted-foreground">
                              {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
                            </span>
                          </div>
                          <p className="text-sm text-foreground">{comment.comment_text}</p>
                          {comment.comment_type && (
                            <Badge variant="outline" className="mt-1 text-xs">
                              {comment.comment_type}
                            </Badge>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-4 text-muted-foreground">No comments yet</div>
                  )}
                </Card>

                {/* Actions */}
                <div className="flex flex-wrap gap-2 pt-4 border-t">
                  <Button
                    variant="outline"
                    onClick={() => navigate(`/dashboard?incident=${selectedIncident.incident_id}`)}
                  >
                    View on Map
                  </Button>
                  {selectedIncident.status?.toLowerCase() === "pending" && (
                    <Button
                      onClick={() => handleOpenAssign(selectedIncident.incident_id)}
                      variant="outline"
                    >
                      Assign Responder
                    </Button>
                  )}
                  {selectedIncident.verification_status?.toLowerCase() !== "verified" && (
                    <Button
                      onClick={() => handleVerify(selectedIncident.incident_id)}
                      variant="outline"
                    >
                      <CheckCircle2 className="w-4 h-4 mr-2" />
                      Verify Incident
                    </Button>
                  )}
                  {selectedIncident.status?.toLowerCase() !== "closed" && (
                    <>
                      <div className="flex-1" />
                      <div className="flex items-center gap-2">
                        <Textarea
                          placeholder="Resolution notes (required to close)"
                          value={resolutionNotes}
                          onChange={(e) => setResolutionNotes(e.target.value)}
                          className="w-64"
                          rows={2}
                        />
                        <Button
                          onClick={handleCloseIncident}
                          variant="destructive"
                          disabled={!resolutionNotes.trim()}
                        >
                          <XCircle className="w-4 h-4 mr-2" />
                          Close Incident
                        </Button>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              Incident not found
            </div>
          )}
        </DialogContent>
      </Dialog>

      {/* Assign Dialog */}
      <Dialog open={assignDialogOpen} onOpenChange={setAssignDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Assign Incident</DialogTitle>
            <DialogDescription>
              Assign this incident to a responder team
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <p className="text-sm text-muted-foreground">
              The incident will be assigned to an available responder team. You can specify a responder ID if needed.
            </p>
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setAssignDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleAssignResponder}>
              Assign Incident
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      <Footer />
    </div>
  );
};

export default IncidentsList;
