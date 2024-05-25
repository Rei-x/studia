/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        hostname: "api.statvoo.com",
      },
    ],
  },
};

export default nextConfig;
