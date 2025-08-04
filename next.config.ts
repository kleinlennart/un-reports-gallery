import type { NextConfig } from "next";

// Only use base path when deployed to GitHub Pages (not for local serve)
const isGithubPages = process.env.GITHUB_ACTIONS === 'true';
const repoName = 'un-reports-gallery';

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath: isGithubPages ? `/${repoName}` : '',
  assetPrefix: isGithubPages ? `/${repoName}/` : '',
  images: {
    unoptimized: true
  }
};

export default nextConfig;
