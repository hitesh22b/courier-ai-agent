# Courier Company AI Agent

A complete AI-powered customer service agent built with AWS Strands, Bedrock, and SST. This project demonstrates how to create a conversational AI that can track packages, create support tickets, answer policy questions, and maintain conversation context.

## 🚀 Features

- **🤖 Intelligent AI Agent**: Powered by AWS Bedrock (Amazon Nova model) with Strands framework
- **📦 Package Tracking**: Real-time package status lookup via tracking numbers
- **🎫 Support Tickets**: Automated ticket creation with validation and error handling
- **📚 Knowledge Base**: Policy and procedure queries with fuzzy text matching
- **💬 Session Management**: Persistent conversation memory using DynamoDB
- **🛠️ Tool Calling**: Modular, extensible tool architecture
- **☁️ Serverless**: Full serverless deployment with SST

## 🏗️ Architecture

```
User Request
     ↓
API Gateway (SST)
     ↓
Lambda Function (Python + Strands)
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   DynamoDB      │   Bedrock       │   External APIs │
│ (Session State) │ (AI Model)      │ (Tools/Services)│
└─────────────────┴─────────────────┴─────────────────┘
```

## 📋 Prerequisites

- AWS Account with appropriate permissions
- Node.js (for SST)
- Python 3.12+
- uv (Python package manager)

## 🚀 Quick Start

1. **Clone and install dependencies:**
```bash
git clone <your-repo>
cd ai-project
npm install
```

2. **Set up Python environment:**
```bash
uv sync
```

3. **Configure AWS credentials:**
```bash
aws configure
# or use AWS SSO, environment variables, etc.
```

4. **Deploy the infrastructure:**
```bash
npx sst deploy --stage dev
```

5. **Test the deployed endpoint:**
```bash
# Use the Python function URL from SST output
curl -X POST "YOUR_FUNCTION_URL" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Track package ABC123", "user_id": "test-user"}'
```

## 💡 Usage Examples

### Basic Conversation
```json
POST /your-function-url
{
  "prompt": "Hi, I need help tracking my package",
  "user_id": "customer-123"
}
```

### Package Tracking
```json
{
  "prompt": "Track package ABC123",
  "user_id": "customer-123"
}
```

### Support Ticket Creation
```json
{
  "prompt": "I want to file a complaint about damaged package. My email is john@example.com and phone is 555-1234",
  "user_id": "customer-123"
}
```

### Policy Questions
```json
{
  "prompt": "What's your refund policy?",
  "user_id": "customer-123"
}
```

## 🗂️ Project Structure

```
ai-project/
├── src/                        # TypeScript API handlers
│   ├── customer-care.ts        # Support ticket creation
│   ├── track-status.ts         # Package tracking
│   └── knowledge-base-query.ts # Policy search
├── python_functions/           # Python Strands agent
│   └── src/python_functions/
│       └── hello.py            # Main AI agent logic
├── sst.config.ts              # Infrastructure configuration
├── package.json               # Node.js dependencies
├── pyproject.toml            # Python project config
├── blog-post.md              # Detailed technical writeup
└── README.md                 # This file
```

## 🔧 Key Components

### AI Agent (Python + Strands)
- **Location**: `python_functions/src/python_functions/hello.py`
- **Purpose**: Main conversational AI with tool calling capabilities
- **Model**: Amazon Nova Micro via Bedrock
- **Tools**: Package tracking, support tickets, knowledge base search

### API Endpoints (TypeScript)
- **Customer Care**: Creates and validates support tickets
- **Package Tracking**: Looks up package status by ID
- **Knowledge Base**: Searches company policies and procedures

### Infrastructure (SST)
- **DynamoDB**: Session state storage
- **API Gateway**: HTTP endpoints for tools
- **Lambda Functions**: Serverless compute
- **IAM Roles**: Bedrock and DynamoDB permissions

## 🛠️ Development

### Adding New Tools
1. Create a new `@tool` function in `hello.py`
2. Register it in the Agent's tools list
3. Optionally create supporting API endpoints in `src/`

### Local Testing
```bash
# Test Python function locally
cd python_functions
uv run python -m pytest

# Test SST resources
npx sst dev --stage dev
```

### Deployment
```bash
# Deploy to AWS
npx sst deploy --stage dev

# Remove resources
npx sst remove --stage dev
```

## 📖 Learn More
- **🔗 AWS Strands**: [Documentation](https://github.com/aws/strands)
- **🔗 SST Framework**: [sst.dev](https://sst.dev)
- **🔗 AWS Bedrock**: [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)

## 🏷️ Tags

`ai-agent` `aws-bedrock` `strands` `sst` `serverless` `python` `typescript` `customer-service` `chatbot`
