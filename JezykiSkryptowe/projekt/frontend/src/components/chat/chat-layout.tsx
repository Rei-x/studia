"use client";

import React from "react";
import { Sidebar } from "../sidebar";
import { Chat } from "./chat";
import { threadsThreadsGet, type ThreadPublicWithMessages } from "@/client";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/router";
import { v4 as uuid } from "uuid";
export function ChatLayout() {
  const selectedThreadId = useRouter().query.id as string;

  const { data: threads } = useQuery({
    queryKey: ["threads"],
    queryFn: async () => threadsThreadsGet(),
  });

  const selectedThread =
    threads?.find((thread) => thread.id === selectedThreadId) ??
    ({
      id: uuid(),
      title: "Start chating",
      messages: [],
    } as ThreadPublicWithMessages);

  return (
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

      <Chat selectedThread={selectedThread} />
    </div>
  );
}
