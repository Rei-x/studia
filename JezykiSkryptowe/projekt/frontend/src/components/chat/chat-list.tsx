import { cn } from "@/lib/utils";
import React, { useRef } from "react";
import { Avatar, AvatarImage } from "../ui/avatar";
import ChatBottombar from "./chat-bottombar";
import { AnimatePresence, motion } from "framer-motion";
import type { MessagePublic } from "@/client";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { FileIcon } from "@radix-ui/react-icons";
import { ScrollArea, ScrollBar } from "../ui/scroll-area";
import type { Document, Search } from "@/lib/types";
import { useSetAtom } from "jotai/react";
import { pdfAtom } from "../PdfViewer";
import Image from "next/image";
import { ImageFallback } from "../ImageFallback";

interface ChatListProps {
  messages: MessagePublic[];

  sendMessage: (newMessage: { content: string }) => void;
}

const KnowledgeBase = ({ message }: { message: MessagePublic }) => {
  const setPdfState = useSetAtom(pdfAtom);
  return (
    <span className="p-3 rounded-md">
      <span className="font-bold">📚 Knowledge Base</span>
      <ScrollArea className="max-w-screen-md mt-2 border rounded-md">
        <div className="flex space-x-4 p-8 max-w-full">
          {JSON.parse(message.content).map((item: Document) => (
            <div
              key={item.page_content}
              className="group relative cursor-pointer overflow-hidden rounded-lg shadow-lg hover:shadow-xl transition-transform duration-300 ease-in-out hover:-translate-y-1"
              onClick={() =>
                setPdfState({
                  file: {
                    id: item.metadata.id,
                    filename: item.metadata.filename,
                  },
                  highlight: item.page_content,
                })
              }
            >
              <div className="bg-gray-100 p-6 dark:bg-gray-800">
                <FileIcon className="h-10 w-10 text-gray-500 dark:text-gray-400" />
              </div>
              <div className="bg-white p-4 dark:bg-gray-950">
                <h3 className="font-semibold text-lg truncate">
                  {item.metadata.filename}
                </h3>
                <p className="text-xs w-36 text-gray-500 line-clamp-3 max-h-32 dark:text-gray-400">
                  {item.page_content.split("\n").join(" ")}
                </p>
              </div>
            </div>
          ))}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </span>
  );
};

