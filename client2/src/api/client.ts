import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5555/api';

const client: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle responses
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (username: string, password: string) =>
    client.post('/users/login', { username, password }),
  
  createUser: (data: { username: string; email: string; password: string; role: string }) =>
    client.post('/users/create', data),
  
  getProfile: (userId: number) =>
    client.get(`/users/${userId}`),
};

export const roomsAPI = {
  list: () => client.get('/rooms'),
  get: (id: number) => client.get(`/rooms/${id}`),
  create: (data: any) => client.post('/rooms', data),
  update: (id: number, data: any) => client.put(`/rooms/${id}`, data),
};

export const tenantsAPI = {
  list: () => client.get('/tenants'),
  get: (id: number) => client.get(`/tenants/${id}`),
  create: (data: any) => client.post('/tenants/check-in', data),
  occupancies: (id: number) => client.get(`/tenants/${id}/occupancies`),
  ledger: (id: number) => client.get(`/tenants/${id}/ledger`),
};

export const occupanciesAPI = {
  list: () => client.get('/occupancies'),
  get: (id: number) => client.get(`/occupancies/${id}`),
  end: (id: number, data: any) => client.post(`/occupancies/${id}/end`, data),
};

export const billingsAPI = {
  list: () => client.get('/billings'),
  get: (id: number) => client.get(`/billings/${id}`),
  generate: (data: any) => client.post('/billings/generate', data),
};

export const paymentsAPI = {
  list: () => client.get('/payments'),
  get: (id: number) => client.get(`/payments/${id}`),
  record: (data: any) => client.post('/payments/record', data),
};

export const reportsAPI = {
  arrears: () => client.get('/reports/arrears'),
  income: () => client.get('/reports/income'),
};

export default client;
