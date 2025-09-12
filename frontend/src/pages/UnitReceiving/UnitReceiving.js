import React, { useState } from 'react';
import {
  Box,
  Container,
  Stack,
} from '@mui/material';

// Components
import {
  HeaderWidget,
  SystemStatusWidget,
  ActionWidget,
  ProcessOverviewWidget,
  UnitReceivingFormWidget,
} from './widgets';

// Hooks
import { usePlusStatus } from './hooks';

const UnitReceiving = ({ isDarkMode }) => {
  const {
    plusStatus,
    isLoading,
    statusMessage,
    handleBeginUnitReceiving,
  } = usePlusStatus();

  const [showForm, setShowForm] = useState(false);
  const [formLoading, setFormLoading] = useState(false);

  // Handle successful navigation - show the form
  React.useEffect(() => {
    if (statusMessage && (
      statusMessage.includes('Successfully navigated to Unit Receiving ADT page') ||
      statusMessage.includes('Already on Unit Receiving ADT page - ready to proceed')
    )) {
      setShowForm(true);
    }
  }, [statusMessage]);

  // Handle form submission
  const handleFormSubmit = async (formData) => {
    setFormLoading(true);
    
    try {
      // Call the form filling API
      const response = await fetch('http://localhost:8000/plus/fill-unit-receiving-form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const result = await response.json();
      
      if (result.success) {
        // Automatically submit the form after filling
        const submitResponse = await fetch('http://localhost:8000/plus/submit-unit-receiving-form', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const submitResult = await submitResponse.json();
        
        if (submitResult.success) {
          alert('✓ Unit receiving processed successfully!');
          setShowForm(false); // Hide form after successful submission
          // Reset for next unit
          setTimeout(() => {
            window.location.reload();
          }, 2000);
        } else {
          alert(`✗ Form submission failed: ${submitResult.message}`);
        }
      } else {
        alert(`✗ Form filling failed: ${result.message}`);
      }
    } catch (error) {
      alert('✗ Error processing unit receiving. Please try again.');
      console.error('Form submission error:', error);
    } finally {
      setFormLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <HeaderWidget isDarkMode={isDarkMode} plusStatus={plusStatus} />

        {/* Main Content */}
        <Stack spacing={4}>
          {/* System Status Card */}
          <SystemStatusWidget plusStatus={plusStatus} />

          {/* Action Card - Hide when form is shown */}
          {!showForm && (
            <ActionWidget 
              isLoading={isLoading}
              statusMessage={statusMessage}
              onBeginUnitReceiving={handleBeginUnitReceiving}
            />
          )}

          {/* Unit Receiving Form - Show after successful navigation */}
          {showForm && (
            <UnitReceivingFormWidget 
              onSubmit={handleFormSubmit}
              isLoading={formLoading}
            />
          )}

          {/* Process Overview Card - Hide when form is shown */}
          {!showForm && <ProcessOverviewWidget />}
        </Stack>
      </Box>
    </Container>
  );
};

export default UnitReceiving;
