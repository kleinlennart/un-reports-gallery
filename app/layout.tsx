import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "UN Annual Reports Gallery",
    description: "Browse Annual Reports from UN entities",
    keywords: ["UN", "United Nations", "annual reports", "reports", "organizations"],
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className="font-sans antialiased">
                {children}
            </body>
        </html>
    );
}
