import { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import FileUpload from '../components/FileUpload';

export default function Dashboard() {
  const [mode, setMode] = useState('text');
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  const [lang, setLang] = useState('hi');
  
  const [output, setOutput] = useState('');
  const [extractedText, setExtractedText] = useState('');
  
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [error, setError] = useState('');
  const [metrics, setMetrics] = useState(null);

  // Load preferences
  useEffect(() => {
    const defaultLang = localStorage.getItem('edusetu_default_lang');
    if (defaultLang) setLang(defaultLang);
  }, []);

  const saveHistory = (sourceType, sourceName, translatedOutput, m) => {
    const autoSave = localStorage.getItem('edusetu_auto_save');
    if (autoSave !== 'false') {
      const saved = localStorage.getItem('stembridge_history');
      const historyList = saved ? JSON.parse(saved) : [];
      historyList.unshift({
        id: Date.now().toString(),
        timestamp: Date.now(),
        sourceType: sourceType,
        source: sourceName,
        lang: lang,
        translated: translatedOutput,
        metrics: m
      });
      localStorage.setItem('stembridge_history', JSON.stringify(historyList));
    }
  };

  const handleTranslateText = async () => {
    if (loading) return; // Strict double-click prevention
    if (!text.trim()) {
      setError("Enter English educational content before translating.");
      return;
    }
    
    setLoading(true);
    setLoadingStage('Processing via API');
    setOutput('');
    setExtractedText('');
    setError('');
    setMetrics(null);

    try {
      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, target_language: lang }),
      });
      const data = await response.json();
      
      if (data.error) throw new Error(data.error);

      setOutput(data.translated_text);
      
      const newMetrics = {
        formula: data.formula_preserved,
        terminology: data.terminology_preserved,
        tech: data.technical_identifiers_preserved,
        morphology: data.morphology_preserved
      };
      setMetrics(newMetrics);
      saveHistory('text', text, data.translated_text, newMetrics);

    } catch (err) {
      setError("Failed to connect to the SIH API. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleTranslateFile = async () => {
    if (loading) return;
    if (!file) {
      setError("Please select a file to translate.");
      return;
    }

    setLoading(true);
    setLoadingStage('Uploading file...');
    setOutput('');
    setExtractedText('');
    setError('');
    setMetrics(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_language', lang);

    try {
      setLoadingStage('Extracting and Translating (this may take a minute)...');
      
      const response = await fetch('http://localhost:8000/translate/file', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || data.error || "Failed to process file.");
      }
      if (data.error) throw new Error(data.error);

      setExtractedText(data.extracted_text);
      setOutput(data.translated_text);
      
      const newMetrics = {
        formula: data.formula_preserved,
        terminology: data.terminology_preserved,
        tech: data.technical_identifiers_preserved,
        morphology: data.morphology_preserved
      };
      setMetrics(newMetrics);
      saveHistory('file', file.name, data.translated_text, newMetrics);

    } catch (err) {
      setError(err.message || "An unexpected error occurred during file translation.");
    } finally {
      setLoading(false);
      setLoadingStage('');
    }
  };

  const handleTranslate = () => {
    if (mode === 'text') handleTranslateText();
    else handleTranslateFile();
  };

  const handleClear = () => {
    setText('');
    setFile(null);
    setOutput('');
    setExtractedText('');
    setMetrics(null);
    setError('');
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(output);
  };

  const handleDownload = () => {
    if (!output) return;
    let ext = 'txt';
    if (mode === 'file' && file) {
      const originalExt = file.name.split('.').pop().toLowerCase();
      if (['srt', 'vtt', 'md', 'txt'].includes(originalExt)) {
        ext = originalExt;
      }
    }
    
    const blob = new Blob([output], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `translated_${lang}.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const renderStatus = (val) => {
    if (val === true) return <span className="status-verified">✓ Verified</span>;
    if (val === false) return <span className="status-review">⚠ Review</span>;
    return <span className="status-neutral">— Not evaluated</span>;
  };

  return (
    <Layout>
      <div className="translation-workspace-page">
        <div className="edusetu-container">
          
          <div className="page-intro" style={{ paddingTop: '1rem' }}>
            <p className="eyebrow">Translation workspace</p>
            <h1>Turn a lesson into accessible learning.</h1>
            <p style={{ fontSize: '0.875rem' }}>Powered by the validated SIH IndicTrans2 pipeline.</p>
          </div>

          <div className="mode-toggle-group">
            <button 
              className={`mode-toggle-btn ${mode === 'text' ? 'active' : ''}`}
              onClick={() => { setMode('text'); handleClear(); }}
            >
              Text
            </button>
            <button 
              className={`mode-toggle-btn ${mode === 'file' ? 'active' : ''}`}
              onClick={() => { setMode('file'); handleClear(); }}
            >
              Upload File
            </button>
          </div>

          <div className="translation-shell">
            {/* Source Panel */}
            <section className="translation-panel">
              <div className="panel-header">
                <div>
                  <p className="panel-label">Source language</p>
                  <h2 className="panel-title">English</h2>
                </div>
                {(text || file) && <button className="text-button" onClick={handleClear}>Clear</button>}
              </div>

              {mode === 'text' ? (
                <>
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste English educational content here..."
                    className="translation-textarea"
                    maxLength={3000}
                  />
                  <div className="panel-footer">
                    <p style={{ fontSize: '0.75rem', color: 'var(--muted)' }}>Paste or type classroom notes, definitions, or concepts.</p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--muted)' }}>{text.length} / 3,000</p>
                  </div>
                </>
              ) : (
                <div style={{ flex: 1, padding: '1rem', display: 'flex', flexDirection: 'column' }}>
                  {!file ? (
                    <FileUpload onFileSelect={(selected) => { setFile(selected); setError(''); }} />
                  ) : (
                    <div className="upload-file-card">
                      <div className="upload-file-info">
                        <div className="upload-file-icon">📄</div>
                        <div>
                          <div className="upload-file-name">{file.name}</div>
                          <div className="upload-file-size">{(file.size / 1024).toFixed(2)} KB</div>
                        </div>
                      </div>
                      <button className="upload-remove-btn" onClick={() => { setFile(null); setOutput(''); setExtractedText(''); }}>Remove</button>
                    </div>
                  )}
                  {extractedText && (
                    <div style={{ marginTop: '1rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                      <p style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--muted)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>Extracted Text</p>
                      <textarea
                        readOnly
                        value={extractedText}
                        className="translation-textarea"
                        style={{ border: '1px solid var(--line)', background: 'var(--soft)' }}
                      />
                    </div>
                  )}
                </div>
              )}
            </section>

            {/* Controls */}
            <div className="translation-control-column">
              <div style={{ width: '100%' }}>
                <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--muted)', marginBottom: '0.5rem' }}>
                  Translate to
                </label>
                <select value={lang} onChange={(e) => setLang(e.target.value)} className="language-select" disabled={loading}>
                  <option value="kn">ಕನ್ನಡ — Kannada</option>
                  <option value="hi">हिन्दी — Hindi</option>
                </select>
              </div>
              
              <button 
                className="button-primary" 
                style={{ width: '100%' }} 
                onClick={handleTranslate} 
                disabled={loading || (mode === 'text' && !text.trim()) || (mode === 'file' && !file)}
              >
                {loading ? 'Translating...' : mode === 'text' ? 'Translate' : 'Extract & Translate'}
              </button>
              
              <div className="status-track">
                <span className={!loading && !output ? "status-dot-active" : "status-dot"}></span>
                <span className={loading ? "status-dot-active" : "status-dot"}></span>
                <span className={output && !loading ? "status-dot-complete" : "status-dot"}></span>
              </div>
              <span className="status-label">
                {!loading && !output ? "Ready" : (loading ? (loadingStage || "Processing...") : "Completed")}
              </span>
            </div>

            {/* Output Panel */}
            <section className="translation-panel">
              <div className="panel-header">
                <div>
                  <p className="panel-label">Translation output</p>
                  <h2 className="panel-title lang-text">
                    {lang === 'hi' ? 'हिन्दी' : 'ಕನ್ನಡ'} <span style={{ color: 'var(--muted)', fontSize: '0.875rem' }}>{lang === 'hi' ? 'Hindi' : 'Kannada'}</span>
                  </h2>
                </div>
                {output && <button className="text-button" onClick={() => { setOutput(''); setMetrics(null); setExtractedText(''); }}>Clear</button>}
              </div>
              
              <div className="output-area">
                {loading ? (
                  <div className="loading-state">
                    <div className="icon-circle indigo">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="animate-spin"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>
                    </div>
                    <p style={{ marginTop: '1.25rem', fontWeight: 700 }}>Processing translation...</p>
                    <p style={{ fontSize: '0.875rem', color: 'var(--muted)', marginTop: '0.5rem' }}>{loadingStage || 'Calling FastAPI backend'}</p>
                  </div>
                ) : output ? (
                  <div className="output-content lang-text">{output}</div>
                ) : (
                  <div className="empty-state">
                    <div className="icon-circle gray">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2-2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    </div>
                    <p style={{ marginTop: '1.25rem', fontWeight: 700 }}>Your translation will appear here</p>
                    <p style={{ fontSize: '0.875rem', color: 'var(--muted)', marginTop: '0.5rem', maxWidth: '16rem' }}>
                      {mode === 'text' ? 'Add English educational content and click translate to begin.' : 'Upload an English file to translate its contents.'}
                    </p>
                  </div>
                )}
              </div>
              
              <div className="panel-footer" style={{ justifyContent: 'flex-start', gap: '0.5rem' }}>
                <button className="output-action" onClick={handleCopy} disabled={!output}>Copy</button>
                {mode === 'file' && <button className="output-action primary" onClick={handleDownload} disabled={!output}>Download</button>}
              </div>
            </section>
          </div>
          
          {error && (
            <div style={{ marginTop: '1.25rem', padding: '0.75rem 1rem', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: '0.75rem', color: '#991b1b', fontSize: '0.875rem', fontWeight: 600 }}>
              {error}
            </div>
          )}

          {/* Integrity Panel */}
          {metrics && (
            <div className="integrity-panel">
              <h3><svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg> Translation integrity</h3>
              <div className="integrity-grid">
                <div className="integrity-item">
                  <span className="integrity-item-label">Formula Preservation</span>
                  <span className="integrity-item-status">{renderStatus(metrics.formula)}</span>
                </div>
                <div className="integrity-item">
                  <span className="integrity-item-label">Technical Identifiers</span>
                  <span className="integrity-item-status">{renderStatus(metrics.tech)}</span>
                </div>
                <div className="integrity-item">
                  <span className="integrity-item-label">Terminology Protection</span>
                  <span className="integrity-item-status">{renderStatus(metrics.terminology)}</span>
                </div>
                <div className="integrity-item">
                  <span className="integrity-item-label">Kannada Morphology</span>
                  <span className="integrity-item-status">{lang === 'kn' ? renderStatus(metrics.morphology) : renderStatus(null)}</span>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </Layout>
  );
}
