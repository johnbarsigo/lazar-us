import React, { useState, useEffect } from 'react';
import { Plus, Search } from 'lucide-react';
import { tenantsAPI, roomsAPI } from '../api/client';
import { Tenant, Room } from '../types';

const initialTenantForm = {
  name: '',
  email: '',
  phone: '',
  national_id: '',
  room_id: 0,
  agreed_rent: 0,
  start_date: new Date().toISOString().slice(0, 10),
};

const TenantsPage: React.FC = () => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [tenantForm, setTenantForm] = useState(initialTenantForm);
  const [creatingTenant, setCreatingTenant] = useState(false);
  const [tenantMessage, setTenantMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchTenants();
    fetchRooms();
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

  const fetchRooms = async () => {
    try {
      const response = await roomsAPI.list();
      setRooms(response.data);
    } catch (err) {
      console.error('Failed to fetch rooms', err);
    }
  };

  const handleTenantInput = (field: string, value: string | number) => {
    setTenantForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleCreateTenant = async () => {
    setCreatingTenant(true);
    setTenantMessage(null);

    try {
      await tenantsAPI.create({
        name: tenantForm.name,
        email: tenantForm.email,
        phone: tenantForm.phone,
        national_id: tenantForm.national_id,
        room_id: tenantForm.room_id,
        agreed_rent: tenantForm.agreed_rent,
        start_date: tenantForm.start_date,
      });
      setTenantMessage('Tenant created successfully.');
      setShowModal(false);
      setTenantForm(initialTenantForm);
      fetchTenants();
    } catch (err) {
      console.error('Failed to create tenant', err);
      setTenantMessage('Could not create tenant.');
    } finally {
      setCreatingTenant(false);
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
        {tenantMessage && (
          <div className="mb-4 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg text-sm text-green-700 dark:text-green-200">
            {tenantMessage}
          </div>
        )}
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
        {/* Minimal placeholder modal to avoid unused state until full modal is implemented */}
        {showModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
            <div className="w-full max-w-lg bg-white dark:bg-slate-900 rounded-2xl shadow-xl p-6">
              <div className="flex items-center justify-between gap-4 mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-slate-900 dark:text-white">New Tenant</h2>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Register a tenant and attach them to a room.</p>
                </div>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-slate-500 hover:text-slate-900 dark:hover:text-white"
                >
                  Close
                </button>
              </div>

              <div className="grid gap-4">
                <div>
                  <label className="label">Name</label>
                  <input
                    type="text"
                    value={tenantForm.name}
                    onChange={(e) => handleTenantInput('name', e.target.value)}
                    className="input-field"
                    placeholder="Tenant name"
                  />
                </div>
                <div>
                  <label className="label">Email</label>
                  <input
                    type="email"
                    value={tenantForm.email}
                    onChange={(e) => handleTenantInput('email', e.target.value)}
                    className="input-field"
                    placeholder="Tenant email"
                  />
                </div>
                <div>
                  <label className="label">Phone</label>
                  <input
                    type="tel"
                    value={tenantForm.phone}
                    onChange={(e) => handleTenantInput('phone', e.target.value)}
                    className="input-field"
                    placeholder="Phone number"
                  />
                </div>
                <div>
                  <label className="label">National ID</label>
                  <input
                    type="text"
                    value={tenantForm.national_id}
                    onChange={(e) => handleTenantInput('national_id', e.target.value)}
                    className="input-field"
                    placeholder="National ID number"
                  />
                </div>
                <div>
                  <label className="label">Room</label>
                  <select
                    value={tenantForm.room_id}
                    onChange={(e) => handleTenantInput('room_id', Number(e.target.value))}
                    className="input-field"
                  >
                    <option value={0}>Select a room</option>
                    {rooms.map((room) => (
                      <option key={room.id} value={room.id}>
                        {room.room_number} — KSh {room.default_rent.toLocaleString()}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="label">Agreed Rent</label>
                  <input
                    type="number"
                    min={0}
                    step={0.01}
                    value={tenantForm.agreed_rent}
                    onChange={(e) => handleTenantInput('agreed_rent', Number(e.target.value))}
                    className="input-field"
                    placeholder="Monthly rent amount"
                  />
                </div>
                <div>
                  <label className="label">Start Date</label>
                  <input
                    type="date"
                    value={tenantForm.start_date}
                    onChange={(e) => handleTenantInput('start_date', e.target.value)}
                    className="input-field"
                  />
                </div>
              </div>

              <div className="mt-6 flex flex-col sm:flex-row items-center gap-3 justify-end">
                <button
                  onClick={() => setShowModal(false)}
                  className="btn-secondary w-full sm:w-auto"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateTenant}
                  disabled={creatingTenant}
                  className="btn-primary w-full sm:w-auto"
                >
                  {creatingTenant ? 'Saving...' : 'Create Tenant'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TenantsPage;
