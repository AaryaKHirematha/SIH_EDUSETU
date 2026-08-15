import Header from './Header';
import Footer from './Footer';

export default function Layout({ children }) {
  return (
    <div className="edusetu-app">
      <Header />
      <main className="edusetu-main">
        {children}
      </main>
      <Footer />
    </div>
  );
}
