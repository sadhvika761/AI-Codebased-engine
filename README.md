# AI Codebase Engine 🤖

A comprehensive AI-powered codebase analysis and interaction system featuring multiple specialized agents, vector embeddings, dependency graph analysis, and intelligent code understanding capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Agents](#agents)
- [Frontend](#frontend)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

AI Codebase Engine is an enterprise-grade system that combines multiple AI agents with advanced code analysis capabilities to provide:

- **Intelligent Code Understanding**: Deep semantic analysis using embeddings and LLMs
- **Multi-Agent Architecture**: Specialized agents for different aspects of code analysis
- **RAG-Powered Q&A**: Ask questions about your codebase in natural language
- **Security Analysis**: Automated vulnerability detection and remediation suggestions
- **Architecture Insights**: Design pattern detection and architectural recommendations
- **Documentation Generation**: Automated docs creation and improvement
- **Dependency Visualization**: Interactive graphs showing code relationships

## ✨ Features

### Core Capabilities

- **🔍 Semantic Code Search**: Vector-based similarity search across your entire codebase
- **💬 Natural Language Queries**: Ask questions about code functionality, patterns, and structure
- **🛡️ Security Scanning**: Automated detection of vulnerabilities using Bandit and custom patterns
- **📊 Dependency Analysis**: Visual dependency graphs with cycle detection
- **🏗️ Architecture Analysis**: Design pattern detection and architectural recommendations
- **📚 Auto Documentation**: Generate comprehensive docs for functions, classes, and modules
- **⚡ Smart Caching**: Redis-based caching for improved performance
- **🎨 Interactive Dashboard**: React-based UI for visualization and interaction

### Advanced Features

- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go
- **Code Metrics**: LOC, complexity, coupling, cohesion analysis
- **Pattern Detection**: Identify MVC, Factory, Singleton, Observer patterns
- **Graph Analytics**: Centrality analysis, circular dependency detection
- **Batch Processing**: Efficient processing of large codebases
- **Real-time Analysis**: Stream processing for immediate insights

## 🏛️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌─────────────┬──────────────┬─────────────┬─────────────┐ │
│  │  Dashboard  │  Chat UI     │  Graph View │  Security   │ │
│  └─────────────┴──────────────┴─────────────┴─────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              API Routes & Controllers                    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │  RAG Agent   │ Security     │ Architecture │   Docs    │ │
│  │              │ Agent        │ Agent        │   Agent   │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
│                                                               │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │ Code Parser  │ Embeddings   │ Graph        │  Caching  │ │
│  │              │ Manager      │ Builder      │           │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────┴─────────────────────────────────────┐
│                   Data Layer                                 │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │  ChromaDB    │    Redis     │  NetworkX    │  File     │ │
│  │  (Vectors)   │   (Cache)    │  (Graphs)    │  System   │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Framework**: FastAPI (Python 3.10+)
- **AI/ML**: OpenAI GPT-4, Anthropic Claude, Sentence Transformers
- **Vector Store**: ChromaDB
- **Cache**: Redis
- **Graph**: NetworkX
- **Code Analysis**: AST, Tree-sitter, Bandit

**Frontend:**
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **State**: React Hooks
- **Visualization**: D3.js, Recharts
- **Build**: Vite/Create React App

**Infrastructure:**
- **Containerization**: Docker, Docker Compose
- **Reverse Proxy**: Nginx
- **Process Manager**: Uvicorn

## 📁 Project Structure

```
ai-codebase-engine/
├── backend/
│   ├── agents/                      # AI Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py           # Base agent class
│   │   ├── architecture_agent.py   # Architecture analysis
│   │   ├── docs_agent.py           # Documentation generation
│   │   ├── parser_agent.py         # Code parsing agent
│   │   ├── rag_agent.py            # RAG for Q&A
│   │   └── security_agent.py       # Security scanning
│   │
│   ├── api/                         # FastAPI routes
│   │   ├── __init__.py
│   │   ├── main.py                 # Main API application
│   │   ├── models.py               # Pydantic models
│   │   └── routes.py               # API endpoints
│   │
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── code_parser.py          # AST-based code parsing
│   │   ├── embeddings.py           # Vector embeddings
│   │   ├── graph_builder.py        # Dependency graphs
│   │   ├── graph_rag.py            # Graph-based RAG
│   │   └── llm_client.py           # LLM API client
│   │
│   ├── utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── analytics.py            # Code analytics
│   │   ├── caching.py              # Redis caching
│   │   ├── file_analyzer.py        # File analysis
│   │   ├── repo_loader.py          # Git repository loader
│   │   ├── security_rules.py       # Security patterns
│   │   └── smell_detector.py       # Code smell detection
│   │
│   ├── config.py                    # Configuration management
│   ├── Dockerfile                   # Backend container
│   └── requirements.txt             # Python dependencies
│
├── data/                            # Data storage
│   ├── embeddings/                  # ChromaDB storage
│   │   └── chroma.sqlite3
│   ├── graphs/                      # Serialized graphs
│   │   └── *.json
│   └── repos/                       # Cloned repositories
│       └── */
│
├── frontend/                        # React application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── ArchitectureView.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── DependencyGraph.jsx
│   │   │   ├── SecurityPanel.jsx
│   │   │   └── StatsOverview.jsx
│   │   │
│   │   ├── pages/                   # Page components
│   │   │   ├── HomePage.jsx
│   │   │   └── RepositoryDashboard.jsx
│   │   │
│   │   ├── App.jsx                  # Main app component
│   │   ├── index.js                 # Entry point
│   │   └── index.css                # Global styles
│   │
│   ├── Dockerfile                   # Frontend container
│   ├── package.json                 # Node dependencies
│   ├── package-lock.json
│   ├── postcss.config.js            # PostCSS config
│   └── tailwind.config.js           # Tailwind config
│
├── tests/                           # Test suite
│   ├── test_api.py
│   ├── test_code_parser.py
│   └── test_graph_builder.py
│
├── .env.example                     # Environment template
├── .gitignore
├── config.py                        # Root configuration
├── docker-compose.yml               # Multi-container setup
├── README.md                        # This file
└── requirements.txt                 # Root dependencies
```

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis 7+
- Docker & Docker Compose (optional)
- Git

### Local Setup

#### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-codebase-engine.git
cd ai-codebase-engine
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install optional tools
pip install bandit safety pylint
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
```

#### 4. Redis Setup

```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install locally
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
brew services start redis
```

### Docker Setup (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# LLM Configuration
LLM_PROVIDER=openai              # openai or anthropic
LLM_MODEL=gpt-4-turbo-preview
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# Database
DATABASE_URL=sqlite:///./codebase.db

# Redis
REDIS_URL=redis://localhost:6379
REDIS_ENABLED=true
CACHE_TTL=3600

# Vector Store
CHROMA_PERSIST_DIRECTORY=./data/embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Paths
REPOS_DIRECTORY=./data/repos
GRAPHS_DIRECTORY=./data/graphs

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Code Analysis
SUPPORTED_LANGUAGES=["python","javascript","typescript","java","go"]
MAX_FILE_SIZE=1048576  # 1MB
```

### Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | Required if using Claude |
| `LLM_PROVIDER` | LLM provider (openai/anthropic) | `openai` |
| `REDIS_ENABLED` | Enable Redis caching | `true` |
| `EMBEDDING_MODEL` | Sentence transformer model | `all-MiniLM-L6-v2` |

## 📖 Usage

### Starting the Application

#### Backend (Development)

```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

#### Frontend (Development)

```bash
cd frontend
npm start
```

Frontend will be available at: `http://localhost:3000`

### Using the System

#### 1. Analyze a Repository

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/username/repo",
    "repo_id": "my-project"
  }'
```

#### 2. Query the Codebase

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does authentication work?",
    "repo_id": "my-project",
    "n_results": 5
  }'
```

#### 3. Security Scan

```bash
curl -X POST "http://localhost:8000/api/security/scan" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/file.py"
  }'
```

#### 4. Generate Documentation

```bash
curl -X POST "http://localhost:8000/api/docs/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "function",
    "code_data": {...}
  }'
```

### Python SDK Usage

```python
from rag_agent import RAGAgent
from security_agent import SecurityAgent
from code_parser import CodeParser

# Initialize agents
rag_agent = RAGAgent()
security_agent = SecurityAgent()
parser = CodeParser()

# Parse code
result = parser.parse_file("path/to/file.py")

# Ask questions
answer = rag_agent.ask("What does this function do?")

# Security scan
import asyncio
scan_result = asyncio.run(
    security_agent.process({"file_path": "path/to/file.py"})
)
```

## 🔌 API Documentation

### Core Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "cache_enabled": true,
  "embeddings_stats": {
    "total_chunks": 1234,
    "collection_name": "code_embeddings"
  }
}
```

#### Query Codebase (RAG)
```http
POST /api/query
Content-Type: application/json

