export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 py-4 px-6">
      <div className="flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-gray-500">
        <p>&copy; {new Date().getFullYear()} Jansewa AI — AI-Powered Governance Intelligence Platform</p>
        <p>Built for Smart India Hackathon 2025</p>
      </div>
    </footer>
  );
}
