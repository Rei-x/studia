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
import { useEffect, useState } from "react";
import type { FilePublic } from "@/client";
import { searchPlugin } from "@react-pdf-viewer/search";
import { PDFHighlight } from "@pdf-highlight/react-pdf-highlight";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { ScrollArea } from "./ui/scroll-area";
export const pdfAtom = atom<{
  file:
    | {
        id: string;
        filename: string;
      }
    | undefined;
  highlight: string | undefined;
}>({
  file: undefined,
  highlight: undefined,
});

export const PdfViewer = () => {
  const defaultLayoutPluginInstance = defaultLayoutPlugin();
  const [pdfState, setPdfState] = useAtom(pdfAtom);
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
      <Dialog
        open={pdfState.file !== undefined}
        onOpenChange={(open) => {
          if (!open) {
            setPdfState({ file: undefined, highlight: pdfState.highlight });
          }
        }}
      >
        <DialogContent className="max-h-80">
          <DialogHeader>
            <DialogTitle>{pdfState.file?.filename}</DialogTitle>
          </DialogHeader>
          <ScrollArea className="text-sm max-h-64 p-4 overflow-hidden prose">
            {pdfState.highlight}
          </ScrollArea>
        </DialogContent>
      </Dialog>
    </Worker>
  );
};