{
  "query": "How does the authentication system work?",
  "repo_id": "my-project",
  "n_results": 5
}
```

**Response:**
```json
{
  "query": "How does the authentication system work?",
  "response": "The authentication system uses JWT tokens...",
  "retrieved_chunks": 5,
  "sources": [
    {
      "file_path": "auth/jwt.py",
      "type": "function",
      "name": "generate_token",
      "relevance_score": 0.89
    }
  ]
}
```

#### Parse Code
```http
POST /api/parse
Content-Type: application/json

{
  "file_path": "/path/to/file.py",
  "repo_id": "my-project"
}
```

**Response:**
```json
{
  "file_path": "/path/to/file.py",
  "language": "python",
  "functions": [...],
  "classes": [...],
  "imports": [...],
  "metrics": {
    "lines_of_code": 150,
    "complexity": 5.2
  }
}
```

#### Security Scan
```http
POST /api/security/scan
Content-Type: application/json

{
  "file_path": "/path/to/file.py"
}
```

**Response:**
```json
{
  "file_path": "/path/to/file.py",
  "vulnerabilities": [
    {
      "severity": "HIGH",
      "title": "SQL Injection vulnerability",
      "line_number": 45,
      "code": "cursor.execute(query)",
      "cwe_id": "CWE-89"
    }
  ],
  "total_issues": 3,
  "severity_breakdown": {
    "CRITICAL": 0,
    "HIGH": 2,
    "MEDIUM": 1,
    "LOW": 0
  }
}
```

#### Build Dependency Graph
```http
POST /api/graph/build
Content-Type: application/json

