import { Suspense } from 'react';
import ReportsGallery from '@/components/ReportsGallery';
import reportsData from '@/data/reports.json';
import type { Report } from '@/types/report';

export default function Page() {
    const reports: Report[] = reportsData;

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center gap-3">
                        <h1 className="text-3xl font-bold text-gray-900">
                            UN Annual Reports Gallery
                        </h1>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-un-blue/20 text-un-blue">
                            alpha
                        </span>
                    </div>
                    <p className="text-un-blue mt-1 text-lg">
                        Browse Annual Reports from UN entities
                    </p>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Suspense fallback={
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
                        {Array.from({ length: 12 }).map((_, i) => (
                            <div key={i} className="aspect-[3/4] bg-gray-200 animate-pulse rounded-lg" />
                        ))}
                    </div>
                }>
                    <ReportsGallery reports={reports} />
                </Suspense>
            </main>

            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 mt-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="text-center text-sm text-gray-500 space-y-2">
                        <p>
                            Click on any report cover to visit the organization&apos;s official report page
                        </p>
                        <div className="border-t border-gray-200 pt-4 mt-4">
                            <p className="mb-2">
                                <strong>Disclaimer:</strong> This is not an official United Nations website.
                                The information provided is for informational purposes only and no completeness or accuracy is assured.
                            </p>
                            <p>
                                Last updated: August 4, 2025
                            </p>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
