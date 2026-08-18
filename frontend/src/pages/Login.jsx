import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';

export default function Login() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (email && password) {
      setLoading(true);
      setError('');
      try {
        const endpoint = isLogin ? '/auth/login' : '/auth/signup';
        const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          throw new Error(data.detail || 'Authentication failed');
        }
        
        if (isLogin) {
          localStorage.setItem('stembridge_auth', data.access_token);
          navigate('/translate');
        } else {
          // Auto login after signup
          const loginResp = await fetch(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/auth/login`, {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ email, password })
          });
          const loginData = await loginResp.json();
          if (loginResp.ok) {
            localStorage.setItem('stembridge_auth', loginData.access_token);
            navigate('/translate');
          } else {
             setIsLogin(true);
             setError('Account created. Please log in.');
          }
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
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
            <h2>{isLogin ? 'Welcome back' : 'Create an account'}</h2>
            <p>{isLogin ? 'Sign in to your EduSetu workspace' : 'Join EduSetu to start translating'}</p>
            
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
              
              <button type="submit" className="button-primary" style={{ width: '100%', marginTop: '0.5rem' }} disabled={loading}>
                {loading ? 'Processing...' : (isLogin ? 'Sign In →' : 'Sign Up →')}
              </button>
            </form>
            
            <p style={{ marginTop: '1.5rem', textAlign: 'center', color: 'var(--muted)', fontSize: '0.875rem' }}>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button 
                onClick={() => { setIsLogin(!isLogin); setError(''); }}
                style={{ background: 'none', border: 'none', color: 'var(--orange-500)', fontWeight: 600, cursor: 'pointer', padding: 0 }}
              >
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
