import axios from 'axios';

// API base URL - will connect to our Python backend
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API functions
export const checkBackendStatus = async () => {
  try {
    const response = await api.get('/health');
    return response.status === 'healthy';
  } catch (error) {
    return false;
  }
};

export const getBotStatus = async () => {
  try {
    return await api.get('/bot/status');
  } catch (error) {
    throw error;
  }
};

export const startBot = async (config = {}) => {
  try {
    return await api.post('/bot/start', config);
  } catch (error) {
    throw error;
  }
};

export const stopBot = async () => {
  try {
    return await api.post('/bot/stop');
  } catch (error) {
    throw error;
  }
};

export const createTask = async (taskData) => {
  try {
    return await api.post('/tasks', taskData);
  } catch (error) {
    throw error;
  }
};

export const getTasks = async () => {
  try {
    return await api.get('/tasks');
  } catch (error) {
    throw error;
  }
};

export const executeTask = async (taskId) => {
  try {
    return await api.post(`/tasks/${taskId}/execute`);
  } catch (error) {
    throw error;
  }
};

export const runTask = async (taskData) => {
  try {
    return await api.post('/tasks/run', taskData);
  } catch (error) {
    throw error;
  }
};

export const getTaskResults = async (taskId) => {
  try {
    return await api.get(`/tasks/${taskId}/results`);
  } catch (error) {
    throw error;
  }
};

export const getSettings = async () => {
  try {
    return await api.get('/settings');
  } catch (error) {
    throw error;
  }
};

export const updateSettings = async (settings) => {
  try {
    return await api.put('/settings', settings);
  } catch (error) {
    throw error;
  }
};

export const getCredentials = async () => {
  try {
    return await api.get('/credentials');
  } catch (error) {
    throw error;
  }
};

export const updateCredentials = async (credentials) => {
  try {
    return await api.put('/credentials', credentials);
  } catch (error) {
    throw error;
  }
};

export const getPerformanceReport = async () => {
  try {
    return await api.get('/performance/report');
  } catch (error) {
    throw error;
  }
};

export const getLogs = async (limit = 100) => {
  try {
    return await api.get(`/logs?limit=${limit}`);
  } catch (error) {
    throw error;
  }
};

export const exportData = async (format = 'csv', data) => {
  try {
    return await api.post(`/export/${format}`, data);
  } catch (error) {
    throw error;
  }
};

// Security Testing API functions
export const authenticateSecurityAccess = async (password) => {
  try {
    return await api.post('/api/security/authenticate', { password });
  } catch (error) {
    throw error;
  }
};

export const startSecuritySession = async (targetUrl, authorizationToken) => {
  try {
    return await api.post('/api/security/start-session', {
      target_url: targetUrl,
      authorization_token: authorizationToken
    });
  } catch (error) {
    throw error;
  }
};

export const runSecurityTest = async (testType, targetElement, customPayload) => {
  try {
    return await api.post('/api/security/run-test', {
      test_type: testType,
      target_element: targetElement,
      custom_payload: customPayload
    });
  } catch (error) {
    throw error;
  }
};

export const getSecuritySessionReport = async () => {
  try {
    return await api.get('/api/security/session-report');
  } catch (error) {
    throw error;
  }
};

export const endSecuritySession = async () => {
  try {
    return await api.post('/api/security/end-session');
  } catch (error) {
    throw error;
  }
};

export const getSecurityStatus = async () => {
  try {
    return await api.get('/api/security/status');
  } catch (error) {
    throw error;
  }
};

export default api;
