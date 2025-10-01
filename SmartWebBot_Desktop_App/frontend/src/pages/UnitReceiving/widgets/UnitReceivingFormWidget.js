import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Grid,
  Alert,
  Chip,
  Box,
  Divider,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Send as ProcessIcon,
  Clear as ClearIcon,
  AutoAwesome as AutoFillIcon,
  Inventory as InventoryIcon,
} from '@mui/icons-material';
import SmartPartLookup from '../../../components/SmartPartLookup';

const UnitReceivingFormWidget = ({ onSubmit, isLoading = false }) => {
  // Form state
  const [formData, setFormData] = useState({
    // Required fields
    trackingNo: '',
    flaggedBoxes: '',
    techId: '',
    partNo: '', // SmartPartLookup will handle part number processing
    batteryRemoval: '',
    dockLogId: '',
    disposition: '',
    
    // Optional fields
    rma: '',
    qtySerial: '',
    mac: '',
    imei: '',
    dateCode: '',
  });

  const [autoFillEnabled, setAutoFillEnabled] = useState(true);
  const [validationErrors, setValidationErrors] = useState({});

  // Handle input changes
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear validation error when user starts typing
    if (validationErrors[field]) {
      setValidationErrors(prev => ({
        ...prev,
        [field]: null
      }));
    }
  };

  // Auto-fill intelligent defaults
  const handleAutoFill = () => {
    const currentDate = new Date();
    const dateCode = currentDate.toISOString().slice(0, 10).replace(/-/g, '');
    
    setFormData(prev => ({
      ...prev,
      techId: prev.techId || 'ADT001', // Smart default based on your operation
      flaggedBoxes: prev.flaggedBoxes || 'NO', // Most common case
      batteryRemoval: prev.batteryRemoval || 'YES', // Safety default
      dateCode: prev.dateCode || dateCode,
      disposition: prev.disposition || 'RECEIVED', // Standard disposition
      // Note: partNo is handled by SmartPartLookup component
    }));
  };

  // Validate required fields
  const validateForm = () => {
    const errors = {};
    const requiredFields = {
      trackingNo: 'Tracking Number',
      flaggedBoxes: 'Flagged Boxes',
      techId: 'Tech ID',
      partNo: 'Part Number',
      batteryRemoval: 'Battery Removal',
      dockLogId: 'Dock Log ID',
      disposition: 'Disposition'
    };

    Object.entries(requiredFields).forEach(([field, label]) => {
      if (!formData[field] || formData[field].trim() === '') {
        errors[field] = `${label} is required`;
      }
    });

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = () => {
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  // Clear form
  const handleClear = () => {
    setFormData({
      trackingNo: '',
      flaggedBoxes: '',
      techId: '',
      partNo: '', // SmartPartLookup will handle default/conversion
      batteryRemoval: '',
      dockLogId: '',
      disposition: '',
      rma: '',
      qtySerial: '',
      mac: '',
      imei: '',
      dateCode: '',
    });
    setValidationErrors({});
  };

  // Count filled required fields
  const requiredFields = ['trackingNo', 'flaggedBoxes', 'techId', 'partNo', 'batteryRemoval', 'dockLogId', 'disposition'];
  const filledRequired = requiredFields.filter(field => formData[field] && formData[field].trim() !== '').length;

  return (
    <Card>
      <CardContent sx={{ p: 4 }}>
        {/* Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <InventoryIcon color="primary" sx={{ fontSize: 32 }} />
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Unit Receiving Form
              </Typography>
              <Typography variant="body2" color="text.secondary">
                ADT Program - Automated Processing
              </Typography>
            </Box>
          </Box>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip 
              label={`${filledRequired}/${requiredFields.length} Required`}
              color={filledRequired === requiredFields.length ? 'success' : 'warning'}
              variant="outlined"
            />
            <FormControlLabel
              control={
                <Switch
                  checked={autoFillEnabled}
                  onChange={(e) => setAutoFillEnabled(e.target.checked)}
                  size="small"
                />
              }
              label="Smart Fill"
              sx={{ m: 0 }}
            />
          </Box>
        </Box>

        {/* Auto-fill button */}
        {autoFillEnabled && (
          <Button
            startIcon={<AutoFillIcon />}
            onClick={handleAutoFill}
            variant="outlined"
            size="small"
            sx={{ mb: 3 }}
          >
            Auto-Fill Defaults
          </Button>
        )}

        {/* Required Fields Section */}
        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: 'error.main' }}>
          Required Fields *
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {/* Tracking No */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Tracking Number *"
              value={formData.trackingNo}
              onChange={(e) => handleInputChange('trackingNo', e.target.value.toUpperCase())}
              error={!!validationErrors.trackingNo}
              helperText={validationErrors.trackingNo}
              placeholder="Enter tracking number"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>

          {/* Tech ID */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Tech ID *"
              value={formData.techId}
              onChange={(e) => handleInputChange('techId', e.target.value.toUpperCase())}
              error={!!validationErrors.techId}
              helperText={validationErrors.techId}
              placeholder="ADT001"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>

          {/* Part No - Smart Lookup */}
          <Grid item xs={12} sm={6}>
            <SmartPartLookup
              value={formData.partNo}
              onChange={(processedPartNo) => handleInputChange('partNo', processedPartNo)}
              error={!!validationErrors.partNo}
              helperText={validationErrors.partNo}
              label="Part Number *"
            />
          </Grid>

          {/* Dock Log ID */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Dock Log ID *"
              value={formData.dockLogId}
              onChange={(e) => handleInputChange('dockLogId', e.target.value.toUpperCase())}
              error={!!validationErrors.dockLogId}
              helperText={validationErrors.dockLogId}
              placeholder="Enter dock log ID"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>

          {/* Flagged Boxes */}
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth error={!!validationErrors.flaggedBoxes}>
              <InputLabel>Flagged Boxes *</InputLabel>
              <Select
                value={formData.flaggedBoxes}
                onChange={(e) => handleInputChange('flaggedBoxes', e.target.value)}
                label="Flagged Boxes *"
              >
                <MenuItem value="">Select...</MenuItem>
                <MenuItem value="NO">NO</MenuItem>
                <MenuItem value="YES">YES</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Battery Removal */}
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth error={!!validationErrors.batteryRemoval}>
              <InputLabel>Battery Removal *</InputLabel>
              <Select
                value={formData.batteryRemoval}
                onChange={(e) => handleInputChange('batteryRemoval', e.target.value)}
                label="Battery Removal *"
              >
                <MenuItem value="">Select...</MenuItem>
                <MenuItem value="NO">NO</MenuItem>
                <MenuItem value="YES">YES</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Disposition */}
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Disposition *"
              value={formData.disposition}
              onChange={(e) => handleInputChange('disposition', e.target.value.toUpperCase())}
              error={!!validationErrors.disposition}
              helperText={validationErrors.disposition}
              placeholder="RECEIVED, DAMAGED, etc."
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        {/* Optional Fields Section */}
        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: 'text.secondary' }}>
          Optional Fields
        </Typography>
        
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {/* RMA */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="RMA"
              value={formData.rma}
              onChange={(e) => handleInputChange('rma', e.target.value.toUpperCase())}
              placeholder="RMA number (optional)"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>

          {/* Qty/Serial */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Qty/Serial"
              value={formData.qtySerial}
              onChange={(e) => handleInputChange('qtySerial', e.target.value.toUpperCase())}
              placeholder="Quantity or serial number"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>

          {/* MAC */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="MAC Address"
              value={formData.mac}
              onChange={(e) => handleInputChange('mac', e.target.value.toUpperCase())}
              placeholder="MAC address"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>

          {/* IMEI */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="IMEI"
              value={formData.imei}
              onChange={(e) => handleInputChange('imei', e.target.value)}
              placeholder="IMEI number"
            />
          </Grid>

          {/* Date Code */}
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Date Code"
              value={formData.dateCode}
              onChange={(e) => handleInputChange('dateCode', e.target.value.toUpperCase())}
              placeholder="Date code"
              inputProps={{ style: { textTransform: 'uppercase' } }}
            />
          </Grid>
        </Grid>

        {/* Action Buttons */}
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
          <Button
            variant="outlined"
            startIcon={<ClearIcon />}
            onClick={handleClear}
            disabled={isLoading}
          >
            Clear
          </Button>
          
          <Button
            variant="contained"
            startIcon={<ProcessIcon />}
            onClick={handleSubmit}
            disabled={isLoading || filledRequired < requiredFields.length}
            sx={{
              background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #33E1FF 0%, #9F67FF 100%)',
              },
            }}
          >
            {isLoading ? 'Processing...' : 'Process Unit'}
          </Button>
        </Box>

        {/* Validation Summary */}
        {Object.keys(validationErrors).length > 0 && (
          <Alert severity="error" sx={{ mt: 3 }}>
            Please fill in all required fields before processing.
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default UnitReceivingFormWidget;
