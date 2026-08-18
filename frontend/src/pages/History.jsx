import { useState, useEffect } from 'react';
import Layout from '../components/Layout';

export default function History() {
  const [history, setHistory] = useState([]);
  
  useEffect(() => {
    const saved = localStorage.getItem('stembridge_history');
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  const handleClear = () => {
    if (window.confirm("Clear all translation history from this browser?")) {
      localStorage.removeItem('stembridge_history');
      setHistory([]);
    }
  };

  const handleDelete = (id) => {
    const updated = history.filter(item => item.id !== id);
    localStorage.setItem('stembridge_history', JSON.stringify(updated));
    setHistory(updated);
  };

  return (
    <Layout>
      <div className="page-intro edusetu-container">
        <p className="eyebrow">Your learning trail</p>
        <h1>Translation history</h1>
        <p>Revisit recent work, reopen a lesson, or continue it in another language.</p>
        {history.length > 0 && (
          <button className="button-secondary" onClick={handleClear} style={{ marginTop: '1.5rem' }}>
            <svg width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" style={{ marginRight: '0.35rem' }}><path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            Clear history
          </button>
        )}
      </div>

      <div className="edusetu-container" style={{ paddingBottom: '4rem' }}>
        {history.length === 0 ? (
          <div className="empty-state" style={{ minHeight: '300px', backgroundColor: 'var(--soft)', borderRadius: '1rem', border: '1px solid var(--line)' }}>
            <div className="icon-circle gray">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </div>
            <p style={{ marginTop: '1.25rem', fontWeight: 700 }}>No history found</p>
            <p style={{ fontSize: '0.875rem', color: 'var(--muted)', marginTop: '0.5rem' }}>Your translated text will appear here automatically.</p>
          </div>
        ) : (
          <div className="history-grid">
            {history.map((item) => (
              <div key={item.id} className="history-card">
                <div className="history-header">
                  <span className="history-lang-badge">EN → {item.lang.toUpperCase()}</span>
                  <span className="history-date">{new Date(item.timestamp).toLocaleString()}</span>
                </div>
                
                <div className="history-content">
                  <div className="history-col">
                    <h4>{item.sourceType === 'file' ? 'Source File' : item.sourceType === 'video' ? 'Source Video' : 'Source'}</h4>
                    <p>
                      {item.sourceType === 'file' && <span style={{display:'inline-block', marginRight:'0.25rem'}}>📄</span>}
                      {item.sourceType === 'video' && <span style={{display:'inline-block', marginRight:'0.25rem'}}>🎬</span>}
                      {item.source}
                    </p>
                  </div>
                  <div className="history-col">
                    <h4>Translation</h4>
                    <p className="lang-text">{item.translated}</p>
                  </div>
                </div>

                <div className="history-footer">
                  <div className="history-metrics">
                    <span className={`metric-pill ${item.metrics?.formula ? 'success' : item.metrics?.formula === false ? 'warning' : ''}`}>Formula: {item.metrics?.formula ? '✓' : item.metrics?.formula === false ? '⚠' : '-'}</span>
                    <span className={`metric-pill ${item.metrics?.tech ? 'success' : item.metrics?.tech === false ? 'warning' : ''}`}>Tech: {item.metrics?.tech ? '✓' : item.metrics?.tech === false ? '⚠' : '-'}</span>
                    <span className={`metric-pill ${item.metrics?.terminology ? 'success' : item.metrics?.terminology === false ? 'warning' : ''}`}>Terminology: {item.metrics?.terminology ? '✓' : item.metrics?.terminology === false ? '⚠' : '-'}</span>
                  </div>
                  <div className="history-actions">
                    <button className="output-action" onClick={() => navigator.clipboard.writeText(item.translated)}>Copy</button>
                    {item.sourceType === 'video' && (
                      <button className="output-action" onClick={() => {
                        const blob = new Blob([item.translated], { type: 'text/plain;charset=utf-8' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `translated_${item.lang}.srt`;
                        a.click();
                        URL.revokeObjectURL(url);
                      }}>Download SRT</button>
                    )}
                    <button className="output-action" style={{ color: '#ef4444' }} onClick={() => handleDelete(item.id)}>Delete</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
