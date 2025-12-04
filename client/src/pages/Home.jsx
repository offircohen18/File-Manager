import { useEffect, useState } from "react";
import { Button } from "@mui/material";
import UploadInput from "../components/UploadInput";
import FileFilters from "../components/FileFilters";
import FileTable from "../components/FileTable";
import { useFiles } from "../hooks/useFiles";
import { auth, provider, signInWithPopup, signOut } from "../firebaseConfig";

export default function Home() {
  const [user, setUser] = useState(null);
  const [userRole, setUserRole] = useState("user");
  const [selectedFiles, setSelectedFiles] = useState([]);

  // Load preferences from localStorage
  const [search, setSearch] = useState(localStorage.getItem("search") || "");
  const [fileType, setFileType] = useState(localStorage.getItem("fileType") || "");
  const [sortBy, setSortBy] = useState(localStorage.getItem("sortBy") || "");

  const { files, isLoading, uploadMutation, deleteMutation } = useFiles(user, search, fileType, sortBy);

  // Save preferences to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("search", search);
  }, [search]);

  useEffect(() => {
    localStorage.setItem("fileType", fileType);
  }, [fileType]);

  useEffect(() => {
    localStorage.setItem("sortBy", sortBy);
  }, [sortBy]);

  const handleLogin = async () => {
    const result = await signInWithPopup(auth, provider);
    setUser(result.user);
    const tokenResult = await result.user.getIdTokenResult();
    setUserRole(tokenResult.claims.role || "user");
  };

  const handleLogout = async () => {
    await signOut(auth);
    setUser(null);
    setUserRole("user");
  };

  return (
    <div style={{ padding: 20 }}>
      {!user ? (
        <Button variant="contained" onClick={handleLogin}>
          Login with Google
        </Button>
      ) : (
        <>
          <Button variant="outlined" onClick={handleLogout}>
            Logout
          </Button>
          <h2>
            Welcome {user.displayName} {userRole === "admin" && "(Admin)"}
          </h2>

          <UploadInput
            selectedFiles={selectedFiles}
            setSelectedFiles={setSelectedFiles}
            uploadMutation={uploadMutation}
          />

          <FileFilters
            search={search}
            setSearch={setSearch}
            fileType={fileType}
            setFileType={setFileType}
            sortBy={sortBy}
            setSortBy={setSortBy}
          />

          {isLoading ? (
            <p>Loading files...</p>
          ) : (
            <FileTable
              files={files}
              user={user}
              userRole={userRole}
              deleteMutation={deleteMutation}
            />
          )}
        </>
      )}
    </div>
  );
}
