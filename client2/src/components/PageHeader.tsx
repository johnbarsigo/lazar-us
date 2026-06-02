import React from 'react';
import { LucideIcon } from 'lucide-react';

interface PageHeaderProps {
  title: string;
  description?: string;
  icon?: LucideIcon;
  action?: {
    label: string;
    onClick: () => void;
    icon: LucideIcon;
  };
}

const PageHeader: React.FC<PageHeaderProps> = ({ title, description, icon: Icon, action }) => {
  return (
    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div className="flex items-start gap-4">
        {Icon && (
          <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-orange-100 text-orange-700 shadow-[0_16px_40px_rgba(255,140,0,0.12)] dark:bg-orange-900/20 dark:text-orange-300">
            <Icon size={28} />
          </div>
        )}
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">{title}</h1>
          {description && (
            <p className="mt-2 max-w-2xl text-sm text-slate-600 dark:text-slate-300">
              {description}
            </p>
          )}
        </div>
      </div>

      {action && (
        <button
          onClick={action.onClick}
          className="btn-primary flex items-center gap-2 whitespace-nowrap"
        >
          <action.icon size={18} />
          {action.label}
        </button>
      )}
    </div>
  );
};

export default PageHeader;
