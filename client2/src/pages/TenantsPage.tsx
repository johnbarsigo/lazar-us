import React, { useState, useEffect } from 'react';
import { Plus, Search, MapPin, Users } from 'lucide-react';
import { tenantsAPI } from '../api/client';
import { Tenant } from '../types';

const TenantsPage: React.FC = () => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      const response = await tenantsAPI.list();
      setTenants(response.data);
    } catch (err) {
      console.error('Failed to fetch tenants', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredTenants = tenants.filter(
    (t) =>
      t.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.national_id.includes(searchTerm)
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Tenants</h1>
        <button
          onClick={() => setShowModal(true)}
          className="btn-primary flex items-center gap-2 w-full sm:w-auto justify-center"
        >
          <Plus size={20} />
          New Tenant
        </button>
      </div>

      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <Search size={20} className="text-slate-400" />
          <input
            type="text"
            placeholder="Search by name, email, or ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field m-0"
          />
        </div>

        {loading ? (
          <div className="text-center py-8">Loading tenants...</div>
        ) : filteredTenants.length === 0 ? (
          <div className="text-center py-8 text-slate-500">No tenants found</div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>ID Number</th>
                  <th>Current Room</th>
                  <th>Since</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredTenants.map((tenant) => (
                  <tr key={tenant.id}>
                    <td className="font-medium">{tenant.name}</td>
                    <td>{tenant.email}</td>
                    <td>{tenant.phone || 'N/A'}</td>
                    <td>{tenant.national_id}</td>
                    <td>
                      {tenant.occupancies && tenant.occupancies.length > 0
                        ? tenant.occupancies[tenant.occupancies.length - 1].room?.room_number
                        : 'N/A'}
                    </td>
                    <td>
                      {tenant.occupancies && tenant.occupancies.length > 0
                        ? new Date(
                            tenant.occupancies[tenant.occupancies.length - 1].start_date
                          ).toLocaleDateString()
                        : 'N/A'}
                    </td>
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
    </div>
  );
};

export default TenantsPage;
