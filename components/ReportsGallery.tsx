'use client';

import type { Report } from '@/types/report';
import Image from 'next/image';
import { useState } from 'react';

interface ReportCardProps {
    report: Report;
}

function ReportCard({ report }: ReportCardProps) {
    const [imageError, setImageError] = useState(false);

    return (
        <a
            href={report.reportUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="group block bg-white rounded-lg hover:bg-gray-50 transition-colors duration-200 relative"
        >
            <div className="aspect-[3/4] relative overflow-hidden rounded-t-lg bg-gray-100">
                <Image
                    src={imageError ? '/covers/placeholder.svg' : `/covers/${report.coverImage}`}
                    alt={`${report.name} Annual Report ${report.year} Cover`}
                    fill
                    className="object-cover transition-all duration-300"
                    sizes="(max-width: 640px) 100vw, (max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw"
                    onError={() => setImageError(true)}
                />
            </div>
            <div className="p-4">
                <h3 className="font-semibold text-gray-900 text-base leading-tight mb-0.5">{report.name}</h3>
                <p className="text-sm text-un-gray leading-tight">{report.year}</p>
            </div>
            <div className="absolute inset-0 bg-un-blue opacity-0 group-hover:opacity-15 transition-opacity duration-300 rounded-lg"></div>
        </a>
    );
}

interface ReportsGalleryProps {
    reports: Report[];
}

export default function ReportsGallery({ reports }: ReportsGalleryProps) {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {reports.map((report) => (
                <ReportCard key={report.id} report={report} />
            ))}
        </div>
    );
}
