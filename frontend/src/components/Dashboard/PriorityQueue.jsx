import { Link } from 'react-router-dom';

const priorityColors = {
  CRITICAL: 'badge-critical',
  HIGH: 'badge-high',
  MEDIUM: 'badge-medium',
  LOW: 'badge-low',
};

export default function PriorityQueue({ complaints = [] }) {
  if (!complaints.length) {
    return (
      <div className="card p-6 text-center text-gray-400">
        <p>No complaints in queue</p>
      </div>
    );
  }

  return (
    <div className="card overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Priority Queue</h3>
        <p className="text-xs text-gray-500 mt-0.5">Top complaints ranked by AI priority score</p>
      </div>
      <div className="divide-y divide-gray-50 max-h-[420px] overflow-y-auto">
        {complaints.map((c, idx) => (
          <Link
            key={c.id}
            to={`/complaints/${c.id}`}
            className="flex items-start gap-3 px-5 py-3 hover:bg-gray-50 transition-colors"
          >
            <span className="text-xs font-bold text-gray-400 mt-1 w-5 text-right">
              {idx + 1}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{c.title}</p>
              <p className="text-xs text-gray-500 mt-0.5">
                {c.ward_name} • {c.category_name}
              </p>
            </div>
            <div className="flex flex-col items-end gap-1">
              <span className={`badge ${priorityColors[c.priority] || 'badge-low'}`}>
                {c.priority}
              </span>
              <span className="text-xs text-gray-400">
                Score: {c.priority_score?.toFixed(1)}
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
