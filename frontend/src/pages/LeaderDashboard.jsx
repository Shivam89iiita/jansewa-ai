import { useState, useEffect } from 'react';
import { dashboardAPI, complaintsAPI, socialAPI } from '../services/api';
import StatsCards from '../components/Dashboard/StatsCards';
import PriorityQueue from '../components/Dashboard/PriorityQueue';
import WardHeatMap from '../components/Dashboard/WardHeatMap';
import SentimentChart from '../components/Dashboard/SentimentChart';
import AlertsPanel from '../components/Dashboard/AlertsPanel';
import LoadingSpinner from '../components/Common/LoadingSpinner';

export default function LeaderDashboard() {
  const [stats, setStats] = useState(null);
  const [queue, setQueue] = useState([]);
  const [heatmap, setHeatmap] = useState([]);
  const [sentiment, setSentiment] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        const [statsRes, queueRes, heatRes, sentRes, alertRes] = await Promise.allSettled([
          complaintsAPI.stats(),
          complaintsAPI.priorityQueue({ limit: 15 }),
          dashboardAPI.wardHeatmap(),
          dashboardAPI.sentimentTrend(30),
          socialAPI.alerts(),
        ]);

        if (statsRes.status === 'fulfilled') setStats(statsRes.value.data);
        if (queueRes.status === 'fulfilled') setQueue(queueRes.value.data?.complaints || queueRes.value.data || []);
        if (heatRes.status === 'fulfilled') setHeatmap(heatRes.value.data || []);
        if (sentRes.status === 'fulfilled') setSentiment(sentRes.value.data || []);
        if (alertRes.status === 'fulfilled') setAlerts(alertRes.value.data || []);
      } catch (e) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <LoadingSpinner label="Loading dashboard…" />;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Leader Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">AI-powered overview of governance operations</p>
      </div>

      {error && (
        <div className="p-3 rounded-lg bg-yellow-50 border border-yellow-200 text-yellow-800 text-sm">
          {error}
        </div>
      )}

      {/* Stats */}
      <StatsCards data={stats} />

      {/* Two-column grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <PriorityQueue complaints={queue} />
        <AlertsPanel alerts={alerts} />
      </div>

      {/* Map + Sentiment */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <WardHeatMap data={heatmap} />
        <SentimentChart data={sentiment} />
      </div>
    </div>
  );
}
