import latestReportsRaw from '@/data/output/un_ilibrary_latest_reports.json';

type LatestItem = {
    title?: string;
    published?: string;
    link?: string;
    cover_image?: string;
};

function formatDateShort(input?: string) {
    if (!input) return '';
    const d = new Date(input);
    if (isNaN(d.getTime())) return '';
    return d.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    });
}

export default function LatestPage() {
    const reports = (latestReportsRaw as unknown as LatestItem[]).filter(
        (r) => r.cover_image && r.link
    );

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 relative">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center gap-3">
                        <h1 className="text-3xl font-bold text-gray-900">
                            Latest UN Reports
                        </h1>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-un-blue/20 text-un-blue">
                            alpha
                        </span>
                    </div>
                    <p className="text-un-blue mt-1 text-lg">
                        Most recent Reports from the{' '}
                        <a
                            href="https://www.un-ilibrary.org/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-medium
 hover:text-un-blue-dark transition-colors"
                        >
                            UN-iLibrary
                        </a>
                    </p>
                    <a
                        href="https://github.com/kleinlennart/un-reports-gallery"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="absolute top-6 right-4 sm:right-6 lg:right-8 p-2 text-gray-800 hover:text-black transition-colors"
                        aria-label="View source on GitHub"
                    >
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                    </a>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {reports.map((item, i) => (
                        <a
                            key={`${item.link}-${i}`}
                            href={item.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="group block bg-white rounded-lg hover:bg-gray-50 transition-colors duration-200 relative overflow-hidden"
                        >
                            <div className="aspect-[3/4] relative overflow-hidden rounded-t-lg bg-gray-100">
                                {/* Using native img to avoid remote image config */}
                                {/* eslint-disable-next-line @next/next/no-img-element */}
                                <img
                                    src={item.cover_image!}
                                    alt={item.title ?? 'UN report cover'}
                                    className="h-full w-full object-cover"
                                    loading="lazy"
                                />
                            </div>
                            <div className="p-4">
                                <h3 className="text-sm font-medium text-gray-900 truncate">
                                    {item.title ?? 'Untitled'}
                                </h3>
                                <p className="text-xs text-un-gray mt-0.5">
                                    {formatDateShort(item.published)}
                                </p>
                            </div>
                            <div className="absolute inset-0 bg-un-blue opacity-0 group-hover:opacity-15 transition-opacity duration-300 rounded-lg" />
                        </a>
                    ))}
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 mt-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="text-center text-sm text-gray-500 space-y-2">
                        <p>
                            Click on any report cover to read the report on{' '}
                            <a
                                href="https://www.un-ilibrary.org/"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-un-blue font-medium hover:underline"
                            >
                                un-ilibrary.org
                            </a>
                        </p>
                        <div className="border-t border-gray-200 pt-4 mt-4">
                            <p className="mb-2">
                                <strong>Disclaimer:</strong> This is not an official United Nations website.
                                
                                <br />
                                The information provided is for informational purposes only and no completeness or accuracy is assured. 
                                <br />
                                Data extracted from the "Latest Content"&nbsp;
                                <a
                                    href="https://www.un-ilibrary.org/rss/content/all/most_recent_items?fmt=rss"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-un-blue font-medium hover:underline"
                                >
                                     RSS
                                </a>
                                &nbsp;of the UN-iLibrary website.
                            </p>
                            <p>
                                Last updated:{" "}
                                {formatDateShort(new Date().toISOString())}
                            </p>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
