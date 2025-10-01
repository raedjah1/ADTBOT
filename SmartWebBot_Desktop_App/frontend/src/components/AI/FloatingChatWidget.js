import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Avatar,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tooltip,
  Fade,
  Collapse,
  CircularProgress,
  Alert,
  Divider,
  Badge,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  Zoom
} from '@mui/material';
import {
  SmartToy as AIIcon,
  Person as UserIcon,
  Send as SendIcon,
  Close as CloseIcon,
  Minimize as MinimizeIcon,
  Maximize as MaximizeIcon,
  DragHandle as DragIcon,
  Settings as SettingsIcon,
  Speed as SpeedIcon,
  Tune as TuneIcon,
  Chat as ChatIcon,
  Memory as ModelIcon,
  Refresh as RefreshIcon,
  Clear as ClearIcon,
  ContentCopy as CopyIcon,
  VolumeOff as MuteIcon,
  VolumeUp as UnmuteIcon,
  Fullscreen as ExpandIcon,
  FullscreenExit as CollapseIcon,
  PlayArrow as PlayIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import aiService from '../../services/aiService';
import toast from 'react-hot-toast';
import '../../styles/FloatingChatWidget.css';

// Draggable container component
const DraggableContainer = styled(Card)(({ theme, isDragging, isMinimized, position }) => ({
  position: 'fixed',
  top: position?.y || 100,
  right: position?.x || 20,
  width: isMinimized ? 60 : 380,
  height: isMinimized ? 60 : 600,
  maxHeight: isMinimized ? 60 : '80vh',
  zIndex: 1300,
  cursor: isDragging ? 'grabbing' : 'default',
  userSelect: 'none',
  boxShadow: theme.shadows[8],
  borderRadius: theme.spacing(2),
  overflow: 'hidden',
  transition: 'all 0.3s ease',
  border: `1px solid ${theme.palette.divider}`,
  backdropFilter: 'blur(8px)',
  backgroundColor: theme.palette.mode === 'dark' 
    ? 'rgba(18, 18, 18, 0.95)' 
    : 'rgba(255, 255, 255, 0.95)',
  '&:hover': {
    boxShadow: theme.shadows[12],
  }
}));

const HeaderContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(1, 2),
  background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
  cursor: 'grab',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  color: 'white',
  '&:active': {
    cursor: 'grabbing',
  },
}));

const MessagesContainer = styled(Box)({
  height: '400px',
  overflowY: 'auto',
  padding: '8px',
  '&::-webkit-scrollbar': {
    width: '6px',
  },
  '&::-webkit-scrollbar-track': {
    background: '#f1f1f1',
    borderRadius: '3px',
  },
  '&::-webkit-scrollbar-thumb': {
    background: '#888',
    borderRadius: '3px',
  },
  '&::-webkit-scrollbar-thumb:hover': {
    background: '#555',
  },
});

