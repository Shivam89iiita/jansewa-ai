import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { complaintsAPI, verificationAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const priorityBadge = {
  CRITICAL: 'badge-critical',
  HIGH: 'badge-high',
  MEDIUM: 'badge-medium',
  LOW: 'badge-low',
};

const statusColors = {
  SUBMITTED: 'bg-gray-100 text-gray-700',
  UNDER_REVIEW: 'bg-blue-100 text-blue-700',
  ASSIGNED: 'bg-yellow-100 text-yellow-800',
  IN_PROGRESS: 'bg-primary-100 text-primary-700',
  RESOLVED: 'bg-green-100 text-green-700',
  CLOSED: 'bg-gray-200 text-gray-600',
};

export default function ComplaintDetail() {
  const { id } = useParams();
  const { hasRole } = useAuth();
  const [complaint, setComplaint] = useState(null);
  const [verification, setVerification] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [statusNote, setStatusNote] = useState('');
  const [newStatus, setNewStatus] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [cRes, vRes] = await Promise.allSettled([
          complaintsAPI.get(id),
          verificationAPI.get(id),
        ]);
        if (cRes.status === 'fulfilled') setComplaint(cRes.value.data);
        if (vRes.status === 'fulfilled') setVerification(vRes.value.data);
      } catch {
        // handled below
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  const handleStatusUpdate = async () => {
    if (!newStatus) return;
    setActionLoading(true);
    try {
      await complaintsAPI.updateStatus(id, { status: newStatus, notes: statusNote });
      const { data } = await complaintsAPI.get(id);
      setComplaint(data);
      setNewStatus('');
      setStatusNote('');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <LoadingSpinner label="Loading complaint…" />;
  if (!complaint) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-lg">Complaint not found</p>
        <Link to="/dashboard" className="text-primary-600 hover:underline mt-2 inline-block">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 flex items-center gap-2">
        <Link to="/dashboard" className="hover:text-primary-600">Dashboard</Link>
        <span>/</span>
        <span className="text-gray-900 font-medium">{complaint.complaint_id}</span>
      </nav>

      {/* Header */}
      <div className="card p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="text-xl font-bold text-gray-900">{complaint.title}</h1>
            <p className="text-sm text-gray-500 mt-1">ID: {complaint.complaint_id}</p>
          </div>
          <div className="flex items-center gap-2">
            <span className={`badge ${priorityBadge[complaint.priority] || 'badge-low'}`}>
              {complaint.priority}
            </span>
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[complaint.status] || ''}`}>
              {complaint.status?.replace('_', ' ')}
            </span>
          </div>
        </div>

        <p className="mt-4 text-sm text-gray-700 leading-relaxed">{complaint.description}</p>

        {/* Metadata grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-4 border-t border-gray-100">
          <MetaItem label="Ward" value={complaint.ward_name} />
          <MetaItem label="Category" value={complaint.category_name} />
          <MetaItem label="Priority Score" value={complaint.priority_score?.toFixed(2)} />
          <MetaItem label="Sentiment" value={complaint.sentiment_label} />
          <MetaItem label="Source" value={complaint.source} />
          <MetaItem label="Created" value={new Date(complaint.created_at).toLocaleString()} />
          <MetaItem label="Assigned To" value={complaint.assigned_to_name || '—'} />
          <MetaItem label="AI Duplicate" value={complaint.is_duplicate ? 'Yes' : 'No'} />
        </div>

        {/* AI Analysis */}
        {complaint.ai_summary && (
          <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
            <p className="text-xs font-semibold text-blue-700 mb-1">AI Summary</p>
            <p className="text-sm text-blue-900">{complaint.ai_summary}</p>
          </div>
        )}

        {/* Image */}
        {complaint.image_url && (
          <div className="mt-4">
            <p className="text-xs font-semibold text-gray-500 mb-2">Attached Image</p>
            <img
              src={complaint.image_url}
              alt="Complaint evidence"
              className="rounded-lg max-h-64 object-cover border"
            />
          </div>
        )}
      </div>

      {/* Verification */}
      {verification && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">4-Layer Verification</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <VerifyItem label="GPS Match" passed={verification.gps_verified} score={verification.gps_score} />
            <VerifyItem label="Timestamp" passed={verification.timestamp_verified} score={verification.timestamp_score} />
            <VerifyItem label="Visual Check" passed={verification.visual_verified} score={verification.visual_score} />
            <VerifyItem label="Tamper Detect" passed={!verification.tamper_detected} score={verification.tamper_score} />
          </div>
          <div className="mt-4 flex items-center gap-4">
            <span className="text-sm text-gray-600">
              Overall Score: <span className="font-bold text-lg">{verification.overall_score?.toFixed(1)}%</span>
            </span>
            <span className={`badge ${verification.is_verified ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {verification.is_verified ? 'Verified' : 'Not Verified'}
            </span>
          </div>
        </div>
      )}

      {/* Status Update (leaders/dept heads only) */}
      {hasRole('LEADER', 'DEPARTMENT_HEAD', 'ADMIN') && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Update Status</h2>
          <div className="flex flex-wrap gap-3">
            <select
              value={newStatus}
              onChange={(e) => setNewStatus(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
            >
              <option value="">Select status…</option>
              {['UNDER_REVIEW', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'].map((s) => (
                <option key={s} value={s}>{s.replace('_', ' ')}</option>
              ))}
            </select>
            <input
              type="text"
              value={statusNote}
              onChange={(e) => setStatusNote(e.target.value)}
              placeholder="Notes (optional)"
              className="flex-1 min-w-[200px] border border-gray-300 rounded-lg px-3 py-2 text-sm"
            />
            <button
              onClick={handleStatusUpdate}
              disabled={!newStatus || actionLoading}
              className="bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium
                hover:bg-primary-700 disabled:opacity-50 transition-colors"
            >
              {actionLoading ? 'Updating…' : 'Update'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function MetaItem({ label, value }) {
  return (
    <div>
      <p className="text-xs text-gray-400">{label}</p>
      <p className="text-sm font-medium text-gray-900">{value || '—'}</p>
    </div>
  );
}

function VerifyItem({ label, passed, score }) {
  return (
    <div className={`p-3 rounded-lg border ${passed ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
      <p className="text-xs text-gray-600">{label}</p>
      <p className={`text-lg font-bold ${passed ? 'text-green-700' : 'text-red-700'}`}>
        {passed ? '✓ Pass' : '✗ Fail'}
      </p>
      {score != null && <p className="text-xs text-gray-500">Score: {score.toFixed(1)}</p>}
    </div>
  );
}