{
  "repo_id": "my-project",
  "directory": "/path/to/repo"
}
```

**Response:**
```json
{
  "repo_id": "my-project",
  "analysis": {
    "total_files": 45,
    "total_dependencies": 123,
    "circular_dependencies": 2
  },
  "graph_data": {
    "nodes": [...],
    "edges": [...]
  }
}
```

### Full API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤖 Agents

### Base Agent

All agents inherit from `BaseAgent` which provides:
- LLM integration (OpenAI/Anthropic)
- Conversation history management
- Context-aware generation
- Standardized processing interface

### RAG Agent

**Purpose**: Answer questions about codebase using retrieval-augmented generation

**Capabilities:**
- Semantic code search
- Context-aware question answering
- Code explanation
- Source attribution

**Example:**
```python
rag_agent = RAGAgent()
result = await rag_agent.process({
    "query": "How is user authentication implemented?",
    "repo_id": "my-project"
})
```

### Security Agent

**Purpose**: Detect security vulnerabilities and suggest fixes

**Capabilities:**
- Bandit integration for Python
- Pattern-based vulnerability detection
- AI-powered security review
- Remediation recommendations

**Detects:**
- SQL injection
- XSS vulnerabilities
- Hardcoded secrets
- Command injection
- Weak cryptography
- Input validation issues

### Architecture Agent

**Purpose**: Analyze system architecture and design patterns

**Capabilities:**
- Design pattern detection (MVC, Factory, Singleton, Observer)
- Coupling and cohesion analysis
- Modularity assessment
- Architectural recommendations

### Docs Agent

**Purpose**: Generate and improve documentation

**Capabilities:**
- Function/class/module documentation
- README generation
- API documentation
- Inline comment generation
- Documentation improvement

## 🎨 Frontend

### Components

#### Dashboard
- Overview statistics
- Recent activity
- Quick actions

#### Chat Interface
- Natural language queries
- Code snippets in responses
- Source references
- Conversation history

#### Dependency Graph
- Interactive D3.js visualization
- Zoom and pan
- Node filtering
- Cycle highlighting

#### Security Panel
- Vulnerability list
- Severity indicators
- Remediation guidance
- Trend analysis

### Pages

- **Home**: Landing page with project selection
- **Repository Dashboard**: Main analysis interface
- **Architecture View**: Design patterns and structure
- **Security Report**: Vulnerability overview

## 🛠️ Development

### Code Style

```bash
# Format code
black .

