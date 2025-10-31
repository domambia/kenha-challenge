import { useEffect } from 'react';
import { useMap } from 'react-leaflet';

// Component to handle map resize when container size changes
const MapResizeHandler = () => {
    const map = useMap();

    useEffect(() => {
        // Trigger resize after a short delay to ensure container is rendered
        const timeoutId = setTimeout(() => {
            map.invalidateSize();
        }, 100);

        // Also listen for window resize events
        const handleResize = () => {
            map.invalidateSize();
        };

        window.addEventListener('resize', handleResize);

        return () => {
            clearTimeout(timeoutId);
            window.removeEventListener('resize', handleResize);
        };
    }, [map]);

    return null;
};

export default MapResizeHandler;

