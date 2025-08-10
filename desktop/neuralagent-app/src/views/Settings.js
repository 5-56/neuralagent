import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { Text } from '../components/Elements/Typography';
import { Button } from '../components/Elements/Button';

const MODEL_TYPES = ['openai', 'azure_openai', 'anthropic', 'bedrock', 'ollama', 'gemini'];

export default function Settings() {
  const isDarkMode = useSelector(state => state.isDarkMode);

  const [overrideType, setOverrideType] = useState('');
  const [overrideId, setOverrideId] = useState('');

  const [plannerOverrideType, setPlannerOverrideType] = useState('');
  const [plannerOverrideId, setPlannerOverrideId] = useState('');

  const [mediaType, setMediaType] = useState('image/jpeg');
  const [jpegQuality, setJpegQuality] = useState(80);

  useEffect(() => {
    const load = async () => {
      const model = await window.electronAPI.getOverrideModel();
      const pmodel = await window.electronAPI.getOverridePlannerModel();
      const shot = await window.electronAPI.getScreenshotPrefs();
      setOverrideType(model?.type || '');
      setOverrideId(model?.id || '');
      setPlannerOverrideType(pmodel?.type || '');
      setPlannerOverrideId(pmodel?.id || '');
      setMediaType(shot?.mediaType || 'image/jpeg');
      setJpegQuality(Number(shot?.jpegQuality || 80));
    };
    load();
  }, []);

  const saveModel = async () => {
    await window.electronAPI.setOverrideModel(overrideType, overrideId);
  };

  const savePlannerModel = async () => {
    await window.electronAPI.setOverridePlannerModel(plannerOverrideType, plannerOverrideId);
  };

  const saveScreenshot = async () => {
    await window.electronAPI.setScreenshotPrefs(mediaType, Number(jpegQuality));
  };

  const fieldStyle = { marginBottom: 10, display: 'flex', gap: 8, alignItems: 'center' };
  const inputStyle = { padding: '6px 8px', borderRadius: 6, border: '1px solid #ccc', flex: 1 };
  const selectStyle = { padding: '6px 8px', borderRadius: 6, border: '1px solid #ccc' };

  return (
    <div style={{ padding: 16, color: isDarkMode ? '#fff' : '#000', width: '100%', overflowY: 'auto' }}>
      <Text fontSize='18px' fontWeight='600'>Custom Model</Text>
      <div style={fieldStyle}>
        <label style={{ width: 140 }}>Model Type</label>
        <select style={selectStyle} value={overrideType} onChange={(e) => setOverrideType(e.target.value)}>
          <option value=''>Use default (.env)</option>
          {MODEL_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div style={fieldStyle}>
        <label style={{ width: 140 }}>Model ID</label>
        <input style={inputStyle} placeholder='e.g. gpt-4o-mini' value={overrideId} onChange={(e) => setOverrideId(e.target.value)} />
      </div>
      <Button onClick={saveModel} style={{ marginBottom: 24 }}>Save Model</Button>

      <Text fontSize='18px' fontWeight='600'>Planner Model (optional)</Text>
      <div style={fieldStyle}>
        <label style={{ width: 140 }}>Model Type</label>
        <select style={selectStyle} value={plannerOverrideType} onChange={(e) => setPlannerOverrideType(e.target.value)}>
          <option value=''>Use default (.env)</option>
          {MODEL_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div style={fieldStyle}>
        <label style={{ width: 140 }}>Model ID</label>
        <input style={inputStyle} placeholder='e.g. gpt-4.1' value={plannerOverrideId} onChange={(e) => setPlannerOverrideId(e.target.value)} />
      </div>
      <Button onClick={savePlannerModel} style={{ marginBottom: 24 }}>Save Planner</Button>

      <Text fontSize='18px' fontWeight='600'>Screenshot</Text>
      <div style={fieldStyle}>
        <label style={{ width: 140 }}>Media Type</label>
        <select style={selectStyle} value={mediaType} onChange={(e) => setMediaType(e.target.value)}>
          <option value='image/jpeg'>image/jpeg (smaller, faster)</option>
          <option value='image/png'>image/png (lossless, larger)</option>
        </select>
      </div>
      {mediaType === 'image/jpeg' && (
        <div style={fieldStyle}>
          <label style={{ width: 140 }}>JPEG Quality</label>
          <input type='number' min={1} max={95} style={inputStyle} value={jpegQuality} onChange={(e) => setJpegQuality(e.target.value)} />
        </div>
      )}
      <Button onClick={saveScreenshot}>Save Screenshot</Button>
    </div>
  );
}