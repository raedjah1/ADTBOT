import React, { useState } from 'react';
import { Box, Typography, Tabs, Tab, Paper, Card, CardContent, Grid, Chip, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import { Assessment, Analytics, History, Assignment, CheckCircle, Error, Schedule } from '@mui/icons-material';

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`results-tabpanel-${index}`}
      aria-labelledby={`results-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 0 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const Results = () => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 3 }}>
        RMA Reports & Analytics 📊
      </Typography>
      
      <Paper sx={{ width: '100%' }}>
        <Tabs 
          value={tabValue} 
          onChange={handleTabChange}
          sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}
        >
          <Tab 
            icon={<Assignment />} 
            label="RMA Processing" 
            id="results-tab-0"
            aria-controls="results-tabpanel-0"
          />
          <Tab 
            icon={<Analytics />} 
            label="Analytics" 
            id="results-tab-1"
            aria-controls="results-tabpanel-1"
          />
          <Tab 
            icon={<Assessment />} 
            label="Reports" 
            id="results-tab-2"
            aria-controls="results-tabpanel-2"
          />
          <Tab 
            icon={<History />} 
            label="Processing History" 
            id="results-tab-3"
            aria-controls="results-tabpanel-3"
          />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              RMA Processing Summary
            </Typography>
            
            <Grid container spacing={3} sx={{ mt: 2 }}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <CheckCircle color="success" sx={{ mr: 1 }} />
                      <Typography variant="h6">1,247</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      Successfully Processed
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Schedule color="warning" sx={{ mr: 1 }} />
                      <Typography variant="h6">23</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      Pending Processing
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Error color="error" sx={{ mr: 1 }} />
                      <Typography variant="h6">5</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      Processing Errors
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Processing Activity
                </Typography>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Batch RMA-2024-001 Completed"
                      secondary="125 items processed successfully - 2 hours ago"
                    />
                    <Chip label="Completed" color="success" size="small" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <Schedule color="warning" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Tracking Validation in Progress"
                      secondary="Validating 47 FedEx tracking numbers - 15 minutes ago"
                    />
                    <Chip label="In Progress" color="warning" size="small" />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <CheckCircle color="success" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Label Generation Complete"
                      secondary="Generated 89 shipping labels for outbound RMAs - 1 hour ago"
                    />
                    <Chip label="Completed" color="success" size="small" />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Box>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              RMA Analytics Dashboard
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 3 }}>
              Performance analytics and processing statistics for RMA operations.
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Processing Efficiency
                    </Typography>
                    <Typography variant="h3" color="primary">
                      94.2%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Average processing success rate
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Average Processing Time
                    </Typography>
                    <Typography variant="h3" color="primary">
                      2.3 min
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Per RMA item processed
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Generated Reports
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 3 }}>
              Download comprehensive reports for RMA processing activities.
            </Typography>
            
            <List>
              <ListItem>
                <ListItemText 
                  primary="Daily Processing Report"
                  secondary="Summary of all RMA activities for today"
                />
                <Chip label="Download" color="primary" variant="outlined" />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Weekly Analytics Report"
                  secondary="Comprehensive analytics for the past 7 days"
                />
                <Chip label="Download" color="primary" variant="outlined" />
              </ListItem>
              <ListItem>
                <ListItemText 
                  primary="Error Analysis Report"
                  secondary="Detailed analysis of processing errors and resolutions"
                />
                <Chip label="Download" color="primary" variant="outlined" />
              </ListItem>
            </List>
          </Box>
        </TabPanel>

        <TabPanel value={tabValue} index={3}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              RMA Processing History
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 3 }}>
              Complete history of all RMA processing activities.
            </Typography>
            
            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="RMA Batch Processing"
                  secondary="Processed 125 items in batch RMA-2024-001 - 2 hours ago"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="Tracking Validation"
                  secondary="Validated 89 tracking numbers successfully - 3 hours ago"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText 
                  primary="Label Generation"
                  secondary="Generated shipping labels for 156 outbound RMAs - 4 hours ago"
                />
              </ListItem>
            </List>
          </Box>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default Results;