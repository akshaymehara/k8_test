import React, { useState } from "react";
import TimeDisplay from "./TimeComponent";

const FileForm = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [downloadStatus, setDownloadStatus] = useState("");

  // Handle file upload change
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // Handle file download name change
  const handleFileNameChange = (e) => {
    setFileName(e.target.value);
  };

  // Handle file upload action
  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const backendUrl = import.meta.env.VITE_REACT_APP_BACKEND_URL;
      try {
        const response = await fetch(`${backendUrl}/uploadfile/`, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setUploadStatus("File uploaded successfully!");
          console.log("Upload Response:", data);
        } else {
          setUploadStatus("Failed to upload the file.");
        }
      } catch (error) {
        setUploadStatus("An error occurred during the upload.");
        console.error("Error:", error);
      }
    } else {
      alert("Please select a file to upload.");
    }
  };

  // Handle file download action (dummy)
  const handleDownload = () => {
    if (fileName) {
      // Simulate a file download (or trigger an API call)
      setDownloadStatus(
        `File "${fileName}" downloaded successfully (simulated).`
      );
      console.log("Downloading:", fileName);
    } else {
      alert("Please enter a filename to download.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <div className="text-2xl font-bold mb-6 text-center">
          <TimeDisplay/>
        </div>
        <h2 className="text-2xl font-bold mb-6 text-center">
          File Upload & Download
        </h2>

        {/* File Upload Section */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload File
          </label>
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none"
          />
        </div>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition mb-2"
        >
          Upload File
        </button>

        {/* Upload Status */}
        {uploadStatus && (
          <p className="text-sm text-green-500 mt-2">{uploadStatus}</p>
        )}

        {/* File Download Section */}
        <div className="mb-4 mt-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Download File
          </label>
          <input
            type="text"
            value={fileName}
            onChange={handleFileNameChange}
            placeholder="Enter filename to download"
            className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        {/* Download Button */}
        <button
          onClick={handleDownload}
          className="w-full px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition"
        >
          Download File
        </button>

        {/* Download Status */}
        {downloadStatus && (
          <p className="text-sm text-blue-500 mt-2">{downloadStatus}</p>
        )}
      </div>
    </div>
  );
};

export default FileForm;
