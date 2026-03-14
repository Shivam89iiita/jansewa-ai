export default function LoadingSpinner({ size = 'md', label = 'Loading…' }) {
  const sizeMap = { sm: 'w-5 h-5', md: 'w-8 h-8', lg: 'w-12 h-12' };
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-3">
      <div
        className={`${sizeMap[size]} border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin`}
      />
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  );
}
