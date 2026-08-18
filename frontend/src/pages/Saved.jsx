import { useState, useEffect } from 'react';
import Layout from '../components/Layout';

export default function Saved() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('stembridge_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to parse history", e);
      }
    }
  }, []);

  const handleDownload = (item) => {
    if (!item.translated) return;
    let ext = 'txt';
    if (item.sourceType === 'video') {
      ext = 'srt';
    } else if (item.sourceType === 'file' && item.source) {
      const originalExt = item.source.split('.').pop().toLowerCase();
      if (['srt', 'vtt', 'md', 'txt'].includes(originalExt)) {
        ext = originalExt;
      }
    }
    
    const blob = new Blob([item.translated], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `translated_${item.lang}.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const formatDate = (timestamp) => {
    if (!timestamp) return 'Unknown Date';
    return new Date(timestamp).toLocaleString();
  };

  const getSourceDisplay = (item) => {
    if (item.sourceType === 'text') {
      return item.source.length > 60 ? item.source.substring(0, 60) + '...' : item.source;
    }
    return item.source;
  };

  const getStatus = (metrics) => {
    if (!metrics) return "—";
    // simplified status
    const passed = Object.values(metrics).filter(v => v === true).length;
    const total = Object.values(metrics).filter(v => v !== null).length;
    if (total === 0) return "—";
    if (passed === total) return "Verified";
    return "Review";
  };

  return (
    <Layout>
      <div className="page-intro edusetu-container">
        <p className="eyebrow">Your curated library</p>
        <h1>Saved Translations</h1>
        <p>Save important translations here so you can easily reference them later.</p>
      </div>

      <div className="edusetu-container" style={{ paddingBottom: '4rem' }}>
        {history.length === 0 ? (
          <div className="empty-state" style={{ minHeight: '300px', backgroundColor: 'var(--soft)', borderRadius: '1rem', border: '1px solid var(--line)' }}>
            <div className="icon-circle gray">
              <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
            </div>
            <p style={{ marginTop: '1.25rem', fontWeight: 700 }}>No saved translations</p>
            <p style={{ fontSize: '0.875rem', color: 'var(--muted)', marginTop: '0.5rem' }}>Translations you save from the workspace will appear here.</p>
          </div>
        ) : (
          <div className="history-list">
            {history.map(item => (
              <div key={item.id} className="history-item">
                <div className="history-meta">
                  <span className={`history-type-badge ${item.sourceType}`}>{item.sourceType}</span>
                  <span className="history-date">{formatDate(item.timestamp)}</span>
                </div>
                <div className="history-main">
                  <div className="history-source">{getSourceDisplay(item)}</div>
                  <div className="history-details">
                    <span className="history-lang">
                      To: <strong>{item.lang === 'hi' ? 'Hindi' : 'Kannada'}</strong>
                    </span>
                    <span className={`history-status status-${getStatus(item.metrics).toLowerCase()}`}>
                      Status: {getStatus(item.metrics)}
                    </span>
                  </div>
                </div>
                <div className="history-actions">
                  <button className="button-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.75rem', minHeight: 'auto' }} onClick={() => handleDownload(item)}>
                    Download
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}
