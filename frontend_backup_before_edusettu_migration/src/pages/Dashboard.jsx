import { useState } from 'react';
import Layout from '../components/Layout';
import Hero from '../components/Hero';
import MetricsStrip from '../components/MetricsStrip';
import TranslationWorkspace from '../components/TranslationWorkspace';
import IntegrityPanel from '../components/IntegrityPanel';
import Footer from '../components/Footer';

export default function Dashboard({ apiStatus }) {
  const [text, setText] = useState('');
  const [lang, setLang] = useState('hi');
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTranslate = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setOutput(null);

    try {
      const response = await fetch('http://localhost:8000/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, target_language: lang }),
      });
      const data = await response.json();
      setOutput(data);
      
      // Save to history
      if (!data.error) {
        const saved = localStorage.getItem('stembridge_history');
        const historyList = saved ? JSON.parse(saved) : [];
        historyList.unshift({
          id: Date.now().toString(),
          timestamp: Date.now(),
          source: text,
          lang: lang,
          translated: data.translated_text,
          metrics: {
            formula: data.formula_preserved,
            terminology: data.terminology_preserved,
            tech: data.technical_identifiers_preserved,
            morphology: data.morphology_preserved
          }
        });
        localStorage.setItem('stembridge_history', JSON.stringify(historyList));
      }
    } catch (err) {
      setOutput({ error: "Failed to connect to API" });
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setOutput(null);
  };

  return (
    <Layout apiStatus={apiStatus}>
      <Hero />
      <MetricsStrip />
      
      <TranslationWorkspace 
        text={text}
        setText={setText}
        lang={lang}
        setLang={setLang}
        output={output}
        loading={loading}
        onTranslate={handleTranslate}
        onClear={handleClear}
      />
      
      <IntegrityPanel output={output} lang={lang} />
      
      <Footer />
    </Layout>
  );
}
