import React, { useState } from 'react';

const SimpleSettings = () => {
  const [baseUrl, setBaseUrl] = useState('https://plus.reconext.com');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [apiKey, setApiKey] = useState('');

  const handleTestConnection = async () => {
    if (!baseUrl || !username || !password) {
      alert('Please fill in URL, username, and password first');
      return;
    }

    try {
      const response = await fetch('/api/plus/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          baseUrl,
          username,
          password,
          apiKey,
        }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        alert('✅ PLUS connection successful!');
      } else {
        alert(`❌ Connection failed: ${result.message || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`❌ Connection error: ${error.message}`);
    }
  };

  const handleSaveSettings = async () => {
    try {
      const response = await fetch('/api/plus/save-credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          baseUrl,
          username,
          password,
          apiKey,
        }),
      });
      
      const result = await response.json();
      
      if (response.ok && result.success) {
        alert('✅ Settings saved successfully!');
      } else {
        alert(`❌ Failed to save: ${result.message || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`❌ Save error: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>PLUS System Settings</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>PLUS System Base URL:</label>
        <input
          type="text"
          value={baseUrl}
          onChange={(e) => setBaseUrl(e.target.value)}
          placeholder="https://your-plus-system.com"
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px'
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Your PLUS username"
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px'
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Your PLUS password"
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px'
          }}
        />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', marginBottom: '5px' }}>API Key (Optional):</label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter your PLUS API key if required"
          style={{
            width: '100%',
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px'
          }}
        />
      </div>

      <div style={{ display: 'flex', gap: '10px', marginTop: '30px' }}>
        <button
          onClick={handleTestConnection}
          disabled={!baseUrl || !username || !password}
          style={{
            padding: '12px 24px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: !baseUrl || !username || !password ? 'not-allowed' : 'pointer',
            opacity: !baseUrl || !username || !password ? 0.6 : 1,
            fontSize: '16px'
          }}
        >
          Test Connection
        </button>
        
        <button
          onClick={handleSaveSettings}
          style={{
            padding: '12px 24px',
            backgroundColor: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          Save Settings
        </button>
      </div>

      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
        <strong>Status:</strong> {baseUrl && username && password ? '✅ Ready to test' : '❌ Please fill in all required fields'}
      </div>
    </div>
  );
};

export default SimpleSettings;
