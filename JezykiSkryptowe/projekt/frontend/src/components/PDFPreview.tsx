import { Button, ScrollMode, Viewer, Worker } from "@react-pdf-viewer/core";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";

import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";
import "@react-pdf-viewer/highlight/lib/styles/index.css";
import "@react-pdf-viewer/search/lib/styles/index.css";
import { atom } from "jotai/vanilla";
import { useAtom } from "jotai/react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import { highlightPlugin } from "@react-pdf-viewer/highlight";
import { useEffect, useState, type ReactNode } from "react";
import type { FilePublic } from "@/client";
import { searchPlugin } from "@react-pdf-viewer/search";
import { PDFHighlight } from "@pdf-highlight/react-pdf-highlight";
import { ScrollArea } from "./ui/scroll-area";

export const PDFPreview = ({
  children,
  pdfState,
}: {
  children: ReactNode;
  pdfState: {
    file: {
      id: string;
      filename: string;
    };
  };
}) => {
  const defaultLayoutPluginInstance = defaultLayoutPlugin();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setIsVisible(true);
    }
  }, []);

  if (!isVisible) {
    return null;
  }

  return (
    <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.js">
      <Dialog>
        <DialogTrigger>{children}</DialogTrigger>
        <DialogContent className="h-screen max-w-screen-lg">
          <DialogHeader>
            <DialogTitle>{pdfState.file.filename}</DialogTitle>
          </DialogHeader>
          <div className="overflow-y-scroll">
            <Viewer
              fileUrl={`http://localhost:8000/files/${pdfState.file?.id}`}
              plugins={[defaultLayoutPluginInstance]}
            />
          </div>
        </DialogContent>
      </Dialog>
    </Worker>
  );
};
