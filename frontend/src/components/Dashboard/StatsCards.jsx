const cards = [
  { key: 'total', label: 'Total Complaints', color: 'bg-blue-500', icon: '📋' },
  { key: 'pending', label: 'Pending', color: 'bg-yellow-500', icon: '⏳' },
  { key: 'in_progress', label: 'In Progress', color: 'bg-primary-500', icon: '🔄' },
  { key: 'resolved', label: 'Resolved', color: 'bg-green-500', icon: '✅' },
  { key: 'critical', label: 'Critical', color: 'bg-red-500', icon: '🚨' },
  { key: 'avg_resolution', label: 'Avg Resolution (hrs)', color: 'bg-purple-500', icon: '⏱️' },
];

export default function StatsCards({ data }) {
  if (!data) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
      {cards.map((card) => (
        <div key={card.key} className="card p-4">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg ${card.color} bg-opacity-10 flex items-center justify-center text-lg`}>
              {card.icon}
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {typeof data[card.key] === 'number'
                  ? card.key === 'avg_resolution'
                    ? data[card.key].toFixed(1)
                    : data[card.key].toLocaleString()
                  : data[card.key] ?? '—'}
              </p>
              <p className="text-xs text-gray-500">{card.label}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
