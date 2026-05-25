import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import {
    MessageSquare,
    Shield,
    GitBranch,
    Activity,
    AlertTriangle,
    CheckCircle
} from 'lucide-react';

import ChatInterface from '../components/ChatInterface';
import DependencyGraph from '../components/DependencyGraph';
import SecurityPanel from '../components/SecurityPanel';
import ArchitectureView from '../components/ArchitectureView';
import StatsOverview from '../components/StatsOverview';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function RepositoryDashboard() {
    const { repoId } = useParams();
    const [activeTab, setActiveTab] = useState('chat');

    // Fetch repository stats
    const { data: stats } = useQuery({
        queryKey: ['repoStats', repoId],
        queryFn: async () => {
            const response = await axios.get(`${API_BASE}/api/repo/${repoId}/stats`);
            return response.data;
        }
    });

    // Fetch security issues
    const { data: security } = useQuery({
        queryKey: ['security', repoId],
        queryFn: async () => {
            const response = await axios.get(`${API_BASE}/api/repo/${repoId}/security`);
            return response.data;
        }
    });

    const tabs = [
        { id: 'chat', label: 'AI Chat', icon: MessageSquare },
        { id: 'graph', label: 'Dependencies', icon: GitBranch },
        { id: 'security', label: 'Security', icon: Shield },
        { id: 'architecture', label: 'Architecture', icon: Activity },
    ];

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white border-b">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <h1 className="text-2xl font-bold text-gray-900">
                            Repository Analysis
                        </h1>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <CheckCircle className="text-green-500" size={20} />
                                <span className="text-sm text-gray-600">
                                    {stats?.total_files || 0} files analyzed
                                </span>
                            </div>
                            {security?.total > 0 && (
                                <div className="flex items-center gap-2">
                                    <AlertTriangle className="text-orange-500" size={20} />
                                    <span className="text-sm text-gray-600">
                                        {security.total} issues found
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Stats Overview */}
            <div className="container mx-auto px-4 py-6">
                <StatsOverview stats={stats} />
            </div>

            {/* Tabs */}
            <div className="container mx-auto px-4">
                <div className="bg-white rounded-lg shadow-sm">
                    <div className="border-b">
                        <div className="flex gap-1">
                            {tabs.map((tab) => {
                                const Icon = tab.icon;
                                return (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveTab(tab.id)}
                                        className={`px-6 py-3 font-medium transition flex items-center gap-2 ${activeTab === tab.id
                                                ? 'border-b-2 border-blue-600 text-blue-600'
                                                : 'text-gray-600 hover:text-gray-900'
                                            }`}
                                    >
                                        <Icon size={18} />
                                        {tab.label}
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    {/* Tab Content */}
                    <div className="p-6">
                        {activeTab === 'chat' && <ChatInterface repoId={repoId} />}
                        {activeTab === 'graph' && <DependencyGraph repoId={repoId} />}
                        {activeTab === 'security' && <SecurityPanel repoId={repoId} />}
                        {activeTab === 'architecture' && <ArchitectureView repoId={repoId} />}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default RepositoryDashboard;
