import SourcePanel from './SourcePanel';
import TargetPanel from './TargetPanel';

export default function TranslationWorkspace({ text, setText, lang, setLang, output, loading, onTranslate, onClear }) {
  return (
    <div className="workspace-grid">
      <SourcePanel text={text} setText={setText} onClear={onClear} />
      <TargetPanel 
        lang={lang} 
        setLang={setLang} 
        loading={loading} 
        output={output} 
        onTranslate={onTranslate} 
        text={text}
      />
    </div>
  );
}
