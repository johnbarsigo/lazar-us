import React, { useState, useEffect } from 'react';
import { Plus, Search, StatusIcon } from 'lucide-react';
import { roomsAPI } from '../api/client';
import { Room } from '../types';

const RoomsPage: React.FC = () => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'available' | 'occupied'>('all');

  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      const response = await roomsAPI.list();
      setRooms(response.data);
    } catch (err) {
      console.error('Failed to fetch rooms', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredRooms = rooms.filter((room) => {
    const matchesSearch = room.room_number.includes(searchTerm);
    const matchesStatus =
      filterStatus === 'all' || room.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const availableCount = rooms.filter((r) => r.status === 'available').length;
  const occupiedCount = rooms.filter((r) => r.status === 'occupied').length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Rooms</h1>
        <button className="btn-primary flex items-center gap-2 w-full sm:w-auto justify-center">
          <Plus size={20} />
          New Room
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="card">
          <div className="text-sm text-slate-600 dark:text-slate-400 mb-1">Total Rooms</div>
          <div className="text-3xl font-bold">{rooms.length}</div>
        </div>
        <div className="card bg-green-50 dark:bg-green-900/20">
          <div className="text-sm text-green-600 dark:text-green-400 mb-1">Available</div>
          <div className="text-3xl font-bold text-green-600 dark:text-green-400">{availableCount}</div>
        </div>
        <div className="card bg-blue-50 dark:bg-blue-900/20">
          <div className="text-sm text-blue-600 dark:text-blue-400 mb-1">Occupied</div>
          <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">{occupiedCount}</div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="card space-y-4">
        <div className="flex items-center gap-2">
          <Search size={20} className="text-slate-400" />
          <input
            type="text"
            placeholder="Search by room number..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-field m-0"
          />
        </div>

        <div className="flex gap-2 flex-wrap">
          {(['all', 'available', 'occupied'] as const).map((status) => (
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

      {/* Rooms Grid */}
      {loading ? (
        <div className="text-center py-8">Loading rooms...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredRooms.map((room) => (
            <div key={room.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                    Room {room.room_number}
                  </h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Capacity: {room.capacity} person{room.capacity > 1 ? 's' : ''}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${
                    room.status === 'available'
                      ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                      : 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400'
                  }`}
                >
                  {room.status === 'available' ? 'Available' : 'Occupied'}
                </span>
              </div>
              <div className="text-sm text-slate-600 dark:text-slate-400">
                <p>Default Rent: <strong>KSh {room.default_rent.toLocaleString()}</strong></p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RoomsPage;
