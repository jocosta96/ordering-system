# Fast Food Self-Ordering Backend System

A **production-ready, cloud-native fast food self-ordering backend system** built with **Clean Architecture principles**. This system enables customers to place orders, make payments via QR codes, and track order status in real-time, while providing comprehensive administration capabilities.

## 🎯 System Overview

- **Domain**: Fast food restaurant self-ordering system
- **Architecture**: Clean Architecture with hexagonal patterns  
- **Tech Stack**: FastAPI + PostgreSQL + Kubernetes + AWS
- **Environment**: Production-ready system with AWS cloud infrastructure
- **Development**: Multi-repository pattern with infrastructure as code

## 🏗️ Architecture Overview

### Multi-Repository Architecture
```
ordering-system-data  →  AWS Parameter Store  ←  ordering-system-infra
       (RDS DB)              (Shared Config)           (EKS Cluster)
                                    ↑
                              ordering-system
                              (FastAPI App)
```

### Clean Architecture Layers
```
External → Controllers → Use Cases → Entities
         ↑                      ↓
   Repositories ← Gateways ← Repositories (interfaces)
```

### System Components

#### **Domain Layer (Entities)**
- **Entities**: Core business entities (Order, Product, Customer, Ingredient)
- **Value Objects**: Immutable objects (Money, Email, OrderStatus, SKU)
- **Business Rules**: Domain logic and validation

#### **Application Layer (Use Cases)**  
- **Use Cases**: Business logic orchestration
- **Repository Interfaces**: Ports for external dependencies
- **DTOs**: Data transfer objects for layer communication

#### **Interface Adapters Layer**
- **Controllers**: HTTP request handling
- **Gateways**: Repository implementations 
- **Presenters**: Response formatting
- **Routes**: API endpoint definitions

#### **Infrastructure Layer**
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Kubernetes**: Container orchestration with auto-scaling
- **AWS Cloud**: EKS, RDS, Parameter Store, S3

## 🚀 API Architecture & Endpoints

### Core Business Endpoints

#### Order Management
```http
POST /fastfood/api/order/checkout           # Create new order
GET  /fastfood/api/order/payment_status/{id} # Check payment status
GET  /fastfood/api/order/list               # List orders (prioritized)
PATCH /fastfood/api/order/update/{id}       # Update order status
POST /fastfood/api/order/payment_request/{id} # Generate QR code
```

#### Product Management (Admin)
```http
GET    /fastfood/api/product/list           # List products
POST   /fastfood/api/product                # Create product (Auth required)
PUT    /fastfood/api/product                # Update product (Auth required)
DELETE /fastfood/api/product/{id}           # Delete product (Auth required)
```

#### Customer Management (Admin)
```http
GET    /fastfood/api/customer/list          # List customers
POST   /fastfood/api/customer               # Create customer (Auth required)
PUT    /fastfood/api/customer               # Update customer (Auth required)
DELETE /fastfood/api/customer/{id}          # Delete customer (Auth required)
```

#### Ingredient Management (Admin)
```http
GET    /fastfood/api/ingredient/list        # List ingredients
POST   /fastfood/api/ingredient             # Create ingredient (Auth required)
PUT    /fastfood/api/ingredient             # Update ingredient (Auth required)
DELETE /fastfood/api/ingredient/{id}        # Delete ingredient (Auth required)
```

### Business Logic Implementation

#### Order Status Flow
1. **RECEBIDO** → Order created, awaiting payment
2. **EM_PREPARACAO** → Payment confirmed, cooking starts
3. **PRONTO** → Order ready for pickup
4. **FINALIZADO** → Order completed (not shown in queue)

#### Order Priority Queue
1. **PRONTO** orders (ready for pickup) - highest priority
2. **EM_PREPARACAO** orders (being prepared)
3. **RECEBIDO** orders (payment pending) - lowest priority
4. Within same status: older orders first

## 💳 Payment Integration

### QR Code Payment Flow
1. Customer creates order → Status: `RECEBIDO`
2. System generates QR code payment request
3. Customer pays via external payment provider
4. Webhook receives payment confirmation
5. Order status updated to `EM_PREPARACAO`

### Payment Webhook
```http
POST /webhook/mercadopago
Content-Type: application/json

{
  "order_id": "uuid",
  "transaction_id": "tx_123",
  "approval_status": true,
  "message": "success",
  "date": "2024-01-15T10:30:00Z"
}
```

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI 0.113+**: Modern, fast web framework with automatic API documentation
- **Pydantic v2**: Data validation and settings management
- **SQLAlchemy 2.0.40**: Modern Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL 16.4**: Advanced open-source relational database

