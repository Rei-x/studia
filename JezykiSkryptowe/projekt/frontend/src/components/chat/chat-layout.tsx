"use client";

import React, { createContext, useContext, useState } from "react";
import { Sidebar } from "../sidebar";
import { Chat } from "./chat";
import {
  filesFilesGet,
  threadsThreadsGet,
  uploadFileUploadPost,
  type ThreadPublicWithMessages,
  deleteFileFilesFileIdDelete,
} from "@/client";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useRouter } from "next/router";
import { v4 as uuid } from "uuid";
import Head from "next/head";
import prettyBytes from "pretty-bytes";
import {
  FileInput,
  FileUploader,
  FileUploaderContent,
  FileUploaderItem,
} from "../ui/file-upload";
import { Loader2, Paperclip } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "../ui/button";
import { toast } from "sonner";
import { DownloadIcon, FileIcon } from "@radix-ui/react-icons";
import { File } from "../files/File";
import { AnimatePresence } from "framer-motion";
import { ScrollArea } from "../ui/scroll-area";

const FileSvgDraw = () => {
  return (
    <>
      <svg
        className="w-8 h-8 mb-3 text-gray-500 dark:text-gray-400"
        aria-hidden="true"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 20 16"
      >
        <path
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
        />
      </svg>
      <p className="mb-1 text-sm text-gray-500 dark:text-gray-400">
        <span className="font-semibold">Click to upload</span>
        &nbsp;or drag and drop
      </p>
      <p className="text-xs text-gray-500 dark:text-gray-400">PDF</p>
    </>
  );
};

const FileUpload = () => {
  const [files, setFiles] = useState<File[] | null>(null);

  const { mutateAsync, isPending } = useMutation({
    mutationFn: async (files: File[]) => {
      return uploadFileUploadPost({
        formData: { files },
      });
    },
  });

  return (
    <div className={cn(isPending && "pointer-events-none", "h-auto")}>
      <FileUploader
        value={files}
        onValueChange={setFiles}
        dropzoneOptions={{
          maxFiles: 20,
          maxSize: 1024 * 1024 * 4,
          multiple: true,
          accept: {
            "application/pdf": [".pdf"],
          },
        }}
        className={cn(
          "relative bg-background rounded-lg p-2 transition-all duration-300 ease-in-out",
          isPending && "opacity-50"
        )}
      >
        <FileInput className={cn("outline-dashed outline-1 outline-white")}>
          <div className="flex items-center justify-center flex-col pt-3 pb-4 w-full ">
            <FileSvgDraw />
          </div>
        </FileInput>

        <ScrollArea className="max-h-32">
          <FileUploaderContent>
            {files &&
              files.length > 0 &&
              files.map((file, i) => (
                <FileUploaderItem key={i} index={i}>
                  <Paperclip className="h-4 w-4 stroke-current" />
                  <span>{file.name}</span>
                </FileUploaderItem>
              ))}
          </FileUploaderContent>
        </ScrollArea>
        <Button
          onClick={() => {
            if (files) {
              mutateAsync(files)
                .then(() => {
                  toast.success("Files uploaded successfully");
                  setFiles(null);
                })
                .catch(() => {
                  toast.error("Failed to upload files");
                });
            }
          }}
          disabled={!files || files?.length === 0 || isPending}
          className="w-auto"
        >
          {isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
          Upload
        </Button>
      </FileUploader>
    </div>
  );
};

const ThreadContext = createContext({
  selectedThreadId: "",
});

export const useSelectedThread = () => {
  return useContext(ThreadContext);
};

export function ChatLayout() {
  const selectedThreadId = useRouter().query.id as string;

  const { data: threads } = useQuery({
    queryKey: ["threads"],
    queryFn: async () => threadsThreadsGet(),
    refetchInterval: 1000,
  });

  const { data: files } = useQuery({
    queryKey: ["files"],
    queryFn: async () => filesFilesGet(),
    refetchInterval: 1000,
  });

  const selectedThread =
    threads?.find((thread) => thread.id === selectedThreadId) ??
    ({
      id: selectedThreadId ?? uuid(),
      title: "Start chating",
      messages: [],
    } as ThreadPublicWithMessages);

  return (
    <ThreadContext.Provider value={{ selectedThreadId }}>
      <div className="h-full flex w-full items-stretch">
        <Sidebar
          threads={
            threads?.map((thread) => ({
              title: thread.title,
              id: thread.id,
              variant: selectedThread.id === thread.id ? "grey" : "ghost",
              messages: thread.messages,
            })) ?? []
          }
        />
        <Head>
          <title>{selectedThread.title}</title>
        </Head>

        <Chat selectedThread={selectedThread} />
        <div className="w-[500px] flex flex-col justify-between">
          <div>
            <h2 className="text-2xl font-medium mb-4 mx-4 mt-4">Documents</h2>
            <ScrollArea className="space-y-4 max-h-full">
              <AnimatePresence mode="popLayout">
                {files?.map((file) => (
                  <File key={`side-${file.id}`} {...file} />
                ))}
              </AnimatePresence>
            </ScrollArea>
          </div>

          <div>
            <hr className="mt-auto" />
            <FileUpload />
          </div>
        </div>
      </div>
    </ThreadContext.Provider>
  );
}
