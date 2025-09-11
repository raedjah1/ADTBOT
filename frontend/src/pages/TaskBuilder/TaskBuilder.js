import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  Grid,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Divider,
  Tooltip,
  Switch,
  FormControlLabel,
  Stepper,
  Step,
  StepLabel,
  StepContent
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayIcon,
  Save as SaveIcon,
  DragIndicator as DragIcon,
  Web as WebIcon,
  Mouse as ClickIcon,
  Keyboard as TypeIcon,
  Timer as WaitIcon,
  CameraAlt as ScreenshotIcon,
  TextFields as ExtractIcon,
  ArrowDownward as ScrollIcon,
  ExpandMore as ExpandMoreIcon,
  Visibility as PreviewIcon,
  Code as CodeIcon,
  SmartToy as AIIcon,
  FileCopy as CopyIcon
} from '@mui/icons-material';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { runTask, createTask } from '../../services/api';

const TaskBuilder = ({ isDarkMode = true }) => {
  const [taskName, setTaskName] = useState('');
  const [taskDescription, setTaskDescription] = useState('');
  const [website, setWebsite] = useState('');
  const [browser, setBrowser] = useState('chrome');
  const [actions, setActions] = useState([]);
  const [showActionDialog, setShowActionDialog] = useState(false);
  const [currentAction, setCurrentAction] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [results, setResults] = useState(null);
  const [activeStep, setActiveStep] = useState(0);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  // Example tasks for quick start
  const exampleTasks = [
    {
      name: 'Google Search Example',
      description: 'Search for something on Google and take a screenshot',
      website: 'https://google.com',
      actions: [
        {
          id: 1,
          type: 'type',
          name: 'Type Text',
          icon: <TypeIcon />,
          color: '#FF9800',
          selector: 'input[name="q"]',
          value: 'SmartWebBot automation',
          clear: true
        },
        {
          id: 2,
          type: 'click',
          name: 'Click Element',
          icon: <ClickIcon />,
          color: '#4CAF50',
          selector: 'input[value="Google Search"]',
          description: 'search button'
        },
        {
          id: 3,
          type: 'wait',
          name: 'Wait/Pause',
          icon: <WaitIcon />,
          color: '#9C27B0',
          waitTime: 3
        },
        {
          id: 4,
          type: 'screenshot',
          name: 'Take Screenshot',
          icon: <ScreenshotIcon />,
          color: '#607D8B',
          filename: 'google-search-results'
        }
      ]
    },
    {
      name: 'Form Filling Example',
      description: 'Fill out a contact form',
      website: 'https://example.com/contact',
      actions: [
        {
          id: 1,
          type: 'type',
          name: 'Type Text',
          icon: <TypeIcon />,
          color: '#FF9800',
          selector: '#name',
          value: 'John Doe',
          clear: true
        },
        {
          id: 2,
          type: 'type',
          name: 'Type Text',
          icon: <TypeIcon />,
          color: '#FF9800',
          selector: '#email',
          value: 'john@example.com',
          clear: true
        },
        {
          id: 3,
          type: 'type',
          name: 'Type Text',
          icon: <TypeIcon />,
          color: '#FF9800',
          selector: '#message',
          value: 'Hello, this is an automated message!',
          clear: true
        },
        {
          id: 4,
          type: 'click',
          name: 'Click Element',
          icon: <ClickIcon />,
          color: '#4CAF50',
          selector: 'button[type="submit"]',
          description: 'submit button'
        }
      ]
    }
  ];

  // Available action types with icons and descriptions
  const actionTypes = [
    {
      type: 'navigate',
      name: 'Navigate to URL',
      icon: <WebIcon />,
      description: 'Navigate to a specific web page',
      color: '#2196F3',
      fields: [
        { name: 'url', label: 'URL', type: 'text', required: true, placeholder: 'https://example.com' }
      ]
    },
    {
      type: 'click',
      name: 'Click Element',
      icon: <ClickIcon />,
      description: 'Click on a button, link, or any element',
      color: '#4CAF50',
      fields: [
        { name: 'selector', label: 'Element Selector (CSS/XPath)', type: 'text', required: true, placeholder: '#button-id, .class-name, //button[text()="Click me"]' },
        { name: 'description', label: 'Element Description (AI)', type: 'text', placeholder: 'login button, submit form, etc.' }
      ]
    },
    {
      type: 'type',
      name: 'Type Text',
      icon: <TypeIcon />,
      description: 'Type text into input fields',
      color: '#FF9800',
      fields: [
        { name: 'selector', label: 'Input Field Selector', type: 'text', required: true, placeholder: '#email, input[name="username"]' },
        { name: 'value', label: 'Text to Type', type: 'text', required: true, placeholder: 'Enter your text here' },
        { name: 'clear', label: 'Clear Field First', type: 'boolean', default: true }
      ]
    },
    {
      type: 'wait',
      name: 'Wait/Pause',
      icon: <WaitIcon />,
      description: 'Wait for a specified amount of time',
      color: '#9C27B0',
      fields: [
        { name: 'waitTime', label: 'Wait Time (seconds)', type: 'number', required: true, default: 2, min: 0.5, max: 60 }
      ]
    },
    {
      type: 'screenshot',
      name: 'Take Screenshot',
      icon: <ScreenshotIcon />,
      description: 'Capture a screenshot of the current page',
      color: '#607D8B',
      fields: [
        { name: 'filename', label: 'Filename (optional)', type: 'text', placeholder: 'my-screenshot' }
      ]
    },
    {
      type: 'extract_text',
      name: 'Extract Text',
      icon: <ExtractIcon />,
      description: 'Extract text from elements on the page',
      color: '#795548',
      fields: [
        { name: 'selector', label: 'Element Selector', type: 'text', required: true, placeholder: '.price, h1, .product-name' },
        { name: 'attribute', label: 'Attribute (optional)', type: 'text', placeholder: 'href, src, title' }
      ]
    },
    {
      type: 'scroll',
      name: 'Scroll Page',
      icon: <ScrollIcon />,
      description: 'Scroll the page up or down',
      color: '#3F51B5',
      fields: [
        { name: 'direction', label: 'Direction', type: 'select', options: [
          { value: 'down', label: 'Scroll Down' },
          { value: 'up', label: 'Scroll Up' },
          { value: 'top', label: 'Scroll to Top' },
          { value: 'bottom', label: 'Scroll to Bottom' }
        ], default: 'down' }
      ]
    }
  ];

  const handleAddAction = (actionType) => {
    const actionTemplate = actionTypes.find(at => at.type === actionType);
    const newAction = {
      id: Date.now(),
      type: actionType,
      name: actionTemplate.name,
      icon: actionTemplate.icon,
      color: actionTemplate.color,
      ...actionTemplate.fields.reduce((acc, field) => {
        acc[field.name] = field.default || '';
        return acc;
      }, {})
    };
    
    setCurrentAction(newAction);
    setShowActionDialog(true);
  };

  const handleSaveAction = () => {
    if (currentAction.id && actions.find(a => a.id === currentAction.id)) {
      // Update existing action
      setActions(actions.map(a => a.id === currentAction.id ? currentAction : a));
    } else {
      // Add new action
      setActions([...actions, currentAction]);
    }
    setShowActionDialog(false);
    setCurrentAction(null);
  };

  const handleEditAction = (action) => {
    setCurrentAction(action);
    setShowActionDialog(true);
  };

  const handleDeleteAction = (actionId) => {
    setActions(actions.filter(a => a.id !== actionId));
  };

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const reorderedActions = Array.from(actions);
    const [reorderedItem] = reorderedActions.splice(result.source.index, 1);
    reorderedActions.splice(result.destination.index, 0, reorderedItem);

    setActions(reorderedActions);
  };

  const handleRunTask = async () => {
    if (!website || actions.length === 0) {
      alert('Please add a website URL and at least one action');
      return;
    }

    setIsRunning(true);
    setResults(null);

    try {
      const taskData = {
        name: taskName || 'Untitled Task',
        description: taskDescription || 'Task created with Task Builder',
        website,
        browser,
        actions: actions.map(action => ({
          type: action.type,
          ...Object.keys(action).reduce((acc, key) => {
            if (!['id', 'name', 'icon', 'color', 'type'].includes(key)) {
              acc[key] = action[key];
            }
            return acc;
          }, {})
        }))
      };

      const result = await runTask(taskData);
      setResults(result);
      alert('Task completed successfully!');
    } catch (error) {
      console.error('Task execution failed:', error);
      alert(`Task failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  const handleSaveTask = async () => {
    if (!taskName) {
      alert('Please enter a task name');
      return;
    }

    try {
      const taskData = {
        name: taskName,
        description: taskDescription,
        url: website,
        actions: actions.map(action => ({
          type: action.type,
          ...Object.keys(action).reduce((acc, key) => {
            if (!['id', 'name', 'icon', 'color', 'type'].includes(key)) {
              acc[key] = action[key];
            }
            return acc;
          }, {})
        })),
        settings: { browser }
      };

      await createTask(taskData);
      alert('Task saved successfully!');
    } catch (error) {
      console.error('Task save failed:', error);
      alert(`Save failed: ${error.response?.data?.detail || error.message}`);
    }
  };

  const loadExampleTask = (example) => {
    setTaskName(example.name);
    setTaskDescription(example.description);
    setWebsite(example.website);
    setActions(example.actions);
  };

  const clearTask = () => {
    setTaskName('');
    setTaskDescription('');
    setWebsite('');
    setActions([]);
    setResults(null);
  };

  const renderActionDialog = () => {
    if (!currentAction) return null;

    const actionTemplate = actionTypes.find(at => at.type === currentAction.type);

    return (
      <Dialog open={showActionDialog} onClose={() => setShowActionDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={2}>
            {actionTemplate.icon}
            <Typography variant="h6">{actionTemplate.name}</Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography color="textSecondary" sx={{ mb: 3 }}>
            {actionTemplate.description}
          </Typography>
          
          <Grid container spacing={2}>
            {actionTemplate.fields.map((field) => (
              <Grid item xs={12} key={field.name}>
                {field.type === 'text' && (
                  <TextField
                    fullWidth
                    label={field.label}
                    value={currentAction[field.name] || ''}
                    onChange={(e) => setCurrentAction({...currentAction, [field.name]: e.target.value})}
                    placeholder={field.placeholder}
                    required={field.required}
                    multiline={field.multiline}
                    rows={field.rows || 1}
                  />
                )}
                {field.type === 'number' && (
                  <TextField
                    fullWidth
                    type="number"
                    label={field.label}
                    value={currentAction[field.name] || field.default || ''}
                    onChange={(e) => setCurrentAction({...currentAction, [field.name]: parseFloat(e.target.value)})}
                    required={field.required}
                    inputProps={{ min: field.min, max: field.max, step: field.step || 1 }}
                  />
                )}
                {field.type === 'select' && (
                  <FormControl fullWidth>
                    <InputLabel>{field.label}</InputLabel>
                    <Select
                      value={currentAction[field.name] || field.default || ''}
                      onChange={(e) => setCurrentAction({...currentAction, [field.name]: e.target.value})}
                      label={field.label}
                    >
                      {field.options.map((option) => (
                        <MenuItem key={option.value} value={option.value}>
                          {option.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}
                {field.type === 'boolean' && (
                  <FormControlLabel
                    control={
                      <Switch
                        checked={currentAction[field.name] !== false}
                        onChange={(e) => setCurrentAction({...currentAction, [field.name]: e.target.checked})}
                      />
                    }
                    label={field.label}
                  />
                )}
              </Grid>
            ))}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowActionDialog(false)}>Cancel</Button>
          <Button onClick={handleSaveAction} variant="contained">
            {currentAction.id && actions.find(a => a.id === currentAction.id) ? 'Update' : 'Add'} Action
          </Button>
        </DialogActions>
      </Dialog>
    );
  };

  const renderActionCard = (action, index) => (
    <Draggable key={action.id} draggableId={action.id.toString()} index={index}>
      {(provided, snapshot) => (
        <Card
          ref={provided.innerRef}
          {...provided.draggableProps}
          sx={{
            mb: 2,
            border: snapshot.isDragging ? '2px solid #2196F3' : `1px solid ${isDarkMode ? '#30363D' : '#e0e0e0'}`,
            transform: snapshot.isDragging ? 'rotate(5deg)' : 'none',
            boxShadow: snapshot.isDragging ? 4 : 1,
          }}
        >
          <CardContent sx={{ py: 2 }}>
            <Box display="flex" alignItems="center" justifyContent="space-between">
              <Box display="flex" alignItems="center" gap={2} flex={1}>
                <Box {...provided.dragHandleProps}>
                  <DragIcon sx={{ color: 'text.secondary', cursor: 'grab' }} />
                </Box>
                
                <Box
                  sx={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    backgroundColor: action.color,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white'
                  }}
                >
                  {action.icon}
                </Box>
                
                <Box flex={1}>
                  <Typography variant="subtitle1" fontWeight="medium">
                    {index + 1}. {action.name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {action.type === 'navigate' && `Go to: ${action.url}`}
                    {action.type === 'click' && `Click: ${action.selector || action.description}`}
                    {action.type === 'type' && `Type "${action.value}" into ${action.selector}`}
                    {action.type === 'wait' && `Wait ${action.waitTime} seconds`}
                    {action.type === 'screenshot' && `Take screenshot${action.filename ? `: ${action.filename}` : ''}`}
                    {action.type === 'extract_text' && `Extract text from: ${action.selector}`}
                    {action.type === 'scroll' && `Scroll ${action.direction || 'down'}`}
                  </Typography>
                </Box>
              </Box>
              
              <Box display="flex" gap={1}>
                <Tooltip title="Edit Action">
                  <IconButton onClick={() => handleEditAction(action)} size="small">
                    <CodeIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Delete Action">
                  <IconButton onClick={() => handleDeleteAction(action.id)} size="small" color="error">
                    <DeleteIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Box>
          </CardContent>
        </Card>
      )}
    </Draggable>
  );

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
        🛠️ Task Builder
      </Typography>
      <Typography variant="body1" color="textSecondary" sx={{ mb: 4 }}>
        Create powerful automation tasks with our drag-and-drop interface. No coding required!
      </Typography>

      <Grid container spacing={3}>
        {/* Left Panel - Task Configuration */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <WebIcon /> Task Configuration
              </Typography>
              
              <TextField
                fullWidth
                label="Task Name"
                value={taskName}
                onChange={(e) => setTaskName(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="My Automation Task"
              />
              
              <TextField
                fullWidth
                label="Description (Optional)"
                value={taskDescription}
                onChange={(e) => setTaskDescription(e.target.value)}
                multiline
                rows={2}
                sx={{ mb: 2 }}
                placeholder="What does this task do?"
              />
              
              <TextField
                fullWidth
                label="Website URL"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
                sx={{ mb: 2 }}
                placeholder="https://example.com"
                required
              />
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Browser</InputLabel>
                <Select value={browser} onChange={(e) => setBrowser(e.target.value)} label="Browser">
                  <MenuItem value="chrome">Chrome</MenuItem>
                  <MenuItem value="firefox">Firefox</MenuItem>
                  <MenuItem value="edge">Edge</MenuItem>
                </Select>
              </FormControl>

              <Box display="flex" gap={1} flexWrap="wrap">
                <Button
                  variant="contained"
                  startIcon={<PlayIcon />}
                  onClick={handleRunTask}
                  disabled={isRunning || !website || actions.length === 0}
                  fullWidth
                  sx={{ mb: 1 }}
                >
                  {isRunning ? 'Running...' : 'Run Task'}
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveTask}
                  disabled={!taskName}
                  fullWidth
                >
                  Save Task
                </Button>
              </Box>

              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle1" sx={{ mb: 1 }}>
                🚀 Quick Start Examples
              </Typography>
              <Box display="flex" flexDirection="column" gap={1}>
                {exampleTasks.map((example, index) => (
                  <Button
                    key={index}
                    variant="text"
                    size="small"
                    onClick={() => loadExampleTask(example)}
                    sx={{ justifyContent: 'flex-start' }}
                  >
                    {example.name}
                  </Button>
                ))}
                <Button
                  variant="text"
                  size="small"
                  onClick={clearTask}
                  color="error"
                  sx={{ justifyContent: 'flex-start' }}
                >
                  Clear Task
                </Button>
              </Box>
            </CardContent>
          </Card>

          {/* Action Palette */}
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Available Actions
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                Click to add actions to your task
              </Typography>
              
              <Grid container spacing={1}>
                {actionTypes.map((actionType) => (
                  <Grid item xs={6} key={actionType.type}>
                    <Tooltip title={actionType.description} placement="top">
                      <Button
                        variant="outlined"
                        onClick={() => handleAddAction(actionType.type)}
                        className="action-palette-button"
                        sx={{
                          width: '100%',
                          height: 60,
                          borderColor: actionType.color,
                          color: actionType.color,
                          '&:hover': {
                            backgroundColor: `${actionType.color}20`,
                            borderColor: actionType.color,
                          }
                        }}
                      >
                        <Box display="flex" flexDirection="column" alignItems="center" gap={0.5}>
                          {actionType.icon}
                          <Typography variant="caption" sx={{ fontSize: '0.7rem', textAlign: 'center' }}>
                            {actionType.name.split(' ')[0]}
                          </Typography>
                        </Box>
                      </Button>
                    </Tooltip>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Right Panel - Task Flow */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                <Typography variant="h6">
                  Task Flow ({actions.length} actions)
                </Typography>
                <Box>
                  <Tooltip title="Preview Task">
                    <IconButton onClick={() => setShowPreview(!showPreview)}>
                      <PreviewIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>

              {actions.length === 0 ? (
                <Paper
                  sx={{
                    p: 4,
                    textAlign: 'center',
                    border: `2px dashed ${isDarkMode ? '#30363D' : '#ccc'}`,
                    backgroundColor: isDarkMode ? '#161B22' : '#f9f9f9'
                  }}
                >
                  <Typography variant="h6" color="textSecondary" sx={{ mb: 1 }}>
                    🎯 Ready to Build Your Task?
                  </Typography>
                  <Typography color="textSecondary" sx={{ mb: 2 }}>
                    Add actions from the left panel or try a quick start example
                  </Typography>
                  <Box display="flex" flexDirection="column" gap={1} alignItems="center">
                    <Typography variant="body2" color="textSecondary">
                      💡 <strong>Pro Tips:</strong>
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                      • Start with "Navigate to URL" to go to your target website
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                      • Use CSS selectors like "#id", ".class", or "button" for elements
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                      • Add "Wait" actions between steps for better reliability
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                      • Use "Screenshot" to capture results
                    </Typography>
                  </Box>
                </Paper>
              ) : (
                <DragDropContext onDragEnd={handleDragEnd}>
                  <Droppable droppableId="actions">
                    {(provided) => (
                      <Box {...provided.droppableProps} ref={provided.innerRef}>
                        {actions.map((action, index) => renderActionCard(action, index))}
                        {provided.placeholder}
                      </Box>
                    )}
                  </Droppable>
                </DragDropContext>
              )}

              {showPreview && actions.length > 0 && (
                <Box sx={{ mt: 3, p: 2, backgroundColor: isDarkMode ? '#21262D' : '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="subtitle1" sx={{ mb: 2 }}>
                    📋 Task Preview
                  </Typography>
                  <Typography variant="body2" component="pre" sx={{ fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
                    {JSON.stringify({
                      name: taskName || 'Untitled Task',
                      website,
                      browser,
                      actions: actions.map(action => ({
                        type: action.type,
                        ...Object.keys(action).reduce((acc, key) => {
                          if (!['id', 'name', 'icon', 'color', 'type'].includes(key) && action[key]) {
                            acc[key] = action[key];
                          }
                          return acc;
                        }, {})
                      }))
                    }, null, 2)}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>

          {/* Results */}
          {results && (
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  📊 Execution Results
                </Typography>
                {results.results && results.results.map((result, index) => (
                  <Alert 
                    key={index}
                    severity={result.result === 'success' || result.result === 'completed' ? 'success' : 'error'}
                    sx={{ mb: 1 }}
                  >
                    <strong>Step {index + 1}:</strong> {result.action} - {result.result}
                  </Alert>
                ))}
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>

      {/* Action Dialog */}
      {renderActionDialog()}
    </Box>
  );
};

export default TaskBuilder;