### Cloud & Infrastructure  
- **AWS EKS**: Managed Kubernetes service
- **AWS RDS**: Managed PostgreSQL database
- **AWS Parameter Store**: Centralized configuration management
- **AWS S3**: Object storage for Terraform state
- **Docker**: Containerization with multi-stage builds

### DevOps & Monitoring
- **Kubernetes**: Container orchestration with HPA
- **Prometheus/Grafana**: Metrics and monitoring (optional)
- **Horizontal Pod Autoscaler**: Auto-scaling (1-5 replicas, 30% CPU)
- **Health Probes**: Readiness and liveness checks
- **Structured Logging**: Context-aware logging system

### Development Tools
- **Pytest**: Testing framework with 79% code coverage
- **Pre-commit Hooks**: Code quality enforcement
- **Swagger/OpenAPI**: Automatic API documentation
- **SlowAPI**: Rate limiting for API protection

## 🔧 Infrastructure Architecture

### Deployment Dependencies
1. **Deploy `ordering-system-data` FIRST** (creates shared config)
2. **Deploy `ordering-system-infra` SECOND** (reads shared config)  
3. **Application automatically connects** to shared resources

### Shared Configuration System
- **Database credentials** stored in Parameter Store
- **Network configuration** shared between repositories
- **Automatic integration** via Terraform data sources
- **Encrypted secrets** for sensitive information

### Auto-Scaling Configuration
- **HPA (Horizontal Pod Autoscaler)**: 1-5 replicas
- **CPU Threshold**: 30% utilization
- **Metrics Server**: Full metrics collection
- **Health Probes**: Readiness and liveness checks

## 🧪 Testing Strategy

### Test Architecture
- **Unit Tests**: Entity business logic, use case orchestration
- **Integration Tests**: Controller and repository implementations
- **Coverage**: 79% with comprehensive test scenarios
- **Mocking**: External dependencies properly mocked

### Running Tests
```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Full coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Specific test files
pytest tests/unit/test_entities.py -v
pytest tests/integration/test_controllers.py -v
```

## 📊 Monitoring & Scaling

### Stress Testing & HPA Demonstration

The system includes comprehensive stress testing capabilities to demonstrate auto-scaling:

#### Quick Stress Test
```bash
# Quick test with automatic IP detection
python infra/scripts/stress_test.py --scenario quick
```

#### Intensive Test for Scaling
```bash
# Test that forces auto-scaling
python infra/scripts/stress_test.py --scenario custom \
  --duration 180 \
  --concurrency 100 \
  --endpoint /order/list
```

#### Available Scenarios
- **Quick**: 3 progressive load scenarios (30s-60s)
- **Full**: 11 comprehensive scenarios (60s-600s)  
- **Custom**: Fully customizable parameters

#### Monitoring During Tests
```bash
# Terminal 1: Monitor HPA
kubectl get hpa -w

# Terminal 2: Monitor pods  
kubectl get pods -l app=dpm-app -w

# Terminal 3: View resource metrics
kubectl top pods -l app=dpm-app
```

### Expected Scaling Results

#### Before Test
```
NAME      REFERENCE            TARGETS       MINPODS   MAXPODS   REPLICAS
hpa-app   Deployment/dpm-app   cpu: 2%/30%   1         5         1
```

#### During High Load
```
NAME      REFERENCE            TARGETS        MINPODS   MAXPODS   REPLICAS
hpa-app   Deployment/dpm-app   cpu: 80%/30%   1         5         1
```

#### After Scaling
```
NAME      REFERENCE            TARGETS       MINPODS   MAXPODS   REPLICAS  
hpa-app   Deployment/dpm-app   cpu: 1%/30%   1         5         3
```

## 🔒 Security Implementation

### Authentication Patterns
- **Public endpoints**: Order creation, product listing, health checks
- **Admin endpoints**: Require Basic Auth (API_USER/API_PWD)
- **Webhook endpoints**: Secure callback handling

### Data Protection
- **Input validation**: Pydantic models with comprehensive validation
- **SQL injection prevention**: SQLAlchemy ORM patterns
- **Rate limiting**: API protection against abuse
- **CORS configuration**: Controlled cross-origin access
- **Encrypted secrets**: AWS Parameter Store with encryption

