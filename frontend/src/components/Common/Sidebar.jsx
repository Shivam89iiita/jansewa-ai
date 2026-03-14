import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const menuItems = [
  {
    to: '/dashboard',
    label: 'Dashboard',
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    ),
    roles: ['LEADER', 'DEPARTMENT_HEAD', 'WORKER', 'ADMIN'],
  },
  {
    to: '/social',
    label: 'Social Media',
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
      </svg>
    ),
    roles: ['LEADER', 'DEPARTMENT_HEAD', 'ADMIN'],
  },
  {
    to: '/communications',
    label: 'Communications',
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    ),
    roles: ['LEADER', 'DEPARTMENT_HEAD', 'ADMIN'],
  },
  {
    to: '/public',
    label: 'Public Portal',
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    roles: ['LEADER', 'DEPARTMENT_HEAD', 'WORKER', 'ADMIN'],
  },
];

export default function Sidebar() {
  const { hasRole } = useAuth();

  const navLinkClass = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'bg-primary-50 text-primary-700'
        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
    }`;

  return (
    <aside className="hidden lg:flex lg:flex-shrink-0">
      <div className="w-64 border-r border-gray-200 bg-white pt-5 pb-4 flex flex-col">
        <nav className="flex-1 px-3 space-y-1">
          {menuItems
            .filter((item) => hasRole(...item.roles))
            .map((item) => (
              <NavLink key={item.to} to={item.to} className={navLinkClass}>
                {item.icon}
                {item.label}
              </NavLink>
            ))}
        </nav>

        {/* Bottom section */}
        <div className="px-3 mt-auto">
          <div className="bg-primary-50 rounded-lg p-4">
            <p className="text-xs font-semibold text-primary-700 mb-1">Jansewa AI v1.0</p>
            <p className="text-xs text-primary-600">
              AI-Powered Governance Intelligence Platform
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
