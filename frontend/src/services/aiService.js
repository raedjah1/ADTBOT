/**
 * AI Service Module
 * 
 * Handles all AI-related API calls with proper error handling and separation of concerns.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class AIService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api/ai`;
  }

  /**
   * Get AI system status and capabilities
   */
  async getStatus() {
    try {
      const response = await fetch(`${this.baseURL}/status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get AI status:', error);
      throw error;
    }
  }

  /**
   * Chat with AI assistant
   */
  async chat(message, sessionId = null, context = null) {
    try {
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
          context
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Chat failed:', error);
      throw error;
    }
  }

  /**
   * Quick chat without session management
   */
  async quickChat(message, model = null) {
    try {
      const params = new URLSearchParams({ message });
      if (model) params.append('model', model);

      const response = await fetch(`${this.baseURL}/quick-chat?${params}`, {
        method: 'POST'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Quick chat failed:', error);
      throw error;
    }
  }

  /**
   * Get AI task suggestions
   */
  async suggestTask(description) {
    try {
      const response = await fetch(`${this.baseURL}/suggest-task`, {
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
      console.error('Task suggestion failed:', error);
      throw error;
    }
  }

  /**
   * Analyze website using AI
   */
  async analyzeWebsite(url, analysisType = 'general') {
    try {
      const response = await fetch(`${this.baseURL}/analyze-website`, {
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
   * Get chat history for a session
   */
  async getChatHistory(sessionId) {
    try {
      const response = await fetch(`${this.baseURL}/history/${sessionId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get chat history:', error);
      throw error;
    }
  }

  /**
   * Clear chat history for a session
   */
  async clearChatHistory(sessionId) {
    try {
      const response = await fetch(`${this.baseURL}/history/${sessionId}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to clear chat history:', error);
      throw error;
    }
  }

  /**
   * Get detailed AI capabilities
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
   * Check if AI service is available
   */
  async isAvailable() {
    try {
      const status = await this.getStatus();
      return status.is_initialized;
    } catch (error) {
      return false;
    }
  }
}

// Export singleton instance
export default new AIService();
