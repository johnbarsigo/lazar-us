import React, { useState, useEffect } from 'react';
import { Plus, Filter } from 'lucide-react';
import { paymentsAPI } from '../api/client';
import { Payment } from '../types';

const PaymentsPage: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<'all' | 'pending' | 'completed' | 'failed'>('all');

  useEffect(() => {
    fetchPayments();
  }, []);

  const fetchPayments = async () => {
    try {
      const response = await paymentsAPI.list();
      setPayments(response.data);
    } catch (err) {
      console.error('Failed to fetch payments', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredPayments = payments.filter(
    (p) => filterStatus === 'all' || p.status === filterStatus
  );

  const stats = {
    completed: payments.filter((p) => p.status === 'completed').length,
    pending: payments.filter((p) => p.status === 'pending').length,
    failed: payments.filter((p) => p.status === 'failed').length,
    total: payments
      .filter((p) => p.status === 'completed')
      .reduce((sum, p) => sum + parseFloat(p.amount.toString()), 0),
  };

  const getStatusColor = (status: Payment['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400';
      case 'pending':
        return 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400';
      case 'failed':
        return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400';
      default:
        return '';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Payments</h1>
        <button className="btn-primary flex items-center gap-2 w-full sm:w-auto justify-center">
          <Plus size={20} />
          Record Payment
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card">
          <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Completed</div>
          <div className="text-3xl font-bold text-green-600">{stats.completed}</div>
        </div>
        <div className="card">
          <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Pending</div>
          <div className="text-3xl font-bold text-yellow-600">{stats.pending}</div>
        </div>
        <div className="card">
          <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Failed</div>
          <div className="text-3xl font-bold text-red-600">{stats.failed}</div>
        </div>
        <div className="card bg-primary-50 dark:bg-primary-900/20">
          <div className="text-sm text-primary-600 dark:text-primary-400 mb-1">Total Received</div>
          <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            KSh {stats.total.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Filter */}
      <div className="card">
        <div className="flex gap-2 flex-wrap">
          {(['all', 'completed', 'pending', 'failed'] as const).map((status) => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filterStatus === status
                  ? 'bg-primary-600 text-white'
                  : 'bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-50 hover:bg-slate-300 dark:hover:bg-slate-600'
              }`}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Payments Table */}
      {loading ? (
        <div className="text-center py-8">Loading payments...</div>
      ) : filteredPayments.length === 0 ? (
        <div className="card text-center py-8 text-slate-500">No payments found</div>
      ) : (
        <div className="card table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Tenant</th>
                <th>Amount</th>
                <th>Method</th>
                <th>Status</th>
                <th>Payment Date</th>
                <th>Receipt</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPayments.map((payment) => (
                <tr key={payment.id}>
                  <td className="font-medium">{payment.monthly_charge?.occupancy?.tenant?.name}</td>
                  <td>KSh {parseFloat(payment.amount.toString()).toLocaleString()}</td>
                  <td className="capitalize">{payment.method}</td>
                  <td>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(payment.status)}`}>
                      {payment.status.charAt(0).toUpperCase() + payment.status.slice(1)}
                    </span>
                  </td>
                  <td>{new Date(payment.payment_date).toLocaleDateString()}</td>
                  <td>{payment.mpesa_receipt || '-'}</td>
                  <td>
                    <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default PaymentsPage;