# Lint
pylint backend/

# Type checking
mypy backend/
```

### Adding a New Agent

1. Create agent file in `backend/agents/`
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Add to API routes
5. Update documentation

Example:
```python
from base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "MyCustomAgent",
            "Your custom system prompt"
        )
    
    async def process(self, input_data):
        # Your logic here
        return {"result": "..."}
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🧪 Testing

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=backend --cov-report=html

# Specific test file
pytest tests/test_code_parser.py

# Verbose
pytest -v
```

### Test Structure

```python
import pytest
from code_parser import CodeParser

def test_parse_python_file():
    parser = CodeParser()
    result = parser.parse_file("test_file.py")
    
    assert result["language"] == "python"
    assert len(result["functions"]) > 0
```

### Integration Tests

```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run integration tests
pytest tests/integration/

# Cleanup
docker-compose -f docker-compose.test.yml down
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Scale backend
docker-compose up -d --scale backend=3

# View logs
docker-compose logs -f backend

# Update services
docker-compose pull
docker-compose up -d
```

### Production Considerations

1. **Environment Variables**: Use secrets management (AWS Secrets Manager, HashiCorp Vault)
2. **Database**: Migrate to PostgreSQL for production
3. **Caching**: Use Redis Cluster for high availability
4. **Load Balancing**: Use Nginx or AWS ALB
5. **Monitoring**: Implement Prometheus + Grafana
6. **Logging**: Use ELK stack or CloudWatch
7. **SSL**: Configure HTTPS with Let's Encrypt

### Docker Compose (Production)

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/codebase
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    deploy:
      replicas: 3

  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=https://api.example.com

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secure_password

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 📊 Performance

### Optimization Tips

1. **Caching**: Enable Redis for frequently accessed data
2. **Batch Processing**: Use batch embeddings generation
3. **Lazy Loading**: Load large graphs on demand
4. **Connection Pooling**: Configure database connection pools
5. **CDN**: Serve static assets from CDN

### Benchmarks

| Operation | Time | Throughput |
|-----------|------|------------|
| Parse single file | ~50ms | 20 files/sec |
| Generate embeddings | ~200ms | 5 chunks/sec |
| RAG query | ~1.5s | 40 queries/min |
| Security scan | ~300ms | 3 files/sec |
| Graph build (100 files) | ~2s | - |

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Ensure CI/CD passes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude
- Hugging Face for Sentence Transformers
- ChromaDB team
- FastAPI community
- React team

## 📞 Support

- **Documentation**: [https://docs.example.com](https://docs.example.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-codebase-engine/issues)
- **Discord**: [Join our community](https://discord.gg/example)
- **Email**: support@example.com

## 🗺️ Roadmap

### Version 2.0 (Q2 2024)
- [ ] Support for more languages (Rust, C++, Ruby)
- [ ] Real-time collaboration features
- [ ] GitHub/GitLab integration
- [ ] Advanced refactoring suggestions
- [ ] ML-based bug prediction

### Version 3.0 (Q4 2024)
- [ ] IDE plugins (VSCode, JetBrains)
- [ ] Cloud-native deployment
- [ ] Enterprise SSO integration
- [ ] Advanced analytics dashboard
- [ ] Custom agent marketplace

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-codebase-engine)
![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-codebase-engine)
![GitHub issues](https://img.shields.io/github/issues/yourusername/ai-codebase-engine)
![License](https://img.shields.io/github/license/yourusername/ai-codebase-engine)

---

**Built with ❤️ by the AI Codebase Engine Team**

*Making code analysis intelligent, one repository at a time.*


## Developed By

- [Shashank0126](https://github.com/Shashank0126)
- [sadhvika761](https://github.com/sadhvika761)
