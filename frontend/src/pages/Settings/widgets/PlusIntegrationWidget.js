import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Alert,
  Paper,
  Chip,
} from '@mui/material';
import {
  CheckCircle,
  Save as SaveIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import toast from 'react-hot-toast';
import ConnectionStatusWidget from './ConnectionStatusWidget';

const PlusIntegrationWidget = ({ isDarkMode = true }) => {
  // State management - clean and simple
  const [baseUrl, setBaseUrl] = useState('https://plus.reconext.com');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [timeout, setTimeout] = useState(30);
  const [retryAttempts, setRetryAttempts] = useState(3);
  const [enabled, setEnabled] = useState(true);
  const [loading, setLoading] = useState(false);

  // Load existing settings on component mount
  React.useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    console.log('📥 Loading PLUS settings from API...');
    try {
      const response = await fetch('http://localhost:8000/api/plus/settings');
      console.log('📡 Settings response:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok
      });
      
      if (response.ok) {
        const settings = await response.json();
        console.log('📋 Loaded settings:', settings);
        setBaseUrl(settings.base_url || 'https://plus.reconext.com');
        setUsername(settings.username || '');
        setPassword(settings.password || '');
        setApiKey(settings.api_key || '');
        setTimeout(settings.timeout || 30);
        setRetryAttempts(settings.retry_attempts || 3);
        setEnabled(settings.enabled !== false);
        console.log('✅ Settings loaded and state updated');
      } else {
        console.error('❌ Failed to load settings:', response.status, response.statusText);
        const errorText = await response.text();
        console.error('❌ Error response:', errorText);
      }
    } catch (error) {
      console.error('💥 Failed to load PLUS settings:', error);
    }
  };

  const handleTestConnection = async () => {
    if (!baseUrl || !username || !password) {
      toast.error('Please fill in URL, username, and password first');
      return;
    }

    setLoading(true);
    const loadingToast = toast.loading('Testing PLUS connection...');
    
    try {
      const response = await fetch('http://localhost:8000/api/plus/test-connection', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ 
          base_url: baseUrl, 
          username, 
          password, 
          api_key: apiKey 
        }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        toast.success('✅ PLUS connection successful!', { id: loadingToast });
      } else {
        toast.error(`❌ Connection failed: ${result.message || 'Unknown error'}`, { id: loadingToast });
      }
    } catch (error) {
      toast.error(`❌ Connection error: ${error.message}`, { id: loadingToast });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    console.log('🔥 SAVE BUTTON CLICKED - Starting save process');
    console.log('📋 Current form data:', {
      baseUrl,
      username: username ? '***' : '(empty)',
      password: password ? '***' : '(empty)', 
      apiKey: apiKey ? '***' : '(empty)',
      timeout,
      retryAttempts,
      enabled
    });

    setLoading(true);
    const loadingToast = toast.loading('Saving settings...');
    
    const requestData = { 
      base_url: baseUrl, 
      username, 
      password, 
      api_key: apiKey,
      timeout,
      retry_attempts: retryAttempts,
      enabled
    };

    console.log('🚀 Making API request to /api/plus/save-credentials');
    console.log('📤 Request payload:', {
      ...requestData,
      username: requestData.username ? '***' : '(empty)',
      password: requestData.password ? '***' : '(empty)',
      api_key: requestData.api_key ? '***' : '(empty)'
    });
    
    try {
      const response = await fetch('http://localhost:8000/api/plus/save-credentials', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(requestData),
      });
      
      console.log('📥 Response received:', {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
        headers: Object.fromEntries(response.headers.entries())
      });

      const responseText = await response.text();
      console.log('📄 Raw response text:', responseText);

      let result;
      try {
        result = JSON.parse(responseText);
        console.log('✅ Parsed JSON result:', result);
      } catch (parseError) {
        console.error('❌ Failed to parse JSON response:', parseError);
        console.error('📄 Response text that failed to parse:', responseText);
        throw new Error(`Invalid JSON response: ${responseText.substring(0, 100)}...`);
      }
      
      if (response.ok && result.success) {
        console.log('🎉 Save successful!');
        toast.success('✅ Settings saved successfully!', { id: loadingToast });
        // Reload settings to confirm they were saved
        console.log('🔄 Reloading settings to confirm save...');
        await loadSettings();
      } else {
        console.error('❌ Save failed:', result);
        toast.error(`❌ Failed to save: ${result.message || 'Unknown error'}`, { id: loadingToast });
      }
    } catch (error) {
      console.error('💥 Save error occurred:', error);
      console.error('🔍 Error details:', {
        name: error.name,
        message: error.message,
        stack: error.stack
      });
      toast.error(`❌ Save error: ${error.message}`, { id: loadingToast });
    } finally {
      setLoading(false);
      console.log('🏁 Save process completed');
    }
  };

  return (
    <Box>
      <Alert severity="info" sx={{ mb: 3 }}>
        Configure connection to your PLUS system for seamless RMA processing integration.
      </Alert>

      <Grid container spacing={3}>
        {/* Connection Settings */}
        <Grid item xs={12} md={8}>
          <Paper elevation={1} sx={{ p: 3, mb: 2 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              Connection Settings
            </Typography>

            {/* Base URL */}
            <TextField
              fullWidth
              label="PLUS System Base URL"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              placeholder="https://your-plus-system.com"
              required
              sx={{ mb: 2 }}
            />
            
            {/* Username and Password Row */}
            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Your PLUS username"
                  autoComplete="username"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Your PLUS password"
                  autoComplete="current-password"
                  required
                />
              </Grid>
            </Grid>
            
            {/* API Key */}
            <TextField
              fullWidth
              label="API Key (Optional)"
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your PLUS API key if required"
              sx={{ mb: 3 }}
            />

            {/* Enable Toggle */}
            <FormControlLabel
              control={
                <Switch
                  checked={enabled}
                  onChange={(e) => setEnabled(e.target.checked)}
                />
              }
              label="Enable PLUS Integration"
              sx={{ mb: 3, display: 'block' }}
            />

            {/* Advanced Settings */}
            <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
              Advanced Settings
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Connection Timeout (seconds)"
                  type="number"
                  value={timeout}
                  onChange={(e) => setTimeout(parseInt(e.target.value) || 30)}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Retry Attempts"
                  type="number"
                  value={retryAttempts}
                  onChange={(e) => setRetryAttempts(parseInt(e.target.value) || 3)}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Connection Status Widget */}
        <Grid item xs={12} md={4}>
          <ConnectionStatusWidget
            baseUrl={baseUrl}
            username={username}
            password={password}
            onTestConnection={handleTestConnection}
          />
        </Grid>
      </Grid>

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 3 }}>
        <Button 
          variant="outlined" 
          onClick={() => window.location.reload()}
        >
          Reset to Defaults
        </Button>
        <Button 
          variant="contained" 
          startIcon={<SaveIcon />}
          onClick={() => {
            console.log('🖱️ Save button clicked!');
            handleSaveSettings();
          }}
          disabled={loading}
        >
          {loading ? 'Saving...' : 'Save Settings'}
        </Button>
      </Box>
    </Box>
  );
};

export default PlusIntegrationWidget;
