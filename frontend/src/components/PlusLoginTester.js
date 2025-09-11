import React, { useState } from 'react';

const PlusLoginTester = () => {
  const [loginStatus, setLoginStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [testResults, setTestResults] = useState(null);

  const checkPlusStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/plus/status');
      const status = await response.json();
      setLoginStatus(status);
      return status;
    } catch (error) {
      console.error('Failed to check PLUS status:', error);
      return null;
    }
  };

  const testPlusLogin = async (forceLogin = false) => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/plus/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ force_login: forceLogin }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        setTestResults({
          success: true,
          message: result.message,
          timestamp: result.timestamp,
          loginStatus: result.login_status
        });
        await checkPlusStatus();
      } else {
        setTestResults({
          success: false,
          message: result.message || 'Login failed',
          error: result.detail || 'Unknown error'
        });
      }
    } catch (error) {
      setTestResults({
        success: false,
        message: 'Connection error',
        error: error.message
      });
    } finally {
      setIsLoading(false);
    }
  };

  const testPlusLogout = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/plus/logout', {
        method: 'POST',
      });
      
      const result = await response.json();
      
      setTestResults({
        success: result.success,
        message: result.message,
        timestamp: result.timestamp
      });
      
      await checkPlusStatus();
    } catch (error) {
      setTestResults({
        success: false,
        message: 'Logout error',
        error: error.message
      });
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    checkPlusStatus();
  }, []);

  return (
    <div style={{
      padding: '20px',
      maxWidth: '800px',
      margin: '0 auto',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h2 style={{ color: '#333', borderBottom: '2px solid #007bff', paddingBottom: '10px' }}>
        🔐 PLUS Login Tester
      </h2>
      
      {/* Current Status */}
      <div style={{
        backgroundColor: loginStatus?.is_logged_in ? '#d4edda' : '#f8d7da',
        border: `1px solid ${loginStatus?.is_logged_in ? '#c3e6cb' : '#f5c6cb'}`,
        color: loginStatus?.is_logged_in ? '#155724' : '#721c24',
        padding: '15px',
        borderRadius: '5px',
        marginBottom: '20px'
      }}>
        <h3>Current Status</h3>
        {loginStatus ? (
          <div>
            <p><strong>Logged In:</strong> {loginStatus.is_logged_in ? '✅ Yes' : '❌ No'}</p>
            {loginStatus.plus_url && (
              <p><strong>PLUS URL:</strong> {loginStatus.plus_url}</p>
            )}
            {loginStatus.username && (
              <p><strong>Username:</strong> {loginStatus.username}</p>
            )}
            {loginStatus.login_timestamp && (
              <p><strong>Login Time:</strong> {new Date(loginStatus.login_timestamp * 1000).toLocaleString()}</p>
            )}
            {loginStatus.session_age_seconds && (
              <p><strong>Session Age:</strong> {Math.round(loginStatus.session_age_seconds / 60)} minutes</p>
            )}
          </div>
        ) : (
          <p>Loading status...</p>
        )}
      </div>

      {/* Test Controls */}
      <div style={{
        backgroundColor: '#f8f9fa',
        padding: '20px',
        borderRadius: '5px',
        marginBottom: '20px'
      }}>
        <h3>Test Controls</h3>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button
            onClick={() => testPlusLogin(false)}
            disabled={isLoading}
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1
            }}
          >
            {isLoading ? '⏳ Testing...' : '🔐 Test Login'}
          </button>
          
          <button
            onClick={() => testPlusLogin(true)}
            disabled={isLoading}
            style={{
              backgroundColor: '#ffc107',
              color: 'black',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1
            }}
          >
            {isLoading ? '⏳ Testing...' : '🔄 Force Re-Login'}
          </button>
          
          <button
            onClick={testPlusLogout}
            disabled={isLoading}
            style={{
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1
            }}
          >
            {isLoading ? '⏳ Testing...' : '🚪 Test Logout'}
          </button>
          
          <button
            onClick={checkPlusStatus}
            disabled={isLoading}
            style={{
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              opacity: isLoading ? 0.6 : 1
            }}
          >
            🔄 Refresh Status
          </button>
        </div>
      </div>

      {/* Test Results */}
      {testResults && (
        <div style={{
          backgroundColor: testResults.success ? '#d4edda' : '#f8d7da',
          border: `1px solid ${testResults.success ? '#c3e6cb' : '#f5c6cb'}`,
          color: testResults.success ? '#155724' : '#721c24',
          padding: '15px',
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          <h3>Test Results</h3>
          <p><strong>Status:</strong> {testResults.success ? '✅ Success' : '❌ Failed'}</p>
          <p><strong>Message:</strong> {testResults.message}</p>
          {testResults.error && (
            <p><strong>Error:</strong> {testResults.error}</p>
          )}
          {testResults.timestamp && (
            <p><strong>Timestamp:</strong> {new Date(testResults.timestamp).toLocaleString()}</p>
          )}
          {testResults.loginStatus && (
            <div>
              <h4>Login Status Details:</h4>
              <pre style={{
                backgroundColor: '#f8f9fa',
                padding: '10px',
                borderRadius: '3px',
                fontSize: '12px',
                overflow: 'auto'
              }}>
                {JSON.stringify(testResults.loginStatus, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      <div style={{
        backgroundColor: '#e7f3ff',
        border: '1px solid #b8daff',
        color: '#004085',
        padding: '15px',
        borderRadius: '5px'
      }}>
        <h3>Instructions</h3>
        <ol>
          <li><strong>Configure PLUS Credentials:</strong> Go to Settings and enter your PLUS system URL, username, and password.</li>
          <li><strong>Test Login:</strong> Click "Test Login" to attempt logging into PLUS using your saved credentials.</li>
          <li><strong>Check Results:</strong> The test will show success/failure and detailed information about the login attempt.</li>
          <li><strong>Verify Session:</strong> If login succeeds, the status will show you're logged in and session details.</li>
          <li><strong>Test Logout:</strong> Use "Test Logout" to verify the logout functionality works.</li>
        </ol>
        
        <h4>Troubleshooting:</h4>
        <ul>
          <li>If login fails, check your credentials in Settings</li>
          <li>Make sure your PLUS system URL is correct and accessible</li>
          <li>Try "Force Re-Login" if you're having session issues</li>
          <li>Check the browser console for detailed error messages</li>
        </ul>
      </div>
    </div>
  );
};

export default PlusLoginTester;
