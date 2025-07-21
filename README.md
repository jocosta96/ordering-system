# Sistema de Autoatendimento de Fast Food

Sistema de controle de pedidos para lanchonete desenvolvido como Tech Challenge da FASE 02, seguindo os princípios de Clean Architecture e Clean Code.

## 🏗️ Arquitetura do Sistema

### Diagrama de Arquitetura
[Visualizar diagrama completo no Miro](https://miro.com/app/board/uXjVIDKgo30=/?share_link_id=192061516718)

### Componentes da Arquitetura

#### **Camada de Domínio (Domain Layer)**
- **Entities**: Entidades de negócio (Order, Product, Customer, Ingredient)
- **Use Cases**: Casos de uso da aplicação
- **Value Objects**: Objetos de valor (Money, Status, Email, etc.)
- **Ports**: Interfaces para adapters

#### **Camada de Adaptadores (Adapter Layer)**
- **Inbound Adapters**: Controllers REST, Webhooks
- **Outbound Adapters**: Repositórios SQL, Integrações externas

#### **Infraestrutura Kubernetes**
- **Deployment**: Aplicação principal com múltiplos containers
- **HPA**: Auto-scaling baseado em CPU (30% - 5 réplicas)
- **Services**: Exposição da aplicação e banco de dados
- **Secrets/ConfigMaps**: Configurações sensíveis
- **Persistent Volumes**: Armazenamento persistente para PostgreSQL

### Fluxo de Pedidos
1. **Checkout**: Cliente cria pedido via `POST /order/checkout`
2. **Pagamento**: Sistema gera QR Code via `POST /order/payment_request/{order_id}`
3. **Confirmação**: Webhook recebe confirmação de pagamento
4. **Preparação**: Status atualizado para "EM_PREPARACAO"
5. **Acompanhamento**: Monitor exibe status em tempo real
6. **Finalização**: Pedido marcado como "FINALIZADO"

## 🚀 APIs Implementadas

### **1. Checkout de Pedido**
```http
POST /fastfood/api/order/checkout
Authorization: Basic <credentials>
Content-Type: application/json

{
  "customer_id": 1,
  "order_items": [
    {
      "product": {
        "name": "Hambúrguer Clássico",
        "price": {"amount": 15.90},
        "category": {"category": "LANCHE"},
        "sku": {"sku": "HAMB001"}
      },
      "additional_ingredient": [],
      "remove_ingredient": []
    }
  ]
}
```

### **2. Consultar Status de Pagamento**
```http
GET /fastfood/api/order/payment_status/{order_id}
```

**Resposta:**
```json
{
  "order_id": "uuid-do-pedido",
  "has_payment_verified": true,
  "payment_date": "2024-01-15T10:30:00",
  "payment_transaction_id": "tx_123456",
  "payment_message": "success",
  "order_status": "EM_PREPARACAO",
  "order_value": 15.90
}
```

### **3. Webhook para Confirmação de Pagamento**
```http
POST /webhook/mercadopago
Content-Type: application/json

{
  "order_id": "uuid-do-pedido",
  "transaction_id": "tx_123456",
  "approval_status": true,
  "message": "success",
  "date": "2024-01-15T10:30:00Z"
}
```

### **4. Lista de Pedidos Ordenada**
```http
GET /fastfood/api/order/list
```

**Ordenação:**
1. Pronto > Em Preparação > Recebido
2. Pedidos mais antigos primeiro
3. Pedidos "FINALIZADO" não aparecem

### **5. Atualizar Status do Pedido**
```http
PATCH /fastfood/api/order/update/{order_id}?status=PRONTO
Authorization: Basic <credentials>
```

### **6. Gerenciamento de Produtos**
```http
# Listar produtos
GET /fastfood/api/product/list

# Criar produto
POST /fastfood/api/product
Authorization: Basic <credentials>

# Atualizar produto
PUT /fastfood/api/product
Authorization: Basic <credentials>

# Deletar produto
DELETE /fastfood/api/product/{product_id}
Authorization: Basic <credentials>
```

### **7. Gerenciamento de Clientes**
```http
# Listar clientes
GET /fastfood/api/customer/list

# Criar cliente
POST /fastfood/api/customer
Authorization: Basic <credentials>

# Atualizar cliente
PUT /fastfood/api/customer
Authorization: Basic <credentials>

# Deletar cliente
DELETE /fastfood/api/customer/{customer_id}
Authorization: Basic <credentials>
```

### Swagger/OpenAPI
- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Banco de Dados**: PostgreSQL
- **Containerização**: Docker, Docker Compose
- **Orquestração**: Kubernetes (Minikube/Kind)
- **Pagamentos**: Mercado Pago (Mock/Integração)
- **Migrations**: Alembic
- **Testes**: Pytest

## 🚀 Instruções de Execução

### **Pré-requisitos**
- Docker e Docker Compose
- Kubernetes (Minikube ou Kind)
- kubectl configurado

### **1. Execução Local com Docker**

```bash
# Clone o repositório
git clone <repo-url>
cd ordering-system

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Execute com Docker Compose
docker compose up --build

# Acesse a aplicação
# API: http://localhost:8080
# Swagger: http://localhost:8080/docs
```

### **2. Execução no Kubernetes**

```bash
# Inicie o cluster (Minikube)
minikube start

# Aplique os manifests na ordem correta
kubectl apply -f infra/deployment/cfm_database.yaml
kubectl apply -f infra/deployment/sec_database.yaml
kubectl apply -f infra/deployment/pv_database.yaml
kubectl apply -f infra/deployment/pvc_database.yaml
kubectl apply -f infra/deployment/dpm_database.yaml
kubectl apply -f infra/deployment/svc_database.yaml
kubectl apply -f infra/deployment/sec_app.yaml
kubectl apply -f infra/deployment/dpm_app.yaml
kubectl apply -f infra/deployment/svc_app.yaml
kubectl apply -f infra/deployment/hpa_app.yaml

# Verifique os pods
kubectl get pods

# Acesse a aplicação
minikube service svc-app
```

### **3. Configuração das Variáveis de Ambiente**

```bash
# Database
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="password123"
POSTGRES_DB="fastfood"
POSTGRES_HOST="postgres"
DRIVER_NAME="postgresql"

# API Authentication
API_USER="admin"
API_PWD="admin123"

# PgAdmin (opcional)
PGADMIN_MAIL="admin@admin.com"
PGADMIN_PW="admin123"
```

## 🧪 Executando Testes

```bash
# Testes unitários
pytest

# Testes com coverage
pytest --cov=app

# Testes end-to-end
pytest tests/end_to_end.py
```

## 🔥 Stress Test - Demonstração do HPA

Para demonstrar o funcionamento do HPA (Horizontal Pod Autoscaler) e comprovar a escalabilidade automática do sistema:

### 🚀 **Teste de Estresse com Python (Recomendado)**

#### Pré-requisitos
`ip install -rdev/dev_requirements.txt`

**💡 Nota:** Se estiver usando **minikube**, o argumento `--api-url` é **opcional** - o script detecta automaticamente o IP do minikube.

#### Teste Básico
```bash
# Teste rápido com endpoint /health (IP detectado automaticamente)
python3 scripts/stress_test.py --scenario quick
```

#### Teste Intenso para Forçar Escalabilidade
```bash
# Teste com endpoint pesado que força escalabilidade
python3 scripts/stress_test.py --scenario custom \
  --duration 180 \
  --concurrency 100 \
  --endpoint /order/list
```

#### Parâmetros Disponíveis
```bash
python3 scripts/stress_test.py --help

# Cenários disponíveis:
# --scenario quick     # Teste rápido (20s, 5 conc)
# --scenario full      # Teste completo (60s, 25 conc)
# --scenario custom    # Teste personalizado

# Parâmetros customizáveis:
# --duration 180       # Duração em segundos
# --concurrency 100    # Número de requisições simultâneas
# --endpoint /order/list  # Endpoint a testar
# --api-url http://IP:30080  # URL da API (OPCIONAL - detecta automaticamente se minikube estiver rodando)
```

### 📊 **Monitoramento em Tempo Real**

#### Durante o Teste
```bash
# Terminal 1: Monitorar HPA
kubectl get hpa -w

# Terminal 2: Monitorar pods
kubectl get pods -l app=dpm-app -w

# Terminal 3: Ver métricas de CPU/Memory
kubectl top pods -l app=dpm-app
```

#### Verificar Status
```bash
# Status do HPA
kubectl get hpa

# Status dos pods
kubectl get pods -l app=dpm-app

# Métricas de recursos
kubectl top pods -l app=dpm-app
```

### 🎯 **Resultados Esperados**

#### Antes do Teste
```
NAME      REFERENCE            TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
hpa-app   Deployment/dpm-app   cpu: 2%/30%   1         5         1          26d
```

#### Durante o Teste (Alta Carga)
```
NAME      REFERENCE            TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
hpa-app   Deployment/dpm-app   cpu: 80%/30%   1         5         1          26d
```

#### Após Escalabilidade
```
NAME      REFERENCE            TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
hpa-app   Deployment/dpm-app   cpu: 1%/30%   1         5         3          26d
```

### 🔥 **Endpoints Recomendados para Teste**

| Endpoint | Carga | Descrição |
|----------|-------|-----------|
| `/health` | Baixa | Teste básico de conectividade |
| `/order/list` | **Alta** | **Recomendado para forçar escalabilidade** |
| `/order/queue/{status}` | Média | Consulta filtrada por status |
| `/product/list` | Média | Listagem de produtos |

### 📈 **Métricas de Performance**

#### Exemplo de Resultado de Teste
```
📋 Resultados do Stress Test
==================================================
Total de Requisições: 100
Requisições Bem-sucedidas: 100
Requisições Falharam: 0
Taxa de Sucesso: 100.00%
Duração Média: 12.274s
Duração Mínima: 0.206s
Duração Máxima: 12.446s
Requisições por Segundo: 8.03
```

### 🎉 **Demonstração do HPA**

O teste com `/order/list` é ideal para demonstrar o HPA porque:
- ✅ Faz consultas complexas no banco de dados
- ✅ Inclui ordenação e filtros
- ✅ Gera carga suficiente para atingir >30% CPU
- ✅ Força o escalonamento automático de 1 para 3+ pods
- ✅ Demonstra distribuição de carga

### 🛠️ **Troubleshooting**

#### Se o teste falhar:
```bash
# Verificar se a aplicação está rodando
curl http://$(minikube ip):30080/health

# Verificar logs da aplicação
kubectl logs -f deployment/dpm-app

# Verificar se o minikube está ativo
minikube status
```

#### Se o HPA não escalar:
```bash
# Verificar configuração do HPA
kubectl describe hpa hpa-app

# Verificar métricas do cluster
kubectl top nodes

# Aumentar carga do teste
python3 scripts/stress_test.py --scenario custom --duration 300 --concurrency 150
```

**📖 Documentação completa**: [scripts/README.md](scripts/README.md)

## 📊 Monitoramento e Métricas

O sistema inclui:
- **Health Checks**: `/health` e `/customer/anonymous`
- **HPA**: Auto-scaling baseado em CPU (30% - 5 réplicas)
- **Métricas**: Prometheus/Grafana (configuração opcional)

## 🔒 Segurança

- **Autenticação**: Basic Auth para endpoints administrativos
- **Secrets**: Credenciais sensíveis em Kubernetes Secrets
- **ConfigMaps**: Configurações não-sensíveis
- **Validação**: Pydantic para validação de entrada

## 📱 Funcionalidades do Sistema

### **Para Clientes:**
- ✅ Identificação via CPF ou cadastro anônimo
- ✅ Montagem de combos (Lanche, Acompanhamento, Bebida)
- ✅ Pagamento via QR Code
- ✅ Acompanhamento em tempo real
- ✅ Notificação de pedido pronto

### **Para Administração:**
- ✅ Gerenciamento de clientes
- ✅ Gerenciamento de produtos e categorias
- ✅ Acompanhamento de pedidos
- ✅ Controle de estoque de ingredientes

## 🎥 Vídeo Demonstrativo

[Assistir vídeo demonstrativo no YouTube](https://youtu.be/SEU_VIDEO_ID)

## 📝 Status dos Requisitos

| Requisito | Status | Observações |
|-----------|--------|-------------|
| Clean Architecture | ✅ | Implementado |
| APIs de Pedido | ✅ | Todas implementadas |
| Webhook Pagamento | ✅ | Funcionando |
| Kubernetes | ✅ | HPA, Secrets, ConfigMaps |
| Documentação | ✅ | README completo |
| Collection Postman | ✅ | postman_collection.json |
| Stress Test HPA | ✅ | Scripts Python + documentação |
| Vídeo Demonstrativo | ⚠️ | Link para YouTube |

## 🤝 Contribuição

Este projeto tem fins educacionais. Pull requests são aceitos apenas dos membros do projeto.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.


**Desenvolvido para o Tech Challenge FASE 02 - Arquitetura de Software**
