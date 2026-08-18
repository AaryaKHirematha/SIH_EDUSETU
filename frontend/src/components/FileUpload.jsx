import React, { useState, useRef } from 'react';

export default function FileUpload({ onFileSelect, supportedExtensions = ['txt', 'pdf', 'docx', 'srt', 'vtt', 'md'], maxSize = 10 * 1024 * 1024, accept = ".txt,.pdf,.docx,.srt,.vtt,.md" }) {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFile = (file) => {
    setError('');
    if (!file) return false;

    const ext = file.name.split('.').pop().toLowerCase();
    if (!supportedExtensions.includes(ext)) {
      setError(`Unsupported file type. Please upload TXT, PDF, DOCX, SRT, VTT, or MD.`);
      return false;
    }
    if (file.size > maxSize) {
      setError(`File is too large. Maximum supported size is ${maxSize / (1024 * 1024)} MB.`);
      return false;
    }
    return true;
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        onFileSelect(file);
      }
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        onFileSelect(file);
      }
    }
  };

  return (
    <div className="file-upload-container">
      <div 
        className={`upload-drop-zone ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
      >
        <input 
          type="file" 
          ref={inputRef}
          onChange={handleChange}
          accept={accept}
          style={{ display: 'none' }}
        />
        
        <div className="upload-content">
          <div className="upload-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <h3 className="upload-title">Upload File</h3>
          <p className="upload-subtitle">Drag & drop your file here</p>
          <div className="upload-or">or</div>
          <button className="button-secondary upload-browse-btn" onClick={(e) => { e.stopPropagation(); inputRef.current.click(); }}>
            Browse Files
          </button>
          <div className="upload-meta">
            {supportedExtensions.map(e => e.toUpperCase()).join(' · ')}<br/>
            Max {maxSize / (1024 * 1024)} MB
          </div>
        </div>
      </div>
      {error && <div className="upload-error-message">{error}</div>}
    </div>
  );
}
