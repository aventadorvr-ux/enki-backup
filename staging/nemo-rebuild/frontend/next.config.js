/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ["images.unsplash.com", "via.placeholder.com"],
  },
  async rewrites() {
    return [
      {
        source: '/api/content-process',
        destination: 'http://127.0.0.1:8000/api/v1/enki/content/generate',
      },
      {
        source: '/api/agents/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/agents/:path*',
      },
      {
        source: '/api/orchestrate/:path*',
        destination: 'http://127.0.0.1:8000/api/v1/orchestrate/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
