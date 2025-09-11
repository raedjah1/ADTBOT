import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Chip,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  LinearProgress
} from '@mui/material';
import {
  PlayArrow as StartIcon,
  CheckCircle as CompleteIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Web as WebIcon,
  Security as SecurityIcon,
  Build as BuildIcon,
  Speed as SpeedIcon,
  School as LearnIcon,
  Lightbulb as TipIcon
} from '@mui/icons-material';

const GuidedWorkflow = ({ onWorkflowComplete, userLevel = 'beginner', isDarkMode = true }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [workflowData, setWorkflowData] = useState({
    goal: '',
    targetUrl: '',
    taskType: '',
    difficulty: 'beginner',
    requirements: []
  });
  const [isComplete, setIsComplete] = useState(false);

  const workflows = {
    beginner: [
      {
        id: 'web_automation',
        title: '🌐 Web Automation',
        description: 'Automate website interactions like form filling, clicking, and navigation',
        difficulty: 'Easy',
        time: '5-10 min',
        icon: <WebIcon />,
        color: '#4CAF50',
        examples: ['Fill contact forms', 'Login to accounts', 'Navigate websites', 'Take screenshots']
      },
      {
        id: 'data_extraction',
        title: '📊 Data Extraction',
        description: 'Extract and collect data from websites automatically',
        difficulty: 'Easy',
        time: '10-15 min',
        icon: <SpeedIcon />,
        color: '#2196F3',
        examples: ['Scrape product prices', 'Collect contact info', 'Extract news articles', 'Gather reviews']
      },
      {
        id: 'task_building',
        title: '⚡ Task Building',
        description: 'Build custom automation workflows with our visual task builder',
        difficulty: 'Easy',
        time: '5-10 min',
        icon: <BuildIcon />,
        color: '#FF5722',
        examples: ['Drag & drop actions', 'Custom workflows', 'Reusable templates', 'Advanced logic']
      }
    ],
    intermediate: [
      {
        id: 'advanced_automation',
        title: '🚀 Advanced Automation',
        description: 'Complex multi-step workflows with error handling',
        difficulty: 'Medium',
        time: '20-30 min',
        icon: <BuildIcon />,
        color: '#9C27B0',
        examples: ['E-commerce workflows', 'Social media automation', 'Report generation', 'API integration']
      }
    ],
    expert: [
      {
        id: 'custom_development',
        title: '⚡ Custom Development',
        description: 'Build custom solutions with advanced features',
        difficulty: 'Expert',
        time: '30+ min',
        icon: <BuildIcon />,
        color: '#F44336',
        examples: ['Custom plugins', 'AI integration', 'Advanced security', 'Enterprise solutions']
      }
    ]
  };

  const steps = [
    {
      label: 'Choose Your Goal',
      description: 'What do you want to accomplish?',
      content: (
        <Box>
          <Typography variant="body1" gutterBottom>
            Select what you'd like to do with SmartWebBot:
          </Typography>
          
          <Grid container spacing={2} sx={{ mt: 1 }}>
            {workflows[userLevel].map((workflow) => (
              <Grid item xs={12} md={6} key={workflow.id}>
                <Paper
                  sx={{
                    p: 2,
                    cursor: 'pointer',
                    border: workflowData.taskType === workflow.id ? 2 : 1,
                    borderColor: workflowData.taskType === workflow.id ? workflow.color : 'divider',
                    '&:hover': { boxShadow: 2 }
                  }}
                  onClick={() => setWorkflowData({...workflowData, taskType: workflow.id})}
                >
                  <Box display="flex" alignItems="center" gap={2} mb={1}>
                    <Box sx={{ color: workflow.color }}>
                      {workflow.icon}
                    </Box>
                    <Box>
                      <Typography variant="h6">{workflow.title}</Typography>
                      <Box display="flex" gap={1} mt={0.5}>
                        <Chip label={workflow.difficulty} size="small" color="primary" />
                        <Chip label={workflow.time} size="small" variant="outlined" />
                      </Box>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="textSecondary" mb={1}>
                    {workflow.description}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Examples: {workflow.examples.join(', ')}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>

        </Box>
      )
    },
    {
      label: 'Target Website',
      description: 'Where do you want to run this automation?',
      content: (
        <Box>
          <Typography variant="body1" gutterBottom>
            Enter the website URL you want to work with:
          </Typography>
          
          <TextField
            fullWidth
            label="Target Website URL"
            placeholder="https://example.com"
            value={workflowData.targetUrl}
            onChange={(e) => setWorkflowData({...workflowData, targetUrl: e.target.value})}
            sx={{ mt: 2 }}
          />

          <Box mt={2}>
            <Typography variant="subtitle2" gutterBottom>
              💡 Quick Tips:
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon><TipIcon fontSize="small" /></ListItemIcon>
                <ListItemText primary="Use full URLs including https://" />
              </ListItem>
              <ListItem>
                <ListItemIcon><TipIcon fontSize="small" /></ListItemIcon>
                <ListItemText primary="Test on staging environments first" />
              </ListItem>
              <ListItem>
                <ListItemIcon><TipIcon fontSize="small" /></ListItemIcon>
                <ListItemText primary="Make sure you have permission to test" />
              </ListItem>
            </List>
          </Box>

        </Box>
      )
    },
    {
      label: 'Configuration',
      description: 'Customize your automation settings',
      content: (
        <Box>
          <Typography variant="body1" gutterBottom>
            Configure your automation preferences:
          </Typography>

          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Browser</InputLabel>
                <Select
                  value={workflowData.browser || 'chrome'}
                  onChange={(e) => setWorkflowData({...workflowData, browser: e.target.value})}
                  label="Browser"
                >
                  <MenuItem value="chrome">Chrome (Recommended)</MenuItem>
                  <MenuItem value="firefox">Firefox</MenuItem>
                  <MenuItem value="edge">Edge</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Speed</InputLabel>
                <Select
                  value={workflowData.speed || 'normal'}
                  onChange={(e) => setWorkflowData({...workflowData, speed: e.target.value})}
                  label="Speed"
                >
                  <MenuItem value="slow">Slow (More Reliable)</MenuItem>
                  <MenuItem value="normal">Normal</MenuItem>
                  <MenuItem value="fast">Fast (Less Reliable)</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <Typography variant="subtitle2" gutterBottom>
                Advanced Options:
              </Typography>
              <Box display="flex" gap={1} flexWrap="wrap">
                <Chip
                  label="Take Screenshots"
                  onClick={() => {
                    const screenshots = workflowData.screenshots || false;
                    setWorkflowData({...workflowData, screenshots: !screenshots});
                  }}
                  color={workflowData.screenshots ? 'primary' : 'default'}
                  variant={workflowData.screenshots ? 'filled' : 'outlined'}
                />
                <Chip
                  label="Stealth Mode"
                  onClick={() => {
                    const stealth = workflowData.stealth || false;
                    setWorkflowData({...workflowData, stealth: !stealth});
                  }}
                  color={workflowData.stealth ? 'primary' : 'default'}
                  variant={workflowData.stealth ? 'filled' : 'outlined'}
                />
                <Chip
                  label="Error Recovery"
                  onClick={() => {
                    const recovery = workflowData.recovery || false;
                    setWorkflowData({...workflowData, recovery: !recovery});
                  }}
                  color={workflowData.recovery ? 'primary' : 'default'}
                  variant={workflowData.recovery ? 'filled' : 'outlined'}
                />
              </Box>
            </Grid>
          </Grid>
        </Box>
      )
    },
    {
      label: 'Review & Launch',
      description: 'Review your configuration and start the automation',
      content: (
        <Box>
          <Typography variant="body1" gutterBottom>
            Review your automation setup:
          </Typography>

          <Paper sx={{ p: 2, mt: 2, bgcolor: isDarkMode ? '#21262D' : '#f5f5f5' }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="primary">Task Type:</Typography>
                <Typography variant="body1">
                  {workflows[userLevel].find(w => w.id === workflowData.taskType)?.title || 'Not selected'}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="primary">Target URL:</Typography>
                <Typography variant="body1">{workflowData.targetUrl || 'Not specified'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="primary">Browser:</Typography>
                <Typography variant="body1">{workflowData.browser || 'Chrome'}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="primary">Speed:</Typography>
                <Typography variant="body1">{workflowData.speed || 'Normal'}</Typography>
              </Grid>
            </Grid>
          </Paper>

          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="subtitle2">🚀 Ready to Launch!</Typography>
            Click "Complete Setup" to proceed to the task builder with your configuration pre-loaded.
          </Alert>
        </Box>
      )
    }
  ];

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleComplete = () => {
    setIsComplete(true);
    if (onWorkflowComplete) {
      onWorkflowComplete(workflowData);
    }
  };

  const canProceed = () => {
    switch (activeStep) {
      case 0:
        return workflowData.taskType;
      case 1:
        return workflowData.targetUrl;
      case 2:
        return true;
      case 3:
        return true;
      default:
        return false;
    }
  };

  if (isComplete) {
    return (
      <Card>
        <CardContent sx={{ textAlign: 'center', py: 4 }}>
          <CompleteIcon sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            🎉 Setup Complete!
          </Typography>
          <Typography variant="body1" color="textSecondary" mb={3}>
            Your automation workflow has been configured and is ready to use.
          </Typography>
          <Button variant="contained" size="large" startIcon={<StartIcon />}>
            Go to Task Builder
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" gap={2} mb={3}>
          <LearnIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Box>
            <Typography variant="h5">Guided Setup Wizard</Typography>
            <Typography variant="body2" color="textSecondary">
              Let's set up your automation in just a few steps
            </Typography>
          </Box>
        </Box>

        <LinearProgress 
          variant="determinate" 
          value={(activeStep / (steps.length - 1)) * 100} 
          sx={{ mb: 3 }}
        />

        <Stepper activeStep={activeStep} orientation="vertical">
          {steps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel>
                <Typography variant="h6">{step.label}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {step.description}
                </Typography>
              </StepLabel>
              <StepContent>
                <Box sx={{ mb: 2 }}>
                  {step.content}
                </Box>
                <Box sx={{ mb: 1 }}>
                  <Button
                    variant="contained"
                    onClick={index === steps.length - 1 ? handleComplete : handleNext}
                    disabled={!canProceed()}
                    sx={{ mt: 1, mr: 1 }}
                  >
                    {index === steps.length - 1 ? 'Complete Setup' : 'Continue'}
                  </Button>
                  <Button
                    disabled={index === 0}
                    onClick={handleBack}
                    sx={{ mt: 1, mr: 1 }}
                  >
                    Back
                  </Button>
                </Box>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </CardContent>
    </Card>
  );
};

export default GuidedWorkflow;
