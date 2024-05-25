import { deleteFileFilesFileIdDelete, type FilePublic } from "@/client";
import { useMutation } from "@tanstack/react-query";
import { FileIcon, DownloadIcon, Loader2Icon, EyeIcon } from "lucide-react";
import prettyBytes from "pretty-bytes";
import React, { useState } from "react";
import { Button } from "../ui/button";
import { motion } from "framer-motion";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "../ui/context-menu";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { useDrag } from "react-dnd";
import { PDFPreview } from "../PDFPreview";

export const File = (file: FilePublic) => {
  const { mutateAsync, isPending } = useMutation({
    mutationFn: async () => {
      return deleteFileFilesFileIdDelete({ fileId: file.id });
    },
  });

  const [collected, drag, dragPreview] = useDrag(() => ({
    type: "file",
    item: file,
    collect(monitor) {
      return {
        isDragging: monitor.isDragging(),
      };
    },
  }));

  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 1, y: 0, x: -10 }}
      animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
      exit={{ opacity: 0, scale: 1, y: 0, x: 10 }}
    >
      {collected.isDragging ? (
        <div
          ref={dragPreview}
          key={file.id}
          className={cn(
            "flex items-center justify-between transition-colors ease-in-out duration-300 bg-white dark:bg-gray-950 p-4 rounded-lg shadow-sm",
            { "bg-gray-100 dark:bg-gray-900": isOpen },
            { "opacity-50": isPending }
          )}
        >
          <div className="flex items-center space-x-4">
            <FileIcon className="h-6 w-6 text-gray-500 " />
            <div>
              <p className="font-medium">{file.filename}</p>
              <p className="text-sm text-gray-500 ">{prettyBytes(file.size)}</p>
            </div>
          </div>
          <Button
            onClick={() => {}}
            size="icon"
            variant="ghost"
            className="hover:bg-slate-200"
          >
            <EyeIcon className="h-5 w-5 text-gray-500" />
          </Button>
        </div>
      ) : (
        <div ref={drag}>
          <ContextMenu
            onOpenChange={(open) => {
              setIsOpen(open);
            }}
          >
            <ContextMenuTrigger disabled={isPending}>
              <div
                key={file.id}
                className={cn(
                  "flex items-center justify-between transition-colors ease-in-out duration-300 bg-white dark:bg-gray-950 p-4 rounded-lg shadow-sm",
                  { "bg-gray-100 dark:bg-gray-900": isOpen },
                  { "opacity-50": isPending }
                )}
              >
                <div className="flex items-center space-x-4">
                  <FileIcon className="h-6 w-6 text-gray-500 " />
                  <div>
                    <p className="font-medium">{file.filename}</p>
                    <p className="text-sm text-gray-500 ">
                      {prettyBytes(file.size)}
                    </p>
                  </div>
                </div>
                <PDFPreview
                  pdfState={{
                    file: {
                      id: file.id,
                      filename: file.filename,
                    },
                  }}
                >
                  <Button
                    size="icon"
                    variant="ghost"
                    className="hover:bg-slate-200"
                  >
                    <EyeIcon className="h-5 w-5 text-gray-500" />
                  </Button>
                </PDFPreview>
              </div>
            </ContextMenuTrigger>
            <ContextMenuContent>
              <ContextMenuItem
                onSelect={(e) => {
                  const loadingId = toast.loading("Deleting file...");
                  mutateAsync()
                    .then(() => {
                      toast.dismiss(loadingId);
                    })
                    .catch(() => {
                      toast.error("Failed to delete file", { id: loadingId });
                    });
                }}
                className="flex gap-2"
              >
                <span>Delete</span>
              </ContextMenuItem>
            </ContextMenuContent>
          </ContextMenu>
        </div>
      )}
    </motion.div>
  );
};
