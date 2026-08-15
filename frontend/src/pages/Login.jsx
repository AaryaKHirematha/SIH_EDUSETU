import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email && password) {
      localStorage.setItem('stembridge_auth', 'true');
      navigate('/translate');
    } else {
      setError('Please enter both email and password.');
    }
  };

  return (
    <div className="edusetu-app">
      <Header />
      <main className="login-split">
        <div className="login-left">
          <h1>Edu<span style={{ color: 'var(--orange-300)' }}>Setu</span></h1>
          <p>Access your personal translation workspace, saved materials, and translation history.</p>
        </div>
        
        <div className="login-right">
          <div className="login-card">
            <h2>Welcome back</h2>
            <p>Sign in to your EduSetu workspace</p>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">Email address</label>
                <input 
                  type="email" 
                  className="form-input" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="student@university.edu"
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Password</label>
                <input 
                  type="password" 
                  className="form-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                />
              </div>
              
              {error && <div style={{ color: 'var(--orange-600)', fontSize: '0.875rem', marginBottom: '1rem', fontWeight: 600 }}>{error}</div>}
              
              <button type="submit" className="button-primary" style={{ width: '100%', marginTop: '0.5rem' }}>
                Sign In →
              </button>
            </form>
            
            <p style={{ marginTop: '1.5rem', textAlign: 'center', color: 'var(--muted)', fontSize: '0.75rem' }}>
              For demonstration purposes, any email and password will work.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
