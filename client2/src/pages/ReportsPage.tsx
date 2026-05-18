import React, { useState, useEffect } from 'react';
import { Download, AlertTriangle } from 'lucide-react';
import { reportsAPI } from '../api/client';

interface ReportData {
  room_number: string;
  tenant_name: string;
  balance: number;
  last_payment_date: string;
}

const ReportsPage: React.FC = () => {
  const [activeReport, setActiveReport] = useState<'arrears' | 'income'>('arrears');
  const [arrears, setArrears] = useState<ReportData[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchReport();
  }, [activeReport]);

  const fetchReport = async () => {
    setLoading(true);
    try {
      if (activeReport === 'arrears') {
        const response = await reportsAPI.arrears();
        setArrears(response.data);
      } else {
        const response = await reportsAPI.income();
        setArrears(response.data);
      }
    } catch (err) {
      console.error('Failed to fetch report', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    // Implement PDF download functionality
    const csv = generateCSV();
    downloadCSV(csv, `${activeReport}-report.csv`);
  };

  const generateCSV = () => {
    if (activeReport === 'arrears') {
      let csv = 'Room,Tenant,Balance,Last Payment Date\n';
      arrears.forEach((row) => {
        csv += `${row.room_number},${row.tenant_name},${row.balance},${row.last_payment_date}\n`;
      });
      return csv;
    } else {
      return 'Income data would be here\n';
    }
  };

  const downloadCSV = (csv: string, filename: string) => {
    const link = document.createElement('a');
    link.href = `data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`;
    link.download = filename;
    link.click();
  };

  const totalArrears = arrears.reduce((sum, item) => sum + (item.balance || 0), 0);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Reports</h1>
        <button
          onClick={handleDownload}
          className="btn-primary flex items-center gap-2 w-full sm:w-auto justify-center"
        >
          <Download size={20} />
          Download Report
        </button>
      </div>

      {/* Report Tabs */}
      <div className="flex gap-2">
        {(['arrears', 'income'] as const).map((report) => (
          <button
            key={report}
            onClick={() => setActiveReport(report)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeReport === report
                ? 'bg-primary-600 text-white'
                : 'bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-50 hover:bg-slate-300 dark:hover:bg-slate-600'
            }`}
          >
            {report === 'arrears' ? 'Arrears Report' : 'Income Report'}
          </button>
        ))}
      </div>

      {/* Summary */}
      {activeReport === 'arrears' && (
        <div className="card bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
          <div className="flex items-center gap-4">
            <AlertTriangle className="text-red-600 flex-shrink-0" size={32} />
            <div>
              <h3 className="text-lg font-bold text-red-900 dark:text-red-100">Total Arrears</h3>
              <p className="text-2xl font-bold text-red-600 dark:text-red-400">
                KSh {totalArrears.toLocaleString()}
              </p>
              <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                {arrears.length} tenant{arrears.length !== 1 ? 's' : ''} with outstanding balance
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Report Data */}
      {loading ? (
        <div className="card text-center py-8">Loading report...</div>
      ) : arrears.length === 0 ? (
        <div className="card text-center py-8 text-slate-500">
          No data available for this report
        </div>
      ) : (
        <div className="card table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Room</th>
                <th>Tenant</th>
                {activeReport === 'arrears' ? (
                  <>
                    <th>Balance Due</th>
                    <th>Last Payment</th>
                  </>
                ) : (
                  <>
                    <th>Income</th>
                    <th>Period</th>
                  </>
                )}
              </tr>
            </thead>
            <tbody>
              {arrears.map((row, idx) => (
                <tr key={idx}>
                  <td className="font-medium">{row.room_number}</td>
                  <td>{row.tenant_name}</td>
                  {activeReport === 'arrears' ? (
                    <>
                      <td className="font-bold text-red-600">
                        KSh {row.balance.toLocaleString()}
                      </td>
                      <td>{new Date(row.last_payment_date).toLocaleDateString()}</td>
                    </>
                  ) : (
                    <>
                      <td>KSh {row.balance.toLocaleString()}</td>
                      <td>{row.last_payment_date}</td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ReportsPage;
