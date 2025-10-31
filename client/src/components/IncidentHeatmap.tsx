import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, Marker, Popup, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat';
import MapBoundsController from './MapBoundsController';
import MapResizeHandler from './MapResizeHandler';
import { useNavigate } from 'react-router-dom';

// Fix for default marker icons in React/Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

// Create colored icons based on severity
const createColoredIcon = (color: string) => {
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10],
    });
};

// Severity color mapping
const getSeverityColor = (severityLevel: string): string => {
    switch (severityLevel?.toLowerCase()) {
        case 'p1':
        case 'critical':
            return '#FF0000'; // Red
        case 'p2':
        case 'high':
            return '#FF6600'; // Orange
        case 'p3':
        case 'medium':
            return '#FFCC00'; // Yellow
        case 'p4':
        case 'low':
            return '#00CC00'; // Green
        default:
            return '#808080'; // Gray
    }
};

interface HeatmapLayerProps {
    points: Array<[number, number, number]>; // [lat, lng, intensity]
}

const HeatmapLayer = ({ points }: HeatmapLayerProps) => {
    const map = useMap();
    // @ts-ignore - leaflet.heat doesn't have proper TypeScript definitions
    const heatLayerRef = useRef<any>(null);

    useEffect(() => {
        if (points.length === 0) {
            if (heatLayerRef.current) {
                map.removeLayer(heatLayerRef.current);
                heatLayerRef.current = null;
            }
            return;
        }

        // Remove existing heat layer
        if (heatLayerRef.current) {
            map.removeLayer(heatLayerRef.current);
        }

        // Create new heat layer
        // @ts-ignore - leaflet.heat types may not be perfect
        const heatLayer = L.heatLayer(points, {
            radius: 25,
            blur: 15,
            maxZoom: 17,
            max: 1.0,
            gradient: {
                0.0: 'blue',
                0.3: 'cyan',
                0.5: 'lime',
                0.7: 'yellow',
                1.0: 'red'
            }
        });

        heatLayer.addTo(map);
        heatLayerRef.current = heatLayer;

        // Note: Map bounds are controlled by MapBoundsController component
        // This layer just handles the heatmap visualization

        return () => {
            if (heatLayerRef.current) {
                map.removeLayer(heatLayerRef.current);
                heatLayerRef.current = null;
            }
        };
    }, [map, points]);

    return null;
};

interface IncidentHeatmapProps {
    incidents: Array<{
        incident_id?: string;
        latitude: number | string;
        longitude: number | string;
        severity?: {
            level?: string;
            name?: string;
        };
        status?: string;
        incident_type?: {
            name?: string;
            category?: string;
        };
        description?: string;
        road_name?: string;
        created_at?: string;
        updated_at?: string;
        verification_status?: string;
        ai_confidence_score?: number | string;
        weather?: string;
        reporter_email?: string;
        is_anonymous?: boolean;
    }>;
    center?: [number, number];
    zoom?: number;
    key?: string | number; // Key to force remount when needed
}