### Security Configuration
```bash
# Environment Variables
API_USER="admin"           # Admin username
API_PWD="admin123"         # Admin password (change in production)
POSTGRES_PASSWORD="..."    # Encrypted in Parameter Store
```

## 📝 Development Workflow

### Adding New Features (Clean Architecture Order)

#### Phase 1: Domain Layer
1. Create value objects in `src/entities/value_objects/`
2. Create/update entities in `src/entities/`
3. Add business rules and validation

#### Phase 2: Application Layer  
1. Create repository interface in `src/application/repositories/`
2. Create DTOs in `src/application/dto/`
3. Create use cases in `src/application/use_cases/`

#### Phase 3: Interface Adapters
1. Implement repository in `src/adapters/gateways/`
2. Create controller in `src/adapters/controllers/`
3. Create routes in `src/adapters/routes/`
4. Update dependency injection container
5. Update presenter for new response formats
6. Register routes in `src/main.py`

#### Phase 4: Testing & Deployment
1. Write comprehensive tests
2. Update documentation
3. Deploy using deployment scripts

### Naming Conventions
- **Entities**: `Customer`, `Order`, `Product`
- **Value Objects**: `Email`, `Money`, `OrderStatus`  
- **Use Cases**: `CustomerCreateUseCase`, `OrderListUseCase`
- **DTOs**: `CustomerCreateRequest`, `OrderResponse`
- **Controllers**: `CustomerController`, `OrderController`
- **Files**: Snake_case (`customer_controller.py`, `order_use_cases.py`)

## 🚀 Deployment & Operations

### Multi-Repository Deployment Order

#### 1. Database Infrastructure First
```bash
cd ordering-system-data
terraform init
terraform plan
terraform apply
```

#### 2. Application Infrastructure Second
```bash  
cd ordering-system-infra
terraform init
terraform plan
terraform apply
```

#### 3. Application Deployment (Automatic)
The application is automatically deployed when the infrastructure is provisioned.

## 🔧 Configuration Management

The application supports multiple configuration sources with priority:
1. **AWS SSM Parameter Store** (production recommended)
2. **Environment Variables** (fallback/development)
3. **Default Values** (development only)

### AWS SSM Parameter Store Configuration

For production deployments, database configuration is managed via AWS SSM Parameter Store, allowing runtime configuration updates without application restarts.

#### Required SSM Parameters:
```
/fastfood/database/host       # Database hostname
/fastfood/database/port       # Database port (5432)
/fastfood/database/database   # Database name (fastfood)
/fastfood/database/username   # Database username
/fastfood/database/password   # Database password (SecureString)
/fastfood/database/driver     # Database driver (postgresql)
```

#### Setup SSM Parameters:
```bash
# Export your database configuration
export DB_HOST=your-rds-endpoint.amazonaws.com
export DB_PASSWORD=your-secure-password
export DB_USERNAME=postgres
export DB_NAME=fastfood

# Run the setup script
./scripts/setup-ssm-parameters.sh --region us-east-1
```

#### AWS Credentials Setup:

**For AWS Labs Environment** (with temporary credentials):

1. Set AWS credentials via API (credentials change frequently in labs):
```bash
curl -X POST http://your-app/health/aws-credentials \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{
    "aws_access_key_id": "AKIA...",
    "aws_secret_access_key": "your-secret-key",
    "aws_session_token": "your-session-token"
  }'
```

2. Verify credentials are set:
```bash
curl http://your-app/health/aws-credentials -u admin:admin123
```

3. Deploy manifests (no IAM roles needed):
```bash
kubectl apply -f dev/k8s/cfm_database.yaml
kubectl apply -f dev/k8s/dpm_app.yaml
kubectl apply -f dev/k8s/dpm_webhook.yaml
```

**For Production Environment** (with IAM roles):
- Create IAM role with SSM permissions
- Use IRSA (IAM Roles for Service Accounts) instead of direct credentials
- See AWS documentation for production setup

#### Configuration Health & Monitoring:
```bash
# Check configuration status
curl http://your-app/health/config

# Reload configuration without restart
curl -X POST http://your-app/health/config/reload
```

### Environment Variables (Fallback)

For local development or when SSM is unavailable:

