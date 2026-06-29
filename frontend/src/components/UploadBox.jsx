function UploadBox({ onUpload }) {
  const handleChange = (event) => {
    const files = Array.from(event.target.files);
    onUpload(files);
  };

  return (
    <div>
      <input
        type="file"
        multiple
        accept="image/*"
        onChange={handleChange}
      />
    </div>
  );
}

export default UploadBox;