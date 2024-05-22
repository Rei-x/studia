import type { AppProps } from "next/app";
import { Inter } from "next/font/google";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "@/styles/globals.css";
import { OpenAPI } from "@/client";

OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const inter = Inter({ subsets: ["latin"] });

const queryClient = new QueryClient();

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <script>{`document.scrollingElement.scroll(0, 1);`}</script>
      <main className={inter.className}>
        <Component {...pageProps} />
      </main>
    </QueryClientProvider>
  );
}
