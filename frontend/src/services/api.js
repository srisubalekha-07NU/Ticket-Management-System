import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  if (user?.role) config.headers['X-Role'] = user.role;
  return config;
});

export default api;
