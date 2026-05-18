import React, { useState, useEffect } from 'react';
import { Plus, AlertCircle } from 'lucide-react';
import { billingsAPI } from '../api/client';
import { MonthlyCharge } from '../types';

const BillingsPage: React.FC = () => {
  const [billings, setBillings] = useState<MonthlyCharge[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterMonth, setFilterMonth] = useState(new Date().getMonth() + 1);
  const [filterYear, setFilterYear] = useState(new Date().getFullYear());

  useEffect(() => {
    fetchBillings();
  }, [filterMonth, filterYear]);

  const fetchBillings = async () => {
    try {
      const response = await billingsAPI.list();
      setBillings(response.data);
    } catch (err) {
      console.error('Failed to fetch billings', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredBillings = billings.filter(
    (b) => b.month === filterMonth && b.year === filterYear
  );

  const totalRent = filteredBillings.reduce((sum, b) => sum + parseFloat(b.rent_amount.toString()), 0);
  const totalWater = filteredBillings.reduce((sum, b) => sum + parseFloat(b.water_bill.toString()), 0);
  const totalBilling = totalRent + totalWater;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Billings</h1>
        <button className="btn-primary flex items-center gap-2 w-full sm:w-auto justify-center">
          <Plus size={20} />
          Generate Billings
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card">
          <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Total Rent</div>
          <div className="text-3xl font-bold">KSh {totalRent.toLocaleString()}</div>
        </div>
        <div className="card">
          <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Total Water Bill</div>
          <div className="text-3xl font-bold">KSh {totalWater.toLocaleString()}</div>
        </div>
        <div className="card bg-primary-50 dark:bg-primary-900/20">
          <div className="text-sm text-primary-600 dark:text-primary-400 mb-1">Total Billings</div>
          <div className="text-3xl font-bold text-primary-600 dark:text-primary-400">
            KSh {totalBilling.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="label">Month</label>
            <select
              value={filterMonth}
              onChange={(e) => setFilterMonth(parseInt(e.target.value))}
              className="input-field"
            >
              {Array.from({ length: 12 }, (_, i) => (
                <option key={i} value={i + 1}>
                  {new Date(2000, i).toLocaleDateString('en-US', { month: 'long' })}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Year</label>
            <select
              value={filterYear}
              onChange={(e) => setFilterYear(parseInt(e.target.value))}
              className="input-field"
            >
              {Array.from({ length: 5 }, (_, i) => (
                <option key={i} value={new Date().getFullYear() - 2 + i}>
                  {new Date().getFullYear() - 2 + i}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Billings Table */}
      {loading ? (
        <div className="text-center py-8">Loading billings...</div>
      ) : filteredBillings.length === 0 ? (
        <div className="card text-center py-8">
          <AlertCircle className="mx-auto mb-2 text-yellow-600" size={32} />
          <p className="text-slate-600 dark:text-slate-400">No billings for this period</p>
        </div>
      ) : (
        <div className="card table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Room</th>
                <th>Tenant</th>
                <th>Rent</th>
                <th>Water</th>
                <th>Total</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredBillings.map((billing) => (
                <tr key={billing.id}>
                  <td className="font-medium">{billing.occupancy?.room?.room_number}</td>
                  <td>{billing.occupancy?.tenant?.name}</td>
                  <td>KSh {parseFloat(billing.rent_amount.toString()).toLocaleString()}</td>
                  <td>KSh {parseFloat(billing.water_bill.toString()).toLocaleString()}</td>
                  <td className="font-bold">
                    KSh {(parseFloat(billing.rent_amount.toString()) + parseFloat(billing.water_bill.toString())).toLocaleString()}
                  </td>
                  <td>{new Date(billing.charge_date).toLocaleDateString()}</td>
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

export default BillingsPage;
