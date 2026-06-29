function App() {
  return (
    <div className="app">
      <h1>🤖 FaceSort AI</h1>

      <p>Organize thousands of photos in seconds using AI.</p>

      <button>📂 Upload Folder</button>

      <div className="stats">
        <div className="card">
          <h2>0</h2>
          <span>Total Photos</span>
        </div>

        <div className="card">
          <h2>0</h2>
          <span>With Faces</span>
        </div>

        <div className="card">
          <h2>0</h2>
          <span>Without Faces</span>
        </div>
      </div>
    </div>
  );
}

export default App;