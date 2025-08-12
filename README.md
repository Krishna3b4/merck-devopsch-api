# Merck DevOps Challenge API 🚀

**A production-ready, enterprise-grade FastAPI application showcasing modern cloud-native architecture, security best practices, and DevOps excellence.**

[![Deploy Backend](https://github.com/Krishna3b4/merck-devopsch-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/Krishna3b4/merck-devopsch-api/actions/workflows/deploy.yml)

## 🌟 Live Application

- **🌐 Application URL**: http://d-devops-challenge-alb-415511780.us-east-1.elb.amazonaws.com
- **📋 Health Check**: http://d-devops-challenge-alb-415511780.us-east-1.elb.amazonaws.com/health
- **📚 API Documentation**: http://d-devops-challenge-alb-415511780.us-east-1.elb.amazonaws.com/docs
- **📖 ReDoc**: http://d-devops-challenge-alb-415511780.us-east-1.elb.amazonaws.com/redoc

### 🔐 Demo Credentials
- **Username**: `krishna3w4@gmail.com`
- **Password**: `Password123!`

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Internet Gateway                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────────┐
│                   Application Load Balancer                    │
│                    (Public Subnets)                           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────────┐
│                    ECS Fargate Tasks                          │
│                   (Private Subnets)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   FastAPI   │  │   Cognito   │  │      CloudWatch         │ │
│  │ Application │  │    Auth     │  │      Monitoring         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────────────┐
│                     NAT Gateway                                │
│                  (Outbound Internet)                           │
└─────────────────────────────────────────────────────────────────┘
```

## 🛡️ Security Architecture & Best Practices

### 🔒 Network Security
- **Private Subnets**: ECS tasks run in private subnets with no direct internet access
- **NAT Gateway**: Secure outbound internet connectivity for private resources
- **Security Groups**: Least privilege access with specific port restrictions
- **VPC Endpoints**: Direct AWS service access without internet routing
  - ECR Docker Registry
  - ECR API Authentication
  - S3 for Docker layers
  - CloudWatch Logs

### 🔐 Authentication & Authorization
- **AWS Cognito**: Enterprise-grade user authentication
- **JWT Tokens**: Secure token-based API access
- **Password Policy**: Enforced complexity requirements
- **Email Verification**: Built-in user verification

### 🛡️ Application Security
- **Input Validation**: Pydantic models with strict validation
- **Security Scanning**: Automated vulnerability detection
  - Bandit for Python security issues
  - Safety for dependency vulnerabilities
  - Trivy for container scanning
- **Secrets Management**: No hardcoded credentials
- **HTTPS Ready**: SSL/TLS termination at ALB

### 🔍 Monitoring & Observability
- **CloudWatch Dashboards**: Real-time metrics visualization
- **Application Logs**: Centralized logging with retention policies
- **Health Checks**: Automated service health monitoring
- **Alarms**: Proactive alerting on performance thresholds

## 🏢 Infrastructure Components

### 🌐 Networking (VPC)
```yaml
Components:
  - VPC: 10.0.0.0/16
  - Public Subnets: 10.0.1.0/24, 10.0.2.0/24 (Multi-AZ)
  - Private Subnets: 10.0.3.0/24, 10.0.4.0/24 (Multi-AZ)
  - Internet Gateway: Public internet access
  - NAT Gateway: Secure outbound for private subnets
  - Route Tables: Proper traffic routing
```

### 🖥️ Compute (ECS Fargate)
```yaml
Components:
  - ECS Cluster: Serverless container orchestration
  - Task Definition: 0.25 vCPU, 0.5 GB RAM
  - Service: Auto-scaling, health checks
  - Application Load Balancer: High availability, SSL termination
  - Target Groups: Health check configuration
```

### 🔐 Authentication (Cognito)
```yaml
Components:
  - User Pool: User management and authentication
  - User Pool Client: Application integration
  - Password Policy: Security requirements
  - JWT Tokens: Secure API access
```

### 📊 Monitoring (CloudWatch)
```yaml
Components:
  - Log Groups: Application and infrastructure logs
  - Dashboards: Real-time metrics visualization
  - Alarms: Proactive monitoring and alerting
  - Metrics: ECS, ALB, and custom application metrics
```

### 🗂️ Storage (ECR)
```yaml
Components:
  - ECR Repository: Private Docker image registry
  - Lifecycle Policy: Automated image cleanup
  - Image Scanning: Vulnerability detection
```

## 🚀 CI/CD Pipeline Features

### 🔄 Automated Workflows
- **Multi-stage Pipeline**: Lint → Test → Build → Deploy
- **Change Detection**: Smart deployment based on file changes
- **Parallel Execution**: Optimized build times
- **Rollback Capability**: Safe deployment practices

### 🧪 Quality Assurance
```yaml
Code Quality:
  - Black: Code formatting
  - isort: Import sorting
  - flake8: Linting and style checks
  - pytest: Automated testing

Security:
  - Bandit: Python security analysis
  - Safety: Dependency vulnerability scanning
  - cfn-lint: CloudFormation template validation
```

### 📦 Build & Deployment
- **Docker Multi-stage**: Optimized container builds
- **ECR Integration**: Secure image storage
- **Blue-Green Deployment**: Zero-downtime updates
- **Infrastructure as Code**: CloudFormation templates

## 📊 API Endpoints

### 🌍 Public Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| POST | `/login` | Cognito authentication |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |

### 🔒 Protected Endpoints (Require Authentication)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get specific item |
| POST | `/items` | Create new item |

### 🔑 Authentication Flow
1. **Login**: POST to `/login` with credentials
2. **Token**: Receive Cognito access token
3. **Access**: Include token in `Authorization: Bearer <token>` header

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Docker
- AWS CLI (for deployment)

### Setup
```bash
# Clone repository
git clone https://github.com/Krishna3b4/merck-devopsch-api.git
cd merck-devopsch-api

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload

# Run tests
pytest app/ -v

# Code quality checks
black app/
isort app/
flake8 app/
bandit -r app/
safety check
```

### Docker Development
```bash
# Build image
docker build -t merck-api .

# Run container
docker run -p 8000:8000 merck-api
```

## ☁️ AWS Deployment

### Prerequisites
- AWS Account with appropriate permissions
- S3 bucket for CloudFormation artifacts
- GitHub repository with secrets configured

### Required GitHub Secrets
```yaml
Secrets:
  AWS_ACCESS_KEY_ID: AWS access key
  AWS_SECRET_ACCESS_KEY: AWS secret key
  CF_BUCKET: S3 bucket for CloudFormation packaging
```

### Deployment Methods

#### 1. Automatic (Recommended)
- Push to `main` branch triggers full deployment
- Pull requests trigger validation only

#### 2. Manual Workflow Dispatch
- Use GitHub Actions UI
- Select environment (dev/staging/prod)
- Optional force full deployment

#### 3. Manual CloudFormation
```bash
# Package templates
aws cloudformation package \
  --template-file cloudformation/nested/network/network.yml \
  --s3-bucket YOUR_BUCKET \
  --output-template-file packaged.yml

# Deploy infrastructure
aws cloudformation deploy \
  --template-file packaged.yml \
  --stack-name merck-devops-network \
  --capabilities CAPABILITY_IAM
```

## 📈 Monitoring & Observability

### CloudWatch Integration
- **Application Logs**: `/ecs/d-devops-challenge-api`
- **Metrics**: ECS service, ALB, and custom metrics
- **Dashboards**: Real-time performance visualization
- **Alarms**: CPU, memory, and error rate monitoring

### Health Monitoring
```bash
# Health check endpoint
curl http://d-devops-challenge-alb-415511780.us-east-1.elb.amazonaws.com/health

# Response
{"status":"healthy","environment":"dev"}
```

## 🔧 Configuration Management

### Environment Variables
```yaml
Application:
  ENV: Environment name (dev/staging/prod)
  AWS_REGION: AWS deployment region
  COGNITO_USER_POOL_ID: Cognito User Pool ID
  COGNITO_CLIENT_ID: Cognito Client ID

Infrastructure:
  Environment: Deployment environment
  ImageURI: ECR image URI for deployment
```

## 🏆 Production-Ready Features

### ✅ Reliability
- Multi-AZ deployment for high availability
- Auto-scaling capabilities
- Health checks and automatic recovery
- Load balancing across multiple instances

### ✅ Security
- Private subnet deployment
- VPC endpoints for AWS services
- IAM roles with least privilege
- Security group restrictions
- Automated security scanning

### ✅ Performance
- Containerized deployment
- Optimized Docker images
- CloudWatch monitoring
- Application Load Balancer

### ✅ Maintainability
- Infrastructure as Code
- Automated CI/CD pipeline
- Code quality enforcement
- Comprehensive documentation

### ✅ Observability
- Centralized logging
- Real-time metrics
- Performance dashboards
- Proactive alerting

## 🧪 Testing Strategy

### Automated Testing
```bash
# Unit tests
pytest app/test_main.py -v

# Integration tests
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

### Manual Testing
1. **Health Check**: Verify service availability
2. **Authentication**: Test Cognito login flow
3. **API Endpoints**: Validate all CRUD operations
4. **Error Handling**: Test invalid inputs and edge cases

## 📚 Additional Resources

### Documentation
- **API Documentation**: Available at `/docs` endpoint
- **Architecture Diagrams**: In `docs/` directory
- **Deployment Guide**: Step-by-step instructions

### Monitoring
- **CloudWatch Dashboard**: AWS Console
- **Application Logs**: CloudWatch Logs
- **Performance Metrics**: ECS and ALB metrics

### Security
- **Security Scanning Reports**: GitHub Actions artifacts
- **Vulnerability Database**: Automated dependency checks
- **Compliance**: Following AWS Well-Architected Framework

---

## 🎯 Challenge Completion Summary

**This implementation demonstrates:**

✅ **Modern Application Development**: FastAPI with async capabilities  
✅ **Cloud-Native Architecture**: ECS Fargate, ALB, Cognito  
✅ **Security Best Practices**: Private subnets, VPC endpoints, IAM roles  
✅ **DevOps Excellence**: CI/CD pipeline, IaC, automated testing  
✅ **Production Readiness**: Monitoring, logging, health checks  
✅ **Scalability**: Auto-scaling, load balancing, multi-AZ  
✅ **Maintainability**: Clean code, documentation, automation  

**Built with ❤️ for the Merck DevOps Challenge**

*Showcasing enterprise-grade cloud application development and deployment practices.*