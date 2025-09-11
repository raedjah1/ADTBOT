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

      // If logged in, navigate to Unit Receiving ADT page
      setStatusMessage('PLUS connection verified. Navigating to Unit Receiving ADT page...');
      
      try {
        const navResponse = await fetch('http://localhost:8000/plus/navigate/unit-receiving', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const navResult = await navResponse.json();
        
        if (navResult.success) {
          setStatusMessage('✓ Successfully navigated to Unit Receiving ADT page!');
          // Additional success logic can be added here
        } else {
          setStatusMessage(`✗ Navigation failed: ${navResult.message}`);
        }
      } catch (navError) {
        setStatusMessage('✗ Failed to navigate to Unit Receiving page. Please try again.');
        console.error('Navigation error:', navError);
      }
      
      setTimeout(() => {
        setIsLoading(false);
      }, 3000);

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
