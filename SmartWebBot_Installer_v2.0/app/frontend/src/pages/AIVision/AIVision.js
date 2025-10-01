import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Paper,
  Badge,
  Tooltip,
  Fade,
  LinearProgress,
  Tabs,
  Tab
} from '@mui/material';
import {
  Visibility as VisionIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  AutoAwesome as MagicIcon,
  Web as WebIcon,
  Mouse as ClickIcon,
  Edit as EditIcon,
  Link as LinkIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  Send as SendIcon,
  Clear as ClearIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
  Chat as ChatIcon,
  SmartToy as AIIcon
} from '@mui/icons-material';
import IntelligentChatInterface from '../../components/IntelligentChat/IntelligentChatInterface';
import aiVisionService from '../../services/aiVisionService';
import toast from 'react-hot-toast';

const AIVision = ({ isDarkMode = true }) => {
  // State management
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [elements, setElements] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResults, setExecutionResults] = useState([]);
  const [activeStep, setActiveStep] = useState(0);
  const [workflow, setWorkflow] = useState(null);
  const [isServiceAvailable, setIsServiceAvailable] = useState(false);
  const [error, setError] = useState(null);
  
  // Tab state
  const [activeTab, setActiveTab] = useState(0); // 0 = Vision Analysis, 1 = Intelligent Chat
  
  // Chat state
  const [chatSessionId] = useState(`vision_session_${Date.now()}`);

  // Check service availability on mount
  useEffect(() => {
    checkServiceAvailability();
  }, []);

  const checkServiceAvailability = async () => {
    try {
      const available = await aiVisionService.isAvailable();
      setIsServiceAvailable(available);
      if (!available) {
        setError('AI Vision service not available. Please check if the backend is running.');
      }
    } catch (error) {
      console.error('Service check failed:', error);
      setIsServiceAvailable(false);
      setError('Failed to connect to AI Vision service.');
    }
  };

  const handleAnalyze = async () => {
    if (!url.trim()) {
      toast.error('Please enter a URL to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysis(null);
    setElements([]);
    setSuggestions([]);

    try {
      const result = await aiVisionService.analyzeWebsite(url, 'comprehensive');
      
      if (result.success) {
        setAnalysis(result.analysis);
        setElements(result.analysis.elements || []);
        setSuggestions(result.analysis.action_suggestions || []);
        toast.success('Website analysis completed!');
      } else {
        throw new Error('Analysis failed');
      }
    } catch (error) {
      console.error('Analysis failed:', error);
      setError('Failed to analyze website. Please check the URL and try again.');
      toast.error('Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleExecuteAction = async (action, elementId = null, parameters = {}) => {
    setIsExecuting(true);
    
    try {
      const result = await aiVisionService.executeAction(action, elementId, parameters);
      
      setExecutionResults(prev => [...prev, {
        ...result,
        timestamp: new Date().toLocaleTimeString()
      }]);
      
      if (result.success) {
        toast.success(`Action executed: ${action}`);
      } else {
        toast.error(`Action failed: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Action execution failed:', error);
      toast.error('Action execution failed');
    } finally {
      setIsExecuting(false);
    }
  };

  const handleSuggestWorkflow = async () => {
    const description = prompt('Describe the task you want to automate:');
    if (!description) return;

    try {
      const result = await aiVisionService.suggestWorkflow(description);
      
      if (result.success) {
        setWorkflow(result.workflow);
        toast.success('Workflow generated!');
      } else {
        throw new Error('Workflow generation failed');
      }
    } catch (error) {
      console.error('Workflow suggestion failed:', error);
      toast.error('Failed to generate workflow');
    }
  };

  const handleExecuteWorkflow = async () => {
    if (!workflow) return;

    setIsExecuting(true);
    setActiveStep(0);
    
    try {
      const result = await aiVisionService.executeWorkflow(workflow.description, workflow.steps);
      
      if (result.success) {
        setExecutionResults(prev => [...prev, {
          type: 'workflow',
          workflow: workflow.description,
          steps: result.results,
          success: true,
          timestamp: new Date().toLocaleTimeString()
        }]);
        toast.success('Workflow executed successfully!');
      } else {
        throw new Error('Workflow execution failed');
      }
    } catch (error) {
      console.error('Workflow execution failed:', error);
      toast.error('Workflow execution failed');
    } finally {
      setIsExecuting(false);
    }
  };

  const getElementIcon = (category) => {
    switch (category) {
      case 'text_input': return <EditIcon />;
      case 'button': return <ClickIcon />;
      case 'link': return <LinkIcon />;
      case 'dropdown': return <ExpandMoreIcon />;
      default: return <WebIcon />;
    }
  };

  const getElementColor = (category) => {
    switch (category) {
      case 'text_input': return 'primary';
      case 'button': return 'success';
      case 'link': return 'info';
      case 'dropdown': return 'warning';
      default: return 'default';
    }
  };

  if (!isServiceAvailable) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          AI Vision service is not available. Please check if the backend is running and Ollama is started.
        </Alert>
        <Button variant="contained" onClick={checkServiceAvailability}>
          Retry Connection
        </Button>
      </Container>
    );
  }
  
  // Chat handlers
  const handleChatWorkflowExecute = (workflowResult) => {
    // Handle workflow execution from chat
    console.log('Chat workflow executed:', workflowResult);
    toast.success('Workflow executed successfully!');
    
    // Add to execution results
    setExecutionResults(prev => [...prev, {
      action: 'Chat Workflow',
      success: true,
      message: 'Intelligent chat workflow completed',
      timestamp: new Date().toLocaleTimeString(),
      details: workflowResult
    }]);
  };
  
  const handleChatCredentialsRequired = (credentialResult) => {
    // Handle credentials submission from chat
    console.log('Chat credentials submitted:', credentialResult);
    toast.success('Credentials submitted successfully!');
  };
  
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" alignItems="center" gap={2} mb={4}>
        <VisionIcon sx={{ fontSize: 40, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" component="h1">
            AI Vision & Automation
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            Real-time website analysis and intelligent automation
          </Typography>
        </Box>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange} aria-label="AI Vision tabs">
          <Tab 
            icon={<VisionIcon />} 
            label="Vision Analysis" 
            id="tab-0" 
            aria-controls="tabpanel-0" 
          />
          <Tab 
            icon={<ChatIcon />} 
            label="Intelligent Chat" 
            id="tab-1" 
            aria-controls="tabpanel-1" 
          />
        </Tabs>
      </Box>

      {/* Tab Panel 0: Vision Analysis */}
      {activeTab === 0 && (
        <Box>
          {/* URL Input */}
          <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" gap={2} alignItems="center">
            <TextField
              fullWidth
              label="Website URL"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isAnalyzing}
              onKeyPress={(e) => e.key === 'Enter' && !isAnalyzing && handleAnalyze()}
            />
            <Button
              variant="contained"
              onClick={handleAnalyze}
              disabled={isAnalyzing || !url.trim()}
              startIcon={isAnalyzing ? <CircularProgress size={20} /> : <VisionIcon />}
              sx={{ minWidth: 140 }}
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Analysis Results */}
      {analysis && (
        <Grid container spacing={3}>
          {/* Website Overview */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <WebIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Website Analysis
                </Typography>
                <Box mb={2}>
                  <Typography variant="body2" color="textSecondary">
                    <strong>URL:</strong> {analysis.url}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    <strong>Title:</strong> {analysis.page_info?.title || 'Unknown'}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    <strong>Elements Found:</strong> {elements.length}
                  </Typography>
                </Box>
                
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="subtitle2">AI Analysis</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
                      {analysis.analysis?.raw_analysis || 'No analysis available'}
                    </Typography>
                  </AccordionDetails>
                </Accordion>
              </CardContent>
            </Card>
          </Grid>

          {/* Action Suggestions */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <MagicIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Action Suggestions
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1}>
                  {suggestions.map((suggestion, index) => (
                    <Chip
                      key={index}
                      label={suggestion.description}
                      color="primary"
                      variant="outlined"
                      onClick={() => handleExecuteAction(suggestion.action)}
                      disabled={isExecuting}
                    />
                  ))}
                </Box>
                <Box mt={2}>
                  <Button
                    variant="outlined"
                    startIcon={<MagicIcon />}
                    onClick={handleSuggestWorkflow}
                    disabled={isExecuting}
                  >
                    Generate Workflow
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Detected Elements */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <WebIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Detected Elements ({elements.length})
                </Typography>
                <Grid container spacing={2}>
                  {elements.map((element, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Paper sx={{ p: 2, height: '100%' }}>
                        <Box display="flex" alignItems="center" gap={1} mb={1}>
                          {getElementIcon(element.category)}
                          <Typography variant="subtitle2" noWrap>
                            {element.text || element.placeholder || element.tag}
                          </Typography>
                          <Chip
                            label={element.category}
                            size="small"
                            color={getElementColor(element.category)}
                          />
                        </Box>
                        <Typography variant="caption" color="textSecondary" display="block">
                          {element.selector}
                        </Typography>
                        <Box mt={1} display="flex" gap={1}>
                          {element.suggested_actions?.slice(0, 2).map((action, actionIndex) => (
                            <Button
                              key={actionIndex}
                              size="small"
                              variant="outlined"
                              onClick={() => handleExecuteAction(action.action, element.selector, action.parameters)}
                              disabled={isExecuting}
                            >
                              {action.description}
                            </Button>
                          ))}
                        </Box>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Workflow Execution */}
          {workflow && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <PlayIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Generated Workflow: {workflow.workflow_name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    {workflow.description}
                  </Typography>
                  
                  <Stepper activeStep={activeStep} orientation="vertical">
                    {workflow.steps.map((step, index) => (
                      <Step key={index}>
                        <StepLabel>{step.description}</StepLabel>
                        <StepContent>
                          <Typography variant="body2" color="textSecondary">
                            Action: {step.action}
                            {step.element_id && ` | Element: ${step.element_id}`}
                          </Typography>
                          <Box mt={2}>
                            <Button
                              variant="contained"
                              onClick={() => handleExecuteAction(step.action, step.element_id, step.parameters)}
                              disabled={isExecuting}
                              sx={{ mr: 1 }}
                            >
                              Execute Step
                            </Button>
                          </Box>
                        </StepContent>
                      </Step>
                    ))}
                  </Stepper>
                  
                  <Box mt={2} display="flex" gap={2}>
                    <Button
                      variant="contained"
                      startIcon={<PlayIcon />}
                      onClick={handleExecuteWorkflow}
                      disabled={isExecuting}
                    >
                      Execute All Steps
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() => setWorkflow(null)}
                    >
                      Clear Workflow
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Execution Results */}
          {executionResults.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <SuccessIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Execution Results
                  </Typography>
                  <List>
                    {executionResults.slice(-10).reverse().map((result, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          {result.success ? <SuccessIcon color="success" /> : <ErrorIcon color="error" />}
                        </ListItemIcon>
                        <ListItemText
                          primary={result.action || result.type}
                          secondary={result.message || result.error || 'No details'}
                        />
                        <ListItemSecondaryAction>
                          <Typography variant="caption" color="textSecondary">
                            {result.timestamp}
                          </Typography>
                        </ListItemSecondaryAction>
                      </ListItem>
                    ))}
                  </List>
                  <Button
                    variant="outlined"
                    startIcon={<ClearIcon />}
                    onClick={() => setExecutionResults([])}
                    sx={{ mt: 2 }}
                  >
                    Clear Results
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      )}

      {/* Loading State */}
      {isAnalyzing && (
        <Box textAlign="center" py={4}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Analyzing website...
          </Typography>
          <Typography variant="body2" color="textSecondary">
            AI is examining the page structure and elements
          </Typography>
        </Box>
      )}
        </Box>
      )}

      {/* Tab Panel 1: Intelligent Chat */}
      {activeTab === 1 && (
        <Card sx={{ height: '70vh' }}>
          <IntelligentChatInterface
            sessionId={chatSessionId}
            currentUrl={url}
            onWorkflowExecute={handleChatWorkflowExecute}
            onCredentialsRequired={handleChatCredentialsRequired}
            isDarkMode={isDarkMode}
          />
        </Card>
      )}
    </Container>
  );
};

export default AIVision;
