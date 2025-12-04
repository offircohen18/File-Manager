import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from "@mui/material";
import * as filesApi from "../api/filesApi";

export default function FileTable({ files, user, userRole, deleteMutation }) {
  return (
    <TableContainer component={Paper} style={{ marginTop: 20 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Filename</TableCell>
            <TableCell>Size (bytes)</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {files.map((file) => {
            const canDelete = userRole === "admin" ? file.user_id === user.uid : true;
            return (
              <TableRow key={file.blob_name}>
                <TableCell>{file.filename}</TableCell>
                <TableCell>{file.size}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => filesApi.downloadFile(user, file.blob_name, file.filename)}
                    style={{ marginRight: 8 }}
                  >
                    Download
                  </Button>
                  <Button
                    variant="outlined"
                    color="error"
                    size="small"
                    onClick={() => deleteMutation.mutate(file.blob_name)}
                    disabled={!canDelete}
                  >
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
