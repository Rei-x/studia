import { ChatLayout } from "@/components/chat/chat-layout";
import { useRouter } from "next/router";
import React from "react";
import { v4 } from "uuid";

const Thread = () => {
  // on press alt + N, it will redirect to the next page

  const router = useRouter();

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.altKey && e.key === "n") {
        router.push(`/thread/${v4()}`).then(() => {
          document.getElementById("chat-input")?.focus();
        });
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [router]);
  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center justify-center p-4 md:px-24 gap-4">
      <div className="z-10 border rounded-lg max-w-screen-2xl w-full h-full text-sm lg:flex">
        <ChatLayout />
      </div>
    </main>
  );
};

export default Thread;
