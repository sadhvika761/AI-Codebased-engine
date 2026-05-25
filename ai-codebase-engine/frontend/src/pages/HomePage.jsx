import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Github, FolderOpen, Loader2 } from 'lucide-react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function HomePage() {
    const [loading, setLoading] = useState(false);
    const [uploadType, setUploadType] = useState('github');
    const [githubUrl, setGithubUrl] = useState('');
    const [file, setFile] = useState(null);
    const navigate = useNavigate();

    const handleGithubUpload = async () => {
        if (!githubUrl) return;

        setLoading(true);
        try {
            const response = await axios.post(`${API_BASE}/api/upload/github`, {
                github_url: githubUrl,
                repo_type: 'github'
            });

            navigate(`/repo/${response.data.repo_id}`);
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Failed to upload repository');
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async () => {
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`${API_BASE}/api/upload/zip`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            navigate(`/repo/${response.data.repo_id}`);
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Failed to upload repository');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <div className="container mx-auto px-4 py-16">
                {/* Header */}
                <div className="text-center mb-16">
                    <h1 className="text-5xl font-bold text-gray-900 mb-4">
                        AI Codebase Understanding Engine
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Analyze your code repository with AI. Get instant insights,
                        documentation, security analysis, and architectural understanding.
                    </p>
                </div>

                {/* Upload Section */}
                <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl p-8">
                    <h2 className="text-2xl font-semibold mb-6">Upload Your Repository</h2>

                    {/* Upload Type Selector */}
                    <div className="flex gap-4 mb-6">
                        <button
                            onClick={() => setUploadType('github')}
                            className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${uploadType === 'github'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            <Github className="inline-block mr-2" size={20} />
                            GitHub URL
                        </button>
                        <button
                            onClick={() => setUploadType('zip')}
                            className={`flex-1 py-3 px-4 rounded-lg font-medium transition ${uploadType === 'zip'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            <Upload className="inline-block mr-2" size={20} />
                            ZIP File
                        </button>
                    </div>

                    {/* GitHub Upload */}
                    {uploadType === 'github' && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                GitHub Repository URL
                            </label>
                            <input
                                type="text"
                                placeholder="https://github.com/username/repository"
                                value={githubUrl}
                                onChange={(e) => setGithubUrl(e.target.value)}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                            <button
                                onClick={handleGithubUpload}
                                disabled={loading || !githubUrl}
                                className="w-full mt-4 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition flex items-center justify-center"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="animate-spin mr-2" size={20} />
                                        Analyzing Repository...
                                    </>
                                ) : (
                                    'Analyze Repository'
                                )}
                            </button>
                        </div>
                    )}

                    {/* ZIP Upload */}
                    {uploadType === 'zip' && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Upload ZIP File
                            </label>
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition cursor-pointer">
                                <input
                                    type="file"
                                    accept=".zip"
                                    onChange={(e) => setFile(e.target.files[0])}
                                    className="hidden"
                                    id="file-upload"
                                />
                                <label htmlFor="file-upload" className="cursor-pointer">
                                    <FolderOpen className="mx-auto mb-4 text-gray-400" size={48} />
                                    <p className="text-gray-600">
                                        {file ? file.name : 'Click to select ZIP file'}
                                    </p>
                                </label>
                            </div>
                            <button
                                onClick={handleFileUpload}
                                disabled={loading || !file}
                                className="w-full mt-4 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
                            >
                                {loading ? 'Uploading...' : 'Upload & Analyze'}
                            </button>
                        </div>
                    )}
                </div>

                {/* Features Section */}
                <div className="max-w-6xl mx-auto mt-16 grid md:grid-cols-3 gap-8">
                    <FeatureCard
                        icon="🤖"
                        title="AI-Powered Analysis"
                        description="Understand complex codebases instantly with Claude AI"
                    />
                    <FeatureCard
                        icon="🔒"
                        title="Security Scanning"
                        description="Detect vulnerabilities and code smells automatically"
                    />
                    <FeatureCard
                        icon="📊"
                        title="Dependency Graphs"
                        description="Visualize architecture and relationships"
                    />
                    <FeatureCard
                        icon="📝"
                        title="Auto Documentation"
                        description="Generate README and API docs instantly"
                    />
                    <FeatureCard
                        icon="💬"
                        title="Interactive Chat"
                        description="Ask questions about your code in natural language"
                    />
                    <FeatureCard
                        icon="⚡"
                        title="Multi-Language"
                        description="Supports Python, JS, Java, Go, C++ and more"
                    />
                </div>
            </div>
        </div>
    );
}

function FeatureCard({ icon, title, description }) {
    return (
        <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
            <div className="text-4xl mb-3">{icon}</div>
            <h3 className="text-xl font-semibold mb-2">{title}</h3>
            <p className="text-gray-600">{description}</p>
        </div>
    );
}

export default HomePage;
