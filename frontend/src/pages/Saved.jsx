import Layout from '../components/Layout';

export default function Saved() {
  return (
    <Layout>
      <div className="page-intro edusetu-container">
        <p className="eyebrow">Your curated library</p>
        <h1>Saved Translations</h1>
        <p>Save important translations here so you can easily reference them later.</p>
      </div>

      <div className="edusetu-container" style={{ paddingBottom: '4rem' }}>
        <div className="empty-state" style={{ minHeight: '300px', backgroundColor: 'var(--soft)', borderRadius: '1rem', border: '1px solid var(--line)' }}>
          <div className="icon-circle gray">
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path></svg>
          </div>
          <p style={{ marginTop: '1.25rem', fontWeight: 700 }}>No saved translations</p>
          <p style={{ fontSize: '0.875rem', color: 'var(--muted)', marginTop: '0.5rem' }}>Translations you save from the workspace will appear here.</p>
        </div>
      </div>
    </Layout>
  );
}
