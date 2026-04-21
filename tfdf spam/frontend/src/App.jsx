import { useState } from 'react';
import { ShieldCheck, ShieldAlert, Loader2, Search, Zap } from 'lucide-react';
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
      setResult(data.prediction); // "spam" or "ham"
    } catch (err) {
      console.error(err);
      setError('Failed to connect to the analysis engine. Make sure the FastAPI backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-panel">
        <header className="header">
          <h1 className="title">
            <Zap size={36} color="#a78bfa" />
            NeuralGuard
          </h1>
          <p className="subtitle">AI-Powered SMS Threat Detection</p>
        </header>

        <div className="input-container">
          <textarea
            className="message-textarea"
            placeholder="Paste a suspicious SMS message here to analyze its contents securely..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={loading}
          />

          <button 
            className="analyze-btn" 
            onClick={handleAnalyze} 
            disabled={!message.trim() || loading}
          >
            {loading ? (
              <>
                <Loader2 className="loader" size={20} />
                Analyzing Neural Threat...
              </>
            ) : (
              <>
                <Search size={20} />
                Analyze Message
              </>
            )}
          </button>
        </div>

        {error && (
          <div style={{ color: '#fca5a5', marginTop: '1rem', padding: '1rem', background: 'rgba(239,68,68,0.1)', borderRadius: '8px' }}>
            {error}
          </div>
        )}

        {result && (
          <div className={`results-banner ${result}`}>
            <h2 className="results-title">
              {result === 'spam' ? <ShieldAlert size={28} /> : <ShieldCheck size={28} />}
              {result === 'spam' ? 'THREAT DETECTED' : 'MESSAGE VERIFIED SAFE'}
            </h2>
            <p className="results-desc">
              {result === 'spam' 
                ? 'Our ML models flagged this as highly suspicious.' 
                : 'No malicious patterns were found in this text.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
