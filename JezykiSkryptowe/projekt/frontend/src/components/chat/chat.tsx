import ChatTopbar from "./chat-topbar";
import { ChatList } from "./chat-list";
import React, { useCallback, useMemo, useState } from "react";
import type { Message, UserData } from "@/lib/data";
import useWebsocket from "react-use-websocket";
import type {
  FilePublic,
  MessagePublic,
  ThreadPublicWithMessages,
} from "@/client";
import { v4 } from "uuid";
import { useRouter } from "next/router";
import { atomFamily } from "jotai/utils";
import { atom } from "jotai/vanilla";
import { useAtom } from "jotai/react";
import { useDrop } from "react-dnd";
import { cn } from "@/lib/utils";
import deepEqual from "fast-deep-equal";
interface ChatProps {
  selectedThread: ThreadPublicWithMessages;
}

interface WsMessage {
  content: string;
  additional_kwargs: Record<string, unknown>;
  response_metadata: Record<string, unknown>;
  type: string;
  name: string | null;
  id: string;
  example: boolean;
  kind: string;
  tool_calls: unknown[];
  invalid_tool_calls: unknown[];
  tool_call_chunks: unknown[];
}

export const chatAtomFamily = atomFamily(
  (param: string) =>
    atom<{ messages: MessagePublic[]; files: FilePublic[]; threadId: string }>({
      messages: [],
      files: [],
      threadId: param,
    }),
  deepEqual
);

export function Chat({ selectedThread }: ChatProps) {
  const chatAtom = useMemo(
    () => chatAtomFamily(selectedThread.id),
    [selectedThread.id]
  );

  const [chatState, setChatState] = useAtom(chatAtom);

  const messages = chatState.messages;

  const allMessages = [...selectedThread.messages, ...messages].filter(
    (message, index, self) =>
      index ===
      self.findIndex(
        (t) =>
          t.id === message.id &&
          t.sent_by === message.sent_by &&
          t.content === message.content
      )
  );

  const handleDrop = useCallback(
    (file: FilePublic) => {
      setChatState((prev) => ({
        ...prev,
        files: [...prev.files.filter((f) => f.id !== file.id), file],
      }));
    },
    [setChatState]
  );

  const [{ isOver, canDrop }, drop] = useDrop(
    () => ({
      accept: "file",
      drop: handleDrop,
      collect: (monitor) => ({
        isOver: !!monitor.isOver(),
        canDrop: !!monitor.canDrop(),
      }),
    }),
    [handleDrop]
  );

  const handleMessage = useCallback(
    (message: MessageEvent<string>) => {
      setChatState(({ messages: prev, ...rest }) => {
        const parsedMessage = JSON.parse(message.data) as MessagePublic;

        if (parsedMessage.kind === "message") {
          if (parsedMessage.content === "") {
            return {
              ...rest,
              messages: prev,
            };
          }
          if (prev[prev.length - 1]?.id === parsedMessage.id) {
            return {
              ...rest,
              messages: prev.map((msg) =>
                msg.id === parsedMessage.id
                  ? {
                      ...msg,
                      content: `${parsedMessage.content}`,
                    }
                  : msg
              ),
            };
          } else {
            return {
              ...rest,
              messages: [...prev, parsedMessage],
            };
          }
        } else if (parsedMessage.kind === "tool_start") {
          return {
            ...rest,
            messages: [...prev, parsedMessage],
          };
        } else if (parsedMessage.kind === "tool_output") {
          return {
            ...rest,
            messages: [...prev, parsedMessage],
          };
        }

        return {
          messages: prev,
          ...rest,
        };
      });
    },
    [selectedThread?.id, setChatState]
  );

  const { sendMessage } = useWebsocket(
    `http://localhost:8000/chat/${selectedThread.id}`,
    {
      onMessage: handleMessage,
      retryOnError: true,
      reconnectAttempts: 10,
    }
  );

  const addNewMessage = (message: { content: string }) => {
    const newMessage = {
      sent_by: "user",
      content: message.content,
      kind: "message",
      id: v4(),
      thread_id: selectedThread.id,
    } as const;

    setChatState((prev) => ({
      ...prev,
      messages: [...prev.messages, newMessage],
    }));
    sendMessage(JSON.stringify(newMessage));
  };

  return (
    <div className="flex flex-col border-x relative justify-between w-full h-full">
      <ChatTopbar selectedUser={selectedThread} />
      <div className="w-full overflow-y-auto overflow-x-hidden h-full flex flex-col">
        <ChatList messages={allMessages} sendMessage={addNewMessage} />
        <div
          ref={drop}
          className={cn(
            canDrop && "transition-all inset-0 bg-black bg-opacity-50 z-10",
            {
              "opacity-0 ": !isOver,
            },
            "absolute"
          )}
        ></div>
      </div>
    </div>
  );
}
