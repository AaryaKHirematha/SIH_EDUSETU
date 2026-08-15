export default function Topbar({ apiStatus }) {
  return (
    <div className="topbar">
      <div className="topbar-title">
        Workspace / Translation Studio
      </div>
      
      <div className="topbar-actions">
        <div className={`api-status ${apiStatus === 'online' ? '' : 'offline'}`}>
          <div className="status-dot" style={{backgroundColor: 'currentColor'}}></div>
          {apiStatus === 'online' ? 'API Connected' : 'API Offline'}
        </div>
      </div>
    </div>
  );
}
