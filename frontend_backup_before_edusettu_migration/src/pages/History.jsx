import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Topbar from '../components/Topbar';

export default function History({ apiStatus }) {
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState('');
  const [filterLang, setFilterLang] = useState('all');

  useEffect(() => {
    const saved = localStorage.getItem('stembridge_history');
    if (saved) {
      try {
        setHistory(JSON.parse(saved));
      } catch (e) {
        setHistory([]);
      }
    }
  }, []);

  const handleClear = () => {
    if (confirm('Are you sure you want to clear all translation history?')) {
      localStorage.removeItem('stembridge_history');
      setHistory([]);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  const filteredHistory = history.filter(item => {
    const matchesSearch = item.source.toLowerCase().includes(search.toLowerCase()) || 
                          item.translated.toLowerCase().includes(search.toLowerCase());
    const matchesLang = filterLang === 'all' || item.lang === filterLang;
    return matchesSearch && matchesLang;
  });

  return (
    <Layout apiStatus={apiStatus}>
      <div className="history-header">
        <h1>Translation History</h1>
        <div className="history-controls">
          <input 
            type="text" 
            placeholder="Search history..." 
            className="history-search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select 
            className="history-filter"
            value={filterLang}
            onChange={(e) => setFilterLang(e.target.value)}
          >
            <option value="all">All Languages</option>
            <option value="hi">Hindi</option>
            <option value="kn">Kannada</option>
          </select>
          <button className="btn-secondary" onClick={handleClear}>Clear History</button>
        </div>
      </div>

      <div className="history-list">
        {filteredHistory.length === 0 ? (
          <div className="empty-state" style={{padding: '3rem'}}>
            No history found. Try making a translation on the dashboard.
          </div>
        ) : (
          filteredHistory.map((item) => (
            <div key={item.id} className="history-card">
              <div className="history-card-header">
                <span className="history-lang">{item.lang === 'hi' ? 'Hindi' : 'Kannada'}</span>
                <span className="history-time">{new Date(item.timestamp).toLocaleString()}</span>
              </div>
              <div className="history-content">
                <div className="history-source">
                  <div className="history-label">Source</div>
                  <div>{item.source}</div>
                </div>
                <div className="history-target">
                  <div className="history-label">Translation</div>
                  <div>{item.translated}</div>
                </div>
              </div>
              
              <div className="history-card-footer">
                <div className="history-metrics">
                  <span className={`metric-tag ${item.metrics.formula ? 'good' : 'bad'}`}>Formula</span>
                  <span className={`metric-tag ${item.metrics.terminology ? 'good' : 'bad'}`}>Terminology</span>
                  <span className={`metric-tag ${item.metrics.tech ? 'good' : 'bad'}`}>Identifiers</span>
                  {item.lang === 'kn' && (
                    <span className={`metric-tag ${item.metrics.morphology ? 'good' : 'bad'}`}>Morphology</span>
                  )}
                </div>
                <button className="btn-copy-small" onClick={() => handleCopy(item.translated)}>Copy output</button>
              </div>
            </div>
          ))
        )}
      </div>
    </Layout>
  );
}
