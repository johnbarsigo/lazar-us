import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuthStore } from '../store';
import {
  LayoutDashboard,
  Users,
  DoorOpen,
  Receipt,
  CreditCard,
  BarChart3,
  Settings,
  X,
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { user } = useAuthStore();
  const isAdmin = user?.role === 'admin';

  const navItems = [
    { label: 'Dashboard', icon: LayoutDashboard, href: '/dashboard' },
    { label: 'Tenants', icon: Users, href: '/tenants' },
    { label: 'Rooms', icon: DoorOpen, href: '/rooms' },
    { label: 'Occupancies', icon: Receipt, href: '/occupancies' },
    { label: 'Billings', icon: Receipt, href: '/billings' },
    { label: 'Payments', icon: CreditCard, href: '/payments' },
    { label: 'Reports', icon: BarChart3, href: '/reports' },
    ...(isAdmin ? [{ label: 'Users', icon: Settings, href: '/users' }] : []),
  ];

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 lg:hidden z-40"
          onClick={onClose}
        ></div>
      )}

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-16 h-[calc(100vh-64px)] w-64 bg-white/95 dark:bg-slate-950/95 border-r border-slate-200 dark:border-slate-800 shadow-lg shadow-slate-900/5 transform transition-transform duration-300 lg:translate-x-0 z-40 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-6 space-y-8">
          {/* Close button for mobile */}
          <button
            onClick={onClose}
            className="lg:hidden absolute top-4 right-4 p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg"
          >
            <X size={20} />
          </button>

          {/* Navigation */}
          <nav className="space-y-2 mt-6">
            {navItems.map((item) => (
              <NavLink
                key={item.href}
                to={item.href}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-2xl transition-colors ${
                    isActive
                      ? 'bg-orange-50 text-orange-700 dark:bg-orange-900/20 dark:text-orange-300 font-semibold shadow-sm'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`
                }
              >
                <item.icon size={20} />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
