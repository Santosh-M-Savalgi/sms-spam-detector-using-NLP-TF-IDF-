import { useState } from 'react';
import './index.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResult(data.prediction); 
    } catch (err) {
      console.error(err);
      setError('FATAL ERROR: BACKEND CONNECTION LOST. CHECK PORT 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-panel">
        <header className="header">
          <h1 className="title">
            NeuralGuard
          </h1>
          <div className="marquee-container">
            {/* The <marquee> element is highly typical of web 1.0 Y2K vibe! */}
            <marquee scrollamount="8">»»»» WARNING: AI-POWERED CYBER THREAT DETECTION MODULE INITIALIZED v2.000 ««««</marquee>
          </div>
        </header>

        <div className="input-container">
          <textarea
            className="message-textarea"
            placeholder="[INPUT RECEIVED DATA STREAM HERE]"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={loading}
          />

          <button 
            className="analyze-btn" 
            onClick={handleAnalyze} 
            disabled={!message.trim() || loading}
          >
            {loading ? 'PROCESSING...' : 'EXECUTE SCAN'}
          </button>
        </div>

        {error && (
          <div style={{ color: '#ff0000', marginTop: '1rem', border: '2px solid red', padding: '10px', background: '#220000' }}>
            {error}
          </div>
        )}

        {result && (
          <div className={`results-banner ${result}`}>
            <h2 className="results-title">
              {result === 'spam' ? '!! THREAT DETECTED !!' : '// MESSAGE VERIFIED SAFE //'}
            </h2>
            <p className="results-desc">
              {result === 'spam' 
                ? 'SCAN RESULTS: MALICIOUS PATTERNS FOUND IN TEXT.' 
                : 'SCAN RESULTS: CLEAN. NO ANOMALIES DETECTED.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
