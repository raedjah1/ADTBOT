import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  TextField,
  Switch,
  FormControlLabel,
  Paper,
  Button,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  Notifications as NotificationIcon,
  Save as SaveIcon,
} from '@mui/icons-material';
import toast from 'react-hot-toast';

const NotificationWidget = ({ isDarkMode = true }) => {
  // Notification settings state
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [smsNotifications, setSmsNotifications] = useState(false);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [emailAddress, setEmailAddress] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [notificationLevel, setNotificationLevel] = useState('important');

  const handleSaveSettings = async () => {
    const loadingToast = toast.loading('Saving notification settings...');
    
    try {
      // Simulate API call - replace with actual endpoint
      await new Promise(resolve => setTimeout(resolve, 1000));
      toast.success('✅ Notification settings saved successfully!', { id: loadingToast });
    } catch (error) {
      toast.error(`❌ Failed to save settings: ${error.message}`, { id: loadingToast });
    }
  };

  return (
    <Box>
      <Paper elevation={1} sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <NotificationIcon sx={{ mr: 2, color: 'primary.main' }} />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Notification Settings
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {/* Notification Types */}
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
              Notification Types
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={emailNotifications}
                    onChange={(e) => setEmailNotifications(e.target.checked)}
                  />
                }
                label="Email Notifications"
                sx={{ m: 0 }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={smsNotifications}
                    onChange={(e) => setSmsNotifications(e.target.checked)}
                  />
                }
                label="SMS Notifications"
                sx={{ m: 0 }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={pushNotifications}
                    onChange={(e) => setPushNotifications(e.target.checked)}
                  />
                }
                label="Push Notifications"
                sx={{ m: 0 }}
              />
            </Box>
          </Grid>

          {/* Contact Information */}
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
              Contact Information
            </Typography>
            
            <TextField
              fullWidth
              label="Email Address"
              type="email"
              value={emailAddress}
              onChange={(e) => setEmailAddress(e.target.value)}
              placeholder="your.email@company.com"
              disabled={!emailNotifications}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label="Phone Number"
              type="tel"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="+1 (555) 123-4567"
              disabled={!smsNotifications}
              sx={{ mb: 2 }}
            />
          </Grid>
        </Grid>

        {/* Notification Level */}
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
            Notification Level
          </Typography>
          
          <FormControl sx={{ minWidth: 200, mb: 2 }}>
            <InputLabel>Notification Level</InputLabel>
            <Select
              value={notificationLevel}
              label="Notification Level"
              onChange={(e) => setNotificationLevel(e.target.value)}
            >
              <MenuItem value="all">All Events</MenuItem>
              <MenuItem value="important">Important Only</MenuItem>
              <MenuItem value="critical">Critical Only</MenuItem>
            </Select>
          </FormControl>

          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              Current Settings:
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {emailNotifications && <Chip label="Email" size="small" color="primary" />}
              {smsNotifications && <Chip label="SMS" size="small" color="primary" />}
              {pushNotifications && <Chip label="Push" size="small" color="primary" />}
              <Chip label={notificationLevel} size="small" color="secondary" />
            </Box>
          </Box>
        </Box>

        {/* Save Button */}
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
          <Button 
            variant="contained" 
            startIcon={<SaveIcon />}
            onClick={handleSaveSettings}
          >
            Save Notification Settings
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default NotificationWidget;
