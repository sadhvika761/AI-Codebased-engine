import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { AlertTriangle, Shield, CheckCircle, XCircle } from 'lucide-react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function SecurityPanel({ repoId }) {
    const { data: security, isLoading } = useQuery({
        queryKey: ['security', repoId],
        queryFn: async () => {
            const response = await axios.get(`${API_BASE}/api/repo/${repoId}/security`);
            return response.data;
        }
    });

    if (isLoading) {
        return <div className="text-center py-8">Loading security analysis...</div>;
    }

    const issues = security?.issues || [];
    const grouped = groupByType(issues);

    return (
        <div>
            {/* Summary */}
            <div className="grid grid-cols-4 gap-4 mb-6">
                <StatCard
                    title="Total Issues"
                    value={issues.length}
                    icon={AlertTriangle}
                    color="text-orange-600"
                />
                <StatCard
                    title="Critical"
                    value={issues.filter(i => i.severity === 'CRITICAL').length}
                    icon={XCircle}
                    color="text-red-600"
                />
                <StatCard
                    title="High"
                    value={issues.filter(i => i.severity === 'HIGH').length}
                    icon={AlertTriangle}
                    color="text-orange-600"
                />
                <StatCard
                    title="Medium"
                    value={issues.filter(i => i.severity === 'MEDIUM').length}
                    icon={Shield}
                    color="text-yellow-600"
                />
            </div>

            {/* Issues by Type */}
            <div className="space-y-6">
                {Object.entries(grouped).map(([type, items]) => (
                    <div key={type} className="bg-white border rounded-lg p-6">
                        <h3 className="text-lg font-semibold mb-4 capitalize">
                            {type.replace(/_/g, ' ')}
                            <span className="ml-2 text-sm text-gray-500">({items.length})</span>
                        </h3>

                        <div className="space-y-3">
                            {items.map((issue, idx) => (
                                <IssueCard key={idx} issue={issue} />
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            {issues.length === 0 && (
                <div className="text-center py-12 bg-green-50 rounded-lg">
                    <CheckCircle className="mx-auto mb-3 text-green-600" size={48} />
                    <h3 className="text-lg font-semibold text-green-900 mb-2">
                        No Security Issues Found
                    </h3>
                    <p className="text-green-700">
                        Your codebase passed all automated security checks!
                    </p>
                </div>
            )}
        </div>
    );
}

function StatCard({ title, value, icon: Icon, color }) {
    return (
        <div className="bg-white border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-gray-600">{title}</span>
                <Icon className={color} size={20} />
            </div>
            <div className="text-2xl font-bold">{value}</div>
        </div>
    );
}

function IssueCard({ issue }) {
    const severityColors = {
        CRITICAL: 'bg-red-100 text-red-800 border-red-300',
        HIGH: 'bg-orange-100 text-orange-800 border-orange-300',
        MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300',
        LOW: 'bg-blue-100 text-blue-800 border-blue-300'
    };

    return (
        <div className="border rounded-lg p-4 hover:shadow-md transition">
            <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                        <span className={`text-xs px-2 py-1 rounded border ${severityColors[issue.severity]}`}>
                            {issue.severity}
                        </span>
                        <span className="text-sm text-gray-600">Line {issue.line}</span>
                    </div>
                    <p className="text-sm text-gray-500 font-mono">{issue.file}</p>
                </div>
            </div>

            <pre className="bg-gray-50 p-3 rounded text-sm overflow-x-auto mb-2">
                <code>{issue.code}</code>
            </pre>

            {issue.description && (
                <p className="text-sm text-gray-700">{issue.description}</p>
            )}
        </div>
    );
}

function groupByType(issues) {
    return issues.reduce((acc, issue) => {
        const type = issue.type || 'other';
        if (!acc[type]) acc[type] = [];
        acc[type].push(issue);
        return acc;
    }, {});
}

export default SecurityPanel;
