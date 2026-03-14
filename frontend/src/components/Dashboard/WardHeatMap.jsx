import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Severity → circle color
const severityColor = {
  CRITICAL: '#ef4444',
  HIGH: '#f97316',
  MEDIUM: '#eab308',
  LOW: '#22c55e',
};

export default function WardHeatMap({ data = [] }) {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);

  useEffect(() => {
    if (mapInstance.current) return;

    // Center on Delhi
    mapInstance.current = L.map(mapRef.current, {
      center: [28.6139, 77.209],
      zoom: 12,
      scrollWheelZoom: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 18,
    }).addTo(mapInstance.current);

    return () => {
      mapInstance.current?.remove();
      mapInstance.current = null;
    };
  }, []);

  // Update markers when data changes
  useEffect(() => {
    if (!mapInstance.current || !data.length) return;

    // Clear old markers
    mapInstance.current.eachLayer((layer) => {
      if (layer instanceof L.CircleMarker) mapInstance.current.removeLayer(layer);
    });

    data.forEach((ward) => {
      if (!ward.latitude || !ward.longitude) return;

      const color = severityColor[ward.top_severity] || '#6b7280';
      const radius = Math.max(8, Math.min(30, (ward.complaint_count || 1) * 2));

      L.circleMarker([ward.latitude, ward.longitude], {
        radius,
        fillColor: color,
        color: '#fff',
        weight: 2,
        fillOpacity: 0.7,
      })
        .bindPopup(
          `<div class="text-sm">
            <p class="font-semibold">${ward.ward_name}</p>
            <p>Complaints: ${ward.complaint_count}</p>
            <p>Trust Score: ${ward.trust_score?.toFixed(1) ?? '—'}</p>
          </div>`
        )
        .addTo(mapInstance.current);
    });
  }, [data]);

  return (
    <div className="card overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Ward Heat Map</h3>
        <p className="text-xs text-gray-500 mt-0.5">Complaint density by geographic area</p>
      </div>
      <div ref={mapRef} className="h-[400px] w-full" />
      {/* Legend */}
      <div className="px-5 py-3 border-t border-gray-100 flex gap-4 text-xs">
        {Object.entries(severityColor).map(([label, color]) => (
          <span key={label} className="flex items-center gap-1">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
            {label}
          </span>
        ))}
      </div>
    </div>
  );
}
