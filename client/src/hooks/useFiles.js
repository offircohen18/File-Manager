import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as filesApi from "../api/filesApi";

export const useFiles = (user, search, fileType, sortBy) => {
  const queryClient = useQueryClient();

  const { data: files = [], isLoading } = useQuery({
    queryKey: ["files", user?.uid, search, fileType, sortBy],
    queryFn: () => filesApi.fetchFiles(user, search, fileType, sortBy),
    enabled: !!user,
  });

  const uploadMutation = useMutation({
    mutationFn: (files) => filesApi.uploadFiles(user, files),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["files"] }),
  });

  const deleteMutation = useMutation({
    mutationFn: (blobName) => filesApi.deleteFile(user, blobName),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["files"] }),
  });

  return { files, isLoading, uploadMutation, deleteMutation };
};