const FloatingChatWidget = ({ isDarkMode = true }) => {
  // Widget state
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [position, setPosition] = useState({ x: 20, y: 100 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Chat state
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "🚀 Hi! I'm your Smart AI Assistant with dual-model power!\n\n✨ **Fast Mode** - Quick responses for simple tasks\n🧠 **Accurate Mode** - Detailed responses for complex workflows\n\n**Quick Commands:**\n• \"Go to Instagram and create a post\"\n• \"Help me login to Facebook\"\n• \"Switch to fast/accurate mode\"\n• \"Clear chat\"\n\nWhat can I help you automate today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(`session_${Date.now()}`);
  
  // AI state
  const [currentModel, setCurrentModel] = useState('gemma2:2b');
  const [modelType, setModelType] = useState('fast');
  const [modelInfo, setModelInfo] = useState(null);
  const [aiStatus, setAiStatus] = useState(null);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  
  // Settings state
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [speedDialOpen, setSpeedDialOpen] = useState(false);
  
  // Refs
  const messagesEndRef = useRef(null);
  const containerRef = useRef(null);
  
  // Model options
  const modelOptions = [
    { 
      value: 'fast', 
      label: '🚀 Fast Mode', 
      model: 'gemma2:2b',
      description: 'Quick responses, great for simple tasks',
      color: 'success'
    },
    { 
      value: 'accurate', 
      label: '🧠 Accurate Mode', 
      model: 'gemma3:4b',
      description: 'Detailed responses, perfect for complex workflows',
      color: 'primary'
    }
  ];

  // Initialize widget
  useEffect(() => {
    checkAIStatus();
    loadCurrentModel();
  }, []);

  // Auto-scroll messages
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      const maxX = window.innerWidth - (isMinimized ? 60 : 380);
      const maxY = window.innerHeight - (isMinimized ? 60 : 600);
      
      setPosition(prev => ({
        x: Math.min(prev.x, maxX),
        y: Math.min(prev.y, maxY)
      }));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isMinimized]);

  const checkAIStatus = async () => {
    try {
      const status = await aiService.getStatus();
      setAiStatus(status);
    } catch (error) {
      console.error('Failed to check AI status:', error);
    }
  };

  const loadCurrentModel = async () => {
    try {
      const response = await fetch('/api/intelligent-chat/current-model');
      if (response.ok) {
        const data = await response.json();
        setCurrentModel(data.current_model);
        setModelInfo(data.model_info);
        
        // Determine model type
        const modelOption = modelOptions.find(opt => opt.model === data.current_model);
        if (modelOption) {
          setModelType(modelOption.value);
        }
      }
    } catch (error) {
      console.error('Failed to load current model:', error);
    }
  };

  const switchModel = async (newModelType) => {
    try {
      const response = await fetch(`/api/intelligent-chat/switch-model?model_type=${newModelType}`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const result = await response.json();
        setCurrentModel(result.model);
        setModelType(newModelType);
        
        // Add system message
        const systemMessage = {
          id: Date.now(),
          type: 'system',
          content: `🔄 Switched to ${newModelType} mode (${result.model})\n💡 ${result.benefits}`,
          timestamp: new Date()
        };
        
        setMessages(prev => [...prev, systemMessage]);
        
        if (!isMuted) {
          toast.success(`Switched to ${newModelType} mode!`);
        }
        
        // Reload model info
        await loadCurrentModel();
        
      } else {
        throw new Error('Failed to switch model');
      }
    } catch (error) {
      console.error('Model switch error:', error);
      toast.error('Failed to switch model');
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    // Handle quick commands
    if (inputMessage.toLowerCase().includes('switch to fast') || inputMessage.toLowerCase() === 'fast mode') {
      await switchModel('fast');
      setInputMessage('');
      return;
    }
    
    if (inputMessage.toLowerCase().includes('switch to accurate') || inputMessage.toLowerCase() === 'accurate mode') {
      await switchModel('accurate');
      setInputMessage('');
      return;
    }
    
    if (inputMessage.toLowerCase() === 'clear chat') {
      setMessages(messages.slice(0, 1));
      setInputMessage('');
      return;
    }

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      // Use intelligent chat API
      const response = await fetch('/api/intelligent-chat/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: currentInput,
          session_id: sessionId,
          current_context: { timestamp: new Date().toISOString() }
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: result.response || 'No response received',
        timestamp: new Date(),
        metadata: {
          type: result.type,
          actions: result.actions,
          execution_plan: result.execution_plan,
          estimated_steps: result.estimated_steps
        }
      };

      setMessages(prev => [...prev, aiResponse]);
      
      // Handle workflow display
      if (result.type === 'execution_plan' && result.execution_plan) {
        // Add workflow as a separate message for better visibility
        const workflowMessage = {
          id: Date.now() + 2,
          type: 'workflow',
          content: '🚀 Workflow Generated!',
          timestamp: new Date(),
          execution_plan: result.execution_plan,
          estimated_steps: result.estimated_steps
        };
        
        setMessages(prev => [...prev, workflowMessage]);
      }
      
      // Update unread count if minimized
      if (isMinimized) {
        setUnreadCount(prev => prev + 1);
      }
      
      // Play notification sound (if not muted)
      if (!isMuted && isMinimized) {
        // You can add a sound notification here
      }

    } catch (error) {
      console.error('Chat error:', error);
      
      const errorResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: `❌ Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  // Dragging handlers
  const handleMouseDown = useCallback((e) => {
    if (isMinimized) return;
    
    setIsDragging(true);
    const rect = containerRef.current.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  }, [isMinimized]);

  const handleMouseMove = useCallback((e) => {
    if (!isDragging) return;
    
    e.preventDefault();
    const newX = window.innerWidth - (e.clientX - dragOffset.x) - (isMinimized ? 60 : 380);
    const newY = e.clientY - dragOffset.y;
    
    const maxX = window.innerWidth - (isMinimized ? 60 : 380);
    const maxY = window.innerHeight - (isMinimized ? 60 : 600);
    
    setPosition({
      x: Math.max(0, Math.min(newX, maxX)),
      y: Math.max(0, Math.min(newY, maxY))
    });
  }, [isDragging, dragOffset, isMinimized]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, handleMouseMove, handleMouseUp]);

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
    if (isMinimized) {
      setUnreadCount(0);
    }
  };

  const closeWidget = () => {
    setIsOpen(false);
    setIsMinimized(false);
  };

  const copyMessage = (content) => {
    navigator.clipboard.writeText(content);
    toast.success('Message copied!');
  };

  const clearChat = () => {
    setMessages(messages.slice(0, 1));
    toast.success('Chat cleared!');
  };

  const handleExecuteWorkflow = async (executionPlan) => {
    try {
      const response = await fetch('/api/intelligent-chat/workflow/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          confirm_execution: true
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      const statusMessage = {
        id: Date.now(),
        type: 'system',
        content: `🚀 Workflow execution started!\n${result.message}`,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, statusMessage]);
      
      if (!isMuted) {
        toast.success('Workflow execution started!');
      }

    } catch (error) {
      console.error('Workflow execution error:', error);
      
      const errorMessage = {
        id: Date.now(),
        type: 'ai',
        content: `❌ Failed to execute workflow: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Failed to execute workflow');
    }
  };

  // Speed dial actions
  const speedDialActions = [
    {
      icon: <ClearIcon />,
      name: 'Clear Chat',
      onClick: clearChat
    },
    {
      icon: <RefreshIcon />,
      name: 'Refresh Status',
      onClick: checkAIStatus
    },
    {
      icon: isMuted ? <VolumeUp /> : <MuteIcon />,
      name: isMuted ? 'Unmute' : 'Mute',
      onClick: () => setIsMuted(!isMuted)
    },
    {
      icon: <SettingsIcon />,
      name: 'Settings',
      onClick: () => setSettingsOpen(true)
    }
  ];

  // Chat FAB when closed
  if (!isOpen) {
    return (
      <Zoom in={true}>
        <Badge
          badgeContent={unreadCount}
          color="error"
          sx={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1300 }}
        >
          <IconButton
            onClick={() => setIsOpen(true)}
            sx={{
              width: 56,
              height: 56,
              bgcolor: 'primary.main',
              color: 'white',
              '&:hover': {
                bgcolor: 'primary.dark',
              },
              boxShadow: 8,
            }}
          >
            <ChatIcon />
          </IconButton>
        </Badge>
      </Zoom>
    );
  }

  return (
    <>
      <DraggableContainer
        ref={containerRef}
        isDragging={isDragging}
        isMinimized={isMinimized}
        position={position}
        elevation={8}
      >
        {/* Header */}
        <HeaderContainer onMouseDown={handleMouseDown}>
          <Box display="flex" alignItems="center" gap={1}>
            <DragIcon sx={{ cursor: 'grab' }} />
            <AIIcon />
            {!isMinimized && (
              <>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Smart AI
                </Typography>
                <Chip
                  label={modelType}
                  size="small"
                  color={modelOptions.find(opt => opt.value === modelType)?.color}
                  sx={{ color: 'white', fontWeight: 500 }}
                />
              </>
            )}
          </Box>
          
          <Box display="flex" alignItems="center">
            {!isMinimized && (
              <>
                <Tooltip title="Model Settings">
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation();
                      setSettingsOpen(true);
                    }}
                    sx={{ color: 'white' }}
                  >
                    <TuneIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title={isExpanded ? "Collapse" : "Expand"}>
                  <IconButton
                    size="small"
                    onClick={() => setIsExpanded(!isExpanded)}
                    sx={{ color: 'white' }}
                  >
                    {isExpanded ? <CollapseIcon /> : <ExpandIcon />}
                  </IconButton>
                </Tooltip>
              </>
            )}
            
            <Tooltip title={isMinimized ? "Restore" : "Minimize"}>
              <IconButton
                size="small"
                onClick={toggleMinimize}
                sx={{ color: 'white' }}
              >
                {isMinimized ? <MaximizeIcon /> : <MinimizeIcon />}
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Close">
              <IconButton
                size="small"
                onClick={closeWidget}
                sx={{ color: 'white' }}
              >
                <CloseIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </HeaderContainer>

        {/* Content */}
        <Collapse in={!isMinimized}>
          <CardContent sx={{ p: 0, height: isExpanded ? '500px' : '400px' }}>
            {/* Status Bar */}
            <Box sx={{ p: 1, bgcolor: 'background.paper', borderBottom: 1, borderColor: 'divider' }}>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Typography variant="caption" color="textSecondary">
                  {aiStatus?.is_initialized ? '🟢 Connected' : '🔴 Disconnected'} • {currentModel}
                </Typography>
                <Chip
                  label={`${messages.length - 1} messages`}
                  size="small"
                  variant="outlined"
                />
              </Box>
            </Box>

            {/* Messages */}
            <MessagesContainer sx={{ height: isExpanded ? '420px' : '320px' }}>
              {messages.map((message) => (
                <Fade in={true} key={message.id}>
                  <Box
                    display="flex"
                    justifyContent={message.type === 'user' ? 'flex-end' : 'flex-start'}
                    mb={1}
                  >
                    <Box
                      sx={{
                        maxWidth: '85%',
                        p: 1.5,
                        borderRadius: 2,
                        bgcolor: message.type === 'user' 
                          ? 'primary.main'
                          : message.type === 'system'
                          ? 'warning.light'
                          : 'background.paper',
                        color: message.type === 'user' ? 'white' : 'text.primary',
                        border: message.type !== 'user' ? 1 : 0,
                        borderColor: 'divider',
                        position: 'relative',
                        '&:hover .copy-btn': {
                          opacity: 1
                        }
                      }}
                    >
                      <Box display="flex" alignItems="flex-start" gap={1}>
                        {message.type !== 'user' && (
                          <Avatar sx={{ width: 24, height: 24, bgcolor: message.type === 'system' ? 'warning.main' : 'secondary.main' }}>
                            {message.type === 'system' ? <SettingsIcon sx={{ fontSize: 14 }} /> : <AIIcon sx={{ fontSize: 14 }} />}
                          </Avatar>
                        )}
                        <Box flex={1}>
                          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', fontSize: '0.85rem' }}>
                            {message.content}
                          </Typography>
                          
                          {/* Workflow Display */}
                          {message.type === 'workflow' && message.execution_plan && (
                            <Card sx={{ mt: 1, bgcolor: 'background.default' }}>
                              <CardContent sx={{ p: 1.5 }}>
                                <Typography variant="subtitle2" sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <PlayIcon sx={{ fontSize: 16 }} />
                                  Execution Plan ({message.execution_plan.length} steps)
                                </Typography>
                                
                                <Box sx={{ maxHeight: 200, overflowY: 'auto' }}>
                                  {message.execution_plan.map((step, index) => (
                                    <Box key={index} sx={{ display: 'flex', gap: 1, mb: 1, alignItems: 'flex-start' }}>
                                      <Chip 
                                        label={index + 1} 
                                        size="small" 
                                        color="primary" 
                                        sx={{ minWidth: 28, height: 20, '& .MuiChip-label': { fontSize: '0.7rem', px: 0.5 } }}
                                      />
                                      <Box flex={1}>
                                        <Typography variant="caption" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                                          {step.description || step.action || step.type}
                                        </Typography>
                                        {step.parameters && (
                                          <Typography variant="caption" color="textSecondary" sx={{ display: 'block', fontSize: '0.7rem' }}>
                                            {step.parameters.url && `URL: ${step.parameters.url.substring(0, 30)}...`}
                                            {step.parameters.goal && `Goal: ${step.parameters.goal.substring(0, 40)}...`}
                                          </Typography>
                                        )}
                                      </Box>
                                    </Box>
                                  ))}
                                </Box>
                                
                                <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                                  <Button
                                    size="small"
                                    variant="contained"
                                    color="primary"
                                    startIcon={<PlayIcon />}
                                    onClick={() => handleExecuteWorkflow(message.execution_plan)}
                                    sx={{ fontSize: '0.7rem', py: 0.5 }}
                                  >
                                    Execute
                                  </Button>
                                  <Button
                                    size="small"
                                    variant="outlined"
                                    onClick={() => copyMessage(JSON.stringify(message.execution_plan, null, 2))}
                                    sx={{ fontSize: '0.7rem', py: 0.5 }}
                                  >
                                    Copy Plan
                                  </Button>
                                </Box>
                              </CardContent>
                            </Card>
                          )}
                          
                          <Typography variant="caption" color="textSecondary" sx={{ mt: 0.5, display: 'block' }}>
                            {message.timestamp.toLocaleTimeString()}
                          </Typography>
                        </Box>
                        <IconButton
                          size="small"
                          className="copy-btn"
                          onClick={() => copyMessage(message.content)}
                          sx={{ 
                            opacity: 0, 
                            transition: 'opacity 0.2s',
                            color: message.type === 'user' ? 'white' : 'text.secondary'
                          }}
                        >
                          <CopyIcon sx={{ fontSize: 14 }} />
                        </IconButton>
                      </Box>
                    </Box>
                  </Box>
                </Fade>
              ))}
              
              {isLoading && (
                <Box display="flex" justifyContent="flex-start" mb={1}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p: 1.5, bgcolor: 'background.paper', borderRadius: 2, border: 1, borderColor: 'divider' }}>
                    <CircularProgress size={16} />
                    <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.85rem' }}>
                      AI is thinking...
                    </Typography>
                  </Box>
                </Box>
              )}
              <div ref={messagesEndRef} />
            </MessagesContainer>

            {/* Input */}
            <Box sx={{ p: 1.5, borderTop: 1, borderColor: 'divider' }}>
              <Box display="flex" gap={1}>
                <TextField
                  fullWidth
                  size="small"
                  placeholder="Type your message... (try 'switch to fast mode')"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  disabled={!aiStatus?.is_initialized || isLoading}
                  sx={{ '& .MuiOutlinedInput-root': { borderRadius: 3 } }}
                />
                <IconButton
                  color="primary"
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim() || isLoading || !aiStatus?.is_initialized}
                >
                  <SendIcon />
                </IconButton>
              </Box>
            </Box>
          </CardContent>
        </Collapse>

        {/* Speed Dial (only when not minimized) */}
        {!isMinimized && (
          <SpeedDial
            ariaLabel="Chat actions"
            sx={{ position: 'absolute', bottom: 80, right: 16 }}
            icon={<SpeedDialIcon />}
            open={speedDialOpen}
            onClose={() => setSpeedDialOpen(false)}
            onOpen={() => setSpeedDialOpen(true)}
            direction="up"
            FabProps={{ size: 'small', color: 'secondary' }}
          >
            {speedDialActions.map((action) => (
              <SpeedDialAction
                key={action.name}
                icon={action.icon}
                tooltipTitle={action.name}
                onClick={() => {
                  action.onClick();
                  setSpeedDialOpen(false);
                }}
              />
            ))}
          </SpeedDial>
        )}
      </DraggableContainer>

      {/* Settings Dialog */}
      <Dialog open={settingsOpen} onClose={() => setSettingsOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <ModelIcon />
            AI Model Settings
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box mb={3}>
            <Alert severity="info" sx={{ mb: 2 }}>
              Switch between Fast mode for quick responses or Accurate mode for detailed analysis.
            </Alert>
            
            <FormControl fullWidth>
              <InputLabel>AI Model</InputLabel>
              <Select
                value={modelType}
                label="AI Model"
                onChange={(e) => switchModel(e.target.value)}
                disabled={isLoading}
              >
                {modelOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    <Box>
                      <Typography variant="body1">{option.label}</Typography>
                      <Typography variant="caption" color="textSecondary">
                        {option.description}
                      </Typography>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {modelInfo && (
              <Box mt={2} p={2} bgcolor="background.paper" borderRadius={1} border={1} borderColor="divider">
                <Typography variant="h6" gutterBottom>Current Model Info</Typography>
                <Typography variant="body2"><strong>Model:</strong> {currentModel}</Typography>
                <Typography variant="body2"><strong>Type:</strong> {modelInfo.type}</Typography>
                <Typography variant="body2"><strong>Size:</strong> {modelInfo.size}</Typography>
                <Typography variant="body2"><strong>Description:</strong> {modelInfo.description}</Typography>
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSettingsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default FloatingChatWidget;
