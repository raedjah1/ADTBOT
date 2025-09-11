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
  Slider,
} from '@mui/material';
import {
  Cloud as CloudIcon,
  Save as SaveIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import toast from 'react-hot-toast';

const PerformanceWidget = ({ isDarkMode = true }) => {
  // Performance settings state
  const [enableCaching, setEnableCaching] = useState(true);
  const [enableLogging, setEnableLogging] = useState(true);
  const [logLevel, setLogLevel] = useState('info');
  const [maxConcurrentTasks, setMaxConcurrentTasks] = useState(5);
  const [taskTimeout, setTaskTimeout] = useState(300);
  const [cacheSize, setCacheSize] = useState(100);
  const [memoryThreshold, setMemoryThreshold] = useState(80);

  const handleSaveSettings = async () => {
    const loadingToast = toast.loading('Saving performance settings...');
    
    try {
      const response = await fetch('http://localhost:8000/api/performance/save-settings', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          enable_caching: enableCaching,
          enable_logging: enableLogging,
          log_level: logLevel,
          max_concurrent_tasks: maxConcurrentTasks,
          task_timeout: taskTimeout,
          cache_size: cacheSize,
          memory_threshold: memoryThreshold
        }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        toast.success('✅ Performance settings saved successfully!', { id: loadingToast });
      } else {
        toast.error(`❌ Failed to save: ${result.message || 'Unknown error'}`, { id: loadingToast });
      }
    } catch (error) {
      toast.error(`❌ Save error: ${error.message}`, { id: loadingToast });
    }
  };

  const handleResetToDefaults = () => {
    setEnableCaching(true);
    setEnableLogging(true);
    setLogLevel('info');
    setMaxConcurrentTasks(5);
    setTaskTimeout(300);
    setCacheSize(100);
    setMemoryThreshold(80);
    toast.info('🔄 Reset to default settings');
  };

  return (
    <Box>
      <Paper elevation={1} sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <SpeedIcon sx={{ mr: 2, color: 'primary.main' }} />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Performance & Monitoring
          </Typography>
        </Box>

        <Grid container spacing={3}>
          {/* System Performance */}
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
              System Performance
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={enableCaching}
                    onChange={(e) => setEnableCaching(e.target.checked)}
                  />
                }
                label="Enable Caching"
                sx={{ mb: 2, display: 'block' }}
              />

              <TextField
                fullWidth
                label="Max Concurrent Tasks"
                type="number"
                value={maxConcurrentTasks}
                onChange={(e) => setMaxConcurrentTasks(parseInt(e.target.value) || 1)}
                inputProps={{ min: 1, max: 20 }}
                sx={{ mb: 2 }}
              />

              <TextField
                fullWidth
                label="Task Timeout (seconds)"
                type="number"
                value={taskTimeout}
                onChange={(e) => setTaskTimeout(parseInt(e.target.value) || 60)}
                inputProps={{ min: 30, max: 3600 }}
                sx={{ mb: 2 }}
              />
            </Box>

            {/* Memory Management */}
            <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
              Memory Management
            </Typography>
            
            <Box sx={{ mb: 2 }}>
              <Typography gutterBottom>
                Memory Usage Threshold: {memoryThreshold}%
              </Typography>
              <Slider
                value={memoryThreshold}
                onChange={(e, newValue) => setMemoryThreshold(newValue)}
                step={5}
                marks
                min={50}
                max={95}
                valueLabelDisplay="auto"
              />
            </Box>

            <TextField
              fullWidth
              label="Cache Size (MB)"
              type="number"
              value={cacheSize}
              onChange={(e) => setCacheSize(parseInt(e.target.value) || 50)}
              inputProps={{ min: 10, max: 1000 }}
              disabled={!enableCaching}
            />
          </Grid>

          {/* Logging & Monitoring */}
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
              Logging & Monitoring
            </Typography>
            
            <FormControlLabel
              control={
                <Switch
                  checked={enableLogging}
                  onChange={(e) => setEnableLogging(e.target.checked)}
                />
              }
              label="Enable Detailed Logging"
              sx={{ mb: 3, display: 'block' }}
            />

            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Log Level</InputLabel>
              <Select
                value={logLevel}
                label="Log Level"
                onChange={(e) => setLogLevel(e.target.value)}
                disabled={!enableLogging}
              >
                <MenuItem value="debug">Debug</MenuItem>
                <MenuItem value="info">Info</MenuItem>
                <MenuItem value="warning">Warning</MenuItem>
                <MenuItem value="error">Error</MenuItem>
              </Select>
            </FormControl>

            {/* Performance Metrics */}
            <Box sx={{ p: 2, backgroundColor: 'action.hover', borderRadius: 1 }}>
              <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                Current Performance Status
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                <Chip label="CPU: 23%" size="small" color="success" />
                <Chip label="Memory: 45%" size="small" color="success" />
                <Chip label="Tasks: 3/5" size="small" color="primary" />
              </Box>
              <Typography variant="body2" color="text.secondary">
                System running optimally
              </Typography>
            </Box>
          </Grid>
        </Grid>

        {/* Action Buttons */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button 
            variant="outlined" 
            onClick={handleResetToDefaults}
          >
            Reset to Defaults
          </Button>
          
          <Button 
            variant="contained" 
            startIcon={<SaveIcon />}
            onClick={handleSaveSettings}
          >
            Save Performance Settings
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default PerformanceWidget;
