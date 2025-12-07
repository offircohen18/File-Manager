import { Button, Typography } from "@mui/material";
import { useState } from "react";

const ALLOWED_EXTENSIONS = [".json", ".txt", ".pdf"];

export default function UploadInput({ selectedFiles, setSelectedFiles, uploadMutation }) {
  const [localError, setLocalError] = useState("");

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    const invalidFiles = files.filter((file) => {
      const ext = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();
      return !ALLOWED_EXTENSIONS.includes(ext);
    });

    if (invalidFiles.length > 0) {
      setLocalError(`Invalid file type: ${invalidFiles.map(f => f.name).join(", ")}`);
      setSelectedFiles([]);
    } else {
      setLocalError("");
      setSelectedFiles(files);
    }
  };

  const handleUpload = () => {
    if (!selectedFiles.length || localError) return;

    uploadMutation.mutate(selectedFiles, {
      onError: (error) => {
        const message = error.response?.data?.detail || "Upload failed, please try again.";
        setLocalError(message);
      },
      onSuccess: () => {
        setSelectedFiles([]);
        setLocalError("");
      },
    });
  };

  return (
    <div style={{ marginTop: 10, marginBottom: 10 }}>
      <input type="file" multiple onChange={handleFileChange} />
      <Button
        variant="contained"
        style={{ marginLeft: 10 }}
        onClick={handleUpload}
        disabled={!selectedFiles.length || !!localError}
      >
        Upload
      </Button>
      {localError && <Typography color="error" variant="body2">{localError}</Typography>}
    </div>
  );
}
