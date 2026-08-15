import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (email && password) {
      // Mock authentication: accept any non-empty email/password
      localStorage.setItem('stembridge_auth', 'true');
      navigate('/');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <div className="brand-title">STEMBridge</div>
          <div className="brand-subtitle">Translation Intelligence</div>
        </div>
        
        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label>Email address</label>
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@stembridge.ai"
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>
          
          <button type="submit" className="btn-primary" style={{marginTop: '1rem'}}>
            Sign In →
          </button>
        </form>
        
        <div className="login-footer">
          SIH Validation Build · v1.0
        </div>
      </div>
    </div>
  );
}
