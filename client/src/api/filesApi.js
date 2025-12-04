import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

export const fetchFiles = async (user, search, fileType, sortBy) => {
  if (!user) return [];
  const token = await user.getIdToken();
  const params = {};
  if (search) params.search = search;
  if (fileType) params.file_type = fileType;
  if (sortBy) params.sort_by = sortBy;

  const res = await axios.get(`${BASE_URL}/files`, {
    headers: { Authorization: `Bearer ${token}` },
    params,
  });
  return res.data;
};

export const uploadFiles = async (user, files) => {
  if (!user || !files.length) return;
  const token = await user.getIdToken();
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  await axios.post(`${BASE_URL}/upload`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });
};

export const deleteFile = async (user, blobName) => {
  if (!user) return;
  const token = await user.getIdToken();
  await axios.delete(`${BASE_URL}/delete/${encodeURIComponent(blobName)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const downloadFile = async (user, blobName, filename) => {
  if (!user) return;
  const token = await user.getIdToken();
  const res = await axios.get(`${BASE_URL}/download/${encodeURIComponent(blobName)}`, {
    headers: { Authorization: `Bearer ${token}` },
    responseType: "blob",
  });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  link.remove();
};
