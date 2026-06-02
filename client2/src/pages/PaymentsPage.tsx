import React, { useState, useEffect } from 'react';
import { Plus, CreditCard } from 'lucide-react';
import PageHeader from '../components/PageHeader';
import { paymentsAPI } from '../api/client';
import { Payment } from '../types';

const initialPaymentForm = {
  monthly_charge_id: 0,
  amount: 0,
  method: 'mpesa' as 'mpesa' | 'cash' | 'bank',
  payment_date: new Date().toISOString().slice(0, 10),
  mpesa_receipt: '',
};

const PaymentsPage: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<'all' | 'pending' | 'completed' | 'failed'>('all');
  const [showRecordModal, setShowRecordModal] = useState(false);
  const [paymentForm, setPaymentForm] = useState(initialPaymentForm);
  const [recordingPayment, setRecordingPayment] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

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

  const handlePaymentInput = (field: string, value: string | number) => {
    setPaymentForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleRecordPayment = async () => {
    setRecordingPayment(true);
    setStatusMessage(null);

    try {
      await paymentsAPI.record({
        monthly_charge_id: paymentForm.monthly_charge_id,
        amount: paymentForm.amount,
        method: paymentForm.method,
        payment_date: paymentForm.payment_date,
        mpesa_receipt: paymentForm.mpesa_receipt || undefined,
      });
      setStatusMessage('Payment recorded successfully.');
      setShowRecordModal(false);
      setPaymentForm(initialPaymentForm);
      fetchPayments();
    } catch (err) {
      console.error('Failed to record payment', err);
      setStatusMessage('Could not record payment.');
    } finally {
      setRecordingPayment(false);
    }
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
      <PageHeader
        title="Payments"
        description="Record and review payments"
        icon={CreditCard}
        action={{
          label: 'Record Payment',
          onClick: () => setShowRecordModal(true),
          icon: Plus,
        }}
      />

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

      {statusMessage && (
        <div className="card text-sm text-slate-700 dark:text-slate-200">
          {statusMessage}
        </div>
      )}

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
                  : 'bg-orange-50 text-orange-700 dark:bg-orange-900/20 dark:text-orange-200 hover:bg-orange-100 dark:hover:bg-orange-800'
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
                    <span className={`status-pill ${getStatusColor(payment.status)}`}>
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

      {showRecordModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="w-full max-w-lg bg-white dark:bg-slate-900 rounded-2xl shadow-xl p-6">
            <div className="flex items-center justify-between gap-4 mb-6">
              <div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Record Payment</h2>
                <p className="text-sm text-slate-500 dark:text-slate-400">Enter payment details to add a new transaction.</p>
              </div>
              <button
                onClick={() => setShowRecordModal(false)}
                className="text-slate-500 hover:text-slate-900 dark:hover:text-white"
              >
                Close
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="label">Monthly Charge ID</label>
                <input
                  type="number"
                  min={1}
                  value={paymentForm.monthly_charge_id}
                  onChange={(e) => handlePaymentInput('monthly_charge_id', Number(e.target.value))}
                  className="input-field"
                  placeholder="Enter billing ID"
                />
              </div>
              <div>
                <label className="label">Amount</label>
                <input
                  type="number"
                  min={0}
                  step={0.01}
                  value={paymentForm.amount}
                  onChange={(e) => handlePaymentInput('amount', Number(e.target.value))}
                  className="input-field"
                />
              </div>
              <div>
                <label className="label">Method</label>
                <select
                  value={paymentForm.method}
                  onChange={(e) => handlePaymentInput('method', e.target.value)}
                  className="input-field"
                >
                  <option value="mpesa">Mpesa</option>
                  <option value="cash">Cash</option>
                  <option value="bank">Bank</option>
                </select>
              </div>
              <div>
                <label className="label">Payment Date</label>
                <input
                  type="date"
                  value={paymentForm.payment_date}
                  onChange={(e) => handlePaymentInput('payment_date', e.target.value)}
                  className="input-field"
                />
              </div>
              <div>
                <label className="label">Receipt Reference</label>
                <input
                  type="text"
                  value={paymentForm.mpesa_receipt}
                  onChange={(e) => handlePaymentInput('mpesa_receipt', e.target.value)}
                  className="input-field"
                  placeholder="Optional receipt code"
                />
              </div>
            </div>

            <div className="mt-6 flex flex-col sm:flex-row items-center gap-3 justify-end">
              <button
                onClick={() => setShowRecordModal(false)}
                className="btn-secondary w-full sm:w-auto"
              >
                Cancel
              </button>
              <button
                onClick={handleRecordPayment}
                disabled={recordingPayment}
                className="btn-primary w-full sm:w-auto"
              >
                {recordingPayment ? 'Recording...' : 'Record Payment'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PaymentsPage;
