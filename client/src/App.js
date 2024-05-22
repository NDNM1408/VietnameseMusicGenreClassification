import "./App.css";
import axios from "axios";
import { useState } from "react";

const App = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setPrediction(response.data.prediction);
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
        <h3>Audio Classification</h3>
        <form onSubmit={handleSubmit} className="form-container">
          <input
            type="file"
            onChange={handleFileChange}
            accept="audio/*"
            className="file-input"
          />
          <button type="submit" className="classify-button">
            Classify
          </button>
        </form>
        {prediction && <p>Prediction: {prediction}</p>}
      </div>
    </div>
  );
};

export default App;
