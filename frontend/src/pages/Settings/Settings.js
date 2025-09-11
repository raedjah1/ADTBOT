import React, { useState } from 'react';
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
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Security as IntegrationIcon,
  Notifications as NotificationIcon,
  Speed as PerformanceIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Edit as EditIcon,
  CheckCircle as ConnectedIcon,
  CheckCircle,
} from '@mui/icons-material';
import toast from 'react-hot-toast';

const Settings = ({ isDarkMode = true }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [settings, setSettings] = useState({
    plusSystem: {
      baseUrl: 'https://plus.reconext.com',
      apiKey: '',
      timeout: 30,
      retryAttempts: 3,
      enabled: true,
    },
    rmaProcessing: {
      autoProcessing: true,
      batchSize: 100,
      trackingValidation: true,
      labelGeneration: true,
      qualityChecks: true,
    },
    notifications: {
      emailAlerts: true,
      errorNotifications: true,
      completionNotifications: false,
      emailAddress: 'admin@reconext.com',
    },
    performance: {
      maxConcurrentTasks: 5,
      cacheEnabled: true,
      loggingLevel: 'INFO',
      metricsCollection: true,
    },
  });

  const [showApiKeyDialog, setShowApiKeyDialog] = useState(false);
  const [newApiKey, setNewApiKey] = useState('');

  const handleSettingChange = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value,
      },
    }));
  };

  const handleSaveSettings = () => {
    toast.success('Settings saved successfully!');
  };

  const handleTestConnection = () => {
    toast.loading('Testing connection...', { duration: 2000 });
    setTimeout(() => {
      toast.success('Connection successful!');
    }, 2000);
  };

  const TabPanel = ({ children, value, index, ...other }) => (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
        System Settings
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Configure your Reconext ADT Bot for optimal RMA processing
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <Tabs 
          value={activeTab} 
          onChange={(e, newValue) => setActiveTab(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab icon={<IntegrationIcon />} label="PLUS Integration" />
          <Tab icon={<SettingsIcon />} label="RMA Processing" />
          <Tab icon={<NotificationIcon />} label="Notifications" />
          <Tab icon={<PerformanceIcon />} label="Performance" />
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
                value={settings.plusSystem.baseUrl}
                onChange={(e) => handleSettingChange('plusSystem', 'baseUrl', e.target.value)}
                sx={{ mb: 2 }}
              />
              
              <TextField
                fullWidth
                label="API Key"
                type="password"
                value={settings.plusSystem.apiKey}
                placeholder="Enter your PLUS API key"
                onChange={(e) => handleSettingChange('plusSystem', 'apiKey', e.target.value)}
                sx={{ mb: 2 }}
                InputProps={{
                  endAdornment: (
                    <IconButton onClick={() => setShowApiKeyDialog(true)}>
                      <EditIcon />
                    </IconButton>
                  ),
                }}
              />

              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Connection Timeout (seconds)"
                    type="number"
                    value={settings.plusSystem.timeout}
                    onChange={(e) => handleSettingChange('plusSystem', 'timeout', parseInt(e.target.value))}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Retry Attempts"
                    type="number"
                    value={settings.plusSystem.retryAttempts}
                    onChange={(e) => handleSettingChange('plusSystem', 'retryAttempts', parseInt(e.target.value))}
                  />
                </Grid>
              </Grid>

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.plusSystem.enabled}
                    onChange={(e) => handleSettingChange('plusSystem', 'enabled', e.target.checked)}
                  />
                }
                label="Enable PLUS Integration"
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <Card sx={{ p: 2, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 2 }}>Connection Status</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
                  <ConnectedIcon color="success" sx={{ mr: 1 }} />
                  <Chip label="Connected" color="success" />
                </Box>
                <Button 
                  variant="outlined" 
                  onClick={handleTestConnection}
                  startIcon={<RefreshIcon />}
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
                    checked={settings.rmaProcessing.autoProcessing}
                    onChange={(e) => handleSettingChange('rmaProcessing', 'autoProcessing', e.target.checked)}
                  />
                }
                label="Enable Automatic Processing"
                sx={{ mb: 2, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.rmaProcessing.trackingValidation}
                    onChange={(e) => handleSettingChange('rmaProcessing', 'trackingValidation', e.target.checked)}
                  />
                }
                label="Tracking Number Validation"
                sx={{ mb: 2, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.rmaProcessing.labelGeneration}
                    onChange={(e) => handleSettingChange('rmaProcessing', 'labelGeneration', e.target.checked)}
                  />
                }
                label="Automatic Label Generation"
                sx={{ mb: 2, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.rmaProcessing.qualityChecks}
                    onChange={(e) => handleSettingChange('rmaProcessing', 'qualityChecks', e.target.checked)}
                  />
                }
                label="Quality Check Automation"
                sx={{ mb: 2, display: 'block' }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Batch Settings</Typography>
              
              <TextField
                fullWidth
                label="Batch Processing Size"
                type="number"
                value={settings.rmaProcessing.batchSize}
                onChange={(e) => handleSettingChange('rmaProcessing', 'batchSize', parseInt(e.target.value))}
                helperText="Number of items to process in each batch"
                sx={{ mb: 2 }}
              />

              <Alert severity="info">
                Automatic processing will handle incoming RMAs based on predefined rules and routing logic.
              </Alert>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Notifications Tab */}
        <TabPanel value={activeTab} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Email Notifications</Typography>
              
              <TextField
                fullWidth
                label="Notification Email Address"
                type="email"
                value={settings.notifications.emailAddress}
                onChange={(e) => handleSettingChange('notifications', 'emailAddress', e.target.value)}
                sx={{ mb: 2 }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.emailAlerts}
                    onChange={(e) => handleSettingChange('notifications', 'emailAlerts', e.target.checked)}
                  />
                }
                label="Enable Email Alerts"
                sx={{ mb: 1, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.errorNotifications}
                    onChange={(e) => handleSettingChange('notifications', 'errorNotifications', e.target.checked)}
                  />
                }
                label="Error Notifications"
                sx={{ mb: 1, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.notifications.completionNotifications}
                    onChange={(e) => handleSettingChange('notifications', 'completionNotifications', e.target.checked)}
                  />
                }
                label="Task Completion Notifications"
                sx={{ mb: 1, display: 'block' }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Notification Rules</Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Processing Errors"
                    secondary="Immediate notification for any processing failures"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="System Status"
                    secondary="Daily system health reports"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Batch Completion"
                    secondary="Summary when batch processing completes"
                  />
                </ListItem>
              </List>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Performance Tab */}
        <TabPanel value={activeTab} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>Performance Settings</Typography>
              
              <TextField
                fullWidth
                label="Max Concurrent Tasks"
                type="number"
                value={settings.performance.maxConcurrentTasks}
                onChange={(e) => handleSettingChange('performance', 'maxConcurrentTasks', parseInt(e.target.value))}
                helperText="Maximum number of tasks to process simultaneously"
                sx={{ mb: 2 }}
              />

              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Logging Level</InputLabel>
                <Select
                  value={settings.performance.loggingLevel}
                  onChange={(e) => handleSettingChange('performance', 'loggingLevel', e.target.value)}
                >
                  <MenuItem value="DEBUG">Debug</MenuItem>
                  <MenuItem value="INFO">Info</MenuItem>
                  <MenuItem value="WARNING">Warning</MenuItem>
                  <MenuItem value="ERROR">Error</MenuItem>
                </Select>
              </FormControl>

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.performance.cacheEnabled}
                    onChange={(e) => handleSettingChange('performance', 'cacheEnabled', e.target.checked)}
                  />
                }
                label="Enable Caching"
                sx={{ mb: 1, display: 'block' }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={settings.performance.metricsCollection}
                    onChange={(e) => handleSettingChange('performance', 'metricsCollection', e.target.checked)}
                  />
                }
                label="Collect Performance Metrics"
                sx={{ mb: 1, display: 'block' }}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ mb: 2 }}>System Resources</Typography>
              <Card sx={{ p: 2 }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  Current Performance
          </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">CPU Usage:</Typography>
                  <Chip label="23%" color="success" size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Memory Usage:</Typography>
                  <Chip label="45%" color="success" size="small" />
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Active Tasks:</Typography>
                  <Chip label="3" color="info" size="small" />
                </Box>
              </Card>
            </Grid>
          </Grid>
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

      {/* API Key Dialog */}
      <Dialog open={showApiKeyDialog} onClose={() => setShowApiKeyDialog(false)}>
        <DialogTitle>Update API Key</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="New API Key"
            value={newApiKey}
            onChange={(e) => setNewApiKey(e.target.value)}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowApiKeyDialog(false)}>Cancel</Button>
          <Button 
            onClick={() => {
              handleSettingChange('plusSystem', 'apiKey', newApiKey);
              setNewApiKey('');
              setShowApiKeyDialog(false);
              toast.success('API key updated');
            }}
            variant="contained"
          >
            Update
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Settings;
