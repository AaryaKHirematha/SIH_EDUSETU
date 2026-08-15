export default function Footer() {
  return (
    <footer style={{ borderTop: '1px solid var(--line)', padding: '2rem 0', marginTop: 'auto', backgroundColor: 'var(--surface)' }}>
      <div className="edusetu-container" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'center' }}>
        <div className="edusetu-brand" style={{ fontSize: '1.125rem' }}>
          Edu<span>Setu</span>
        </div>
        <p style={{ color: 'var(--muted)', fontSize: '0.875rem' }}>Education without language barriers.</p>
        <p style={{ color: 'var(--muted)', fontSize: '0.75rem', marginTop: '1rem' }}>
          © {new Date().getFullYear()} EduSetu / SIH Demonstration. Not connected to a live model.
        </p>
      </div>
    </footer>
  );
}
