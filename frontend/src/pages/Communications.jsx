import { useState, useEffect } from 'react';
import { communicationsAPI } from '../services/api';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const TYPE_OPTIONS = ['press_release', 'social_update', 'citizen_notice', 'emergency_alert', 'progress_report'];
const FORMAT_OPTIONS = ['formal', 'simple', 'social_media'];

export default function Communications() {
  const [comms, setComms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    complaint_id: '',
    comm_type: 'citizen_notice',
    format: 'simple',
    language: 'english',
  });
  const [generatedContent, setGeneratedContent] = useState(null);

  useEffect(() => {
    loadComms();
  }, []);

  async function loadComms() {
    setLoading(true);
    try {
      const { data } = await communicationsAPI.list({ limit: 30 });
      setComms(data || []);
    } finally {
      setLoading(false);
    }
  }

  const handleGenerate = async (e) => {
    e.preventDefault();
    setGenerating(true);
    try {
      const { data } = await communicationsAPI.generate(form);
      setGeneratedContent(data);
      await loadComms();
    } catch (err) {
      alert(err.response?.data?.detail || 'Generation failed');
    } finally {
      setGenerating(false);
    }
  };

  const handleApprove = async (id) => {
    await communicationsAPI.approve(id);
    await loadComms();
  };

  const handlePublish = async (id) => {
    await communicationsAPI.publish(id);
    await loadComms();
  };

  if (loading) return <LoadingSpinner label="Loading communications…" />;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Communications</h1>
          <p className="text-sm text-gray-500 mt-1">Generate, approve, and publish governance communications</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors"
        >
          {showForm ? 'Close' : '+ Generate New'}
        </button>
      </div>

      {/* Generate form */}
      {showForm && (
        <form onSubmit={handleGenerate} className="card p-6 space-y-4">
          <h2 className="text-lg font-semibold">Generate Communication</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Complaint ID (optional)</label>
              <input
                type="text"
                value={form.complaint_id}
                onChange={(e) => setForm({ ...form, complaint_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                placeholder="CMP-2025-00001"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
              <select
                value={form.comm_type}
                onChange={(e) => setForm({ ...form, comm_type: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                {TYPE_OPTIONS.map((t) => (
                  <option key={t} value={t}>{t.replace(/_/g, ' ')}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Format</label>
              <select
                value={form.format}
                onChange={(e) => setForm({ ...form, format: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                {FORMAT_OPTIONS.map((f) => (
                  <option key={f} value={f}>{f.replace(/_/g, ' ')}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Language</label>
              <select
                value={form.language}
                onChange={(e) => setForm({ ...form, language: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="english">English</option>
                <option value="hindi">Hindi</option>
                <option value="bilingual">Bilingual</option>
              </select>
            </div>
          </div>
          <button
            type="submit"
            disabled={generating}
            className="bg-primary-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium
              hover:bg-primary-700 disabled:opacity-50 transition-colors"
          >
            {generating ? 'Generating with AI…' : 'Generate'}
          </button>
        </form>
      )}

      {/* Generated preview */}
      {generatedContent && (
        <div className="card p-6 border-l-4 border-primary-500">
          <h3 className="font-semibold mb-2">Generated Content</h3>
          <div className="prose prose-sm max-w-none whitespace-pre-wrap text-gray-700">
            {generatedContent.content || generatedContent.english_content}
          </div>
          {generatedContent.hindi_content && (
            <div className="mt-4 pt-4 border-t prose prose-sm max-w-none whitespace-pre-wrap text-gray-700">
              <p className="text-xs font-semibold text-gray-500 mb-1">Hindi Version</p>
              {generatedContent.hindi_content}
            </div>
          )}
        </div>
      )}

      {/* Communications list */}
      <div className="card overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-100">
          <h2 className="font-semibold text-gray-900">All Communications</h2>
        </div>
        <div className="divide-y">
          {comms.length === 0 ? (
            <p className="px-5 py-8 text-center text-gray-400">No communications yet</p>
          ) : (
            comms.map((c) => (
              <div key={c.id} className="px-5 py-4 flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium px-2 py-0.5 rounded bg-gray-100 text-gray-600">
                      {c.comm_type?.replace(/_/g, ' ')}
                    </span>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded ${
                      c.status === 'PUBLISHED' ? 'bg-green-100 text-green-700'
                        : c.status === 'APPROVED' ? 'bg-blue-100 text-blue-700'
                        : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {c.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700 line-clamp-2">{c.content?.slice(0, 200)}</p>
                  <p className="text-xs text-gray-400 mt-1">{new Date(c.created_at).toLocaleString()}</p>
                </div>
                <div className="flex gap-2">
                  {c.status === 'DRAFT' && (
                    <button
                      onClick={() => handleApprove(c.id)}
                      className="text-xs text-blue-600 hover:underline"
                    >
                      Approve
                    </button>
                  )}
                  {c.status === 'APPROVED' && (
                    <button
                      onClick={() => handlePublish(c.id)}
                      className="text-xs text-green-600 hover:underline"
                    >
                      Publish
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
