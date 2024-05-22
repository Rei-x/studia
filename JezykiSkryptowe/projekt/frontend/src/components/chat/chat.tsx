import ChatTopbar from "./chat-topbar";
import { ChatList } from "./chat-list";
import React, { useCallback, useState } from "react";
import type { Message, UserData } from "@/lib/data";
import useWebsocket from "react-use-websocket";
import type { MessagePublic, ThreadPublicWithMessages } from "@/client";
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
  tool_calls: unknown[];
  invalid_tool_calls: unknown[];
  tool_call_chunks: unknown[];
}

export function Chat({ selectedThread }: ChatProps) {
  const [messagesState, setMessages] = useState<MessagePublic[]>([]);

  const allMessages = [...selectedThread.messages, ...messagesState];

  const handleMessage = useCallback((message: MessageEvent<string>) => {
    setMessages((prev) => {
      const parsedMessage = JSON.parse(message.data) as WsMessage;

      if (prev[prev.length - 1]?.id === parsedMessage.id) {
        return prev.map((msg) =>
          msg.id === parsedMessage.id
            ? {
                ...msg,
                content: `${msg.content}${parsedMessage.content}`,
              }
            : msg
        );
      } else {
        return [
          ...prev,
          {
            id: parsedMessage.id,
            content: parsedMessage.content,
            thread_id: selectedThread?.id,
            sent_by: "bot",
          },
        ];
      }
    });
  }, []);

  const { sendMessage } = useWebsocket(
    `http://localhost:8000/chat/${selectedThread.id}`,
    {
      onMessage: handleMessage,
      retryOnError: true,
      reconnectAttempts: 10,
    }
  );

  const addNewMessage = (message: { content: string }) => {
    setMessages((prev) => [
      ...prev,
      {
        id: Math.random().toString(),
        content: message.content,
        sent_by: "user",
        thread_id: selectedThread.id,
      },
    ]);
    sendMessage(message.content);
  };

  return (
    <div className="flex flex-col border-l justify-between w-full h-full">
      <ChatTopbar selectedUser={selectedThread} />
      <ChatList messages={allMessages} sendMessage={addNewMessage} />
    </div>
  );
}
