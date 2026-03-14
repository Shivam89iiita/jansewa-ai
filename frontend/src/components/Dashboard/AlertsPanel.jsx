const severityStyles = {
  critical: 'border-red-400 bg-red-50',
  high: 'border-orange-400 bg-orange-50',
  medium: 'border-yellow-400 bg-yellow-50',
  info: 'border-blue-400 bg-blue-50',
};

export default function AlertsPanel({ alerts = [] }) {
  if (!alerts.length) {
    return (
      <div className="card p-6 text-center text-gray-400">
        <p>No active alerts</p>
      </div>
    );
  }

  return (
    <div className="card overflow-hidden">
      <div className="px-5 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Active Alerts</h3>
        <p className="text-xs text-gray-500 mt-0.5">Real-time alerts from social media and AI</p>
      </div>
      <div className="divide-y divide-gray-50 max-h-[360px] overflow-y-auto">
        {alerts.map((alert, i) => {
          const sev = alert.severity?.toLowerCase() || 'info';
          return (
            <div
              key={i}
              className={`px-5 py-3 border-l-4 ${severityStyles[sev] || severityStyles.info}`}
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <p className="text-sm font-medium text-gray-900">{alert.title || alert.message}</p>
                  {alert.description && (
                    <p className="text-xs text-gray-600 mt-0.5">{alert.description}</p>
                  )}
                  {alert.ward_name && (
                    <span className="text-xs text-gray-400">Ward: {alert.ward_name}</span>
                  )}
                </div>
                <span className="text-xs text-gray-400 whitespace-nowrap">{alert.time || ''}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
