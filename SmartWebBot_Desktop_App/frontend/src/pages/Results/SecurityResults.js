import React, { useState, useEffect } from 'react';
import {
  Container, Typography, Paper, Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Button, Chip, Box, Grid, Card, CardContent,
  Dialog, DialogTitle, DialogContent, DialogActions, CircularProgress,
  Tabs, Tab, List, ListItem, ListItemText, ListItemIcon, Divider,
  IconButton, Tooltip, Alert
} from '@mui/material';
import {
  Download, Visibility, Security, BugReport, Web, Schedule,
  Assessment, TrendingUp, Warning, CheckCircle, Error,
  GetApp, TableChart, Description
} from '@mui/icons-material';

const SecurityResults = () => {
  const [sessions, setSessions] = useState([]);
  const [summary, setSummary] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);
  const [sessionDetails, setSessionDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    loadSecurityData();
  }, []);

  const loadSecurityData = async () => {
    setLoading(true);
    try {
      // Load sessions and summary in parallel
      const [sessionsResponse, summaryResponse] = await Promise.all([
        fetch('http://localhost:8000/api/security/results/sessions'),
        fetch('http://localhost:8000/api/security/results/summary')
      ]);

      if (sessionsResponse.ok) {
        const sessionsData = await sessionsResponse.json();
        setSessions(sessionsData.sessions || []);
      }

      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json();
        setSummary(summaryData);
      }
    } catch (error) {
      console.error('Failed to load security data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSessionDetails = async (sessionId) => {
    setDetailsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/security/results/session/${sessionId}`);
      if (response.ok) {
        const details = await response.json();
        setSessionDetails(details);
        setDialogOpen(true);
      }
    } catch (error) {
      console.error('Failed to load session details:', error);
    } finally {
      setDetailsLoading(false);
    }
  };

  const downloadReport = async (sessionId, format) => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/security/results/export/${sessionId}?format=${format}`
      );
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `security_report_${sessionId}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Failed to download report:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL': return 'error';
      case 'HIGH': return 'warning';
      case 'MEDIUM': return 'info';
      case 'LOW': return 'success';
      default: return 'default';
    }
  };

  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel?.toUpperCase()) {
      case 'CRITICAL': return '#f44336';
      case 'HIGH': return '#ff9800';
      case 'MEDIUM': return '#2196f3';
      case 'LOW': return '#4caf50';
      default: return '#9e9e9e';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress size={60} />
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <Assessment sx={{ mr: 2, color: 'primary.main' }} />
        Security Testing Results
      </Typography>

      {/* Summary Cards */}
      {summary && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                      {sessions.length}
                    </Typography>
                    <Typography variant="body2">
                      Total Sessions
                    </Typography>
                  </Box>
                  <Security sx={{ fontSize: 40, opacity: 0.7 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                      {summary.vulnerability_types?.reduce((sum, type) => sum + type.count, 0) || 0}
                    </Typography>
                    <Typography variant="body2">
                      Total Vulnerabilities
                    </Typography>
                  </Box>
                  <BugReport sx={{ fontSize: 40, opacity: 0.7 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                      {summary.vulnerability_types?.length || 0}
                    </Typography>
                    <Typography variant="body2">
                      Vulnerability Types
                    </Typography>
                  </Box>
                  <Warning sx={{ fontSize: 40, opacity: 0.7 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
                      {summary.recent_stats?.total_sessions || 0}
                    </Typography>
                    <Typography variant="body2">
                      Recent Sessions (30d)
                    </Typography>
                  </Box>
                  <TrendingUp sx={{ fontSize: 40, opacity: 0.7 }} />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Main Content */}
      <Paper sx={{ width: '100%', mb: 2 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tab label="All Sessions" icon={<Assessment />} />
          <Tab label="Vulnerability Summary" icon={<BugReport />} />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {tabValue === 0 && (
            <>
              <Typography variant="h6" gutterBottom>
                Security Testing Sessions
              </Typography>
              {sessions.length === 0 ? (
                <Alert severity="info" sx={{ mt: 2 }}>
                  No security testing sessions found. Run some security tests to see results here.
                </Alert>
              ) : (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Target URL</TableCell>
                        <TableCell>Start Time</TableCell>
                        <TableCell>Tests</TableCell>
                        <TableCell>Vulnerabilities</TableCell>
                        <TableCell>Elements</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {sessions.map((session) => (
                        <TableRow key={session.session_id} hover>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Web sx={{ mr: 1, color: 'primary.main' }} />
                              <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                                {session.target_url}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                              <Schedule sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
                              {formatDate(session.start_time)}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={session.total_tests || 0} 
                              size="small" 
                              color="primary" 
                              variant="outlined"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={session.vulnerabilities_found || 0}
                              size="small"
                              color={session.vulnerabilities_found > 0 ? 'error' : 'success'}
                              icon={session.vulnerabilities_found > 0 ? <Warning /> : <CheckCircle />}
                            />
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={session.elements_discovered || 0}
                              size="small"
                              color="info"
                              variant="outlined"
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', gap: 1 }}>
                              <Tooltip title="View Details">
                                <IconButton 
                                  size="small" 
                                  onClick={() => loadSessionDetails(session.session_id)}
                                  disabled={detailsLoading}
                                >
                                  <Visibility />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Download JSON Report">
                                <IconButton 
                                  size="small" 
                                  onClick={() => downloadReport(session.session_id, 'json')}
                                >
                                  <Description />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Download CSV Report">
                                <IconButton 
                                  size="small" 
                                  onClick={() => downloadReport(session.session_id, 'csv')}
                                >
                                  <TableChart />
                                </IconButton>
                              </Tooltip>
                            </Box>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </>
          )}

          {tabValue === 1 && summary && (
            <>
              <Typography variant="h6" gutterBottom>
                Vulnerability Analysis
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Vulnerability Types
                      </Typography>
                      <List>
                        {summary.vulnerability_types?.map((type, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <BugReport color="error" />
                            </ListItemIcon>
                            <ListItemText 
                              primary={type.type.replace('_', ' ').toUpperCase()}
                              secondary={`${type.count} found`}
                            />
                            <Chip 
                              label={type.count} 
                              size="small" 
                              color="error" 
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        Severity Breakdown
                      </Typography>
                      <List>
                        {summary.severity_breakdown?.map((severity, index) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <Error sx={{ color: getRiskLevelColor(severity.severity) }} />
                            </ListItemIcon>
                            <ListItemText 
                              primary={severity.severity}
                              secondary={`${severity.count} vulnerabilities`}
                            />
                            <Chip 
                              label={severity.count} 
                              size="small" 
                              sx={{ 
                                backgroundColor: getRiskLevelColor(severity.severity),
                                color: 'white'
                              }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </>
          )}
        </Box>
      </Paper>

      {/* Session Details Dialog */}
      <Dialog 
        open={dialogOpen} 
        onClose={() => setDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          Security Session Details
          {sessionDetails && (
            <Typography variant="body2" color="text.secondary">
              Session ID: {selectedSession}
            </Typography>
          )}
        </DialogTitle>
        <DialogContent>
          {detailsLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
              <CircularProgress />
            </Box>
          ) : sessionDetails ? (
            <Box sx={{ mt: 2 }}>
              {/* Session Info */}
              <Typography variant="h6" gutterBottom>Session Information</Typography>
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">Target URL:</Typography>
                  <Typography variant="body1" sx={{ fontFamily: 'monospace', wordBreak: 'break-all' }}>
                    {sessionDetails.session.target_url}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">Duration:</Typography>
                  <Typography variant="body1">
                    {sessionDetails.session.start_time && sessionDetails.session.end_time ? 
                      `${Math.round((new Date(sessionDetails.session.end_time) - new Date(sessionDetails.session.start_time)) / 1000)}s` : 
                      'N/A'
                    }
                  </Typography>
                </Grid>
              </Grid>

              <Divider sx={{ my: 2 }} />

              {/* Vulnerabilities */}
              <Typography variant="h6" gutterBottom>
                Vulnerabilities Found ({sessionDetails.vulnerabilities?.length || 0})
              </Typography>
              {sessionDetails.vulnerabilities?.length > 0 ? (
                <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Type</TableCell>
                        <TableCell>Severity</TableCell>
                        <TableCell>Element</TableCell>
                        <TableCell>Evidence</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {sessionDetails.vulnerabilities.map((vuln, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            <Chip 
                              label={vuln.vulnerability_type.replace('_', ' ').toUpperCase()} 
                              size="small"
                              color="error"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={vuln.severity} 
                              size="small"
                              color={getSeverityColor(vuln.severity)}
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                              {vuln.element_type}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" sx={{ maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                              {vuln.evidence}
                            </Typography>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Alert severity="success" sx={{ mb: 3 }}>
                  No vulnerabilities found in this session.
                </Alert>
              )}

              {/* Discovered Elements */}
              <Typography variant="h6" gutterBottom>
                Discovered Elements ({sessionDetails.elements?.length || 0})
              </Typography>
              {sessionDetails.elements?.length > 0 && (
                <TableContainer component={Paper} variant="outlined">
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Type</TableCell>
                        <TableCell>ID</TableCell>
                        <TableCell>URL</TableCell>
                        <TableCell>Method</TableCell>
                        <TableCell>Parameters</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {sessionDetails.elements.slice(0, 10).map((element, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            <Chip label={element.element_type} size="small" variant="outlined" />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                              {element.element_id}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" sx={{ fontFamily: 'monospace', maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                              {element.element_url}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip label={element.method || 'GET'} size="small" color="primary" />
                          </TableCell>
                          <TableCell>{element.parameters_count || 0}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </Box>
          ) : null}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Close</Button>
          {selectedSession && (
            <>
              <Button 
                onClick={() => downloadReport(selectedSession, 'json')}
                startIcon={<GetApp />}
                variant="outlined"
              >
                Download JSON
              </Button>
              <Button 
                onClick={() => downloadReport(selectedSession, 'csv')}
                startIcon={<GetApp />}
                variant="outlined"
              >
                Download CSV
              </Button>
            </>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default SecurityResults;
