import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { verificationAPI } from '../services/api';
import LoadingSpinner from '../components/Common/LoadingSpinner';

export default function VerificationPage() {
  const { id: complaintId } = useParams();
  const [file, setFile] = useState(null);
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');
  const [notes, setNotes] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);

  // Pre-fetch existing verification
  useEffect(() => {
    verificationAPI
      .get(complaintId)
      .then((res) => setResult(res.data))
      .catch(() => {})
      .finally(() => setFetchLoading(false));
  }, [complaintId]);

  // Capture current location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLat(pos.coords.latitude.toFixed(6));
          setLng(pos.coords.longitude.toFixed(6));
        },
        () => {}
      );
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData();
      if (file) formData.append('image', file);
      formData.append('latitude', lat);
      formData.append('longitude', lng);
      formData.append('notes', notes);

      const { data } = await verificationAPI.submit(complaintId, formData);
      setResult(data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Verification submission failed');
    } finally {
      setLoading(false);
    }
  };

  if (fetchLoading) return <LoadingSpinner label="Loading verification…" />;

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">4-Layer Verification</h1>
        <p className="text-sm text-gray-500 mt-1">Complaint #{complaintId}</p>
      </div>

      {/* Result view */}
      {result && (
        <div className="card p-6 space-y-4">
          <h2 className="text-lg font-semibold">Verification Result</h2>
          <div className="grid grid-cols-2 gap-4">
            <VLayer label="GPS Match" ok={result.gps_verified} score={result.gps_score} />
            <VLayer label="Timestamp" ok={result.timestamp_verified} score={result.timestamp_score} />
            <VLayer label="Visual Change" ok={result.visual_verified} score={result.visual_score} />
            <VLayer label="Tamper Detection" ok={!result.tamper_detected} score={result.tamper_score} />
          </div>
          <div className="flex items-center gap-4 pt-2 border-t">
            <span className="text-lg font-bold text-gray-900">
              Overall: {result.overall_score?.toFixed(1)}%
            </span>
            <span className={`badge ${result.is_verified ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {result.is_verified ? 'Verified' : 'Not Verified'}
            </span>
          </div>
        </div>
      )}

      {/* Submit form (show if no result yet) */}
      {!result && (
        <form onSubmit={handleSubmit} className="card p-6 space-y-5">
          <h2 className="text-lg font-semibold">Submit Verification Evidence</h2>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Photo evidence</label>
            <input
              type="file"
              accept="image/*"
              capture="environment"
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0 file:text-sm file:font-medium
                file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Latitude</label>
              <input
                type="text"
                value={lat}
                onChange={(e) => setLat(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                placeholder="Auto-detected"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Longitude</label>
              <input
                type="text"
                value={lng}
                onChange={(e) => setLng(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                placeholder="Auto-detected"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              placeholder="Any additional observations…"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="bg-primary-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium
              hover:bg-primary-700 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Submitting…' : 'Submit Verification'}
          </button>
        </form>
      )}
    </div>
  );
}

function VLayer({ label, ok, score }) {
  return (
    <div className={`p-3 rounded-lg border ${ok ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
      <p className="text-xs text-gray-600">{label}</p>
      <p className={`text-lg font-bold ${ok ? 'text-green-700' : 'text-red-700'}`}>
        {ok ? '✓ Pass' : '✗ Fail'}
      </p>
      {score != null && <p className="text-xs text-gray-500">Score: {(score * 100).toFixed(0)}%</p>}
    </div>
  );
}
