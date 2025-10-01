import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Avatar,
  Chip,
  Fade,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton,
  Tooltip,
  Alert,
  Snackbar
} from '@mui/material';
import {
  SmartToy as AIIcon,
  Person as UserIcon,
  LightbulbOutlined as SuggestionIcon,
  Security as SecurityIcon,
  AutoAwesome as MagicIcon,
  Send as SendIcon,
  Clear as ClearIcon,
  ContentCopy as CopyIcon,
  PlayArrow as RunIcon,
  Error as ErrorIcon,
  CheckCircle as SuccessIcon
} from '@mui/icons-material';
import aiService from '../../services/aiService';
import toast from 'react-hot-toast';

const AIAssistant = ({ onTaskSuggestion, onSecurityAdvice, onActionGenerate, isDarkMode = true }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "👋 Hi! I'm your AI Assistant powered by Ollama. I can help you:\n\n• Build automation tasks with natural language\n• Suggest security tests for your targets\n• Generate smart actions and selectors\n• Provide ethical hacking guidance\n• Analyze websites and suggest improvements\n\nWhat would you like to do today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [aiStatus, setAiStatus] = useState(null);
  const [sessionId] = useState(`session_${Date.now()}`);
  const [error, setError] = useState(null);
  const [suggestions] = useState([
    "Create a login automation task",
    "Generate a form filling workflow", 
    "Create a data scraping task",
    "Build a navigation workflow",
    "Help me automate file uploads",
    "Create a monitoring task"
  ]);

  // Check AI status on component mount
  useEffect(() => {
    checkAIStatus();
  }, []);

  const checkAIStatus = async () => {
    try {
      const status = await aiService.getStatus();
      setAiStatus(status);
      if (!status.is_initialized) {
        setError('AI service is not initialized. Please check if Ollama is running.');
      }
    } catch (error) {
      console.error('Failed to check AI status:', error);
      setError('Failed to connect to AI service. Please check if the backend is running.');
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

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
    setError(null);

    try {
      // Call real AI backend
      const response = await aiService.chat(currentInput, sessionId);
      
      const aiResponse = {
        id: Date.now(),
        type: 'ai',
        content: response.response || 'No response received',
        timestamp: new Date(),
        confidence: response.confidence || 0.0,
        actions: response.actions || []
      };

      setMessages(prev => [...prev, aiResponse]);
      
      // Show confidence level
      if (response.confidence && response.confidence < 0.5) {
        toast('AI response confidence is low. Please provide more details.', { 
          icon: '⚠️',
          duration: 3000 
        });
      }

    } catch (error) {
      console.error('AI chat failed:', error);
      setError('Failed to get AI response. Please try again.');
      
      const errorResponse = {
        id: Date.now(),
        type: 'ai',
        content: 'Sorry, I encountered an error. Please check if the AI service is running and try again.',
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateAIResponse = (userInput) => {
    const input = userInput.toLowerCase();
    
    let response = "";
    let actionButtons = [];

    if (input.includes('login') || input.includes('sign in')) {
      response = "🔐 I'll help you create a login automation task!\n\nHere's what I suggest:\n1. Navigate to the login page\n2. Find username/email field\n3. Enter credentials\n4. Click login button\n5. Wait for redirect\n6. Take screenshot\n\nWould you like me to generate this task for you?";
      actionButtons = [
        { label: "Generate Login Task", action: "generate_login", icon: <RunIcon /> }
      ];
    } else if (input.includes('sql') || input.includes('injection')) {
      response = "🛡️ Security Testing:\n\n**For security testing features, please use the dedicated Security Testing tab.**\n\nI can help you with:\n• Web automation tasks\n• Data extraction workflows\n• Form filling automation\n• Navigation scripts\n\nFor security testing, click on the 'Security Testing' tab in the main navigation.";
      actionButtons = [
        { label: "Go to Security Testing", action: "security_redirect", icon: <SecurityIcon /> }
      ];
    } else if (input.includes('form') || input.includes('fill')) {
      response = "📝 Form Automation Made Easy!\n\nI can help you:\n• Auto-detect form fields\n• Generate smart selectors\n• Handle different input types\n• Add validation checks\n• Create retry logic\n\nWhat type of form are you working with?";
      actionButtons = [
        { label: "Create Form Task", action: "form_task", icon: <RunIcon /> }
      ];
    } else if (input.includes('scrape') || input.includes('extract')) {
      response = "🕷️ Data Extraction Assistant:\n\n1. **Identify target elements**\n   - Use CSS selectors or XPath\n   - Try: .price, .title, .description\n\n2. **Handle dynamic content**\n   - Add wait conditions\n   - Scroll to load more\n\n3. **Export options**\n   - CSV, JSON, Excel\n   - Real-time or batch\n\nLet me create a scraping task for you!";
      actionButtons = [
        { label: "Build Scraper", action: "scraper_task", icon: <RunIcon /> }
      ];
    } else if (input.includes('security') || input.includes('test') || input.includes('hack')) {
      response = "🔒 Security Testing:\n\n**All security testing features are available in the dedicated Security Testing tab.**\n\nI can help you with regular automation tasks:\n• Website navigation\n• Form automation\n• Data extraction\n• Task building\n\nFor security testing, please navigate to the 'Security Testing' tab.";
      actionButtons = [
        { label: "Go to Security Testing", action: "security_redirect", icon: <SecurityIcon /> }
      ];
    } else {
      response = "🤔 I understand you want to: " + userInput + "\n\nLet me help you break this down:\n\n1. **Define the goal** - What's the end result?\n2. **Identify steps** - What actions are needed?\n3. **Handle challenges** - What could go wrong?\n4. **Test & refine** - How to verify success?\n\nCould you provide more details about what you're trying to accomplish?";
      actionButtons = [
        { label: "Task Builder", action: "task_builder", icon: <RunIcon /> },
        { label: "Get More Help", action: "help", icon: <SuggestionIcon /> }
      ];
    }

    return {
      id: Date.now(),
      type: 'ai',
      content: response,
      timestamp: new Date(),
      actionButtons
    };
  };

  const handleActionClick = async (action) => {
    try {
      switch (action) {
        case 'generate_login':
          if (onTaskSuggestion) {
            onTaskSuggestion({
              name: 'Login Automation',
              description: 'Automated login workflow with error handling',
              actions: [
                { type: 'navigate_to', url: 'https://example.com/login' },
                { type: 'fill_form', selector: '#username', value: 'your_username' },
                { type: 'fill_form', selector: '#password', value: 'your_password' },
                { type: 'click_element', selector: 'button[type="submit"]' },
                { type: 'wait', waitTime: 3 },
                { type: 'take_screenshot', filename: 'login_success' }
              ]
            });
          }
          break;
        case 'security_redirect':
        case 'security_session':
        case 'security_module':
          toast.info('Please use the Security Testing tab for all security features.');
          break;
        case 'form_task':
          if (onTaskSuggestion) {
            onTaskSuggestion({
              name: 'Smart Form Filler',
              description: 'Intelligent form filling with validation',
              actions: [
                { type: 'navigate_to', url: 'https://example.com/contact' },
                { type: 'fill_form', selector: 'input[name="name"]', value: 'John Doe' },
                { type: 'fill_form', selector: 'input[name="email"]', value: 'john@example.com' },
                { type: 'fill_form', selector: 'textarea[name="message"]', value: 'Hello from AI Assistant!' },
                { type: 'click_element', selector: 'button[type="submit"]' }
              ]
            });
          }
          break;
        case 'analyze_website':
          const url = prompt('Enter website URL to analyze:');
          if (url) {
            try {
              const analysis = await aiService.analyzeWebsite(url);
              const analysisMessage = {
                id: Date.now(),
                type: 'ai',
                content: `🔍 Website Analysis for ${url}:\n\n${analysis.analysis}`,
                timestamp: new Date()
              };
              setMessages(prev => [...prev, analysisMessage]);
            } catch (error) {
              toast.error('Failed to analyze website');
            }
          }
          break;
        case 'suggest_task':
          const description = prompt('Describe the task you want to create:');
          if (description) {
            try {
              const suggestion = await aiService.suggestTask(description);
              if (onTaskSuggestion) {
                onTaskSuggestion(suggestion);
              }
            } catch (error) {
              toast.error('Failed to generate task suggestion');
            }
          }
          break;
        default:
          console.log('Action:', action);
      }
    } catch (error) {
      console.error('Action failed:', error);
      toast.error('Action failed. Please try again.');
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };

  const copyMessage = (content) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', p: 2 }}>
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <Avatar sx={{ bgcolor: isDarkMode ? '#2196F3' : '#1976D2' }}>
            <AIIcon />
          </Avatar>
          <Box flexGrow={1}>
            <Typography variant="h6">AI Assistant</Typography>
            <Typography variant="body2" color="textSecondary">
              {aiStatus ? `${aiStatus.provider} (${aiStatus.model})` : 'Smart automation & security advisor'}
            </Typography>
            {aiStatus && (
              <Box display="flex" alignItems="center" gap={1} mt={0.5}>
                {aiStatus.is_initialized ? (
                  <Chip 
                    size="small" 
                    label="Connected" 
                    color="success" 
                    icon={<SuccessIcon />}
                  />
                ) : (
                  <Chip 
                    size="small" 
                    label="Disconnected" 
                    color="error" 
                    icon={<ErrorIcon />}
                  />
                )}
              </Box>
            )}
          </Box>
        </Box>

        <Divider sx={{ mb: 2 }} />

        {/* Error Display */}
        {error && (
          <Alert 
            severity="error" 
            sx={{ mb: 2 }}
            action={
              <Button color="inherit" size="small" onClick={checkAIStatus}>
                Retry
              </Button>
            }
          >
            {error}
          </Alert>
        )}

        {/* Quick Suggestions */}
        <Box mb={2}>
          <Typography variant="subtitle2" gutterBottom color="textSecondary">
            Quick Suggestions:
          </Typography>
          <Box display="flex" gap={1} flexWrap="wrap">
            {suggestions.slice(0, 3).map((suggestion, index) => (
              <Chip
                key={index}
                label={suggestion}
                size="small"
                onClick={() => handleSuggestionClick(suggestion)}
                sx={{ cursor: 'pointer' }}
                disabled={!aiStatus?.is_initialized}
              />
            ))}
            <Chip
              label="Analyze Website"
              size="small"
              onClick={() => handleActionClick('analyze_website')}
              sx={{ cursor: 'pointer' }}
              disabled={!aiStatus?.is_initialized}
              color="primary"
              variant="outlined"
            />
            <Chip
              label="Suggest Task"
              size="small"
              onClick={() => handleActionClick('suggest_task')}
              sx={{ cursor: 'pointer' }}
              disabled={!aiStatus?.is_initialized}
              color="primary"
              variant="outlined"
            />
          </Box>
        </Box>

        {/* Messages */}
        <Box 
          flexGrow={1} 
          sx={{ 
            overflowY: 'auto', 
            maxHeight: '400px',
            pr: 1
          }}
        >
          {messages.map((message) => (
            <Fade in={true} key={message.id}>
              <Box
                display="flex"
                justifyContent={message.type === 'user' ? 'flex-end' : 'flex-start'}
                mb={2}
              >
                <Box
                  sx={{
                    maxWidth: '80%',
                    p: 2,
                    borderRadius: 2,
                    bgcolor: message.type === 'user' ? (isDarkMode ? '#2196F3' : '#1976D2') : (isDarkMode ? '#21262D' : '#f5f5f5'),
                    color: message.type === 'user' ? 'white' : 'text.primary'
                  }}
                >
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    {message.type === 'ai' ? <AIIcon fontSize="small" /> : <UserIcon fontSize="small" />}
                    <Typography variant="caption">
                      {message.type === 'ai' ? 'AI Assistant' : 'You'}
                    </Typography>
                    <Tooltip title="Copy message">
                      <IconButton 
                        size="small" 
                        onClick={() => copyMessage(message.content)}
                        sx={{ ml: 'auto' }}
                      >
                        <CopyIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </Box>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
                    {message.content}
                  </Typography>
                  
                  {/* Confidence Level */}
                  {message.confidence !== undefined && (
                    <Box mt={1} display="flex" alignItems="center" gap={1}>
                      <Typography variant="caption" color="textSecondary">
                        Confidence: {Math.round(message.confidence * 100)}%
                      </Typography>
                      <Box 
                        sx={{ 
                          width: 60, 
                          height: 4, 
                          bgcolor: 'grey.300', 
                          borderRadius: 2,
                          overflow: 'hidden'
                        }}
                      >
                        <Box
                          sx={{
                            width: `${message.confidence * 100}%`,
                            height: '100%',
                            bgcolor: message.confidence > 0.7 ? 'success.main' : 
                                    message.confidence > 0.4 ? 'warning.main' : 'error.main',
                            transition: 'width 0.3s ease'
                          }}
                        />
                      </Box>
                    </Box>
                  )}
                  
                  {/* AI Actions */}
                  {message.actions && message.actions.length > 0 && (
                    <Box mt={2}>
                      <Typography variant="caption" color="textSecondary" gutterBottom>
                        Suggested Actions:
                      </Typography>
                      <Box display="flex" gap={1} flexWrap="wrap" mt={1}>
                        {message.actions.map((action, index) => (
                          <Chip
                            key={index}
                            label={`${action.type}: ${action.selector || action.url || 'action'}`}
                            size="small"
                            variant="outlined"
                            color="primary"
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                  
                  {/* Action Buttons */}
                  {message.actionButtons && (
                    <Box mt={2} display="flex" gap={1} flexWrap="wrap">
                      {message.actionButtons.map((button, index) => (
                        <Button
                          key={index}
                          size="small"
                          variant="outlined"
                          startIcon={button.icon}
                          onClick={() => handleActionClick(button.action)}
                          disabled={!aiStatus?.is_initialized}
                          sx={{ 
                            borderColor: message.type === 'user' ? 'white' : 'primary.main',
                            color: message.type === 'user' ? 'white' : 'primary.main'
                          }}
                        >
                          {button.label}
                        </Button>
                      ))}
                    </Box>
                  )}
                </Box>
              </Box>
            </Fade>
          ))}
          
          {isLoading && (
            <Box display="flex" justifyContent="flex-start" mb={2}>
              <Box
                sx={{
                  p: 2,
                  borderRadius: 2,
                  bgcolor: isDarkMode ? '#21262D' : '#f5f5f5',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 2
                }}
              >
                <CircularProgress size={16} />
                <Typography variant="body2" color="textSecondary">
                  AI is thinking...
                </Typography>
              </Box>
            </Box>
          )}
        </Box>

        {/* Input */}
        <Box display="flex" gap={1} mt={2}>
          <TextField
            fullWidth
            size="small"
            placeholder={
              aiStatus?.is_initialized 
                ? "Ask me anything about automation or security..." 
                : "AI service not available. Please check connection."
            }
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
            multiline
            maxRows={3}
            disabled={!aiStatus?.is_initialized || isLoading}
          />
          <IconButton 
            color="primary" 
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading || !aiStatus?.is_initialized}
            title={!aiStatus?.is_initialized ? "AI service not available" : "Send message"}
          >
            <SendIcon />
          </IconButton>
          <IconButton 
            onClick={() => setMessages(messages.slice(0, 1))}
            title="Clear chat"
          >
            <ClearIcon />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );
};

export default AIAssistant;
