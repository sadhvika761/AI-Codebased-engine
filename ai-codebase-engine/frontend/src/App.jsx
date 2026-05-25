import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import HomePage from './pages/HomePage';
import RepositoryDashboard from './pages/RepositoryDashboard';


const queryClient = new QueryClient();

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <Router>
                <div className="min-h-screen bg-gray-50">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/repo/:repoId" element={<RepositoryDashboard />} />
                    </Routes>
                </div>
            </Router>
        </QueryClientProvider>
    );
}

export default App;