const Search = ({ message }: { message: MessagePublic }) => {
  const searchData = JSON.parse(message.content) as Search[];

  return (
    <div>
      <div className="flex items-center">
        <span className="text-xl">📄</span>
        <h2 className="text-lg font-semibold mb-2 ml-1">Sources</h2>
      </div>
      <div className="flex gap-4">
        <ScrollArea className="max-w-screen-md mt-2 border rounded-md">
          <div className="flex space-x-4 p-8 max-w-full">
            {searchData.map((source) => (
              <div
                key={source.content}
                className="bg-slate-100 relative w-max flex items-center rounded-lg shadow-lg hover:shadow-xl transition-transform duration-300 ease-in-out group hover:-translate-y-1 gap-2 p-4"
              >
                <ImageFallback
                  src={`https://api.statvoo.com/favicon/${
                    new URL(source.url).hostname
                  }`}
                  fallbackSrc={"/favicon.ico"}
                  alt={""}
                  width={48}
                  height={48}
                  className="mr-3 w-12 h-12"
                />
                <div>
                  <a
                    className="block group-hover:underline after:inset-0 after:absolute font-semibold"
                    href={source.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {new URL(source.url).hostname}
                  </a>
                  <p className="text-xs   line-clamp-3 max-w-40 text-gray-500">
                    {source.content}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      </div>
    </div>
  );
};

const ToolOutput = ({ message }: { message: MessagePublic }) => {
  return (
    <span className="p-3 rounded-md">
      {message.tool_name === "baza_wiedzy" && (
        <KnowledgeBase message={message} />
      )}
      {message.tool_name === "google_search" && <Search message={message} />}
    </span>
  );
};

const NormalMessageContent = ({ message }: { message: MessagePublic }) => {
  return (
    <span className="bg-accent p-3 rounded-md max-w-xs">
      <Markdown
        components={{
          h1: ({ className, ...props }) => (
            <h1
              className={cn(
                "mt-2 scroll-m-20 text-2xl font-bold tracking-tight",
                className
              )}
              {...props}
            />
          ),
          h2: ({ className, ...props }) => (
            <h2
              className={cn(
                "scroll-m-20 border-b pb-1 text-1xl font-semibold tracking-tight first:mt-0",
                className
              )}
              {...props}
            />
          ),
          h3: ({ className, ...props }) => (
            <h3
              className={cn(
                "scroll-m-20 font-semibold tracking-tight",
                className
              )}
              {...props}
            />
          ),
          h4: ({ className, ...props }) => (
            <h4
              className={cn(
                "scroll-m-20 text-xl font-semibold tracking-tight",
                className
              )}
              {...props}
            />
          ),
          h5: ({ className, ...props }) => (
            <h5
              className={cn(
                "scroll-m-20 text-lg font-semibold tracking-tight",
                className
              )}
              {...props}
            />
          ),
          h6: ({ className, ...props }) => (
            <h6
              className={cn(
                "scroll-m-20 text-base font-semibold tracking-tight",
                className
              )}
              {...props}
            />
          ),
          a: ({ className, ...props }) => (
            <a
              className={cn(
                "font-medium underline underline-offset-4",
                className
              )}
              {...props}
            />
          ),
          p: ({ className, ...props }) => (
            <p
              className={cn("leading-7 [&:not(:first-child)]:mt-2", className)}
              {...props}
            />
          ),
          ul: ({ className, ...props }) => (
            <ul className={cn("my-2 ml-6 list-disc", className)} {...props} />
          ),
          ol: ({ className, ...props }) => (
            <ol
              className={cn("my-2 ml-6 list-decimal", className)}
              {...props}
            />
          ),
          li: ({ className, ...props }) => (
            <li className={cn("mt-2", className)} {...props} />
          ),
          blockquote: ({ className, ...props }) => (
            <blockquote
              className={cn(
                "mt-2 border-l-2 pl-6 italic [&>*]:text-muted-foreground",
                className
              )}
              {...props}
            />
          ),
          img: ({
            className,
            alt,
            ...props
          }: React.ImgHTMLAttributes<HTMLImageElement>) => (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              className={cn("rounded-md border", className)}
              alt={alt}
              {...props}
            />
          ),
          hr: ({ ...props }) => <hr className="my-2 md:my-8" {...props} />,
          table: ({
            className,
            ...props
          }: React.HTMLAttributes<HTMLTableElement>) => (
            <div className="my-2 w-full overflow-y-auto">
              <table className={cn("w-full", className)} {...props} />
            </div>
          ),
          tr: ({
            className,
            ...props
          }: React.HTMLAttributes<HTMLTableRowElement>) => (
            <tr
              className={cn("m-0 border-t p-0 even:bg-muted", className)}
              {...props}
            />
          ),
          th: ({ className, ...props }) => (
            <th
              className={cn(
                "border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right",
                className
              )}
              {...props}
            />
          ),
          td: ({ className, ...props }) => (
            <td
              className={cn(
                "border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right",
                className
              )}
              {...props}
            />
          ),
          pre: ({ className, ...props }) => (
            <pre
              className={cn(
                "mb-4 mt-6 overflow-x-auto rounded-lg py-4",
                className
              )}
              {...props}
            />
          ),
          code: ({ className, ...props }) => (
            <code
              className={cn(
                "relative rounded px-[0.3rem] py-[0.2rem] font-mono text-sm",
                className
              )}
              {...props}
            />
          ),
        }}
        remarkPlugins={[remarkGfm]}
      >
        {message.content}
      </Markdown>
    </span>
  );
};

const Message = ({ message }: { message: MessagePublic }) => {
  return (
    <div className="flex gap-3">
      {message.sent_by === "bot" && (
        <Avatar className="flex justify-center items-center">
          <AvatarImage src={"/User1.png"} alt={"bot"} width={6} height={6} />
        </Avatar>
      )}
      {message.kind === "message" && <NormalMessageContent message={message} />}
      {message.kind === "tool_start" && (
        <span className="bg-green-100 p-3 rounded-md max-w-xs">
          🔧{" "}
          {message.tool_name
            ?.replaceAll("_", " ")
            .split(" ")
            .map((t) => t.at(0)?.toUpperCase() + t.slice(1))
            .join(" ")}
        </span>
      )}
      {message.kind === "tool_output" && <ToolOutput message={message} />}
      {message.sent_by === "user" && (
        <Avatar className="flex justify-center items-center">
          <AvatarImage
            src={"/LoggedInUser.jpg"}
            alt={"you"}
            width={6}
            height={6}
          />
        </Avatar>
      )}
    </div>
  );
};

export function ChatList({ sendMessage, messages }: ChatListProps) {
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <>
      <div
        ref={messagesContainerRef}
        className="w-full overflow-y-auto overflow-x-hidden h-full flex flex-col"
      >
        <AnimatePresence mode="popLayout">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, scale: 1, y: -50, x: 0 }}
              animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
              transition={{
                opacity: { duration: 0.1 },
                layout: {
                  type: "spring",
                  bounce: 0.3,
                  duration: messages.indexOf(message) * 0.05 + 0.2,
                },
              }}
              style={{
                originX: 0.5,
                originY: 0.5,
              }}
              className={cn(
                "flex flex-col gap-2 p-4 whitespace-pre-wrap [overflow-anchor:none]",
                message.sent_by !== "bot" ? "items-end" : "items-start"
              )}
            >
              <Message message={message} />
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      <ChatBottombar sendMessage={sendMessage} />
    </>
  );
}
