export default function MetricsStrip() {
  return (
    <div className="metrics-strip">
      <div className="metric-card">
        <div className="metric-label">Formula integrity</div>
        <div className="metric-value">100%</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Terminology</div>
        <div className="metric-value">100%</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Identifier safety</div>
        <div className="metric-value">100%</div>
      </div>
      <div className="metric-card">
        <div className="metric-label">Peak VRAM</div>
        <div className="metric-value">475 MB</div>
      </div>
    </div>
  );
}
