import React, { useState, useEffect } from 'react';
import {
  Container,
  Card,
  CardContent,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Box,
  Chip,
  Alert,
  Grid,
  InputAdornment,
  Fab,
  Tooltip,
  TablePagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Settings as SettingsIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  CloudUpload as ImportIcon,
  CloudDownload as ExportIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';

const PartMappingSettings = () => {
  const [mappings, setMappings] = useState([]);
  const [filteredMappings, setFilteredMappings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [categoryFilter, setCategoryFilter] = useState('all');
  
  // Dialog states
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  
  // Form states
  const [formData, setFormData] = useState({
    original: '',
    processAs: '',
    description: '',
    notes: '',
    disposition: ''
  });
  const [editingMapping, setEditingMapping] = useState(null);
  const [deletingMapping, setDeletingMapping] = useState(null);
  
  // Error/success states
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Load all mappings
  const loadMappings = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/part-mappings/all');
      const result = await response.json();
      
      if (result.success) {
        setMappings(result.mappings);
        setFilteredMappings(result.mappings);
        setError('');
      } else {
        setError('Failed to load part mappings');
      }
    } catch (error) {
      console.error('Error loading mappings:', error);
      setError('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  // Force reload all 121 mappings
  const forceReloadAllMappings = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/part-mappings/reload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const result = await response.json();
      
      if (result.success) {
        setSuccess(`Successfully reloaded ${result.mappings_loaded} part mappings!`);
        // Now load the fresh mappings
        await loadMappings();
      } else {
        setError('Failed to force reload part mappings');
      }
    } catch (error) {
      console.error('Error force reloading mappings:', error);
      setError('Error connecting to server during force reload');
    } finally {
      setLoading(false);
    }
  };

  // Filter mappings based on search and category
  const filterMappings = () => {
    let filtered = mappings;
    
    // Search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(mapping => 
        mapping.original.toLowerCase().includes(term) ||
        mapping.processAs.toLowerCase().includes(term) ||
        mapping.description.toLowerCase().includes(term) ||
        mapping.notes.toLowerCase().includes(term)
      );
    }
    
    // Category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(mapping => {
        const desc = mapping.description.toUpperCase();
        switch (categoryFilter) {
          case 'keypads':
            return desc.includes('KEYPAD');
          case 'cameras':
            return desc.includes('CAMERA');
          case 'sensors':
            return desc.includes('SENSOR');
          case 'network':
            return desc.includes('ROUTER') || desc.includes('WIFI');
          case 'detectors':
            return desc.includes('SMOKE') || desc.includes('DETECTOR') || desc.includes('CARBON MONOXIDE');
          case 'locks':
            return desc.includes('LOCK');
          default:
            return true;
        }
      });
    }
    
    setFilteredMappings(filtered);
    setPage(0); // Reset to first page when filtering
  };

  // Add new mapping
  const handleAddMapping = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/part-mappings/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const result = await response.json();
      
      if (result.success) {
        setSuccess('Part mapping added successfully');
        setAddDialogOpen(false);
        resetForm();
        loadMappings();
      } else {
        setError(result.message || 'Failed to add mapping');
      }
    } catch (error) {
      console.error('Error adding mapping:', error);
      setError('Error connecting to server');
    }
  };

  // Update existing mapping
  const handleUpdateMapping = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/part-mappings/update/${editingMapping.original}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const result = await response.json();
      
      if (result.success) {
        setSuccess('Part mapping updated successfully');
        setEditDialogOpen(false);
        resetForm();
        loadMappings();
      } else {
        setError(result.message || 'Failed to update mapping');
      }
    } catch (error) {
      console.error('Error updating mapping:', error);
      setError('Error connecting to server');
    }
  };

  // Delete mapping
  const handleDeleteMapping = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/part-mappings/delete/${deletingMapping.original}`, {
        method: 'DELETE',
      });
      
      const result = await response.json();
      
      if (result.success) {
        setSuccess('Part mapping deleted successfully');
        setDeleteDialogOpen(false);
        setDeletingMapping(null);
        loadMappings();
      } else {
        setError(result.message || 'Failed to delete mapping');
      }
    } catch (error) {
      console.error('Error deleting mapping:', error);
      setError('Error connecting to server');
    }
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      original: '',
      processAs: '',
      description: '',
      notes: '',
      disposition: ''
    });
    setEditingMapping(null);
  };

  // Open edit dialog
  const openEditDialog = (mapping) => {
    setEditingMapping(mapping);
    setFormData({
      original: mapping.original,
      processAs: mapping.processAs,
      description: mapping.description,
      notes: mapping.notes || '',
      disposition: mapping.disposition || ''
    });
    setEditDialogOpen(true);
  };

  // Open delete dialog
  const openDeleteDialog = (mapping) => {
    setDeletingMapping(mapping);
    setDeleteDialogOpen(true);
  };

  // Export data
  const handleExport = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(mappings, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "part_mappings.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  // Effects
  useEffect(() => {
    loadMappings();
  }, []);

  useEffect(() => {
    filterMappings();
  }, [searchTerm, categoryFilter, mappings]);

  // Clear alerts after 5 seconds
  useEffect(() => {
    if (error || success) {
      const timer = setTimeout(() => {
        setError('');
        setSuccess('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, success]);

  // Get category color
  const getCategoryColor = (description) => {
    const desc = description.toUpperCase();
    if (desc.includes('KEYPAD')) return 'primary';
    if (desc.includes('CAMERA')) return 'secondary';
    if (desc.includes('SENSOR')) return 'info';
    if (desc.includes('ROUTER') || desc.includes('WIFI')) return 'warning';
    if (desc.includes('SMOKE') || desc.includes('DETECTOR')) return 'error';
    if (desc.includes('LOCK')) return 'success';
    return 'default';
  };

  const paginatedMappings = filteredMappings.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <SettingsIcon color="primary" sx={{ fontSize: 32 }} />
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 600 }}>
                    Part Mapping Management
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Manage part number conversions for Unit Receiving ADT
                  </Typography>
                </Box>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  startIcon={<RefreshIcon />}
                  onClick={forceReloadAllMappings}
                  disabled={loading}
                >
                  Force Reload All
                </Button>
                <Button
                  startIcon={<ExportIcon />}
                  onClick={handleExport}
                  variant="outlined"
                >
                  Export
                </Button>
                <Button
                  startIcon={<AddIcon />}
                  variant="contained"
                  onClick={() => setAddDialogOpen(true)}
                  sx={{
                    background: 'linear-gradient(135deg, #00D9FF 0%, #7C3AED 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #33E1FF 0%, #9F67FF 100%)',
                    },
                  }}
                >
                  Add New Mapping
                </Button>
              </Box>
            </Box>

            {/* Statistics */}
            <Grid container spacing={2}>
              <Grid item xs={12} sm={3}>
                <Chip 
                  label={`Total: ${mappings.length}`} 
                  color="primary" 
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={3}>
                <Chip 
                  label={`Filtered: ${filteredMappings.length}`} 
                  color="secondary" 
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={3}>
                <Chip 
                  label={`Keypads: ${mappings.filter(m => m.description.toUpperCase().includes('KEYPAD')).length}`} 
                  color="info" 
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={3}>
                <Chip 
                  label={`Cameras: ${mappings.filter(m => m.description.toUpperCase().includes('CAMERA')).length}`} 
                  color="warning" 
                  variant="outlined"
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Alerts */}
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
            {success}
          </Alert>
        )}

        {/* Filters */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Search mappings"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                  }}
                  placeholder="Search by original, process as, description..."
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <FormControl fullWidth>
                  <InputLabel>Category Filter</InputLabel>
                  <Select
                    value={categoryFilter}
                    onChange={(e) => setCategoryFilter(e.target.value)}
                    label="Category Filter"
                  >
                    <MenuItem value="all">All Categories</MenuItem>
                    <MenuItem value="keypads">Keypads</MenuItem>
                    <MenuItem value="cameras">Cameras</MenuItem>
                    <MenuItem value="sensors">Sensors</MenuItem>
                    <MenuItem value="network">Network</MenuItem>
                    <MenuItem value="detectors">Detectors</MenuItem>
                    <MenuItem value="locks">Smart Locks</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Table */}
        <Card>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell><strong>Original Part #</strong></TableCell>
                  <TableCell><strong>Process As</strong></TableCell>
                  <TableCell><strong>Description</strong></TableCell>
                  <TableCell><strong>Notes</strong></TableCell>
                  <TableCell><strong>Disposition</strong></TableCell>
                  <TableCell align="center"><strong>Actions</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography>Loading mappings...</Typography>
                    </TableCell>
                  </TableRow>
                ) : paginatedMappings.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography color="text.secondary">No mappings found</Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  paginatedMappings.map((mapping, index) => (
                    <TableRow key={index} hover>
                      <TableCell>
                        <Typography variant="body1" sx={{ fontFamily: 'monospace', fontWeight: 600 }}>
                          {mapping.original}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body1" sx={{ fontFamily: 'monospace', color: 'primary.main' }}>
                          {mapping.processAs}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body2">
                            {mapping.description}
                          </Typography>
                          <Chip 
                            label={getCategoryColor(mapping.description)} 
                            size="small" 
                            color={getCategoryColor(mapping.description)}
                            variant="outlined"
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" color="text.secondary">
                          {mapping.notes || '-'}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        {mapping.disposition ? (
                          <Chip 
                            label={mapping.disposition} 
                            size="small" 
                            color="warning"
                            variant="filled"
                          />
                        ) : (
                          <Typography variant="body2" color="text.secondary">-</Typography>
                        )}
                      </TableCell>
                      <TableCell align="center">
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Tooltip title="Edit mapping">
                            <IconButton 
                              size="small" 
                              color="primary"
                              onClick={() => openEditDialog(mapping)}
                            >
                              <EditIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Delete mapping">
                            <IconButton 
                              size="small" 
                              color="error"
                              onClick={() => openDeleteDialog(mapping)}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
          
          <TablePagination
            rowsPerPageOptions={[25, 50, 100, { label: 'All', value: -1 }]}
            component="div"
            count={filteredMappings.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={(event, newPage) => setPage(newPage)}
            onRowsPerPageChange={(event) => {
              setRowsPerPage(parseInt(event.target.value, 10));
              setPage(0);
            }}
          />
        </Card>

        {/* Add Dialog */}
        <Dialog open={addDialogOpen} onClose={() => setAddDialogOpen(false)} maxWidth="md" fullWidth>
          <DialogTitle>Add New Part Mapping</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Original Part Number *"
                  value={formData.original}
                  onChange={(e) => setFormData(prev => ({ ...prev, original: e.target.value.toUpperCase() }))}
                  helperText="What operators see on the physical unit"
                  inputProps={{ style: { textTransform: 'uppercase' } }}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Process As *"
                  value={formData.processAs}
                  onChange={(e) => setFormData(prev => ({ ...prev, processAs: e.target.value.toUpperCase() }))}
                  helperText="What should be entered in the system"
                  inputProps={{ style: { textTransform: 'uppercase' } }}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description *"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  helperText="Brief description of the part"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Notes"
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                  helperText="Optional notes or special instructions"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Disposition"
                  value={formData.disposition}
                  onChange={(e) => setFormData(prev => ({ ...prev, disposition: e.target.value.toUpperCase() }))}
                  helperText="e.g., SCRAP, HOLD, CR PROGRAM"
                  inputProps={{ style: { textTransform: 'uppercase' } }}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => { setAddDialogOpen(false); resetForm(); }}>
              Cancel
            </Button>
            <Button 
              onClick={handleAddMapping}
              variant="contained"
              startIcon={<SaveIcon />}
              disabled={!formData.original || !formData.processAs || !formData.description}
            >
              Add Mapping
            </Button>
          </DialogActions>
        </Dialog>

        {/* Edit Dialog */}
        <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="md" fullWidth>
          <DialogTitle>Edit Part Mapping</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Original Part Number *"
                  value={formData.original}
                  onChange={(e) => setFormData(prev => ({ ...prev, original: e.target.value.toUpperCase() }))}
                  helperText="What operators see on the physical unit"
                  inputProps={{ style: { textTransform: 'uppercase' } }}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Process As *"
                  value={formData.processAs}
                  onChange={(e) => setFormData(prev => ({ ...prev, processAs: e.target.value.toUpperCase() }))}
                  helperText="What should be entered in the system"
                  inputProps={{ style: { textTransform: 'uppercase' } }}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description *"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  helperText="Brief description of the part"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Notes"
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                  helperText="Optional notes or special instructions"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Disposition"
                  value={formData.disposition}
                  onChange={(e) => setFormData(prev => ({ ...prev, disposition: e.target.value.toUpperCase() }))}
                  helperText="e.g., SCRAP, HOLD, CR PROGRAM"
                  inputProps={{ style: { textTransform: 'uppercase' } }}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => { setEditDialogOpen(false); resetForm(); }}>
              Cancel
            </Button>
            <Button 
              onClick={handleUpdateMapping}
              variant="contained"
              startIcon={<SaveIcon />}
              disabled={!formData.original || !formData.processAs || !formData.description}
            >
              Update Mapping
            </Button>
          </DialogActions>
        </Dialog>

        {/* Delete Dialog */}
        <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
          <DialogTitle>Delete Part Mapping</DialogTitle>
          <DialogContent>
            <Typography>
              Are you sure you want to delete the mapping for:
            </Typography>
            <Box sx={{ mt: 2, p: 2, bgcolor: 'error.lighter', borderRadius: 1 }}>
              <Typography variant="body1" sx={{ fontFamily: 'monospace', fontWeight: 600 }}>
                {deletingMapping?.original} → {deletingMapping?.processAs}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {deletingMapping?.description}
              </Typography>
            </Box>
            <Typography sx={{ mt: 2 }} color="error">
              This action cannot be undone.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => { setDeleteDialogOpen(false); setDeletingMapping(null); }}>
              Cancel
            </Button>
            <Button 
              onClick={handleDeleteMapping}
              variant="contained"
              color="error"
              startIcon={<DeleteIcon />}
            >
              Delete Mapping
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default PartMappingSettings;
