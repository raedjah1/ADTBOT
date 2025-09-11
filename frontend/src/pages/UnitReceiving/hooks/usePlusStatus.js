import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const usePlusStatus = () => {
  const navigate = useNavigate();
  const [plusStatus, setPlusStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  // Check PLUS login status
  const checkPlusStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/plus/status');
      const data = await response.json();
      setPlusStatus(data);
      return data;
    } catch (error) {
      console.error('Failed to check PLUS status:', error);
      const fallbackStatus = { is_logged_in: false };
      setPlusStatus(fallbackStatus);
      return fallbackStatus;
    }
  };

  // Handle begin unit receiving logic
  const handleBeginUnitReceiving = async () => {
    setIsLoading(true);
    setStatusMessage('');

    try {
      // First check if user is logged in to PLUS
      const currentStatus = await checkPlusStatus();
      
      if (!currentStatus?.is_logged_in) {
        setStatusMessage('PLUS login required. Redirecting to settings...');
        setTimeout(() => {
          navigate('/settings');
        }, 2000);
        return;
      }

      // If logged in, proceed with unit receiving (placeholder for now)
      setStatusMessage('PLUS connection verified. Ready to begin unit receiving...');
      
      // TODO: Add actual unit receiving logic here
      setTimeout(() => {
        setStatusMessage('Unit receiving process ready to start!');
        setIsLoading(false);
      }, 2000);

    } catch (error) {
      setStatusMessage('Error checking PLUS connection. Please try again.');
      console.error('Unit receiving error:', error);
    } finally {
      if (statusMessage.includes('Redirecting')) {
        setTimeout(() => setIsLoading(false), 2000);
      }
    }
  };

  // Check status on mount
  useEffect(() => {
    checkPlusStatus();
  }, []);

  return {
    plusStatus,
    isLoading,
    statusMessage,
    checkPlusStatus,
    handleBeginUnitReceiving,
  };
};

export default usePlusStatus;
