# Merck DevOps Challenge API

A production-ready FastAPI application with complete AWS infrastructure and CI/CD pipeline.

## 🚀 Features

- **FastAPI Application**: Modern Python API with automatic documentation
- **AWS Infrastructure**: Complete ECS Fargate deployment with ALB
- **CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- **Monitoring**: CloudWatch dashboards and alarms
- **Containerized**: Docker-ready application

## 🏗️ Architecture

- **Network**: VPC with public subnets across multiple AZs
- **Compute**: ECS Fargate cluster with Application Load Balancer
- **Monitoring**: CloudWatch dashboards and CPU utilization alarms
- **Security**: Security groups with least privilege access

## 🛠️ Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Run tests**:
   ```bash
   pytest app/test_main.py -v
   ```

4. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🐳 Docker

```bash
# Build image
docker build -t merck-api .

# Run container
docker run -p 8000:8000 merck-api
```

## ☁️ AWS Deployment

### Prerequisites
- AWS CLI configured
- S3 bucket for CloudFormation templates
- ECR repository (created automatically)

### GitHub Secrets Required
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `CF_BUCKET` (S3 bucket for CloudFormation packaging)

### Deploy
1. Push to main branch for automatic deployment
2. Or use manual workflow dispatch with environment selection

### Manual Deployment
```bash
# Package templates
aws cloudformation package \
  --template-file cloudformation/main.yml \
  --s3-bucket YOUR_BUCKET \
  --output-template-file packaged.yml

# Deploy stack
aws cloudformation deploy \
  --template-file packaged.yml \
  --stack-name dev-merck-devopsch \
  --parameter-overrides Environment=dev ImageURI=YOUR_IMAGE_URI \
  --capabilities CAPABILITY_IAM
```

## 📊 API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `POST /login` - Login to get access token

### Protected Endpoints (require authentication)
- `GET /items` - List all items
- `GET /items/{id}` - Get specific item
- `POST /items` - Create new item

### Authentication
Use the `/login` endpoint with demo credentials:
```json
{
  "username": "demo",
  "password": "password123"
}
```
Then include the token in requests:
```
Authorization: Bearer <your-token>
```

## 🔧 Configuration

Copy `.env.example` to `.env` and adjust values:
```bash
ENV=development
AWS_REGION=us-east-1
LOG_LEVEL=INFO
```

## 📈 Monitoring

After deployment, access:
- CloudWatch Dashboard: Available in AWS Console
- Application Logs: CloudWatch Logs `/ecs/{environment}-merck-api`
- Metrics: ECS service and ALB metrics

## 🏆 Production Ready Features

✅ Comprehensive error handling and logging  
✅ Input validation with Pydantic models  
✅ Health checks and monitoring  
✅ Security groups and IAM roles  
✅ Automated testing and deployment  
✅ Infrastructure as Code  
✅ Container orchestration  
✅ Load balancing and auto-scaling ready  
✅ Code quality enforcement (Black, isort, flake8)  
✅ Security scanning (Bandit, Safety, Trivy)  
✅ Change detection for optimized deployments  
✅ PR validation and conventional commits  
✅ Comprehensive linting and validation  

## 🔧 Development Workflow

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/

# Security scan
bandit -r app/
safety check
```

### Infrastructure Changes
- CloudFormation templates are linted with cfn-lint
- Infrastructure changes trigger full redeployment
- Separate validation for infrastructure vs application changes  

---

**Built for the Merck DevOps Challenge** - Demonstrating modern cloud-native application development and deployment practices.