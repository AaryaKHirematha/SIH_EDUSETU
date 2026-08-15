import { useState } from 'react';

export default function TargetPanel({ lang, setLang, loading, output, onTranslate, text }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (output && output.translated_text) {
      navigator.clipboard.writeText(output.translated_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">Translation output</div>
        <select className="lang-select" value={lang} onChange={(e) => setLang(e.target.value)}>
          <option value="hi">हिन्दी · Hindi</option>
          <option value="kn">ಕನ್ನಡ · Kannada</option>
        </select>
      </div>
      <div className="panel-body">
        <div className="output-area">
          {loading ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <div className="loading-text">Running protected translation</div>
              <div className="loading-subtext">Preserving formulas, identifiers and STEM terminology…</div>
            </div>
          ) : output ? (
            output.error ? (
              <div style={{color: '#ef4444'}}>Error: {output.error}</div>
            ) : (
              <div style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
                <div style={{flex: 1}}>{output.translated_text}</div>
              </div>
            )
          ) : (
            <div className="empty-state">Waiting for input...</div>
          )}
        </div>
        
        <button 
          className="btn-primary" 
          onClick={onTranslate} 
          disabled={loading || !text.trim()}
        >
          {loading ? "Translating…" : "Translate →"}
        </button>

        {output && !loading && !output.error && (
          <div className="target-footer">
            <button className="btn-copy" onClick={handleCopy}>
              {copied ? "Copied!" : "Copy output"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
