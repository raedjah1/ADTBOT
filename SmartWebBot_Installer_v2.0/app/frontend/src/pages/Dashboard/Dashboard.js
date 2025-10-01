import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  LinearProgress,
  IconButton,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab,
  Zoom,
  Paper,
  Alert,
  Tabs,
  Tab
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  SmartToy as AIIcon,
  School as GuideIcon,
  Add as AddIcon,
  AutoAwesome as MagicIcon,
  Security as SecurityIcon,
  Build as BuildIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import AIAssistant from '../../components/AI/AIAssistant';
import GuidedWorkflow from '../../components/GuidedWorkflow/GuidedWorkflow';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import toast from 'react-hot-toast';

import { getBotStatus, startBot, stopBot, getPerformanceReport } from '../../services/api';

const Dashboard = ({ backendStatus, botStatus, isDarkMode }) => {
  const [performanceData, setPerformanceData] = useState([]);
  const [recentTasks, setRecentTasks] = useState([]);
  const [stats, setStats] = useState({
    totalTasks: 0,
    successfulTasks: 0,
    averageDuration: 0,
    successRate: 0,
  });
  
  // New UI state
  const [showAIAssistant, setShowAIAssistant] = useState(false);
  const [showGuidedSetup, setShowGuidedSetup] = useState(false);
  const [showQuickStart, setShowQuickStart] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [userLevel, setUserLevel] = useState('beginner'); // beginner, intermediate, expert

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      const report = await getPerformanceReport();
      
      // Mock data for demonstration
      const mockPerformanceData = [
        { time: '00:00', tasks: 0, success: 0 },
        { time: '04:00', tasks: 2, success: 2 },
        { time: '08:00', tasks: 5, success: 4 },
        { time: '12:00', tasks: 8, success: 7 },
        { time: '16:00', tasks: 12, success: 11 },
        { time: '20:00', tasks: 15, success: 14 },
      ];

      const mockRecentTasks = [
        {
          id: 1,
          name: 'Login to Gmail',
          status: 'completed',
          duration: '2.3s',
          timestamp: new Date(Date.now() - 300000).toISOString(),
        },
        {
          id: 2,
          name: 'Fill Contact Form',
          status: 'completed',
          duration: '4.1s',
          timestamp: new Date(Date.now() - 600000).toISOString(),
        },
        {
          id: 3,
          name: 'Extract Product Data',
          status: 'running',
          duration: '12.5s',
          timestamp: new Date(Date.now() - 900000).toISOString(),
        },
      ];

      setPerformanceData(mockPerformanceData);
      setRecentTasks(mockRecentTasks);
      setStats({
        totalTasks: 15,
        successfulTasks: 14,
        averageDuration: 3.2,
        successRate: 93.3,
      });

    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  const handleStartBot = async () => {
    try {
      await startBot();
      toast.success('Bot started successfully!');
    } catch (error) {
      toast.error('Failed to start bot');
    }
  };

  const handleStopBot = async () => {
    try {
      await stopBot();
      toast.success('Bot stopped');
    } catch (error) {
      toast.error('Failed to stop bot');
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckIcon color="success" />;
      case 'running':
        return <ScheduleIcon color="warning" />;
      case 'failed':
        return <ErrorIcon color="error" />;
      default:
        return <ScheduleIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'running':
        return 'warning';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  // New handler functions
  const handleAITaskSuggestion = (taskData) => {
    toast.success('Task suggestion received! Opening Task Builder...');
    setShowAIAssistant(false);
    // TODO: Navigate to task builder with pre-filled data
  };

  const handleSecurityAdvice = (adviceType) => {
    if (adviceType === 'security_testing') {
      toast.info('Opening Security Testing module...');
      setShowAIAssistant(false);
      // TODO: Navigate to security testing
    }
  };

  const handleWorkflowComplete = (workflowData) => {
    toast.success('Workflow configured! Redirecting to Task Builder...');
    setShowGuidedSetup(false);
    // TODO: Navigate to task builder with workflow data
  };

  const quickStartOptions = [
    {
      title: '🌐 Web Automation',
      description: 'Automate website interactions, form filling, and navigation',
      difficulty: 'Beginner',
      time: '5 min',
      color: '#4CAF50',
      action: () => setShowGuidedSetup(true)
    },
    {
      title: '📊 Data Extraction',
      description: 'Scrape and extract data from websites automatically',
      difficulty: 'Beginner',
      time: '10 min',
      color: '#2196F3',
      action: () => setShowGuidedSetup(true)
    },
    {
      title: '🤖 AI Assistant',
      description: 'Get help from AI to build your automation tasks',
      difficulty: 'Any Level',
      time: '2 min',
      color: '#9C27B0',
      action: () => setShowAIAssistant(true)
    },
    {
      title: '⚡ Task Builder',
      description: 'Build custom automation workflows with drag & drop',
      difficulty: 'Beginner',
      time: '3 min',
      color: '#FF5722',
      action: () => {
        setShowQuickStart(false);
        // TODO: Navigate to Task Builder
        toast.info('Opening Task Builder...');
      }
    }
  ];

  return (
    <Box sx={{ height: '100%', overflow: 'auto' }}>
      {/* Welcome Header */}
      <Box sx={{ mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
              Welcome back! 👋
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Your intelligent RMA processing command center
            </Typography>
          </Box>
          <Box display="flex" gap={2}>
            <Button
              variant="outlined"
              startIcon={<GuideIcon />}
              onClick={() => setShowGuidedSetup(true)}
              sx={{ borderRadius: 2 }}
            >
              Guided Setup
            </Button>
            <Button
              variant="contained"
              startIcon={<MagicIcon />}
              onClick={() => setShowQuickStart(true)}
              sx={{ 
                borderRadius: 2,
                background: isDarkMode 
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : 'linear-gradient(135deg, #1976D2 0%, #1565C0 100%)'
              }}
            >
              Quick Start
            </Button>
          </Box>
        </Box>
      </Box>

      {/* Quick Start Banner for New Users */}
      {stats.totalTasks === 0 && (
        <Alert 
          severity="info" 
          sx={{ mb: 3, borderRadius: 2 }}
          action={
            <Button 
              color="inherit" 
              size="small" 
              onClick={() => setShowQuickStart(true)}
            >
              Get Started
            </Button>
          }
        >
          <Typography variant="subtitle1" fontWeight="medium">
            🚀 Ready to automate? Let's get you started!
          </Typography>
          <Typography variant="body2">
            Use our guided setup or AI assistant to create your first automation task.
          </Typography>
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Quick Stats */}
        <Grid item xs={12} md={3}>
          <Card sx={{ 
            height: '100%',
            transition: 'all 0.3s ease',
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: isDarkMode 
                ? '0 8px 25px rgba(102, 126, 234, 0.3)'
                : '0 8px 25px rgba(25, 118, 210, 0.15)',
            }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <TrendingUpIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {stats.totalTasks}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Tasks
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card sx={{ 
            height: '100%',
            transition: 'all 0.3s ease',
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: isDarkMode 
                ? '0 8px 25px rgba(102, 126, 234, 0.3)'
                : '0 8px 25px rgba(25, 118, 210, 0.15)',
            }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <CheckIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {stats.successRate}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Success Rate
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card sx={{ 
            height: '100%',
            transition: 'all 0.3s ease',
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: isDarkMode 
                ? '0 8px 25px rgba(102, 126, 234, 0.3)'
                : '0 8px 25px rgba(25, 118, 210, 0.15)',
            }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <SpeedIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {stats.averageDuration}s
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Avg Duration
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card sx={{ 
            height: '100%',
            transition: 'all 0.3s ease',
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: isDarkMode 
                ? '0 8px 25px rgba(102, 126, 234, 0.3)'
                : '0 8px 25px rgba(25, 118, 210, 0.15)',
            }
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Chip
                  label={backendStatus === 'connected' ? 'Online' : 'Offline'}
                  color={backendStatus === 'connected' ? 'success' : 'error'}
                  sx={{ fontWeight: 600 }}
                />
              </Box>
              <Typography variant="body2" color="text.secondary">
                System Status
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Bot Control */}
        <Grid item xs={12} md={8}>
          <Card sx={{ 
            height: 400,
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
          }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Performance Overview
                </Typography>
                <IconButton onClick={loadDashboardData}>
                  <RefreshIcon />
                </IconButton>
              </Box>
              
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={performanceData}>
                  <CartesianGrid 
                    strokeDasharray="3 3" 
                    stroke={isDarkMode ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)"} 
                  />
                  <XAxis 
                    dataKey="time" 
                    stroke={isDarkMode ? "rgba(255,255,255,0.5)" : "rgba(0,0,0,0.7)"} 
                  />
                  <YAxis 
                    stroke={isDarkMode ? "rgba(255,255,255,0.5)" : "rgba(0,0,0,0.7)"} 
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: isDarkMode ? '#2d2d2d' : '#ffffff', 
                      border: isDarkMode 
                        ? '1px solid rgba(255,255,255,0.1)'
                        : '1px solid rgba(0,0,0,0.1)',
                      borderRadius: '8px',
                      color: isDarkMode ? '#ffffff' : '#000000'
                    }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="tasks" 
                    stroke={isDarkMode ? "#667eea" : "#1976D2"} 
                    strokeWidth={2}
                    name="Total Tasks"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="success" 
                    stroke={isDarkMode ? "#4caf50" : "#059669"} 
                    strokeWidth={2}
                    name="Successful"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Tasks */}
        <Grid item xs={12} md={4}>
          <Card sx={{ 
            height: 400,
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
          }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Recent Tasks
              </Typography>
              
              <List sx={{ maxHeight: 300, overflow: 'auto' }}>
                {recentTasks.map((task, index) => (
                  <React.Fragment key={task.id}>
                    <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                      <ListItemAvatar>
                        <Avatar sx={{ width: 32, height: 32 }}>
                          {getStatusIcon(task.status)}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={task.name}
                        secondary={
                          <Box>
                            <Chip
                              label={task.status}
                              color={getStatusColor(task.status)}
                              size="small"
                              sx={{ mr: 1, mb: 0.5 }}
                            />
                            <Typography variant="caption" display="block">
                              Duration: {task.duration}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < recentTasks.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Card sx={{ 
            backgroundColor: isDarkMode ? '#161B22' : '#FFFFFF',
            border: isDarkMode ? '1px solid #30363D' : '1px solid #E2E8F0',
          }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Quick Actions
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={<PlayIcon />}
                  onClick={handleStartBot}
                  disabled={botStatus.isRunning}
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
                    },
                  }}
                >
                  Start Bot
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<StopIcon />}
                  onClick={handleStopBot}
                  disabled={!botStatus.isRunning}
                >
                  Stop Bot
                </Button>
                
                <Button variant="outlined">
                  Create New Task
                </Button>
                
                <Button variant="outlined">
                  View All Results
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Floating Action Buttons */}
      <Box sx={{ position: 'fixed', bottom: 24, right: 24, display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Zoom in={!showAIAssistant}>
          <Fab 
            color="primary" 
            onClick={() => setShowAIAssistant(true)}
            sx={{ 
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)',
              }
            }}
          >
            <AIIcon />
          </Fab>
        </Zoom>
      </Box>

      {/* AI Assistant Dialog */}
      <Dialog 
        open={showAIAssistant} 
        onClose={() => setShowAIAssistant(false)}
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: { borderRadius: 3, minHeight: '70vh' }
        }}
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">🤖 AI Assistant</Typography>
            <IconButton onClick={() => setShowAIAssistant(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent sx={{ p: 0 }}>
          <AIAssistant 
            onTaskSuggestion={handleAITaskSuggestion}
            onSecurityAdvice={handleSecurityAdvice}
            onActionGenerate={() => {}}
            isDarkMode={isDarkMode}
          />
        </DialogContent>
      </Dialog>

      {/* Guided Setup Dialog */}
      <Dialog 
        open={showGuidedSetup} 
        onClose={() => setShowGuidedSetup(false)}
        maxWidth="lg" 
        fullWidth
        PaperProps={{
          sx: { borderRadius: 3, minHeight: '80vh' }
        }}
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">🎯 Guided Workflow Setup</Typography>
            <IconButton onClick={() => setShowGuidedSetup(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <GuidedWorkflow 
            onWorkflowComplete={handleWorkflowComplete}
            userLevel={userLevel}
            isDarkMode={isDarkMode}
          />
        </DialogContent>
      </Dialog>

      {/* Quick Start Dialog */}
      <Dialog 
        open={showQuickStart} 
        onClose={() => setShowQuickStart(false)}
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: { borderRadius: 3 }
        }}
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">🚀 Quick Start</Typography>
            <IconButton onClick={() => setShowQuickStart(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1" gutterBottom sx={{ mb: 3 }}>
            Choose what you'd like to do with SmartWebBot:
          </Typography>
          
          <Grid container spacing={2}>
            {quickStartOptions.map((option, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card 
                  sx={{ 
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': { 
                      transform: 'translateY(-2px)',
                      boxShadow: 4
                    }
                  }}
                  onClick={() => {
                    setShowQuickStart(false);
                    option.action();
                  }}
                >
                  <CardContent>
                    <Box display="flex" alignItems="center" gap={2} mb={1}>
                      <Box 
                        sx={{ 
                          width: 40, 
                          height: 40, 
                          borderRadius: '50%', 
                          bgcolor: option.color,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'white'
                        }}
                      >
                        {option.title.includes('🌐') && <BuildIcon />}
                        {option.title.includes('📊') && <TrendingUpIcon />}
                        {option.title.includes('🤖') && <AIIcon />}
                        {option.title.includes('⚡') && <BuildIcon />}
                      </Box>
                      <Box>
                        <Typography variant="h6" fontWeight="medium">
                          {option.title}
                        </Typography>
                        <Box display="flex" gap={1}>
                          <Chip label={option.difficulty} size="small" />
                          <Chip label={option.time} size="small" variant="outlined" />
                        </Box>
                      </Box>
                    </Box>
                    <Typography variant="body2" color="textSecondary">
                      {option.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowQuickStart(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Dashboard;
