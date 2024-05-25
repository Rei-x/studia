"use client";

import Link from "next/link";
import { MoreHorizontal, SquarePen } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "./ui/context-menu";
import { useRef, useState } from "react";
import type { SentBy } from "@/client";
import { v4 } from "uuid";

interface Thread {
  id: string;
  title: string;
  variant: "grey" | "ghost";
  messages: { content: string; sent_by?: SentBy }[];
}
interface SidebarProps {
  threads: Thread[];
  onClick?: () => void;
}

const ThreadLink = ({ thread }: { thread: Thread }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(thread.title);
  const titleRef = useRef<HTMLSpanElement>(null);

  const latestMessage = thread.messages[thread.messages.length - 1];
  return (
    <ContextMenu>
      <ContextMenuTrigger>
        <Link
          href={`/thread/${thread.id}`}
          className={cn(
            buttonVariants({ variant: thread.variant, size: "xl" }),
            thread.variant === "grey" && "bg-gray-200 shrink scale-105",
            "justify-start gap-4 w-full transition-all"
          )}
        >
          <div className="flex flex-col overflow-ellipsis max-w-56">
            <span
              ref={titleRef}
              contentEditable={isEditing}
              className="truncate"
              onBlur={() => setIsEditing(false)}
            >
              {title}
            </span>
            {thread.messages.length > 0 && (
              <span
                className={cn(
                  "text-zinc-300 text-xs truncate",
                  thread.variant === "grey" && "text-zinc-500"
                )}
              >
                {latestMessage.sent_by === "user" ? "You" : "AI"}:{" "}
                {latestMessage.content}
              </span>
            )}
          </div>
        </Link>
      </ContextMenuTrigger>
      <ContextMenuContent>
        <ContextMenuItem>Delete</ContextMenuItem>
        <ContextMenuItem
          onClick={() => {
            setIsEditing(true);
            setTimeout(() => titleRef.current?.focus(), 200);
          }}
        >
          Edit
        </ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
};

export function Sidebar({ threads }: SidebarProps) {
  return (
    <div className="relative group flex flex-col h-full w-[400px] gap-4 p-2 data-[collapsed=true]:p-2 ">
      <div className="flex justify-between p-2 items-center">
        <div className="flex gap-2 items-center text-2xl">
          <p className="font-medium">Chats</p>
          <span className="text-zinc-300">({threads.length})</span>
        </div>

        <div>
          {/* <Link
            href="#"
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9"
            )}
          >
            <MoreHorizontal size={20} />
          </Link> */}

          <Link
            href={`/thread/${v4()}`}
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9"
            )}
          >
            <SquarePen size={20} />
          </Link>
        </div>
      </div>

      <nav className="grid gap-1  overflow-y-auto px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
        {threads?.map((thread) => (
          <ThreadLink key={thread.id} thread={thread} />
        ))}
      </nav>
    </div>
  );
}
