"use client";

import Link from "next/link";
import { MoreHorizontal, SquarePen } from "lucide-react";
import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";

interface SidebarProps {
  threads: {
    id: string;
    title: string;
    variant: "grey" | "ghost";
    messages: { content: string }[];
  }[];
  onClick?: () => void;
}

export function Sidebar({ threads }: SidebarProps) {
  return (
    <div className="relative group flex flex-col h-full w-[400px] gap-4 p-2 data-[collapsed=true]:p-2 ">
      <div className="flex justify-between p-2 items-center">
        <div className="flex gap-2 items-center text-2xl">
          <p className="font-medium">Chats</p>
          <span className="text-zinc-300">({threads.length})</span>
        </div>

        <div>
          <Link
            href="#"
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9"
            )}
          >
            <MoreHorizontal size={20} />
          </Link>

          <Link
            href="#"
            className={cn(
              buttonVariants({ variant: "ghost", size: "icon" }),
              "h-9 w-9"
            )}
          >
            <SquarePen size={20} />
          </Link>
        </div>
      </div>

      <nav className="grid gap-1  px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
        {threads?.map((thread, index) => (
          <Link
            key={thread.id}
            href={`/thread/${thread.id}`}
            className={cn(
              buttonVariants({ variant: thread.variant, size: "xl" }),
              thread.variant === "grey" &&
                "dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white shrink",
              "justify-start gap-4"
            )}
          >
            <div className="flex flex-col overflow-ellipsis max-w-56">
              <span>{thread.title}</span>
              {thread.messages.length > 0 && (
                <span className="text-zinc-300 text-xs truncate">
                  AI: {thread.messages[thread.messages.length - 1].content}
                </span>
              )}
            </div>
          </Link>
        ))}
      </nav>
    </div>
  );
}
