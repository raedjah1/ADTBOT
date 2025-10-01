class WebSocketService {
  constructor() {
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.eventListeners = new Map();
    this.isConnecting = false;
  }

  connect() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return Promise.resolve(this.socket);
    }

    if (this.isConnecting) {
      return Promise.resolve();
    }

    this.isConnecting = true;

    return new Promise((resolve, reject) => {
      this.socket = new WebSocket('ws://localhost:8000/ws');

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.isConnecting = false;
        this.emit('connect');
        resolve(this.socket);
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.reason);
        this.isConnecting = false;
        this.emit('disconnect', event.reason);
        
        // Auto-reconnect logic
        setTimeout(() => {
          if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            this.connect();
          }
        }, 2000 * this.reconnectAttempts);
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('WebSocket received:', data);
          
          // Emit specific event types
          if (data.type) {
            this.emit(data.type, data);
          }
          
          // Emit general message event
          this.emit('message', data);
        } catch (error) {
          console.error('WebSocket message parse error:', error);
        }
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.isConnecting = false;
        this.emit('error', error);
        reject(error);
      };
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  send(event, data) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ event, data }));
    } else {
      console.warn('WebSocket not connected, cannot send message');
    }
  }

  isConnected() {
    return this.socket && this.socket.readyState === WebSocket.OPEN;
  }

  // Event system
  on(event, callback) {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }
    this.eventListeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.eventListeners.has(event)) {
      const listeners = this.eventListeners.get(event);
      const index = listeners.indexOf(callback);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
  }

  emit(event, ...args) {
    if (this.eventListeners.has(event)) {
      this.eventListeners.get(event).forEach(callback => {
        try {
          callback(...args);
        } catch (error) {
          console.error(`Error in event listener for ${event}:`, error);
        }
      });
    }
  }
}

// Create singleton instance
const websocketService = new WebSocketService();

// Auto-connect on import
websocketService.connect().catch(console.error);

// Legacy exports for backward compatibility
export const connectWebSocket = (onMessage, onConnect, onDisconnect) => {
  if (onMessage) websocketService.on('message', onMessage);
  if (onConnect) websocketService.on('connect', onConnect);
  if (onDisconnect) websocketService.on('disconnect', onDisconnect);
  return websocketService.connect();
};

export const disconnectWebSocket = () => websocketService.disconnect();
export const sendMessage = (event, data) => websocketService.send(event, data);
export const isConnected = () => websocketService.isConnected();

// Export the service instance
export { websocketService };
