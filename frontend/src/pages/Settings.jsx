import { useState, useEffect } from 'react';
import Layout from '../components/Layout';

export default function Settings() {
  const [defaultLang, setDefaultLang] = useState('kn');
  const [autoSave, setAutoSave] = useState(true);
  const [appearance, setAppearance] = useState('light');
  
  useEffect(() => {
    const savedLang = localStorage.getItem('edusetu_default_lang');
    if (savedLang) setDefaultLang(savedLang);
    
    const savedAutoSave = localStorage.getItem('edusetu_auto_save');
    if (savedAutoSave !== null) setAutoSave(savedAutoSave === 'true');
    
    const savedApp = localStorage.getItem('edusetu_appearance');
    if (savedApp) setAppearance(savedApp);
  }, []);

  const handleSave = () => {
    localStorage.setItem('edusetu_default_lang', defaultLang);
    localStorage.setItem('edusetu_auto_save', autoSave.toString());
    localStorage.setItem('edusetu_appearance', appearance);
    
    if (appearance === 'dark') {
      document.documentElement.classList.add('dark-mode');
    } else {
      document.documentElement.classList.remove('dark-mode');
    }
    
    alert('Settings saved successfully!');
  };

  return (
    <Layout>
      <div className="page-intro edusetu-container">
        <p className="eyebrow">Preferences</p>
        <h1>Settings</h1>
        <p>Manage your translation preferences.</p>
      </div>

      <div className="edusetu-container" style={{ paddingBottom: '4rem' }}>
        <div style={{ maxWidth: '32rem', backgroundColor: 'var(--surface)', borderRadius: '1rem', border: '1px solid var(--line)', padding: '2rem' }}>
          
          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label className="form-label" style={{ fontSize: '0.875rem', color: 'var(--ink)' }}>Default Target Language</label>
            <p style={{ fontSize: '0.75rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>This language will be pre-selected in the translation workspace.</p>
            <select 
              className="language-select" 
              value={defaultLang} 
              onChange={(e) => setDefaultLang(e.target.value)}
              style={{ width: '100%' }}
            >
              <option value="kn">Kannada</option>
              <option value="hi">Hindi</option>
            </select>
          </div>

          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <label className="form-label" style={{ fontSize: '0.875rem', color: 'var(--ink)' }}>Auto-save Translations</label>
            <p style={{ fontSize: '0.75rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>Automatically save successful translations to your history.</p>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={autoSave} 
                onChange={(e) => setAutoSave(e.target.checked)} 
                style={{ width: '1rem', height: '1rem', accentColor: 'var(--indigo)' }}
              />
              <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>Enable Auto-save</span>
            </label>
          </div>

          <div className="form-group" style={{ marginBottom: '2.5rem' }}>
            <label className="form-label" style={{ fontSize: '0.875rem', color: 'var(--ink)' }}>Appearance</label>
            <p style={{ fontSize: '0.75rem', color: 'var(--muted)', marginBottom: '0.5rem' }}>Choose your preferred color theme.</p>
            <select 
              className="language-select" 
              value={appearance} 
              onChange={(e) => setAppearance(e.target.value)}
              style={{ width: '100%' }}
            >
              <option value="light">Light</option>
              <option value="dark">Dark (if supported)</option>
              <option value="system">System Default</option>
            </select>
          </div>

          <button className="button-primary" onClick={handleSave} style={{ width: '100%' }}>Save Preferences</button>
        </div>
      </div>
    </Layout>
  );
}