```bash
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastfood
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
DRIVER_NAME=postgresql

# API Authentication
API_USER=admin
API_PWD=admin123

# Application Settings
LOG_LEVEL=INFO
DEBUG=false

# AWS SSM Configuration
USE_SSM_PARAMETERS=true
AWS_DEFAULT_REGION=us-east-1
SSM_PARAMETER_PREFIX=/fastfood/database/
```

### Local Development
```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment variables (for local development)
export POSTGRES_HOST="localhost"
export POSTGRES_USER="postgres"  
export POSTGRES_PASSWORD="password123"
export POSTGRES_DB="fastfood"
export API_USER="admin"
export API_PWD="admin123"
export USE_SSM_PARAMETERS="false"  # Disable SSM for local development

# Run application
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Kubernetes Operations
```bash
# Quick deployment (if infrastructure exists)
sh infra/scripts/k8s-deploy.sh

# Manual deployment
kubectl apply -f infra/deployment/ -R

# Update application
kubectl rollout restart deployment/dpm-app

# View logs
kubectl logs -f deployment/dpm-app

# Check scaling status
kubectl get hpa
kubectl get pods -l app=dpm-app
```

## 📚 Documentation & Resources

### API Documentation
- **Swagger UI**: Available at `/docs` endpoint
- **ReDoc**: Available at `/redoc` endpoint
- **OpenAPI Spec**: Auto-generated from FastAPI

### Architecture Guides
- **Clean Architecture**: `CLEAN_ARCHITECTURE_CHECKLIST.md`
- **System Overview**: `FASTFOOD_ORDERING_SYSTEM_PROMPT.md`
- **Infrastructure Guide**: See `ordering-system-infra/README.md`
- **Database Guide**: See `ordering-system-data/README.md`

### Deployment Resources
- **Repository-specific READMEs**: Detailed deployment instructions
- **Terraform Documentation**: Infrastructure as code patterns
- **Kubernetes Manifests**: Production-ready configurations

## 🎯 Key Development Principles

1. **Clean Architecture First**: Always follow dependency inversion
2. **Domain-Driven Design**: Business rules in entities, not controllers
3. **Test-Driven Development**: Write tests for business logic
4. **Infrastructure as Code**: All infrastructure versioned and automated  
5. **Multi-Repository Coordination**: Maintain shared configuration integrity
6. **Security by Design**: Authentication, validation, and secure defaults
7. **Observability**: Comprehensive logging, monitoring, and health checks

## ⚡ Quick Reference

### Essential Configuration
```bash
# Production (SSM Parameter Store)
/fastfood/database/host, /fastfood/database/username, /fastfood/database/password, etc.

# Development (Environment Variables)
POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
API_USER, API_PWD
USE_SSM_PARAMETERS, AWS_DEFAULT_REGION, SSM_PARAMETER_PREFIX

# Application Settings  
LOG_LEVEL, DEBUG
```

### Health Check Endpoints
```bash
# Basic health check
curl http://localhost:8080/health

# Database connectivity
curl http://localhost:8080/health/db

# Configuration status (SSM + Environment + AWS Credentials)
curl http://localhost:8080/health/config

# AWS Credentials management (for labs environment) - Requires Admin Auth
# Set AWS credentials
curl -X POST http://localhost:8080/health/aws-credentials \
  -H "Content-Type: application/json" \
  -u admin:admin123 \
  -d '{"aws_access_key_id":"AKIA...","aws_secret_access_key":"secret","aws_session_token":"token"}'

# Check AWS credentials status  
curl http://localhost:8080/health/aws-credentials -u admin:admin123

# Clear AWS credentials
curl -X DELETE http://localhost:8080/health/aws-credentials -u admin:admin123

# Reload SSM configuration without restart
curl -X POST http://localhost:8080/health/config/reload

