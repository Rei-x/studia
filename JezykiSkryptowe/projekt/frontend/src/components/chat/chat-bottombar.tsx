import { Paperclip, SendHorizontal, ThumbsUp, Trash2 } from "lucide-react";
import Link from "next/link";
import React, { useRef, useState } from "react";
import { buttonVariants } from "../ui/button";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";

import { Textarea } from "../ui/textarea";
import { useAtom } from "jotai/react";
import { useSelectedThread } from "./chat-layout";
import { chatAtomFamily } from "./chat";
import { badgeVariants } from "../ui/badge";

interface ChatBottombarProps {
  sendMessage: (newMessage: { content: string }) => void;
}

export const BottombarIcons = [{ icon: Paperclip, id: "paperclip" }];

export default function ChatBottombar({ sendMessage }: ChatBottombarProps) {
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const { selectedThreadId } = useSelectedThread();
  const [chatState, setChatState] = useAtom(chatAtomFamily(selectedThreadId));

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(event.target.value);
  };

  const handleThumbsUp = () => {
    const newMessage = {
      content: "👍",
    };
    sendMessage(newMessage);
    setMessage("");
  };

  const handleSend = () => {
    if (message.trim()) {
      const newMessage = {
        content: message.trim(),
      };
      sendMessage(newMessage);
      setMessage("");

      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }

    if (event.key === "Enter" && event.shiftKey) {
      event.preventDefault();
      setMessage((prev) => prev + "\n");
    }
  };

  return (
    <div>
      <div className="p-2 flex justify-between w-full items-end gap-2">
        <div className="flex align-bottom justify-start">
          {!message.trim() && (
            <div className="flex">
              {BottombarIcons.map((icon) => (
                <Link
                  key={icon.id}
                  href="#"
                  className={cn(
                    buttonVariants({ variant: "ghost", size: "icon" }),
                    "h-9 w-9",
                    "dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white"
                  )}
                >
                  <icon.icon size={20} className="text-muted-foreground" />
                </Link>
              ))}
            </div>
          )}
        </div>

        <div className="w-full">
          <div className="mb-1">
            <AnimatePresence initial={false}>
              {chatState.files &&
                chatState.files.length > 0 &&
                chatState.files.map((file, i) => (
                  <motion.div
                    key={`list-${file.id}`}
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className={cn(
                      badgeVariants({
                        variant: "outline",
                      }),
                      "h-6 p-1 w-auto gap-1"
                    )}
                  >
                    <div className="font-medium leading-none tracking-tight">
                      {file.filename}
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        const newFiles = chatState.files.filter(
                          (f) => f.id !== file.id
                        );
                        setChatState((prev) => ({
                          ...prev,
                          files: newFiles,
                        }));
                      }}
                    >
                      <span className="sr-only">
                        remove item {file.filename}
                      </span>
                      <Trash2 className="w-4 h-4 hover:stroke-destructive duration-200 ease-in-out" />
                    </button>
                  </motion.div>
                ))}
            </AnimatePresence>
          </div>
          <AnimatePresence initial={false}>
            <motion.div
              key="input-text"
              layout
              initial={{ opacity: 0, scale: 1 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1 }}
              transition={{
                opacity: { duration: 0.05 },
                layout: {
                  type: "spring",
                  bounce: 0.15,
                },
              }}
            >
              <Textarea
                id="chat-input"
                autoComplete="off"
                value={message}
                ref={inputRef}
                onKeyDown={handleKeyPress}
                onChange={handleInputChange}
                name="message"
                placeholder="Aa"
                className=" w-full border rounded-full flex items-center h-9 resize-none overflow-hidden bg-background"
              ></Textarea>
            </motion.div>
          </AnimatePresence>
        </div>

        {message.trim() ? (
          <Link
            href="#"
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9",
              "dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white shrink-0"
            )}
            onClick={handleSend}
          >
            <SendHorizontal size={20} className="text-muted-foreground" />
          </Link>
        ) : (
          <Link
            href="#"
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9",
              "dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white shrink-0"
            )}
            onClick={handleThumbsUp}
          >
            <ThumbsUp size={20} className="text-muted-foreground" />
          </Link>
        )}
      </div>
    </div>
  );
}
