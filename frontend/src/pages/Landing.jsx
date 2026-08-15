import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

export default function Landing() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="edusetu-hero">
        <div className="edusetu-hero-bg"></div>
        <div className="edusetu-container edusetu-hero-content">
          <div style={{ maxWidth: '48rem' }}>
            <p style={{ fontSize: '4rem', fontWeight: 900, lineHeight: 1 }}>
              Edu<span style={{ color: 'var(--orange-300)' }}>Setu</span>
            </p>
            <h1>Education without language barriers.</h1>
            <p>Transform English educational content into accessible Kannada and Hindi learning material, with a simple workspace built for focused study.</p>
            <div className="hero-actions">
              <Link to="/translate" className="button-accent">Start Translating →</Link>
              <a href="#how-it-works" className="button-ghost-light">See How It Works ↓</a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="how-it-works" style={{ backgroundColor: 'var(--paper)', padding: '5rem 0' }}>
        <div className="edusetu-container">
          <div style={{ maxWidth: '42rem', marginBottom: '4rem' }}>
            <p className="eyebrow">Built for education</p>
            <h2 className="section-title">Translation with a purpose beyond words.</h2>
            <p className="section-copy">EduSetu focuses the experience on educational access, so learners can spend less time navigating tools and more time understanding concepts.</p>
          </div>
          
          <div className="features-grid">
            <div className="feature-list">
              <div className="feature-item">
                <span className="feature-num">01</span>
                <div>
                  <h3 className="feature-title">English to Kannada</h3>
                  <p className="feature-desc">Make English educational explanations available to Kannada-speaking learners.</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-num">02</span>
                <div>
                  <h3 className="feature-title">English to Hindi</h3>
                  <p className="feature-desc">Turn classroom-ready English content into clear Hindi learning material.</p>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-num">03</span>
                <div>
                  <h3 className="feature-title">Educational context</h3>
                  <p className="feature-desc">A focused experience designed around lessons, concepts, and academic language. Preserves critical formulas and terminology.</p>
                </div>
              </div>
            </div>
            
            <div style={{ backgroundColor: 'var(--soft)', padding: '3rem', borderRadius: '1rem', border: '1px solid var(--line)' }}>
              <p className="eyebrow">Integrity First</p>
              <h3 style={{ fontSize: '1.5rem', fontWeight: 800, marginTop: '1rem', marginBottom: '1.5rem' }}>The SIH Pipeline</h3>
              <p style={{ color: 'var(--muted)', marginBottom: '1rem' }}>Behind EduSetu is the validated SIH translation pipeline powered by IndicTrans2-200M.</p>
              <ul style={{ color: 'var(--ink)', fontWeight: 600, display: 'flex', flexDirection: 'column', gap: '0.75rem', paddingLeft: '1.5rem' }}>
                <li>Formula Preservation (e.g. E = mc²)</li>
                <li>Technical Identifier Protection (Python, a, b)</li>
                <li>Hindi / Kannada Terminology Mapping</li>
                <li>Kannada Morphology Rules Engine</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{ backgroundColor: '#fff7ed', padding: '4rem 0' }}>
        <div className="edusetu-container" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '2rem' }}>
          <div>
            <p className="eyebrow">Ready to begin?</p>
            <h2 style={{ fontSize: '2.25rem', fontWeight: 800, marginTop: '0.5rem', letterSpacing: '-0.04em' }}>Bring the next lesson closer.</h2>
          </div>
          <Link to="/translate" className="button-primary">Open translation workspace →</Link>
        </div>
      </section>
    </Layout>
  );
}
