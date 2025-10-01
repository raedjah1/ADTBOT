import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  CircularProgress,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Card,
  CardContent,
  Divider,
  Tooltip,
  IconButton,
  Badge
} from '@mui/material';
import {
  Send as SendIcon,
  SmartToy as AIIcon,
  Person as PersonIcon,
  Security as SecurityIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  AutoAwesome as MagicIcon,
  Search as SearchIcon,
  Link as LinkIcon,
  VpnKey as KeyIcon,
  Clear as ClearIcon
} from '@mui/icons-material';

const IntelligentChatInterface = ({ 
  sessionId, 
  currentUrl, 
  onWorkflowExecute, 
  onCredentialsRequired,
  isDarkMode = true 
}) => {
  // Chat state
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "🤖 Hi! I'm your intelligent AI assistant. I can help you automate complex workflows with natural language commands.\n\nTry saying things like:\n• \"Go to Instagram and create a post\"\n• \"Login to my Facebook account\"\n• \"Market my product on social media\"\n• \"Find the contact form and fill it out\"\n\nI'll handle authentication, URL finding, and complex multi-step processes automatically!",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [sessionStatus, setSessionStatus] = useState(null);
  
  // Workflow state
  const [currentWorkflow, setCurrentWorkflow] = useState(null);
  const [executionPlan, setExecutionPlan] = useState(null);
  const [workflowStatus, setWorkflowStatus] = useState('idle'); // idle, planned, executing, completed, error
  
  // Credential state
  const [credentialRequest, setCredentialRequest] = useState(null);
  const [credentialDialog, setCredentialDialog] = useState(false);
  const [credentials, setCredentials] = useState({});
  
  // UI state
  const [suggestions] = useState([
    "Go to Instagram",
    "Login to Facebook",
    "Create a social media post",
    "Find contact information",
    "Fill out a form",
    "Search for products",
    "Market my business online"
  ]);
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  
  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);
  
  // Load session status
  useEffect(() => {
    loadSessionStatus();
  }, [sessionId]);
  
  const loadSessionStatus = async () => {
    try {
      const response = await fetch(`/api/intelligent-chat/session/${sessionId}/status`);
      if (response.ok) {
        const status = await response.json();
        setSessionStatus(status);
      }
    } catch (error) {
      console.error('Failed to load session status:', error);
    }
  };
  
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isProcessing) return;
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsProcessing(true);
    
    try {
      const response = await fetch('/api/intelligent-chat/command', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId,
          current_context: {
            url: currentUrl,
            timestamp: new Date().toISOString()
          }
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      // Handle different response types
      await handleChatResponse(result);
      
    } catch (error) {
      console.error('Chat error:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: `❌ Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleChatResponse = async (result) => {
    const aiMessage = {
      id: Date.now() + 1,
      type: 'ai',
      content: result.response,
      timestamp: new Date(),
      metadata: {
        type: result.type,
        session_id: result.session_id,
        actions: result.actions,
        estimated_steps: result.estimated_steps
      }
    };
    
    setMessages(prev => [...prev, aiMessage]);
    
    // Handle different response types
    switch (result.type) {
      case 'execution_plan':
        setExecutionPlan(result.execution_plan);
        setWorkflowStatus('planned');
        break;
        
      case 'credential_request':
        setCredentialRequest(result.credential_request);
        setCredentialDialog(true);
        break;
        
      case 'execution_complete':
        setWorkflowStatus('completed');
        if (onWorkflowExecute) {
          onWorkflowExecute(result);
        }
        break;
        
      case 'execution_error':
        setWorkflowStatus('error');
        break;
        
      case 'url_request':
        // Handle URL request - could show a dialog or input field
        break;
        
      default:
        // Handle simple responses
        break;
    }
  };
  
  const handleExecuteWorkflow = async () => {
    if (!executionPlan) return;
    
    setWorkflowStatus('executing');
    
    try {
      const response = await fetch('/api/intelligent-chat/workflow/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          confirm_execution: true
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      const statusMessage = {
        id: Date.now(),
        type: 'ai',
        content: `🚀 ${result.message}`,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, statusMessage]);
      
    } catch (error) {
      console.error('Workflow execution error:', error);
      setWorkflowStatus('error');
      
      const errorMessage = {
        id: Date.now(),
        type: 'ai',
        content: `❌ Failed to execute workflow: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    }
  };
  
  const handleSubmitCredentials = async () => {
    try {
      const response = await fetch('/api/intelligent-chat/credentials/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          request_id: credentialRequest?.request_id,
          credentials: credentials
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      setCredentialDialog(false);
      setCredentials({});
      setCredentialRequest(null);
      
      const successMessage = {
        id: Date.now(),
        type: 'ai',
        content: `✅ Credentials received! Continuing with your request...`,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, successMessage]);
      
      if (onCredentialsRequired) {
        onCredentialsRequired(result);
      }
      
    } catch (error) {
      console.error('Credential submission error:', error);
      
      const errorMessage = {
        id: Date.now(),
        type: 'ai',
        content: `❌ Failed to submit credentials: ${error.message}`,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    }
  };
  
  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
    inputRef.current?.focus();
  };
  
  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };
  
  const getMessageIcon = (message) => {
    if (message.type === 'user') {
      return <PersonIcon />;
    } else if (message.isError) {
      return <ErrorIcon color="error" />;
    } else {
      return <AIIcon color="primary" />;
    }
  };
  
  const getWorkflowStatusColor = () => {
    switch (workflowStatus) {
      case 'planned': return 'info';
      case 'executing': return 'warning';
      case 'completed': return 'success';
      case 'error': return 'error';
      default: return 'default';
    }
  };
  
  const getWorkflowStatusIcon = () => {
    switch (workflowStatus) {
      case 'planned': return <InfoIcon />;
      case 'executing': return <CircularProgress size={16} />;
      case 'completed': return <CheckIcon />;
      case 'error': return <ErrorIcon />;
      default: return <MagicIcon />;
    }
  };
  
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <MagicIcon color="primary" />
          Intelligent AI Assistant
          {workflowStatus !== 'idle' && (
            <Chip
              icon={getWorkflowStatusIcon()}
              label={workflowStatus.toUpperCase()}
              color={getWorkflowStatusColor()}
              size="small"
              sx={{ ml: 2 }}
            />
          )}
        </Typography>
        {sessionStatus && (
          <Typography variant="caption" color="textSecondary">
            Session: {sessionId} • Credentials: {sessionStatus.credentials_stored}
          </Typography>
        )}
      </Box>
      
      {/* Messages */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
        <List>
          {messages.map((message) => (
            <ListItem key={message.id} sx={{ alignItems: 'flex-start' }}>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: message.type === 'user' ? 'primary.main' : 'secondary.main' }}>
                  {getMessageIcon(message)}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Typography
                    variant="body1"
                    sx={{
                      whiteSpace: 'pre-wrap',
                      color: message.isError ? 'error.main' : 'inherit'
                    }}
                  >
                    {message.content}
                  </Typography>
                }
                secondary={
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="caption" color="textSecondary">
                      {message.timestamp.toLocaleTimeString()}
                    </Typography>
                    {message.metadata?.actions && (
                      <Box sx={{ mt: 1 }}>
                        {message.metadata.actions.map((action, index) => (
                          <Chip
                            key={index}
                            label={action}
                            size="small"
                            variant="outlined"
                            sx={{ mr: 1, mb: 0.5 }}
                          />
                        ))}
                      </Box>
                    )}
                  </Box>
                }
              />
            </ListItem>
          ))}
          
          {/* Execution Plan Display */}
          {executionPlan && (
            <ListItem>
              <ListItemText
                primary={
                  <Card variant="outlined" sx={{ mt: 1 }}>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        <PlayIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                        Execution Plan
                      </Typography>
                      
                      <Stepper orientation="vertical">
                        {executionPlan.map((step, index) => (
                          <Step key={index} active={true}>
                            <StepLabel>{step.description || step.action}</StepLabel>
                            <StepContent>
                              <Typography variant="body2" color="textSecondary">
                                Action: {step.action}
                                {step.url && ` | URL: ${step.url}`}
                                {step.selector && ` | Element: ${step.selector}`}
                              </Typography>
                            </StepContent>
                          </Step>
                        ))}
                      </Stepper>
                      
                      <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                        <Button
                          variant="contained"
                          startIcon={<PlayIcon />}
                          onClick={handleExecuteWorkflow}
                          disabled={workflowStatus === 'executing'}
                        >
                          {workflowStatus === 'executing' ? 'Executing...' : 'Execute Plan'}
                        </Button>
                        <Button
                          variant="outlined"
                          onClick={() => {
                            setExecutionPlan(null);
                            setWorkflowStatus('idle');
                          }}
                        >
                          Cancel
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                }
              />
            </ListItem>
          )}
          
          {isProcessing && (
            <ListItem>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: 'secondary.main' }}>
                  <CircularProgress size={24} />
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Typography variant="body1" color="textSecondary">
                    AI is thinking...
                  </Typography>
                }
              />
            </ListItem>
          )}
        </List>
        <div ref={messagesEndRef} />
      </Box>
      
      {/* Quick Suggestions */}
      {messages.length <= 1 && (
        <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
          <Typography variant="subtitle2" gutterBottom>
            Quick Suggestions:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {suggestions.map((suggestion, index) => (
              <Chip
                key={index}
                label={suggestion}
                variant="outlined"
                size="small"
                onClick={() => handleSuggestionClick(suggestion)}
                sx={{ cursor: 'pointer' }}
              />
            ))}
          </Box>
        </Box>
      )}
      
      {/* Input */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            ref={inputRef}
            fullWidth
            multiline
            maxRows={4}
            placeholder="Tell me what you want to do... (e.g., 'Go to Instagram and create a post')"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isProcessing}
            variant="outlined"
            size="small"
          />
          <Button
            variant="contained"
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isProcessing}
            sx={{ minWidth: 'auto', px: 2 }}
          >
            <SendIcon />
          </Button>
        </Box>
      </Box>
      
      {/* Credential Dialog */}
      <Dialog
        open={credentialDialog}
        onClose={() => setCredentialDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <KeyIcon color="primary" />
            Authentication Required
          </Box>
        </DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            {credentialRequest?.prompt_message || 'Please provide your credentials to continue.'}
          </Alert>
          
          {credentialRequest?.required_fields?.map((field) => (
            <TextField
              key={field}
              fullWidth
              label={field.charAt(0).toUpperCase() + field.slice(1)}
              type={field.includes('password') ? 'password' : 'text'}
              value={credentials[field] || ''}
              onChange={(e) => setCredentials(prev => ({
                ...prev,
                [field]: e.target.value
              }))}
              margin="normal"
              variant="outlined"
            />
          ))}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCredentialDialog(false)}>
            Cancel
          </Button>
          <Button
            onClick={handleSubmitCredentials}
            variant="contained"
            disabled={!credentialRequest?.required_fields?.every(field => credentials[field])}
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default IntelligentChatInterface;
