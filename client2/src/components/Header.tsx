import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store';
import { LogOut, Menu } from 'lucide-react';
import ThemeToggle from './ThemeToggle';

interface HeaderProps {
  onToggleSidebar: () => void;
}

const Header: React.FC<HeaderProps> = ({ onToggleSidebar }) => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-white/95 dark:bg-slate-950/95 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-50 backdrop-blur">
      <div className="px-6 py-4 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={onToggleSidebar}
            className="lg:hidden p-2 rounded-2xl text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <Menu size={24} />
          </button>

          <div>
            <h1 className="text-2xl font-bold text-orange-600">OKS Hostel</h1>
            <p className="text-sm text-slate-600 dark:text-orange-200">Management System</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <ThemeToggle />

          <div className="hidden sm:block h-8 w-px bg-slate-300 dark:bg-slate-700" />

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-slate-900 dark:text-white">{user?.username}</p>
              <p className="text-xs text-slate-600 dark:text-orange-200 capitalize">{user?.role}</p>
            </div>

            <button
              onClick={handleLogout}
              className="p-2 rounded-2xl text-orange-600 hover:bg-orange-100 dark:hover:bg-orange-900/20"
              title="Logout"
            >
              <LogOut size={20} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
