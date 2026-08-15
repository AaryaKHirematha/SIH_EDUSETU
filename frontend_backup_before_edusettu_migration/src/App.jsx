import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import History from './pages/History';

function ProtectedRoute({ children }) {
  const isAuthenticated = localStorage.getItem('stembridge_auth') === 'true';
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function App() {
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          setApiStatus('online');
        }
      })
      .catch(() => setApiStatus('offline'));
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <Dashboard apiStatus={apiStatus} />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/history" 
          element={
            <ProtectedRoute>
              <History apiStatus={apiStatus} />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
