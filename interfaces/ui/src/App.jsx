import { useState } from 'react';
import './App.css';

function App() {
  const [projectRoot, setProjectRoot] = useState('');
  const [indexStatus, setIndexStatus] = useState('');
  const [isIndexing, setIsIndexing] = useState(false);

  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isChatting, setIsChatting] = useState(false);

  const handleIndex = async () => {
    if (!projectRoot) {
      setIndexStatus('Please enter a project root path.');
      return;
    }
    
    setIsIndexing(true);
    setIndexStatus('Indexing...');
    
    try {
      const res = await fetch('http://localhost:8000/index', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: projectRoot })
      });
      
      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`);
      }
      
      const data = await res.json();
      setIndexStatus(`Successfully indexed ${data.files_indexed || 0} files (${data.chunks_indexed || 0} chunks).`);
    } catch (err) {
      setIndexStatus(`Failed to index: ${err.message}`);
    } finally {
      setIsIndexing(false);
    }
  };

  const handleChat = async (e) => {
    e.preventDefault();
    if (!message.trim() || !projectRoot) return;

    const userMessage = { role: 'user', text: message };
    setChatHistory(prev => [...prev, userMessage]);
    setMessage('');
    setIsChatting(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.text, project_root: projectRoot })
      });

      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`);
      }

      const data = await res.json();
      const assistantMessage = { 
        role: 'assistant', 
        text: data.response,
        sources: data.sources || []
      };
      
      setChatHistory(prev => [...prev, assistantMessage]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'assistant', text: `Error: ${err.message}` }]);
    } finally {
      setIsChatting(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'system-ui, sans-serif' }}>
      <h1>Local Code Explainer</h1>
      
      <section style={{ marginBottom: '30px', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h2>1. Index Project</h2>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={projectRoot}
            onChange={(e) => setProjectRoot(e.target.value)}
            placeholder="/path/to/your/project"
            style={{ flex: 1, padding: '8px' }}
          />
          <button onClick={handleIndex} disabled={isIndexing} style={{ padding: '8px 16px' }}>
            {isIndexing ? 'Indexing...' : 'Index'}
          </button>
        </div>
        {indexStatus && <p style={{ marginTop: '10px', fontSize: '0.9em', color: '#555' }}>{indexStatus}</p>}
      </section>

      <section style={{ display: 'flex', flexDirection: 'column', height: '500px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <div style={{ padding: '15px', borderBottom: '1px solid #eee', backgroundColor: '#f9f9f9' }}>
          <h2 style={{ margin: 0 }}>2. Chat</h2>
        </div>
        
        <div style={{ flex: 1, padding: '15px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {chatHistory.length === 0 ? (
            <p style={{ color: '#888', textAlign: 'center', marginTop: 'auto', marginBottom: 'auto' }}>
              Ask a question about your indexed project.
            </p>
          ) : (
            chatHistory.map((msg, i) => (
              <div key={i} style={{ 
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: msg.role === 'user' ? '#007bff' : '#e9ecef',
                color: msg.role === 'user' ? 'white' : 'black',
                padding: '10px 15px',
                borderRadius: '8px',
                maxWidth: '80%',
                whiteSpace: 'pre-wrap',
                textAlign: 'left'
              }}>
                <div>{msg.text}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: `1px solid ${msg.role === 'user' ? '#4da3ff' : '#ccc'}`, fontSize: '0.85em' }}>
                    <strong>Sources:</strong>
                    <ul style={{ margin: '5px 0 0 0', paddingLeft: '20px' }}>
                      {msg.sources.map((src, idx) => (
                        <li key={idx}>
                          <code>{src.file_path}</code> (Line {src.start_line})
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))
          )}
          {isChatting && (
            <div style={{ alignSelf: 'flex-start', color: '#888', fontStyle: 'italic', padding: '10px 15px' }}>
              Assistant is typing...
            </div>
          )}
        </div>

        <form onSubmit={handleChat} style={{ display: 'flex', padding: '15px', borderTop: '1px solid #eee', gap: '10px' }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="e.g. How does the indexing work?"
            style={{ flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
            disabled={isChatting}
          />
          <button type="submit" disabled={isChatting || !message.trim()} style={{ padding: '10px 20px', borderRadius: '4px', border: 'none', backgroundColor: '#007bff', color: 'white', cursor: 'pointer' }}>
            Send
          </button>
        </form>
      </section>
    </div>
  );
}

export default App;