const IncidentHeatmap = ({
    incidents,
    center = [-1.2921, 36.8219], // Default to Nairobi, Kenya
    zoom = 7
}: IncidentHeatmapProps) => {
    // Filter and validate incidents within Kenya bounds
    // Kenya approximate bounds: Lat -4.7 to 5.5, Lng 33.9 to 41.9
    const validIncidents = incidents.filter(incident => {
        const lat = Number(incident.latitude);
        const lng = Number(incident.longitude);
        return (
            !isNaN(lat) && !isNaN(lng) &&
            lat !== 0 && lng !== 0 &&
            lat >= -5 && lat <= 6 && // Kenya latitude bounds
            lng >= 33 && lng <= 42   // Kenya longitude bounds
        );
    });

    // Convert incidents to heatmap points with intensity based on severity
    const heatmapPoints: Array<[number, number, number]> = validIncidents.map(incident => {
        const lat = Number(incident.latitude);
        const lng = Number(incident.longitude);

        // Calculate intensity based on severity
        let intensity = 0.5; // Default
        const severityLevel = incident.severity?.level || incident.severity?.name?.toLowerCase() || '';

        switch (severityLevel.toLowerCase()) {
            case 'p1':
            case 'critical':
                intensity = 1.0;
                break;
            case 'p2':
            case 'high':
                intensity = 0.7;
                break;
            case 'p3':
            case 'medium':
                intensity = 0.5;
                break;
            case 'p4':
            case 'low':
                intensity = 0.3;
                break;
            default:
                intensity = 0.5;
        }

        return [lat, lng, intensity] as [number, number, number];
    });

    // Format date for display
    const formatDate = (dateString?: string) => {
        if (!dateString) return 'Unknown';
        try {
            return new Date(dateString).toLocaleString('en-KE', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    };

    return (
        <div className="w-full h-full">
            <MapContainer
                center={center}
                zoom={zoom}
                style={{ height: '100%', width: '100%', zIndex: 0 }}
                scrollWheelZoom={true}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <MapBoundsController incidents={incidents} />
                <MapResizeHandler />
                <HeatmapLayer points={heatmapPoints} />

                {/* Add markers for each incident */}
                {validIncidents.map((incident, index) => {
                    const lat = Number(incident.latitude);
                    const lng = Number(incident.longitude);
                    const severityLevel = incident.severity?.level || incident.severity?.name || '';
                    const markerColor = getSeverityColor(severityLevel);
                    const icon = createColoredIcon(markerColor);

                    // Create a component for the marker content that has access to navigate
                    const MarkerContent = () => {
                        const navigate = useNavigate();

                        const handleViewDetails = () => {
                            if (incident.incident_id) {
                                navigate(`/incidents?incident=${incident.incident_id}`);
                            }
                        };

                        return (
                            <>
                                <Tooltip
                                    permanent={false}
                                    direction="top"
                                    offset={[0, -10]}
                                    className="custom-tooltip"
                                >
                                    <div className="text-center">
                                        <div className="font-semibold text-xs">
                                            {incident.incident_id || `Incident #${index + 1}`}
                                        </div>
                                        <div className="text-xs text-muted-foreground">
                                            {incident.incident_type?.name || 'Unknown Type'}
                                        </div>
                                        <div className="text-xs font-medium" style={{ color: markerColor }}>
                                            {incident.severity?.level || incident.severity?.name || 'Unknown'}
                                        </div>
                                    </div>
                                </Tooltip>

                                <Popup className="custom-popup" maxWidth={350}>
                                    <div className="p-3 min-w-[250px] max-w-[350px]">
                                        {/* Header */}
                                        <div className="flex items-start justify-between mb-3 pb-2 border-b">
                                            <div className="flex-1">
                                                <div className="font-bold text-base mb-1">
                                                    {incident.incident_id || `Incident #${index + 1}`}
                                                </div>
                                                <div className="flex items-center gap-2 flex-wrap">
                                                    <span
                                                        className="px-2 py-0.5 rounded-full text-xs font-semibold"
                                                        style={{
                                                            backgroundColor: `${markerColor}20`,
                                                            color: markerColor
                                                        }}
                                                    >
                                                        {incident.severity?.level || incident.severity?.name || 'Unknown'}
                                                    </span>
                                                    <span className="px-2 py-0.5 rounded-full text-xs bg-muted text-muted-foreground">
                                                        {incident.status || 'Unknown'}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Main Info */}
                                        <div className="space-y-2 text-sm mb-3">
                                            <div className="grid grid-cols-2 gap-2">
                                                <div>
                                                    <span className="text-xs text-muted-foreground">Type:</span>
                                                    <div className="font-medium">
                                                        {incident.incident_type?.name || 'Unknown'}
                                                    </div>
                                                </div>
                                                {incident.incident_type?.category && (
                                                    <div>
                                                        <span className="text-xs text-muted-foreground">Category:</span>
                                                        <div className="font-medium capitalize">
                                                            {incident.incident_type.category}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>

                                            {incident.road_name && (
                                                <div>
                                                    <span className="text-xs text-muted-foreground">Location:</span>
                                                    <div className="font-medium">{incident.road_name}</div>
                                                </div>
                                            )}

                                            <div className="grid grid-cols-2 gap-2">
                                                <div>
                                                    <span className="text-xs text-muted-foreground">Coordinates:</span>
                                                    <div className="font-mono text-xs">
                                                        {lat.toFixed(4)}, {lng.toFixed(4)}
                                                    </div>
                                                </div>
                                                {incident.weather && (
                                                    <div>
                                                        <span className="text-xs text-muted-foreground">Weather:</span>
                                                        <div className="font-medium capitalize">
                                                            {incident.weather}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>

                                            {incident.verification_status && (
                                                <div>
                                                    <span className="text-xs text-muted-foreground">Verification:</span>
                                                    <div className="font-medium capitalize">
                                                        {incident.verification_status}
                                                    </div>
                                                </div>
                                            )}

                                            {incident.ai_confidence_score !== undefined && (
                                                <div>
                                                    <span className="text-xs text-muted-foreground">AI Confidence:</span>
                                                    <div className="flex items-center gap-2">
                                                        <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                                                            <div
                                                                className="h-full bg-primary transition-all"
                                                                style={{
                                                                    width: `${Number(incident.ai_confidence_score)}%`
                                                                }}
                                                            />
                                                        </div>
                                                        <span className="text-xs font-medium">
                                                            {Number(incident.ai_confidence_score).toFixed(1)}%
                                                        </span>
                                                    </div>
                                                </div>
                                            )}
                                        </div>

                                        {/* Description */}
                                        {incident.description && (
                                            <div className="mb-3 pt-2 border-t">
                                                <span className="text-xs text-muted-foreground mb-1 block">Description:</span>
                                                <p className="text-sm text-foreground leading-relaxed">
                                                    {incident.description}
                                                </p>
                                            </div>
                                        )}

                                        {/* Metadata */}
                                        <div className="pt-2 border-t space-y-1 text-xs text-muted-foreground">
                                            {incident.created_at && (
                                                <div>
                                                    <span className="font-medium">Reported:</span> {formatDate(incident.created_at)}
                                                </div>
                                            )}
                                            {incident.updated_at && incident.updated_at !== incident.created_at && (
                                                <div>
                                                    <span className="font-medium">Updated:</span> {formatDate(incident.updated_at)}
                                                </div>
                                            )}
                                            {incident.reporter_email && !incident.is_anonymous && (
                                                <div>
                                                    <span className="font-medium">Reporter:</span> {incident.reporter_email}
                                                </div>
                                            )}
                                            {incident.is_anonymous && (
                                                <div className="text-xs italic">Anonymous Report</div>
                                            )}
                                        </div>

                                        {/* Action Button */}
                                        {incident.incident_id && (
                                            <div className="mt-3 pt-3 border-t">
                                                <button
                                                    onClick={handleViewDetails}
                                                    className="w-full px-3 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                                                >
                                                    View Full Details →
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </Popup>
                            </>
                        );
                    };

                    return (
                        <Marker
                            key={incident.incident_id || `incident-${index}`}
                            position={[lat, lng]}
                            icon={icon}
                            eventHandlers={{
                                mouseover: (e) => {
                                    e.target.openTooltip();
                                },
                                mouseout: (e) => {
                                    e.target.closeTooltip();
                                }
                            }}
                        >
                            <MarkerContent />
                        </Marker>
                    );
                })}
            </MapContainer>
        </div>
    );
};

export default IncidentHeatmap;

