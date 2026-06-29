import { useState } from "react";
import UploadBox from "./components/UploadBox";

function App() {
  const [images, setImages] = useState([]);

  return (
    <div className="app">
      <h1>🤖 FaceSort AI</h1>

      <p>Organize thousands of photos using AI.</p>

      <UploadBox onUpload={setImages} />

      <h3>{images.length} photos selected</h3>

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