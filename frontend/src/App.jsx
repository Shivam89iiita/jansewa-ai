import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Pages
import Login from './pages/Login';
import LeaderDashboard from './pages/LeaderDashboard';
import ComplaintDetail from './pages/ComplaintDetail';
import VerificationPage from './pages/VerificationPage';
import SocialMediaInsights from './pages/SocialMediaInsights';
import Communications from './pages/Communications';
import PublicPortal from './pages/PublicPortal';

// Layout
import Navbar from './components/Common/Navbar';
import Sidebar from './components/Common/Sidebar';

function ProtectedLayout({ children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 bg-gray-50 overflow-auto">{children}</main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/public" element={<PublicPortal />} />
          <Route path="/public/ward/:wardId" element={<PublicPortal />} />

          {/* Protected routes */}
          <Route path="/dashboard" element={<ProtectedLayout><LeaderDashboard /></ProtectedLayout>} />
          <Route path="/complaints/:id" element={<ProtectedLayout><ComplaintDetail /></ProtectedLayout>} />
          <Route path="/verification/:id" element={<ProtectedLayout><VerificationPage /></ProtectedLayout>} />
          <Route path="/social" element={<ProtectedLayout><SocialMediaInsights /></ProtectedLayout>} />
          <Route path="/communications" element={<ProtectedLayout><Communications /></ProtectedLayout>} />

          {/* Default redirect */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
