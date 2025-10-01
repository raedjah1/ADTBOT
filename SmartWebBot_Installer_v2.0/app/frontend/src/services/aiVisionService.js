/**
 * AI Vision Service Module
 * 
 * Handles all AI Vision and real-time automation API calls.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class AIVisionService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api/ai-vision`;
  }

  /**
   * Get AI Vision service status
   */
  async getStatus() {
    try {
      const response = await fetch(`${this.baseURL}/status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get AI Vision status:', error);
      throw error;
    }
  }

  /**
   * Analyze a website with AI vision
   */
  async analyzeWebsite(url, analysisType = 'comprehensive') {
    try {
      const response = await fetch(`${this.baseURL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          analysis_type: analysisType
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Website analysis failed:', error);
      throw error;
    }
  }

  /**
   * Get current page state and analysis
   */
  async getCurrentState() {
    try {
      const response = await fetch(`${this.baseURL}/current-state`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get current state:', error);
      throw error;
    }
  }

  /**
   * Execute a specific action on the current page
   */
  async executeAction(action, elementId = null, parameters = {}) {
    try {
      const response = await fetch(`${this.baseURL}/execute-action`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action,
          element_id: elementId,
          parameters
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Action execution failed:', error);
      throw error;
    }
  }

  /**
   * Interact with a specific element
   */
  async interactWithElement(elementId, interactionType, data = {}) {
    try {
      const response = await fetch(`${this.baseURL}/interact-element`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          element_id: elementId,
          interaction_type: interactionType,
          data
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Element interaction failed:', error);
      throw error;
    }
  }

  /**
   * Get AI-suggested workflow for a task
   */
  async suggestWorkflow(description) {
    try {
      const response = await fetch(`${this.baseURL}/suggest-workflow`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Workflow suggestion failed:', error);
      throw error;
    }
  }

  /**
   * Execute a complete workflow
   */
  async executeWorkflow(description, steps) {
    try {
      const response = await fetch(`${this.baseURL}/execute-workflow`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          description,
          steps
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Workflow execution failed:', error);
      throw error;
    }
  }

  /**
   * Get all detected elements from current analysis
   */
  async getDetectedElements() {
    try {
      const response = await fetch(`${this.baseURL}/elements`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get elements:', error);
      throw error;
    }
  }

  /**
   * Get action suggestions for current page
   */
  async getActionSuggestions() {
    try {
      const response = await fetch(`${this.baseURL}/suggestions`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get suggestions:', error);
      throw error;
    }
  }

  /**
   * Refresh analysis of current page
   */
  async refreshAnalysis(analysisType = 'quick') {
    try {
      const response = await fetch(`${this.baseURL}/refresh-analysis?analysis_type=${analysisType}`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Analysis refresh failed:', error);
      throw error;
    }
  }

  /**
   * Get AI Vision capabilities
   */
  async getCapabilities() {
    try {
      const response = await fetch(`${this.baseURL}/capabilities`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get capabilities:', error);
      throw error;
    }
  }

  /**
   * Check if AI Vision service is available
   */
  async isAvailable() {
    try {
      const status = await this.getStatus();
      return status.status === 'active';
    } catch (error) {
      return false;
    }
  }
}

// Export singleton instance
export default new AIVisionService();
