import React, { useState, useRef } from 'react';
import { uploadFidelityCSV, uploadTradierCSV, uploadWebullCSV } from '../api';

export const CSVUpload: React.FC<{ onUploadSuccess: () => void }> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState<'fidelity' | 'tradier' | 'webull' | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const fidelityInputRef = useRef<HTMLInputElement>(null);
  const tradierInputRef = useRef<HTMLInputElement>(null);
  const webullInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (
    file: File | null,
    type: 'fidelity' | 'tradier' | 'webull'
  ) => {
    if (!file) return;

    setUploading(type);
    setError(null);
    setSuccess(null);

    try {
      if (type === 'fidelity') {
        await uploadFidelityCSV(file);
        setSuccess('Fidelity CSV uploaded successfully!');
      } else if (type === 'tradier') {
        await uploadTradierCSV(file);
        setSuccess('Tradier CSV uploaded successfully!');
      } else {
        await uploadWebullCSV(file);
        setSuccess('Webull CSV uploaded successfully!');
      }
      
      // Refresh positions after upload
      setTimeout(() => {
        onUploadSuccess();
        setSuccess(null);
      }, 1500);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setUploading(null);
    }
  };

  return (
    <div className="csv-upload">
      <div className="upload-buttons">
        <label className="upload-button">
          <input
            ref={fidelityInputRef}
            type="file"
            accept=".csv"
            onChange={(e) => handleFileSelect(e.target.files?.[0] || null, 'fidelity')}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="primary-button"
            disabled={uploading !== null}
            onClick={() => fidelityInputRef.current?.click()}
          >
            {uploading === 'fidelity' ? 'Uploading...' : '📁 Upload Fidelity CSV'}
          </button>
        </label>

        <label className="upload-button">
          <input
            ref={tradierInputRef}
            type="file"
            accept=".csv"
            onChange={(e) => handleFileSelect(e.target.files?.[0] || null, 'tradier')}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="primary-button"
            disabled={uploading !== null}
            onClick={() => tradierInputRef.current?.click()}
          >
            {uploading === 'tradier' ? 'Uploading...' : '📁 Upload Tradier CSV'}
          </button>
        </label>

        <label className="upload-button">
          <input
            ref={webullInputRef}
            type="file"
            accept=".csv"
            onChange={(e) => handleFileSelect(e.target.files?.[0] || null, 'webull')}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="primary-button"
            disabled={uploading !== null}
            onClick={() => webullInputRef.current?.click()}
          >
            {uploading === 'webull' ? 'Uploading...' : '📁 Upload Webull CSV'}
          </button>
        </label>
      </div>

      {error && (
        <div className="upload-message error">
          ⚠️ {error}
        </div>
      )}

      {success && (
        <div className="upload-message success">
          ✅ {success}
        </div>
      )}
    </div>
  );
};

