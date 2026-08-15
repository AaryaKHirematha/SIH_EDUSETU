export default function IntegrityPanel({ output, lang }) {
  const renderStatus = (statusValue) => {
    if (!output || statusValue === undefined) return <span className="status-neutral">Not evaluated</span>;
    if (statusValue === null) return <span className="status-neutral">Not evaluated</span>;
    
    if (statusValue) {
      return (
        <span className="status-verified">
          <svg style={{width: '16px', marginRight: '4px'}} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
          Verified
        </span>
      );
    } else {
      return (
        <span className="status-review">
          <svg style={{width: '16px', marginRight: '4px'}} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          Review
        </span>
      );
    }
  };

  return (
    <div className="integrity-panel">
      <div className="integrity-header">
        <div className="integrity-kicker">Output Assurance</div>
        <div className="integrity-title">Translation integrity</div>
      </div>
      
      <div className="integrity-grid">
        <div className="integrity-item">
          <div className="integrity-label">Formula preservation</div>
          <div className="integrity-status">{renderStatus(output?.formula_preserved)}</div>
        </div>
        
        <div className="integrity-item">
          <div className="integrity-label">Terminology preservation</div>
          <div className="integrity-status">{renderStatus(output?.terminology_preserved)}</div>
        </div>
        
        <div className="integrity-item">
          <div className="integrity-label">Technical identifiers</div>
          <div className="integrity-status">{renderStatus(output?.technical_identifiers_preserved)}</div>
        </div>
        
        <div className="integrity-item">
          <div className="integrity-label">Kannada morphology</div>
          <div className="integrity-status">
            {lang === 'hi' ? <span className="status-neutral">Not evaluated</span> : renderStatus(output?.morphology_preserved)}
          </div>
        </div>
      </div>
      
      <div className="integrity-note">
        * Structural assurance reflects the protected pipeline checks. Linguistic fluency is validated on the critical human-review subset.
      </div>
    </div>
  );
}
