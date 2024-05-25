import type { AppProps } from "next/app";
import { Inter } from "next/font/google";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "@/styles/globals.css";
import { OpenAPI } from "@/client";
import { Provider as JotaiProvider } from "jotai/react";
import Head from "next/head";
import { Toaster } from "@/components/ui/sonner";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const inter = Inter({ subsets: ["latin"] });

const queryClient = new QueryClient();

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <JotaiProvider>
      <Head>
        <title>Studendix</title>
      </Head>
      <QueryClientProvider client={queryClient}>
        <script>{`document.scrollingElement.scroll(0, 1);`}</script>
        <main className={inter.className}>
          <DndProvider backend={HTML5Backend}>
            <Component {...pageProps} />
          </DndProvider>
        </main>
        <Toaster closeButton={true} />
      </QueryClientProvider>
    </JotaiProvider>
  );
}
