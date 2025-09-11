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
} from '@mui/material';
import {
  Save as SaveIcon,
} from '@mui/icons-material';
import toast from 'react-hot-toast';

const RmaProcessingWidget = ({ isDarkMode = true }) => {
  // RMA Processing settings state
  const [autoProcessing, setAutoProcessing] = useState(true);
  const [batchSize, setBatchSize] = useState(100);
  const [trackingValidation, setTrackingValidation] = useState(true);
  const [labelGeneration, setLabelGeneration] = useState(true);
  const [qualityChecks, setQualityChecks] = useState(true);
  const [loading, setLoading] = useState(false);

  // Load existing settings on component mount
  React.useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/rma/settings');
      if (response.ok) {
        const settings = await response.json();
        setAutoProcessing(settings.auto_processing !== false);
        setBatchSize(settings.batch_size || 100);
        setTrackingValidation(settings.tracking_validation !== false);
        setLabelGeneration(settings.label_generation !== false);
        setQualityChecks(settings.quality_checks !== false);
      } else {
        console.error('Failed to load RMA settings:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Failed to load RMA settings:', error);
    }
  };

  const handleSaveSettings = async () => {
    setLoading(true);
    const loadingToast = toast.loading('Saving RMA settings...');
    
    try {
      const response = await fetch('http://localhost:8000/api/rma/save-settings', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          auto_processing: autoProcessing,
          batch_size: batchSize,
          tracking_validation: trackingValidation,
          label_generation: labelGeneration,
          quality_checks: qualityChecks
        }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        toast.success('✅ RMA settings saved successfully!', { id: loadingToast });
        // Reload settings to confirm they were saved
        await loadSettings();
      } else {
        toast.error(`❌ Failed to save: ${result.message || 'Unknown error'}`, { id: loadingToast });
      }
    } catch (error) {
      toast.error(`❌ Save error: ${error.message}`, { id: loadingToast });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Paper elevation={1} sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
          Processing Options
        </Typography>
        
        <Grid container spacing={3}>
          {/* Processing Toggles */}
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={autoProcessing}
                    onChange={(e) => setAutoProcessing(e.target.checked)}
                  />
                }
                label="Enable Automatic Processing"
                sx={{ m: 0 }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={trackingValidation}
                    onChange={(e) => setTrackingValidation(e.target.checked)}
                  />
                }
                label="Tracking Number Validation"
                sx={{ m: 0 }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={labelGeneration}
                    onChange={(e) => setLabelGeneration(e.target.checked)}
                  />
                }
                label="Automatic Label Generation"
                sx={{ m: 0 }}
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={qualityChecks}
                    onChange={(e) => setQualityChecks(e.target.checked)}
                  />
                }
                label="Quality Checks"
                sx={{ m: 0 }}
              />
            </Box>
          </Grid>

          {/* Processing Settings */}
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Batch Size"
              type="number"
              value={batchSize}
              onChange={(e) => setBatchSize(parseInt(e.target.value) || 100)}
              helperText="Number of RMAs to process in each batch"
              inputProps={{ min: 1, max: 1000 }}
            />
          </Grid>
        </Grid>

        {/* Additional Settings Section */}
        <Box sx={{ mt: 4 }}>
          <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
            Processing Rules
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Max Processing Time (minutes)"
                type="number"
                defaultValue={30}
                inputProps={{ min: 1, max: 120 }}
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Error Retry Count"
                type="number"
                defaultValue={3}
                inputProps={{ min: 0, max: 10 }}
                sx={{ mb: 2 }}
              />
            </Grid>
          </Grid>
        </Box>

        {/* Save Button */}
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
          <Button 
            variant="contained" 
            startIcon={<SaveIcon />}
            onClick={handleSaveSettings}
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save Processing Settings'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default RmaProcessingWidget;
