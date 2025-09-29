import React, { useState, useEffect, useRef } from 'react';
import {
  TextField,
  Autocomplete,
  Chip,
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  CircularProgress,
  Paper,
  Grid,
  Divider
} from '@mui/material';
import {
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Add as AddIcon,
  Search as SearchIcon,
  AutoAwesome as AutoIcon
} from '@mui/icons-material';
const SmartPartLookup = ({ 
  value = '', 
  onChange, 
  error, 
  helperText,
  label = "Part Number *",
  disabled = false 
}) => {
  const [inputValue, setInputValue] = useState('');
  const [processedValue, setProcessedValue] = useState(value);
  const [suggestions, setSuggestions] = useState([]);
  const [autoConversion, setAutoConversion] = useState(null);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [newPartData, setNewPartData] = useState({
    original: '',
    processAs: '',
    description: '',
    notes: '',
    disposition: ''
  });
  const [loading, setLoading] = useState(false);
  const [conversionStatus, setConversionStatus] = useState('none'); // 'none', 'auto', 'manual', 'new'
  
  const debounceRef = useRef();

  // API helper functions
  const searchPartNumber = async (query) => {
    try {
      const response = await fetch('http://localhost:8000/api/part-mappings/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      const result = await response.json();
      return result.success ? result.results : [];
    } catch (error) {
      console.error('Part search error:', error);
      return [];
    }
  };

  const getAutoConversion = async (input) => {
    const results = await searchPartNumber(input);
    // Find exact match for auto-conversion
    return results.find(mapping => 
      mapping.original && mapping.original.toUpperCase() === input.toUpperCase()
    ) || null;
  };

  const addNewPartMapping = async (originalPart, processAsPart, description, notes = '', disposition = '') => {
    try {
      const response = await fetch('http://localhost:8000/api/part-mappings/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          original: originalPart,
          processAs: processAsPart,
          description: description,
          notes: notes,
          disposition: disposition
        }),
      });
      
      const result = await response.json();
      if (result.success) {
        return result.mapping;
      } else {
        throw new Error(result.message || 'Failed to add mapping');
      }
    } catch (error) {
      console.error('Add mapping error:', error);
      throw error;
    }
  };

  // Update input when value prop changes
  useEffect(() => {
    if (value !== processedValue) {
      setInputValue(value);
      setProcessedValue(value);
    }
  }, [value, processedValue]);

  // Handle input changes with smart lookup
  useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(() => {
      handlePartLookup(inputValue);
    }, 300);

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [inputValue]);

  const handlePartLookup = async (input) => {
    if (!input || input.trim() === '') {
      setSuggestions([]);
      setAutoConversion(null);
      setConversionStatus('none');
      return;
    }

    setLoading(true);
    
    try {
      // Check for auto-conversion first
      const autoConvert = await getAutoConversion(input);
      
      if (autoConvert) {
        setAutoConversion(autoConvert);
        setProcessedValue(autoConvert.processAs);
        setConversionStatus('auto');
        onChange?.(autoConvert.processAs);
        
        // Still get suggestions for alternatives
        const searchResults = await searchPartNumber(input);
        setSuggestions(searchResults.slice(0, 5));
      } else {
        // No exact match, show suggestions
        const searchResults = await searchPartNumber(input);
        setSuggestions(searchResults);
        setAutoConversion(null);
        setConversionStatus(searchResults.length > 0 ? 'manual' : 'new');
        
        if (searchResults.length === 0) {
          setProcessedValue(input.toUpperCase());
          onChange?.(input.toUpperCase());
        }
      }
    } catch (error) {
      console.error('Part lookup error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event, newValue, reason) => {
    if (reason === 'input') {
      setInputValue(newValue);
    }
  };

  const handleOptionSelect = (event, selectedOption, reason) => {
    if (selectedOption && typeof selectedOption === 'object') {
      setProcessedValue(selectedOption.processAs);
      setInputValue(selectedOption.original);
      setAutoConversion(selectedOption);
      setConversionStatus('manual');
      onChange?.(selectedOption.processAs);
    } else if (typeof selectedOption === 'string') {
      setInputValue(selectedOption);
      setProcessedValue(selectedOption.toUpperCase());
      onChange?.(selectedOption.toUpperCase());
    }
  };

  const handleAddNewPart = async () => {
    try {
      const newMapping = await addNewPartMapping(
        newPartData.original || inputValue,
        newPartData.processAs,
        newPartData.description,
        newPartData.notes,
        newPartData.disposition
      );
      
      setAutoConversion(newMapping);
      setProcessedValue(newMapping.processAs);
      setConversionStatus('auto');
      onChange?.(newMapping.processAs);
      setShowAddDialog(false);
      
      // Reset form
      setNewPartData({
        original: '',
        processAs: '',
        description: '',
        notes: '',
        disposition: ''
      });
    } catch (error) {
      console.error('Error adding new part mapping:', error);
    }
  };

  const getStatusIcon = () => {
    switch (conversionStatus) {
      case 'auto':
        return <CheckIcon color="success" sx={{ fontSize: 20 }} />;
      case 'manual':
        return <WarningIcon color="warning" sx={{ fontSize: 20 }} />;
      case 'new':
        return <AddIcon color="info" sx={{ fontSize: 20 }} />;
      default:
        return <SearchIcon color="disabled" sx={{ fontSize: 20 }} />;
    }
  };

  const getStatusText = () => {
    switch (conversionStatus) {
      case 'auto':
        return `Auto-converted to: ${processedValue}`;
      case 'manual':
        return `${suggestions.length} matches found - select one`;
      case 'new':
        return 'Part not found - add new mapping?';
      default:
        return 'Enter part number from unit';
    }
  };

  const getStatusColor = () => {
    switch (conversionStatus) {
      case 'auto':
        return 'success.main';
      case 'manual':
        return 'warning.main';
      case 'new':
        return 'info.main';
      default:
        return 'text.secondary';
    }
  };

  return (
    <>
      <Box>
        <Autocomplete
          freeSolo
          options={suggestions}
          getOptionLabel={(option) => {
            if (typeof option === 'string') return option;
            return option.original;
          }}
          renderOption={(props, option) => (
            <Box component="li" {...props}>
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                  {option.original} → {option.processAs}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {option.description}
                </Typography>
                {option.disposition && (
                  <Chip 
                    label={option.disposition} 
                    size="small" 
                    color="primary" 
                    sx={{ mt: 0.5 }} 
                  />
                )}
              </Box>
            </Box>
          )}
          inputValue={inputValue}
          onInputChange={handleInputChange}
          onChange={handleOptionSelect}
          disabled={disabled}
          loading={loading}
          renderInput={(params) => (
            <TextField
              {...params}
              label={label}
              error={!!error}
              helperText={error || helperText}
              InputProps={{
                ...params.InputProps,
                endAdornment: (
                  <>
                    {loading && <CircularProgress color="inherit" size={20} />}
                    {params.InputProps.endAdornment}
                  </>
                ),
                startAdornment: getStatusIcon(),
                style: { textTransform: 'uppercase' }
              }}
            />
          )}
        />
        
        {/* Status Display */}
        <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography 
            variant="caption" 
            sx={{ color: getStatusColor(), display: 'flex', alignItems: 'center', gap: 0.5 }}
          >
            <AutoIcon sx={{ fontSize: 16 }} />
            {getStatusText()}
          </Typography>
          
          {conversionStatus === 'new' && (
            <Button 
              size="small" 
              startIcon={<AddIcon />}
              onClick={() => {
                setNewPartData(prev => ({ ...prev, original: inputValue }));
                setShowAddDialog(true);
              }}
              sx={{ fontSize: 'inherit' }}
            >
              Add New
            </Button>
          )}
        </Box>

        {/* Auto-conversion Display */}
        {autoConversion && conversionStatus === 'auto' && (
          <Paper sx={{ mt: 2, p: 2, bgcolor: 'success.lighter', border: '1px solid', borderColor: 'success.light' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <CheckIcon color="success" sx={{ fontSize: 20 }} />
              <Typography variant="subtitle2" color="success.dark">
                Automatic Conversion Applied
              </Typography>
            </Box>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Original:</Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                  {autoConversion.original}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Process As:</Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace', fontWeight: 600 }}>
                  {autoConversion.processAs}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="body2" color="text.secondary">Description:</Typography>
                <Typography variant="body2">
                  {autoConversion.description}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        )}
      </Box>

      {/* Add New Part Dialog */}
      <Dialog open={showAddDialog} onClose={() => setShowAddDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Add New Part Number Mapping
        </DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 3 }}>
            This will add a permanent mapping for future use. Make sure the information is accurate.
          </Alert>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Part # on Unit"
                value={newPartData.original}
                onChange={(e) => setNewPartData(prev => ({ ...prev, original: e.target.value.toUpperCase() }))}
                helperText="What operators see on the physical unit"
                inputProps={{ style: { textTransform: 'uppercase' } }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Process As *"
                value={newPartData.processAs}
                onChange={(e) => setNewPartData(prev => ({ ...prev, processAs: e.target.value.toUpperCase() }))}
                helperText="What should be entered in the system"
                required
                inputProps={{ style: { textTransform: 'uppercase' } }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Description *"
                value={newPartData.description}
                onChange={(e) => setNewPartData(prev => ({ ...prev, description: e.target.value }))}
                helperText="Brief description of the part"
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Notes"
                value={newPartData.notes}
                onChange={(e) => setNewPartData(prev => ({ ...prev, notes: e.target.value }))}
                helperText="Optional notes or special instructions"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Disposition"
                value={newPartData.disposition}
                onChange={(e) => setNewPartData(prev => ({ ...prev, disposition: e.target.value.toUpperCase() }))}
                helperText="e.g., SCRAP, HOLD, CR PROGRAM"
                inputProps={{ style: { textTransform: 'uppercase' } }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAddDialog(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleAddNewPart}
            variant="contained"
            disabled={!newPartData.processAs || !newPartData.description}
          >
            Add Mapping
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default SmartPartLookup;
