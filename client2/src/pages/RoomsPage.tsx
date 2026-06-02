import React, { useState, useEffect } from 'react';
import { Plus, Search, DoorOpen } from 'lucide-react';
import PageHeader from '../components/PageHeader';
import { roomsAPI } from '../api/client';
import { Room } from '../types';

const initialRoomForm = {
  room_number: '',
  capacity: 1,
  default_rent: 0,
};

const RoomsPage: React.FC = () => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'available' | 'occupied'>('all');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [roomForm, setRoomForm] = useState(initialRoomForm);
  const [creatingRoom, setCreatingRoom] = useState(false);
  const [roomMessage, setRoomMessage] = useState<string | null>(null);

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

  const handleRoomInput = (field: string, value: string | number) => {
    setRoomForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleCreateRoom = async () => {
    setCreatingRoom(true);
    setRoomMessage(null);
    try {
      await roomsAPI.create({
        room_number: roomForm.room_number,
        capacity: roomForm.capacity,
        default_rent: roomForm.default_rent,
      });
      setRoomMessage('Room created successfully.');
      setShowCreateModal(false);
      setRoomForm(initialRoomForm);
      fetchRooms();
    } catch (err) {
      console.error('Failed to create room', err);
      setRoomMessage('Could not create room.');
    } finally {
      setCreatingRoom(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Rooms"
        description="View and manage rooms"
        icon={DoorOpen}
        action={{
          label: 'New Room',
          onClick: () => setShowCreateModal(true),
          icon: Plus,
        }}
      />

      {roomMessage && (
        <div className="card text-sm text-slate-700 dark:text-slate-200">
          {roomMessage}
        </div>
      )}

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
                  : 'bg-orange-50 text-orange-700 dark:bg-orange-900/20 dark:text-orange-200 hover:bg-orange-100 dark:hover:bg-orange-800'
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

      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
          <div className="w-full max-w-lg bg-white dark:bg-slate-900 rounded-2xl shadow-xl p-6">
            <div className="flex items-center justify-between gap-4 mb-6">
              <div>
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Add New Room</h2>
                <p className="text-sm text-slate-500 dark:text-slate-400">Create a room and set its default rent.</p>
              </div>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-slate-500 hover:text-slate-900 dark:hover:text-white"
              >
                Close
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="label">Room Number</label>
                <input
                  type="text"
                  value={roomForm.room_number}
                  onChange={(e) => handleRoomInput('room_number', e.target.value)}
                  className="input-field"
                  placeholder="e.g. 101"
                />
              </div>
              <div>
                <label className="label">Capacity</label>
                <input
                  type="number"
                  min={1}
                  value={roomForm.capacity}
                  onChange={(e) => handleRoomInput('capacity', Number(e.target.value))}
                  className="input-field"
                />
              </div>
              <div>
                <label className="label">Default Rent</label>
                <input
                  type="number"
                  min={0}
                  step={0.01}
                  value={roomForm.default_rent}
                  onChange={(e) => handleRoomInput('default_rent', Number(e.target.value))}
                  className="input-field"
                  placeholder="e.g. 6000"
                />
              </div>
            </div>

            <div className="mt-6 flex flex-col sm:flex-row items-center gap-3 justify-end">
              <button
                onClick={() => setShowCreateModal(false)}
                className="btn-secondary w-full sm:w-auto"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateRoom}
                disabled={creatingRoom}
                className="btn-primary w-full sm:w-auto"
              >
                {creatingRoom ? 'Saving...' : 'Create Room'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RoomsPage;
