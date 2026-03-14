import { useState, useEffect, useRef } from 'react';
import { publicAPI } from '../services/api';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const WARD_OPTIONS = Array.from({ length: 15 }, (_, i) => ({
  id: i + 1,
  name: `Ward ${i + 1}`,
}));

export default function PublicPortal() {
  const [selectedWard, setSelectedWard] = useState(1);
  const [scorecard, setScorecard] = useState(null);
  const [actions, setActions] = useState([]);
  const [trust, setTrust] = useState(null);
  const [loading, setLoading] = useState(true);

  // Complaint form
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: '', description: '', ward_id: 1, citizen_name: '', citizen_phone: '' });
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const mapRef = useRef(null);
  const mapInstance = useRef(null);

  useEffect(() => {
    loadWard(selectedWard);
  }, [selectedWard]);

  async function loadWard(wardId) {
    setLoading(true);
    try {
      const [scRes, acRes, trRes] = await Promise.allSettled([
        publicAPI.wardScorecard(wardId),
        publicAPI.recentActions(wardId),
        publicAPI.wardTrust(wardId),
      ]);
      if (scRes.status === 'fulfilled') setScorecard(scRes.value.data);
      if (acRes.status === 'fulfilled') setActions(acRes.value.data || []);
      if (trRes.status === 'fulfilled') setTrust(trRes.value.data);
    } finally {
      setLoading(false);
    }
  }

  // Leaflet map
  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return;
    mapInstance.current = L.map(mapRef.current, {
      center: [28.6139, 77.209],
      zoom: 11,
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap',
    }).addTo(mapInstance.current);

    return () => {
      mapInstance.current?.remove();
      mapInstance.current = null;
    };
  }, []);

  const handleComplaint = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await publicAPI.submitComplaint({ ...form, ward_id: selectedWard });
      setSubmitted(true);
      setForm({ title: '', description: '', ward_id: selectedWard, citizen_name: '', citizen_phone: '' });
    } catch (err) {
      alert(err.response?.data?.detail || 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-12 px-4">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-3xl md:text-4xl font-bold">Jansewa AI Public Portal</h1>
          <p className="mt-2 text-primary-100 text-lg">Transparent governance for every citizen</p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
        {/* Ward selector */}
        <div className="flex items-center gap-4">
          <label className="text-sm font-medium text-gray-700">Select Ward:</label>
          <select
            value={selectedWard}
            onChange={(e) => setSelectedWard(Number(e.target.value))}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
          >
            {WARD_OPTIONS.map((w) => (
              <option key={w.id} value={w.id}>{w.name}</option>
            ))}
          </select>
          <button
            onClick={() => { setShowForm(!showForm); setSubmitted(false); }}
            className="ml-auto bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700"
          >
            {showForm ? 'Close' : 'Report Issue'}
          </button>
        </div>

        {/* Complaint form */}
        {showForm && !submitted && (
          <form onSubmit={handleComplaint} className="card p-6 space-y-4">
            <h2 className="text-lg font-semibold">Report a Grievance</h2>
            <input
              type="text"
              required
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              placeholder="Brief title"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
            <textarea
              required
              rows={3}
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Describe the issue in detail…"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
            <div className="grid grid-cols-2 gap-4">
              <input
                type="text"
                value={form.citizen_name}
                onChange={(e) => setForm({ ...form, citizen_name: e.target.value })}
                placeholder="Your name (optional)"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              />
              <input
                type="tel"
                value={form.citizen_phone}
                onChange={(e) => setForm({ ...form, citizen_phone: e.target.value })}
                placeholder="Phone (optional)"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="bg-primary-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium disabled:opacity-50"
            >
              {submitting ? 'Submitting…' : 'Submit'}
            </button>
          </form>
        )}
        {submitted && (
          <div className="card p-6 text-center text-green-700 bg-green-50 border border-green-200">
            ✅ Your complaint has been submitted and will be processed by AI.
          </div>
        )}

        {loading ? (
          <div className="text-center py-12 text-gray-400">Loading ward data…</div>
        ) : (
          <>
            {/* Scorecard */}
            {scorecard && (
              <div className="card p-6">
                <h2 className="text-lg font-semibold mb-4">Ward Scorecard</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <ScoreItem label="Total Complaints" value={scorecard.total_complaints} />
                  <ScoreItem label="Resolved" value={scorecard.resolved} />
                  <ScoreItem label="Pending" value={scorecard.pending} />
                  <ScoreItem label="Avg Resolution" value={`${scorecard.avg_resolution_hours?.toFixed(1) || '—'} hrs`} />
                </div>
              </div>
            )}

            {/* Trust score */}
            {trust && (
              <div className="card p-6">
                <h2 className="text-lg font-semibold mb-4">Trust Score</h2>
                <div className="flex items-center gap-6">
                  <div className="w-24 h-24 rounded-full border-8 border-primary-200 flex items-center justify-center">
                    <span className="text-2xl font-bold text-primary-700">
                      {trust.overall_score?.toFixed(0) || '—'}
                    </span>
                  </div>
                  <div className="flex-1 grid grid-cols-2 gap-3 text-sm">
                    <div><span className="text-gray-500">Responsiveness:</span> {trust.responsiveness?.toFixed(1)}</div>
                    <div><span className="text-gray-500">Resolution:</span> {trust.resolution_rate?.toFixed(1)}</div>
                    <div><span className="text-gray-500">Transparency:</span> {trust.transparency?.toFixed(1)}</div>
                    <div><span className="text-gray-500">Citizen Satisfaction:</span> {trust.citizen_satisfaction?.toFixed(1)}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Recent actions */}
            <div className="card overflow-hidden">
              <div className="px-5 py-4 border-b border-gray-100">
                <h2 className="font-semibold">Recent Actions</h2>
              </div>
              <div className="divide-y">
                {actions.length === 0 ? (
                  <p className="px-5 py-8 text-center text-gray-400">No recent actions for this ward</p>
                ) : (
                  actions.map((a, i) => (
                    <div key={i} className="px-5 py-3">
                      <p className="text-sm font-medium text-gray-900">{a.title}</p>
                      <p className="text-xs text-gray-500 mt-0.5">{a.description}</p>
                      <p className="text-xs text-gray-400 mt-1">{new Date(a.created_at).toLocaleDateString()}</p>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Map */}
            <div className="card overflow-hidden">
              <div className="px-5 py-4 border-b border-gray-100">
                <h2 className="font-semibold">Ward Map</h2>
              </div>
              <div ref={mapRef} className="h-[350px] w-full" />
            </div>
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-400 text-center py-6 text-sm mt-8">
        &copy; {new Date().getFullYear()} Jansewa AI — Empowering transparent local governance
      </footer>
    </div>
  );
}

function ScoreItem({ label, value }) {
  return (
    <div className="text-center">
      <p className="text-2xl font-bold text-gray-900">{value ?? '—'}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  );
}
