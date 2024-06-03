import "./App.css";
import axios from "axios";
import { useState } from "react";

const App = () => {
  const [url, setUrl] = useState("");
  const [prediction, setPrediction] = useState("");
  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleClear = () => {
    setUrl("");
    setPrediction("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setPrediction("Đang phân loại ...");
      const response = await axios.post(`http://127.0.0.1:8000/predict`, {
        url,
      });
      setPrediction(response.data.genre);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };
  return (
    <div
      className="App"
      style={{
        fontSize: 32,
        height: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#f0f0f0",
      }}
    >
      <div
        style={{
          top: "-10%",
          width: "50%",
          padding: "20px",
          textAlign: "center",
          position: "relative",
          borderRadius: "15px",
          background: "#1e3a8a",
          boxShadow: "0 4px 8px rgba(1, 2, 3, 0.5)",
        }}
      >
        <h3>Phân loại nhạc</h3>
        <form className="form-container">
          <input
            value={url}
            className="file-input"
            placeholder="youtube link"
            onChange={handleUrlChange}
          />
          <div style={{ display: "flex", gap: "10px" }}>
            <button onClick={handleClear} className="clear-button">
              Xoá
            </button>
            <button
              onClick={handleSubmit}
              type="submit"
              className="classify-button"
            >
              Phân loại
            </button>
          </div>
        </form>
        {prediction && <p>{prediction}</p>}
      </div>
    </div>
  );
};

export default App;
