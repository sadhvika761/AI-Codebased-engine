import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Loader2, Box, Layers, GitBranch } from 'lucide-react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ArchitectureView({ repoId }) {
    const { data: analysis, isLoading } = useQuery({
        queryKey: ['architecture', repoId],
        queryFn: async () => {
            const response = await axios.get(`${API_BASE}/api/repo/${repoId}/architecture`);
            return response.data;
        }
    });

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <Loader2 className="animate-spin text-blue-600" size={48} />
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Architecture Overview */}
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                    <Box className="text-blue-600" />
                    Architecture Analysis
                </h3>
                <div className="prose max-w-none">
                    <ReactMarkdown>{analysis?.analysis || 'No analysis available'}</ReactMarkdown>
                </div>
            </div>

            {/* Key Insights */}
            <div className="grid md:grid-cols-2 gap-6">
                <InsightCard
                    icon={Layers}
                    title="Design Patterns"
                    items={[
                        "MVC Architecture",
                        "Repository Pattern",
                        "Factory Pattern",
                        "Observer Pattern"
                    ]}
                />
                <InsightCard
                    icon={GitBranch}
                    title="Key Components"
                    items={[
                        "Authentication System",
                        "Database Layer",
                        "API Controllers",
                        "Business Logic"
                    ]}
                />
            </div>
        </div>
    );
}

function InsightCard({ icon: Icon, title, items }) {
    return (
        <div className="bg-white border rounded-lg p-6">
            <h4 className="font-semibold mb-4 flex items-center gap-2">
                <Icon size={20} className="text-blue-600" />
                {title}
            </h4>
            <ul className="space-y-2">
                {items.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-blue-600 mt-1">•</span>
                        <span>{item}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ArchitectureView;
