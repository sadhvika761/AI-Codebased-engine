import React, { useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ForceGraph2D from 'react-force-graph-2d';
import { Loader2, ZoomIn, ZoomOut, Maximize2 } from 'lucide-react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function DependencyGraph({ repoId }) {
    const graphRef = useRef();
    const [selectedNode, setSelectedNode] = useState(null);
    const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

    const { data: graphData, isLoading } = useQuery({
        queryKey: ['graph', repoId],
        queryFn: async () => {
            const response = await axios.get(`${API_BASE}/api/repo/${repoId}/graph`);
            return response.data;
        }
    });

    useEffect(() => {
        const updateDimensions = () => {
            const container = document.getElementById('graph-container');
            if (container) {
                setDimensions({
                    width: container.offsetWidth,
                    height: Math.max(600, window.innerHeight - 400)
                });
            }
        };

        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-96">
                <Loader2 className="animate-spin text-blue-600" size={48} />
            </div>
        );
    }

    if (!graphData || !graphData.nodes) {
        return <div className="text-center text-gray-600">No graph data available</div>;
    }

    // Process graph data
    const processedData = {
        nodes: graphData.nodes.map(node => ({
            id: node.id,
            name: node.name,
            type: node.type,
            file: node.file,
            color: getNodeColor(node.type)
        })),
        links: graphData.edges.map(edge => ({
            source: edge.source,
            target: edge.target
        }))
    };

    const handleNodeClick = (node) => {
        setSelectedNode(node);
    };

    const handleZoomIn = () => {
        graphRef.current?.zoom(1.5, 300);
    };

    const handleZoomOut = () => {
        graphRef.current?.zoom(0.5, 300);
    };

    const handleFit = () => {
        graphRef.current?.zoomToFit(300, 50);
    };

    return (
        <div>
            {/* Controls */}
            <div className="flex justify-between items-center mb-4">
                <div>
                    <h3 className="text-lg font-semibold">Dependency Graph</h3>
                    <p className="text-sm text-gray-600">
                        {graphData.nodes.length} nodes, {graphData.edges.length} dependencies
                    </p>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={handleZoomIn}
                        className="p-2 bg-white border rounded hover:bg-gray-50"
                        title="Zoom In"
                    >
                        <ZoomIn size={20} />
                    </button>
                    <button
                        onClick={handleZoomOut}
                        className="p-2 bg-white border rounded hover:bg-gray-50"
                        title="Zoom Out"
                    >
                        <ZoomOut size={20} />
                    </button>
                    <button
                        onClick={handleFit}
                        className="p-2 bg-white border rounded hover:bg-gray-50"
                        title="Fit to Screen"
                    >
                        <Maximize2 size={20} />
                    </button>
                </div>
            </div>

            {/* Legend */}
            <div className="flex gap-4 mb-4 text-sm">
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full bg-blue-500"></div>
                    <span>Functions</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full bg-green-500"></div>
                    <span>Classes</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-4 h-4 rounded-full bg-purple-500"></div>
                    <span>Imports</span>
                </div>
            </div>

            <div className="flex gap-4">
                {/* Graph */}
                <div id="graph-container" className="flex-1 bg-white border rounded-lg overflow-hidden">
                    <ForceGraph2D
                        ref={graphRef}
                        graphData={processedData}
                        width={dimensions.width}
                        height={dimensions.height}
                        nodeLabel="name"
                        nodeColor="color"
                        nodeRelSize={6}
                        linkDirectionalArrowLength={3}
                        linkDirectionalArrowRelPos={1}
                        linkColor={() => '#cbd5e1'}
                        onNodeClick={handleNodeClick}
                        nodeCanvasObject={(node, ctx, globalScale) => {
                            const label = node.name;
                            const fontSize = 12 / globalScale;
                            ctx.font = `${fontSize}px Sans-Serif`;
                            ctx.fillStyle = node.color;
                            ctx.beginPath();
                            ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
                            ctx.fill();

                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
                            ctx.fillStyle = '#1f2937';
                            ctx.fillText(label, node.x, node.y + 10);
                        }}
                    />
                </div>

                {/* Node Details */}
                {selectedNode && (
                    <div className="w-80 bg-white border rounded-lg p-4">
                        <h4 className="font-semibold mb-3">Node Details</h4>
                        <div className="space-y-2 text-sm">
                            <div>
                                <span className="text-gray-600">Name:</span>
                                <p className="font-medium">{selectedNode.name}</p>
                            </div>
                            <div>
                                <span className="text-gray-600">Type:</span>
                                <p className="font-medium capitalize">{selectedNode.type}</p>
                            </div>
                            <div>
                                <span className="text-gray-600">File:</span>
                                <p className="font-medium text-xs break-all">{selectedNode.file}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

function getNodeColor(type) {
    const colors = {
        function: '#3b82f6',
        class: '#10b981',
        import: '#8b5cf6',
        variable: '#f59e0b'
    };
    return colors[type] || '#6b7280';
}

export default DependencyGraph;