# Stress testing for auto-scaling
python infra/scripts/stress_test.py --scenario full
```

## 📊 Monitoramento e Métricas

O sistema inclui:
- **Health Checks**: `/health`, `/health/db`, `/health/config`
- **Configuration Management**: Runtime reload via `/health/config/reload`
- **AWS Credentials Management**: Set/check/clear credentials via `/health/aws-credentials`
- **SSM Parameter Store**: Monitoramento de conectividade e status
- **HPA**: Auto-scaling baseado em CPU (30% - 5 réplicas)
- **Métricas**: Prometheus/Grafana (configuração opcional)
- **Logs Estruturados**: Com contexto e níveis configuráveis
- **Readiness/Liveness Probes**: Para Kubernetes

## 🔒 Segurança

- **Autenticação**: Basic Auth para endpoints administrativos
- **Secrets Management**: 
  - **Produção**: AWS SSM Parameter Store com SecureString (encrypted)
  - **Desenvolvimento**: Kubernetes Secrets / Environment Variables
- **ConfigMaps**: Configurações não-sensíveis
- **IAM Integration**: Service accounts com roles específicos para SSM
- **Validação**: Pydantic para validação de entrada
- **CORS**: Configurado para permitir origens específicas
- **Rate Limiting**: Proteção contra abuso de API

## 📱 Funcionalidades do Sistema

### **Para Clientes:**
- ✅ Identificação via CPF ou cadastro anônimo
- ✅ Montagem de combos (Lanche, Acompanhamento, Bebida)
- ✅ Pagamento via QR Code
- ✅ Acompanhamento em tempo real
- ✅ Notificação de pedido pronto
- ✅ Histórico de pedidos

### **Para Administração:**
- ✅ Gerenciamento de clientes
- ✅ Gerenciamento de produtos e categorias
- ✅ Acompanhamento de pedidos
- ✅ Controle de estoque de ingredientes
- ✅ Relatórios de vendas
- ✅ Gestão de pagamentos

## 🎥 Vídeo Demonstrativo

[Assistir vídeo demonstrativo no YouTube](https://www.youtube.com/watch?v=m7bB2DgLaSQ)

## 📝 Status dos Requisitos

| Requisito | Status | Observações |
|-----------|--------|-------------|
| Clean Architecture | ✅ | Implementado com separação clara de camadas |
| APIs de Pedido | ✅ | Todas implementadas |
| Webhook Pagamento | ✅ | Funcionando |
| Kubernetes | ✅ | HPA, Secrets, ConfigMaps |
| Documentação | ✅ | README completo |
| Collection Postman | ✅ | postman_collection.json |
| Stress Test HPA | ✅ | Scripts Python + documentação |
| Testes Automatizados | ✅ | 79% de cobertura |
| Logs Estruturados | ✅ | Implementado |
| Vídeo Demonstrativo | ✅ | Link para YouTube |

## 🛠️ Desenvolvimento

### **Estrutura de Desenvolvimento**

O projeto segue os princípios de Clean Architecture com as seguintes camadas:

1. **Entities** (`src/entities/`): Regras de negócio centrais
2. **Application** (`src/application/`): Casos de uso e interfaces
3. **Adapters** (`src/adapters/`): Controllers, repositórios e presenters
4. **Infrastructure** (`infra/`): Configuração Kubernetes e scripts

### **Guia de Desenvolvimento**

Consulte o arquivo `CLEAN_ARCHITECTURE_CHECKLIST.md` para um guia passo-a-passo de como adicionar novas funcionalidades seguindo os princípios de Clean Architecture.

### **Comandos Úteis**

```bash
# Create test order
curl -X POST http://localhost:8080/fastfood/api/order/checkout \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "order_items": [...]}'

# Check order status
curl http://localhost:8080/fastfood/api/order/payment_status/{order_id}

# Run stress test
python infra/scripts/stress_test.py --scenario quick
```

## 📋 System Requirements Status

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Clean Architecture | ✅ | Complete separation of concerns |
| Order Management APIs | ✅ | All endpoints implemented |
| Payment Integration | ✅ | QR code + webhook system |  
| Kubernetes Deployment | ✅ | HPA, secrets, services |
| Multi-Repository Setup | ✅ | Shared configuration system |
| AWS Cloud Native | ✅ | EKS, RDS, Parameter Store |
| Auto-Scaling | ✅ | HPA with stress testing |
| Security | ✅ | Authentication + validation |
| Monitoring | ✅ | Health checks + metrics |
| Testing | ✅ | 79% coverage with integration tests |
| Documentation | ✅ | Comprehensive guides |

---

**🎯 Production-Ready System**: This represents a **production-ready, enterprise-grade fast food ordering backend** built with Clean Architecture principles, comprehensive testing, and cloud-native deployment practices. Always maintain the architectural integrity and follow the established patterns when extending functionality.

**📖 For detailed deployment instructions**, see the individual repository README files:
- **Database**: `ordering-system-data/README.md`
- **Infrastructure**: `ordering-system-infra/README.md`  
- **Application**: This file

**Desenvolvido para o Tech Challenge FASE 02 - Arquitetura de Software**
