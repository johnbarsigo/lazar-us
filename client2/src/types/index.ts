export interface User {
  id: number;
  username: string;
  email: string;
  role: 'admin' | 'manager';
  created_at?: string;
  updated_at?: string;
}

export interface Room {
  id: number;
  room_number: string;
  capacity: number;
  default_rent: number;
  status: 'available' | 'occupied';
  created_at?: string;
}

export interface Tenant {
  id: number;
  name: string;
  email: string;
  phone?: string;
  national_id: string;
  created_at?: string;
  updated_at?: string;
  occupancies?: Occupancy[];
}

export interface Occupancy {
  id: number;
  tenant_id: number;
  room_id: number;
  agreed_rent: number;
  damages_or_dues?: number;
  damages_reason?: string;
  start_date: string;
  end_date?: string;
  check_in_notes?: string;
  check_out_notes?: string;
  created_at?: string;
  updated_at?: string;
  tenant?: Tenant;
  room?: Room;
  monthly_charges?: MonthlyCharge[];
}

export interface MonthlyCharge {
  id: number;
  occupancy_id: number;
  rent_amount: number;
  water_bill: number;
  month: number;
  year: number;
  charge_date: string;
  total_amount?: number;
  created_at?: string;
  updated_at?: string;
  occupancy?: Occupancy;
  payments?: Payment[];
}

export interface Payment {
  id: number;
  tenant_id: number;
  monthly_charge_id: number;
  status: 'pending' | 'completed' | 'failed';
  amount: number;
  method: 'mpesa' | 'cash' | 'bank';
  mpesa_receipt?: string;
  payment_date: string;
  created_at?: string;
  monthly_charge?: MonthlyCharge;
}

export interface AuthResponse {
  token: string;
  user: User;
  message: string;
}

export interface ApiError {
  error: string;
  message?: string;
}
