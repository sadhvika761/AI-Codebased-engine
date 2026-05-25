import React from 'react';
import { FileCode, Folder, AlertCircle, CheckCircle } from 'lucide-react';

function StatsOverview({ stats }) {
    if (!stats) return null;

    const metrics = [
        {
            label: 'Total Files',
            value: stats.total_files || 0,
            icon: FileCode,
            color: 'text-blue-600',
            bg: 'bg-blue-50'
        },
        {
            label: 'Functions',
            value: stats.total_functions || 0,
            icon: Folder,
            color: 'text-green-600',
            bg: 'bg-green-50'
        },
        {
            label: 'Classes',
            value: stats.total_classes || 0,
            icon: CheckCircle,
            color: 'text-purple-600',
            bg: 'bg-purple-50'
        },
        {
            label: 'Security Issues',
            value: stats.security_issues || 0,
            icon: AlertCircle,
            color: 'text-orange-600',
            bg: 'bg-orange-50'
        }
    ];

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {metrics.map((metric, idx) => {
                const Icon = metric.icon;
                return (
                    <div key={idx} className="bg-white rounded-lg shadow-sm p-6">
                        <div className={`w-12 h-12 ${metric.bg} rounded-lg flex items-center justify-center mb-3`}>
                            <Icon className={metric.color} size={24} />
                        </div>
                        <div className="text-2xl font-bold mb-1">{metric.value}</div>
                        <div className="text-sm text-gray-600">{metric.label}</div>
                    </div>
                );
            })}
        </div>
    );
}

export default StatsOverview;