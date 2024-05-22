import { cn } from "@/lib/utils";
import React, { useRef } from "react";
import { Avatar, AvatarImage } from "../ui/avatar";
import ChatBottombar from "./chat-bottombar";
import { AnimatePresence, motion } from "framer-motion";
import type { MessagePublic } from "@/client";

interface ChatListProps {
  messages: MessagePublic[];

  sendMessage: (newMessage: { content: string }) => void;
}

export function ChatList({ sendMessage, messages }: ChatListProps) {
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop =
        messagesContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="w-full overflow-y-auto overflow-x-hidden h-full flex flex-col">
      <div
        ref={messagesContainerRef}
        className="w-full overflow-y-auto overflow-x-hidden h-full flex flex-col"
      >
        <AnimatePresence mode="popLayout">
          {messages.map((message, index) => (
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
              <div className="flex gap-3">
                {message.sent_by === "bot" && (
                  <Avatar className="flex justify-center items-center">
                    <AvatarImage
                      src={"/User1.png"}
                      alt={"bot"}
                      width={6}
                      height={6}
                    />
                  </Avatar>
                )}
                <span className=" bg-accent p-3 rounded-md max-w-xs">
                  {message.content}
                </span>
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
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      <ChatBottombar sendMessage={sendMessage} />
    </div>
  );
}
