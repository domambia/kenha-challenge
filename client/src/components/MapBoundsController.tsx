import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

interface MapBoundsControllerProps {
    incidents: Array<{ latitude: number | string; longitude: number | string }>;
}

// Component to control map bounds based on incidents
const MapBoundsController = ({ incidents }: MapBoundsControllerProps) => {
    const map = useMap();

    useEffect(() => {
        const validIncidents = incidents.filter(incident => {
            const lat = Number(incident.latitude);
            const lng = Number(incident.longitude);
            return (
                !isNaN(lat) && !isNaN(lng) &&
                lat !== 0 && lng !== 0 &&
                lat >= -5 && lat <= 6 &&
                lng >= 33 && lng <= 42
            );
        });

        if (validIncidents.length === 0) {
            // If no incidents, center on Nairobi, Kenya
            map.setView([-1.2921, 36.8219], 7);
            return;
        }

        if (validIncidents.length === 1) {
            // Single incident - center on it
            const lat = Number(validIncidents[0].latitude);
            const lng = Number(validIncidents[0].longitude);
            map.setView([lat, lng], 12);
        } else {
            // Multiple incidents - fit bounds
            const bounds = validIncidents.map(incident => [
                Number(incident.latitude),
                Number(incident.longitude)
            ] as [number, number]);

            // Create a LatLngBounds object
            const latLngBounds = L.latLngBounds(bounds);
            map.fitBounds(latLngBounds, { padding: [50, 50], maxZoom: 12 });
        }
    }, [map, incidents]);

    return null;
};

export default MapBoundsController;

