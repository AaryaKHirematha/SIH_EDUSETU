export default function SourcePanel({ text, setText, onClear }) {
  const examples = [
    { category: "Physics", text: "The famous equation E = mc² describes the relationship between energy and mass." },
    { category: "Mathematics", text: "The limits of integration are from a to b." },
    { category: "Computer Science", text: "Python and NumPy are widely used in data science." }
  ];

  return (
    <div className="panel">
      <div className="panel-header">
        <div className="panel-title">English content</div>
      </div>
      <div className="panel-body">
        <textarea 
          className="source-input"
          placeholder="Paste a scientific paragraph, equation, technical definition or programming concept…"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="input-footer">
          <span>{text.length} characters</span>
          <button className="btn-clear" onClick={onClear}>Clear</button>
        </div>
        
        <div className="quick-start">
          <h3>Quick Start (Validated examples)</h3>
          <div className="example-cards">
            {examples.map((ex, idx) => (
              <div key={idx} className="example-card" onClick={() => setText(ex.text)}>
                <div className="example-category">{ex.category}</div>
                <div className="example-text">{ex.text}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
