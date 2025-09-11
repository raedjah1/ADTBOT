import React, { useState, useRef } from 'react';
import {
  Box,
  Typography,
  Card,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Divider,
  Alert,
  Tabs,
  Tab,
  IconButton,
  Chip,
} from '@mui/material';
import {
  CheckCircle,
  Save as SaveIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import toast from 'react-hot-toast';

const SettingsFixed = ({ isDarkMode = true }) => {
  const [activeTab, setActiveTab] = useState(0);
  
  // Separate controlled inputs - PROPER React pattern
  const [baseUrl, setBaseUrl] = useState('https://plus.reconext.com');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [timeout, setTimeout] = useState(30);
  const [retryAttempts, setRetryAttempts] = useState(3);
  const [enabled, setEnabled] = useState(true);
  
  // RMA Processing settings
  const [autoProcessing, setAutoProcessing] = useState(true);
  const [batchSize, setBatchSize] = useState(100);
  const [trackingValidation, setTrackingValidation] = useState(true);
  const [labelGeneration, setLabelGeneration] = useState(true);
  const [qualityChecks, setQualityChecks] = useState(true);

  const handleTestConnection = async () => {
    if (!baseUrl || !username || !password) {
      toast.error('Please fill in URL, username, and password first');
      return;
    }

    const loadingToast = toast.loading('Testing PLUS connection...');
    
    try {
      const response = await fetch('/api/plus/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          baseUrl,
          username,
          password,
          apiKey,
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
    }
  };

  const handleSaveSettings = async () => {
    const loadingToast = toast.loading('Saving settings...');
    
    try {
      const response = await fetch('/api/plus/save-credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          baseUrl,
          username,
          password,
          apiKey,
        }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        toast.success('✅ Settings saved successfully!', { id: loadingToast });
      } else {
        toast.error(`❌ Failed to save: ${result.message || 'Unknown error'}`, { id: loadingToast });
      }
    } catch (error) {
      toast.error(`❌ Save error: ${error.message}`, { id: loadingToast });
    }
  };

  const TabPanel = ({ children, value, index, ...other }) => (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        System Settings
      </Typography>

      <Card sx={{ mb: 3 }}>
        <Tabs 
          value={activeTab} 
          onChange={(e, newValue) => setActiveTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="PLUS Integration" />
          <Tab label="RMA Processing" />
          <Tab label="Notifications" />
          <Tab label="Performance" />
        </Tabs>

        {/* PLUS Integration Tab */}
        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Alert severity="info" sx={{ mb: 3 }}>
                Configure connection to your PLUS system for seamless RMA processing integration.
              </Alert>
            </Grid>
            
            <Grid item xs={12} md={8}>
              <TextField
                fullWidth
                label="PLUS System Base URL"
                value={baseUrl}
                onChange={(e) => setBaseUrl(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="https://your-plus-system.com"
              />
              
              <TextField
                fullWidth
                label="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="Your PLUS username"
                autoComplete="username"
              />
              
              <TextField
                fullWidth
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="Your PLUS password"
                autoComplete="current-password"
              />
              
              <TextField
                fullWidth
                label="API Key (Optional)"
                type="password"
                value={apiKey}
                placeholder="Enter your PLUS API key if required"
                onChange={(e) => setApiKey(e.target.value)}
                sx={{ mb: 2 }}
              />

              <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                <Button 
                  variant="outlined" 
                  onClick={handleTestConnection}
                  startIcon={<CheckCircle />}
                >
                  Test Connection
                </Button>
                <FormControlLabel
                  control={
                    <Switch
                      checked={enabled}
                      onChange={(e) => setEnabled(e.target.checked)}
                    />
                  }
                  label="Enable PLUS Integration"
                />
              </Box>

              <Grid container spacing={2} sx={{ mb: 2 }}>
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
            </Grid>

            <Grid item xs={12} md={4}>
              <Card sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 2 }}>Connection Status</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                  <CheckCircle color={baseUrl && username && password ? "success" : "disabled"} sx={{ mr: 1 }} />
                  <Chip 
                    label={baseUrl && username && password ? "Ready to Test" : "Not Configured"} 
                    color={baseUrl && username && password ? "success" : "default"} 
                  />
                </Box>
                <Button 
                  variant="outlined" 
                  onClick={handleTestConnection}
                  startIcon={<RefreshIcon />}
                  disabled={!baseUrl || !username || !password}
                >
                  Test Connection
                </Button>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* RMA Processing Tab */}
        <TabPanel value={activeTab} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Processing Options</Typography>
              
              <FormControlLabel
                control={
                  <Switch
                    checked={autoProcessing}
                    onChange={(e) => setAutoProcessing(e.target.checked)}
                  />
                }
                label="Enable Automatic Processing"
                sx={{ mb: 2, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={trackingValidation}
                    onChange={(e) => setTrackingValidation(e.target.checked)}
                  />
                }
                label="Tracking Number Validation"
                sx={{ mb: 2, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={labelGeneration}
                    onChange={(e) => setLabelGeneration(e.target.checked)}
                  />
                }
                label="Automatic Label Generation"
                sx={{ mb: 2, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={qualityChecks}
                    onChange={(e) => setQualityChecks(e.target.checked)}
                  />
                }
                label="Quality Checks"
                sx={{ mb: 2, display: 'block' }}
              />

              <TextField
                fullWidth
                label="Batch Size"
                type="number"
                value={batchSize}
                onChange={(e) => setBatchSize(parseInt(e.target.value) || 100)}
                sx={{ mb: 2 }}
              />
            </Grid>
          </Grid>
        </TabPanel>

        {/* Notifications Tab */}
        <TabPanel value={activeTab} index={2}>
          <Typography variant="h6">Notification Settings</Typography>
          <Typography color="text.secondary">
            Configure email alerts and notifications (Coming soon)
          </Typography>
        </TabPanel>

        {/* Performance Tab */}
        <TabPanel value={activeTab} index={3}>
          <Typography variant="h6">Performance Settings</Typography>
          <Typography color="text.secondary">
            Configure performance and monitoring options (Coming soon)
          </Typography>
        </TabPanel>

        <Divider sx={{ my: 3 }} />
        
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, p: 3 }}>
          <Button variant="outlined" onClick={() => window.location.reload()}>
            Reset to Defaults
          </Button>
          <Button 
            variant="contained" 
            startIcon={<SaveIcon />}
            onClick={handleSaveSettings}
          >
            Save Settings
          </Button>
        </Box>
      </Card>
    </Box>
  );
};

export default SettingsFixed;
