import Layout from '../components/Layout';

const faqs = [
  {
    question: "What is EduSetu?",
    answer: "EduSetu is an educational accessibility platform concept that helps turn English educational text into Kannada or Hindi learning material."
  },
  {
    question: "How does the translation work?",
    answer: "This application uses a real FastAPI backend connected to the validated SIH translation pipeline (IndicTrans2-200M). It executes real model inference locally on your machine."
  },
  {
    question: "What happens to my data?",
    answer: "All translations are processed locally. Your history and settings are saved securely in your browser's local storage and are never uploaded to the cloud."
  }
];

export default function Help() {
  return (
    <Layout>
      <div className="page-intro edusetu-container">
        <p className="eyebrow">Help center</p>
        <h1>How EduSetu Works</h1>
        <p>A deep dive into the SIH translation pipeline.</p>
      </div>

      <div className="edusetu-container" style={{ paddingBottom: '3rem' }}>
        <div style={{ backgroundColor: 'var(--surface)', borderRadius: '1rem', border: '1px solid var(--line)', padding: '2.5rem', marginBottom: '3rem' }}>
          
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '1.5rem', color: 'var(--ink)' }}>The Translation Workflow</h2>
          <p style={{ color: 'var(--muted)', marginBottom: '2rem', lineHeight: '1.75' }}>
            EduSetu connects directly to a Python FastAPI backend which runs the validated IndicTrans2-200M model. 
            Unlike standard machine translation that often corrupts mathematical and technical context, our pipeline is designed specifically for STEM education.
          </p>

          <div style={{ display: 'grid', gap: '2rem', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
            
            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.5rem' }}>Hindi & Kannada Support</h3>
              <p style={{ color: 'var(--muted)', fontSize: '0.875rem', lineHeight: '1.6' }}>
                We currently support translating English source material into Hindi and Kannada, maintaining high fidelity for educational dialects in both target languages.
              </p>
            </div>

            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.5rem' }}>Formula Preservation</h3>
              <p style={{ color: 'var(--muted)', fontSize: '0.875rem', lineHeight: '1.6' }}>
                Our boundary-aware safe replacement algorithm protects mathematical formulas (like E = mc²) from being corrupted, translated literally, or hallucinated by the AI.
              </p>
            </div>

            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.5rem' }}>Technical Identifier Protection</h3>
              <p style={{ color: 'var(--muted)', fontSize: '0.875rem', lineHeight: '1.6' }}>
                Standalone variables (a, b, x, y) and programming terms (Python, NumPy) are shielded to ensure the logical flow of the lesson remains intact.
              </p>
            </div>

            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.5rem' }}>Terminology Protection</h3>
              <p style={{ color: 'var(--muted)', fontSize: '0.875rem', lineHeight: '1.6' }}>
                Standardized academic terminology is mapped directly. "Limits of integration" becomes "समाकलन की सीमाएँ", ensuring educational consistency.
              </p>
            </div>

            <div>
              <h3 style={{ fontSize: '1.125rem', fontWeight: 800, marginBottom: '0.5rem' }}>Kannada Morphology</h3>
              <p style={{ color: 'var(--muted)', fontSize: '0.875rem', lineHeight: '1.6' }}>
                When translating to Kannada, a specialized morphology engine ensures that protected terms are integrated smoothly into sentence structures using correct suffixes and grammar.
              </p>
            </div>

          </div>
        </div>
      </div>

      <div className="edusetu-container faq-grid" style={{ paddingBottom: '6rem' }}>
        <div>
          <div style={{ color: 'var(--orange-600)', marginBottom: '1rem' }}>
            <svg width="30" height="30" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          </div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>Frequently asked questions</h2>
          <p style={{ marginTop: '0.75rem', color: 'var(--muted)' }}>Quick answers to common questions about using the platform.</p>
        </div>
        
        <div className="faq-list">
          {faqs.map((faq, index) => (
            <details key={index} className="faq-item" open={index === 0}>
              <summary className="faq-summary">
                {faq.question}
                <span className="faq-icon" aria-hidden="true">+</span>
              </summary>
              <p className="faq-content">{faq.answer}</p>
            </details>
          ))}
        </div>
      </div>
    </Layout>
  );
}
