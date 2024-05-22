import { ChatLayout } from "@/components/chat/chat-layout";
import { useRouter } from "next/router";
import React from "react";

const Thread = () => {
  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center justify-center p-4 md:px-24 gap-4">
      <div className="z-10 border rounded-lg max-w-5xl w-full h-full text-sm lg:flex">
        <ChatLayout />
      </div>
    </main>
  );
};

export default Thread;
