import { useState } from "react";
import UploadBox from "./components/UploadBox";

function App() {
  const [images, setImages] = useState([]);
  const [isScanning, setIsScanning] = useState(false);

  const [stats, setStats] = useState({
    total: 0,
    with_faces: 0,
    without_faces: 0,
    scan_time: 0,
  });

  const startScan = async () => {
    if (images.length === 0) {
      alert("Please upload some images first!");
      return;
    }

    setIsScanning(true);

    const formData = new FormData();

    images.forEach((image) => {
      formData.append("files", image);
    });

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      setStats(data);
    } catch (error) {
      alert("❌ Backend connection failed.");
      console.error(error);
    }

    setIsScanning(false);
  };

  const downloadResults = () => {
    window.open("http://127.0.0.1:8000/download", "_blank");
  };

  return (
    <div className="app">
      <h1>🤖 FaceSort AI</h1>

      <p>Organize thousands of photos using AI.</p>

      <UploadBox onUpload={setImages} />

      <div className="stats">

        <div className="card">
          <h2>{stats.total || images.length}</h2>
          <p>📸 Total Photos</p>
        </div>

        <div className="card">
          <h2>{stats.with_faces}</h2>
          <p>👤 People</p>
        </div>

        <div className="card">
          <h2>{stats.without_faces}</h2>
          <p>🖼 No People</p>
        </div>

        <div className="card">
          <h2>{stats.scan_time}s</h2>
          <p>⚡ Scan Time</p>
        </div>

      </div>

      <button
        className="scan-btn"
        onClick={startScan}
        disabled={isScanning}
      >
        {isScanning ? "⏳ AI is Scanning..." : "🚀 Start AI Scan"}
      </button>

      {stats.total > 0 && (
        <button
          className="scan-btn"
          onClick={downloadResults}
          style={{ marginTop: "15px" }}
        >
          📥 Download Sorted Images
        </button>
      )}

      <div className="gallery">
        {images.map((image, index) => (
          <img
            key={index}
            src={URL.createObjectURL(image)}
            alt={image.name}
            className="preview-image"
          />
        ))}
      </div>
    </div>
  );
}

export default App;