import { useState } from "react";
import UploadBox from "./components/UploadBox";

function App() {
  const [images, setImages] = useState([]);
  const [isScanning, setIsScanning] = useState(false);

  const startScan = () => {
    if (images.length === 0) {
      alert("Please upload some images first!");
      return;
    }

    setIsScanning(true);

    // Fake AI Scan (we'll replace this with Python later)
    setTimeout(() => {
      setIsScanning(false);
      alert("✅ Scan Completed! Backend integration coming next.");
    }, 3000);
  };

  return (
    <div className="app">
      <h1>🤖 FaceSort AI</h1>

      <p>Organize thousands of photos using AI.</p>

      <UploadBox onUpload={setImages} />

      <div className="stats">
        <div className="card">
          <h2>{images.length}</h2>
          <p>Total Photos</p>
        </div>

        <div className="card">
          <h2>0</h2>
          <p>With Faces</p>
        </div>

        <div className="card">
          <h2>0</h2>
          <p>Without Faces</p>
        </div>
      </div>

      <button
        className="scan-btn"
        onClick={startScan}
        disabled={isScanning}
      >
        {isScanning ? "⏳ Scanning..." : "🚀 Start AI Scan"}
      </button>

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