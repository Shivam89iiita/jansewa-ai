import { useState, useEffect } from 'react';
import { socialAPI } from '../services/api';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const sentimentBadge = {
  POSITIVE: 'bg-green-100 text-green-700',
  NEGATIVE: 'bg-red-100 text-red-700',
  NEUTRAL: 'bg-gray-100 text-gray-600',
};

export default function SocialMediaInsights() {
  const [posts, setPosts] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [feedRes, alertRes, sentRes] = await Promise.allSettled([
        socialAPI.feed({ limit: 30 }),
        socialAPI.alerts(),
        socialAPI.sentiment(),
      ]);
      if (feedRes.status === 'fulfilled') setPosts(feedRes.value.data || []);
      if (alertRes.status === 'fulfilled') setAlerts(alertRes.value.data || []);
      if (sentRes.status === 'fulfilled') setSentimentData(sentRes.value.data);
    } finally {
      setLoading(false);
    }
  }

  const handleScan = async () => {
    setScanning(true);
    try {
      await socialAPI.scan();
      await loadData();
    } finally {
      setScanning(false);
    }
  };

  if (loading) return <LoadingSpinner label="Loading social media insights…" />;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Social Media Intelligence</h1>
          <p className="text-sm text-gray-500 mt-1">Real-time monitoring of public discourse</p>
        </div>
        <button
          onClick={handleScan}
          disabled={scanning}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg text-sm font-medium
            hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center gap-2"
        >
          {scanning ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Scanning…
            </>
          ) : (
            'Scan Now'
          )}
        </button>
      </div>

      {/* Sentiment summary */}
      {sentimentData && (
        <div className="grid grid-cols-3 gap-4">
          <SentCard label="Positive" count={sentimentData.positive} color="text-green-600" bg="bg-green-50" />
          <SentCard label="Negative" count={sentimentData.negative} color="text-red-600" bg="bg-red-50" />
          <SentCard label="Neutral" count={sentimentData.neutral} color="text-gray-600" bg="bg-gray-50" />
        </div>
      )}

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="card overflow-hidden">
          <div className="px-5 py-4 border-b border-gray-100 bg-red-50">
            <h2 className="font-semibold text-red-800">🚨 Active Alerts ({alerts.length})</h2>
          </div>
          <div className="divide-y max-h-60 overflow-y-auto">
            {alerts.map((a, i) => (
              <div key={i} className="px-5 py-3 flex items-start gap-3">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{a.title || a.message}</p>
                  {a.ward_name && <p className="text-xs text-gray-500">Ward: {a.ward_name}</p>}
                </div>
                <span className="text-xs text-gray-400">{a.virality_score?.toFixed(1)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feed */}
      <div className="card overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-100">
          <h2 className="font-semibold text-gray-900">Social Feed</h2>
        </div>
        <div className="divide-y">
          {posts.length === 0 ? (
            <p className="px-5 py-8 text-center text-gray-400">No posts found. Click "Scan Now" to fetch.</p>
          ) : (
            posts.map((post, i) => (
              <div key={i} className="px-5 py-4">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-gray-900">
                        @{post.author || 'anonymous'}
                      </span>
                      <span className="text-xs text-gray-400">{post.platform}</span>
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${sentimentBadge[post.sentiment?.toUpperCase()] || sentimentBadge.NEUTRAL}`}>
                        {post.sentiment}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700">{post.content}</p>
                    {post.ward_name && (
                      <p className="text-xs text-gray-400 mt-1">Ward: {post.ward_name}</p>
                    )}
                  </div>
                  <div className="text-right text-xs text-gray-400">
                    <p>❤️ {post.likes || 0}</p>
                    <p>🔄 {post.shares || 0}</p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

function SentCard({ label, count, color, bg }) {
  return (
    <div className={`card p-4 ${bg}`}>
      <p className="text-xs text-gray-500">{label}</p>
      <p className={`text-2xl font-bold ${color}`}>{count ?? 0}</p>
    </div>
  );
}
