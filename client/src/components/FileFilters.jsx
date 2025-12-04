import { TextField, Select, MenuItem, InputLabel, FormControl } from "@mui/material";

export default function FileFilters({ search, setSearch, fileType, setFileType, sortBy, setSortBy }) {
  return (
    <div style={{ marginTop: 10, marginBottom: 10 }}>
      <TextField
        placeholder="Search by name"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginRight: 10 }}
      />
      <TextField
        placeholder="File type (.txt, .pdf, .json)"
        value={fileType}
        onChange={(e) => setFileType(e.target.value)}
        style={{ marginRight: 10 }}
      />
      <FormControl style={{ width: 150 }}>
        <InputLabel id="sort-by-label">Sort By</InputLabel>
        <Select
          labelId="sort-by-label"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <MenuItem value="">Sort by</MenuItem>
          <MenuItem value="date">Date</MenuItem>
          <MenuItem value="size">Size</MenuItem>
        </Select>
      </FormControl>
    </div>
  );
}
