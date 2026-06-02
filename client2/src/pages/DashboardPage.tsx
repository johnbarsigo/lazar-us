import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store';
import PageHeader from '../components/PageHeader';

const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    activeTenants: 0,
    occupiedRooms: 0,
    pendingPayments: 0,
    monthlyRevenue: 0,
  });

  useEffect(() => {
    // Fetch dashboard stats from API
    // This is a placeholder
    setStats({
      activeTenants: 24,
      occupiedRooms: 18,
      pendingPayments: 12,
      monthlyRevenue: 450000,
    });
  }, []);

  const quickActions = [
    {
      title: 'Manage Tenants',
      description: 'View and add tenants',
      action: () => navigate('/tenants'),
      color: 'from-orange-400 to-orange-600',
    },
    {
      title: 'Generate Billings',
      description: 'Create monthly charges',
      action: () => navigate('/billings'),
      color: 'from-orange-500 to-orange-700',
    },
    {
      title: 'View Reports',
      description: 'Check system reports',
      action: () => navigate('/reports'),
      color: 'from-orange-300 to-orange-500',
    },
    {
      title: 'Manage Rooms',
      description: 'View room status',
      action: () => navigate('/rooms'),
      color: 'from-orange-400 to-orange-600',
    },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title={`Welcome back, ${user?.username}!`}
        description="Track occupancy, collections, and hostel performance from one dashboard."
      />

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Active Tenants"
          value={stats.activeTenants}
          icon="👥"
          color="blue"
        />
        <StatCard
          title="Occupied Rooms"
          value={stats.occupiedRooms}
          icon="🚪"
          color="green"
        />
        <StatCard
          title="Pending Payments"
          value={stats.pendingPayments}
          icon="⏳"
          color="yellow"
        />
        <StatCard
          title="Monthly Revenue"
          value={`KSh ${stats.monthlyRevenue.toLocaleString()}`}
          icon="💰"
          color="orange"
        />
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">
          Quick Actions
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => (
            <button
              key={action.title}
              onClick={action.action}
              className={`bg-gradient-to-br ${action.color} text-white rounded-lg p-6 hover:shadow-lg transform hover:scale-105 transition-all`}
            >
              <h3 className="text-lg font-bold mb-1">{action.title}</h3>
              <p className="text-sm opacity-90">{action.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">
          Recent Activity
        </h2>
        <div className="space-y-3">
          <ActivityItem
            type="payment"
            message="Payment received from John Doe for Room 101"
            time="2 hours ago"
          />
          <ActivityItem
            type="tenant"
            message="New tenant Sarah Smith checked in to Room 205"
            time="5 hours ago"
          />
          <ActivityItem
            type="billing"
            message="Monthly billings generated for May 2026"
            time="1 day ago"
          />
        </div>
      </div>
    </div>
  );
};

interface StatCardProps {
  title: string;
  value: string | number;
  icon: string;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400',
    purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400',
    orange: 'bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-200',
  };

  return (
    <div className={`card ${colorClasses[color as keyof typeof colorClasses]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-600 dark:text-orange-200">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );
};

interface ActivityItemProps {
  type: 'payment' | 'tenant' | 'billing';
  message: string;
  time: string;
}

const ActivityItem: React.FC<ActivityItemProps> = ({ type, message, time }) => {
  const icons = {
    payment: '💳',
    tenant: '👤',
    billing: '📄',
  };

  return (
    <div className="flex gap-4 pb-3 border-b border-slate-200 dark:border-slate-700 last:border-0">
      <div className="text-2xl">{icons[type]}</div>
      <div className="flex-1">
        <p className="text-slate-900 dark:text-white text-sm">{message}</p>
        <p className="text-xs text-slate-500 dark:text-orange-200 mt-1">{time}</p>
      </div>
    </div>
  );
};

export default DashboardPage;
