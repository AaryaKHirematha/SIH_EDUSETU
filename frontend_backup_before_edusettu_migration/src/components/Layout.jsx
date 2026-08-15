import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function Layout({ children, apiStatus }) {
  return (
    <div className="app-container">
      <Sidebar />
      <div className="main-content">
        <Topbar apiStatus={apiStatus} />
        <div className="page-content">
          {children}
        </div>
      </div>
    </div>
  );
}
