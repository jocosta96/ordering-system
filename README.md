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

### Estrutura do Projeto

```
ordering-system/
├── src/                          # Código fonte principal
│   ├── adapters/                 # Camada de adaptadores
│   │   ├── controllers/          # Controllers
│   │   ├── gateways/             # Implementações de repositórios
│   │   ├── presenters/           # Formatação de respostas
│   │   └── routes/               # Definição de rotas
│   ├── application/              # Camada de aplicação
│   │   ├── dto/                  # Objetos de transferência
│   │   ├── repositories/         # Interfaces de repositórios
│   │   └── use_cases/            # Casos de uso
│   ├── entities/                 # Camada de domínio
│   │   ├── value_objects/        # Objetos de valor
│   │   └── *.py                  # Entidades de negócio
│   ├── config/                   # Configurações
│   └── security/                 # Autenticação e segurança
├── infra/                        # Infraestrutura Kubernetes
│   ├── deployment/               # Manifests de deploy
│   ├── maintenance/              # Jobs de manutenção
│   └── scripts/                  # Scripts de automação
├── tests/                        # Testes automatizados
│   ├── unit/                     # Testes unitários
│   └── integration/              # Testes de integração
└── webhook/                      # Webhooks externos
```

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

### **8. Gerenciamento de Ingredientes**
```http
# Listar ingredientes
GET /fastfood/api/ingredient/list

# Criar ingrediente
POST /fastfood/api/ingredient
Authorization: Basic <credentials>

# Atualizar ingrediente
PUT /fastfood/api/ingredient
Authorization: Basic <credentials>

# Deletar ingrediente
DELETE /fastfood/api/ingredient/{ingredient_id}
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
- **Logging**: Structured logging com contexto
- **Validação**: Pydantic para validação de entrada
- **Autenticação**: Basic Auth para endpoints administrativos

## 🚀 Instruções de Execução

### **Pré-requisitos**
- Docker e Docker Compose
- Kubernetes (Minikube ou Kind)
- kubectl configurado
- Python 3.10+ (para desenvolvimento local)

### **1. Setup Rápido (Recomendado)**

```bash
# Clone o repositório
git clone <repository-url>
cd ordering-system

# Execute o script de inicialização
sh infra/scripts/k8s-deploy.sh
```

### **2. Setup Manual**

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

### **3. Desenvolvimento Local**

```bash
# Ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure as variáveis de ambiente
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="password123"
export POSTGRES_DB="fastfood"
export POSTGRES_HOST="localhost"
export API_USER="admin"
export API_PWD="admin123"

# Execute a aplicação
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### **4. Configuração das Variáveis de Ambiente**

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

# Logging
LOG_LEVEL="INFO"
DEBUG="false"
```

## 🧪 Executando Testes

```bash
# Ative o ambiente virtual primeiro
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Testes unitários
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Todos os testes com coverage
pytest --cov=src --cov-report=html --cov-report=term

# Testes específicos
pytest tests/unit/test_entities.py -v
pytest tests/integration/test_controllers.py -v
```

## 🔥 Stress Test - Demonstração do HPA

Para demonstrar o funcionamento do HPA (Horizontal Pod Autoscaler) e comprovar a escalabilidade automática do sistema:

### 🚀 **Teste de Estresse com Python (Recomendado)**

#### Pré-requisitos
```bash
# Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt
```

**💡 Nota:** Se estiver usando **minikube**, o argumento `--api-url` é **opcional** - o script detecta automaticamente o IP do minikube.

#### Teste Básico
```bash
# Teste rápido com endpoint /health (IP detectado automaticamente)
python infra/scripts/stress_test.py --scenario quick
```

#### Teste Intenso para Forçar Escalabilidade
```bash
# Teste com endpoint pesado que força escalabilidade
python infra/scripts/stress_test.py --scenario custom \
  --duration 180 \
  --concurrency 100 \
  --endpoint /order/list
```

#### Cenários Disponíveis

##### **Cenário Quick (Rápido)**
```bash
python infra/scripts/stress_test.py --scenario quick
```
- **Carga Baixa**: 30s, 20 conexões concorrentes
- **Carga Média**: 45s, 50 conexões concorrentes  
- **Carga Alta**: 60s, 100 conexões concorrentes

##### **Cenário Full (Completo)**
```bash
python infra/scripts/stress_test.py --scenario full
```
- **Carga Baixa**: 60s, 50 conexões concorrentes
- **Carga Média**: 90s, 150 conexões concorrentes
- **Carga Alta**: 120s, 300 conexões concorrentes
- **Carga Extrema**: 180s, 500 conexões concorrentes
- **Teste Endpoint Pesado**: 120s, 200 conexões - `/order/list?skip=0&limit=100`
- **Teste Produtos**: 90s, 300 conexões - `/product/list?include_inactive=true`
- **Teste Ingredientes**: 90s, 300 conexões - `/ingredient/list?include_inactive=false`
- **Teste Database**: 120s, 250 conexões - `/health/db`
- **Teste Extremo - 5min**: 300s, 1000 conexões - `/health`
- **Teste Extremo - Database**: 300s, 800 conexões - `/health/db`
- **Teste Contínuo - 10min**: 600s, 1500 conexões - `/health/db`

##### **Cenário Custom (Personalizado)**
```bash
python infra/scripts/stress_test.py --scenario custom \
  --duration 180 \
  --concurrency 100 \
  --endpoint /order/list
```

#### Parâmetros Disponíveis
```bash
python infra/scripts/stress_test.py --help

# Cenários disponíveis:
# --scenario quick     # Teste rápido (3 cenários)
# --scenario full      # Teste completo (11 cenários)
# --scenario custom    # Teste personalizado

# Parâmetros customizáveis:
# --duration 180       # Duração em segundos
# --concurrency 100    # Número de requisições simultâneas
# --endpoint /order/list  # Endpoint a testar
# --api-url http://IP:30080  # URL da API (OPCIONAL - detecta automaticamente se minikube estiver rodando)
```

### 📊 **Monitoramento em Tempo Real**

O script de stress test inclui monitoramento automático do Kubernetes:

#### **Funcionalidades de Monitoramento**
- ✅ **Status do HPA**: Monitora automaticamente o Horizontal Pod Autoscaler
- ✅ **Status dos Pods**: Verifica pods antes e depois de cada cenário
- ✅ **Métricas de Performance**: Calcula RPS, latência, taxa de sucesso
- ✅ **Logs Coloridos**: Output colorido com timestamps
- ✅ **Detecção Automática**: Detecta IP do minikube automaticamente

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

#### **Exemplo de Output do Script**
```
[14:30:15] Status Atual do Sistema
==================================================
HPA: hpa-app
  Min Replicas: 1
  Max Replicas: 5
  Current Replicas: 1
  Target CPU: 30%

Pods (1):
  dpm-app-7f8d9c4b5-abc12: Running (Ready)

[14:30:25] Executando Cenário: Carga Alta
----------------------------------------
[14:30:25] Iniciando Stress Test
  Duração: 60s
  Concorrência: 100
  Endpoint: /health

[14:31:25] Resultados do Stress Test
==================================================
Total de Requisições: 100
Requisições Bem-sucedidas: 100
Requisições Falharam: 0
Taxa de Sucesso: 100.00%
Duração Média: 0.245s
Duração Mínima: 0.123s
Duração Máxima: 0.567s
Requisições por Segundo: 1.67
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

### 💡 **Dicas e Melhores Práticas**

#### **Para Demonstrações**
```bash
# 1. Inicie com teste rápido para verificar funcionamento
python infra/scripts/stress_test.py --scenario quick

# 2. Execute teste completo para demonstração completa
python infra/scripts/stress_test.py --scenario full

# 3. Use cenário custom para testes específicos
python infra/scripts/stress_test.py --scenario custom \
  --duration 300 \
  --concurrency 200 \
  --endpoint /order/list
```

#### **Para Desenvolvimento**
```bash
# Teste rápido durante desenvolvimento
python infra/scripts/stress_test.py --scenario custom \
  --duration 30 \
  --concurrency 10 \
  --endpoint /health

# Teste de endpoints específicos
python infra/scripts/stress_test.py --scenario custom \
  --duration 60 \
  --concurrency 50 \
  --endpoint /product/list
```

#### **Para Produção**
```bash
# Teste de carga extrema (apenas em ambiente de teste)
python infra/scripts/stress_test.py --scenario custom \
  --duration 600 \
  --concurrency 1000 \
  --endpoint /health/db
```

#### **Monitoramento Recomendado**
```bash
# Terminal 1: Stress test
python infra/scripts/stress_test.py --scenario full

# Terminal 2: Monitor HPA
kubectl get hpa -w

# Terminal 3: Monitor pods
kubectl get pods -l app=dpm-app -w

# Terminal 4: Métricas de recursos
kubectl top pods -l app=dpm-app
```

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
python infra/scripts/stress_test.py --scenario custom --duration 300 --concurrency 150
```

### 🔧 **Características Técnicas do Script**

#### **Tecnologias Utilizadas**
- **AsyncIO**: Requisições assíncronas para alta concorrência
- **aiohttp**: Cliente HTTP assíncrono para performance
- **subprocess**: Integração com kubectl para monitoramento
- **argparse**: Interface de linha de comando robusta
- **JSON**: Parsing de respostas do Kubernetes

#### **Funcionalidades Avançadas**
- 🔄 **Requisições Assíncronas**: Suporte a milhares de conexões simultâneas
- 📊 **Métricas Detalhadas**: RPS, latência, taxa de sucesso, percentis
- 🎨 **Output Colorido**: Logs organizados com cores para facilitar leitura
- ⏱️ **Timestamps**: Cada log inclui timestamp preciso
- 🔍 **Monitoramento K8s**: Integração automática com kubectl
- 🎯 **Cenários Pré-definidos**: Testes otimizados para diferentes cargas
- 🔧 **Configuração Flexível**: Parâmetros customizáveis via CLI

#### **Exemplo de Execução Completa**
```bash
# Executar teste completo com monitoramento
python infra/scripts/stress_test.py --scenario full

# Output esperado:
# [14:30:00] Stress Test - Sistema de Autoatendimento de Fast Food
# ====================================================
# API URL: http://192.168.49.2:30080
# 
# [14:30:05] Executando Cenário: Carga Baixa
# ----------------------------------------
# [14:30:05] Status Atual do Sistema
# ===================================================
# HPA: hpa-app
#   Min Replicas: 1
#   Max Replicas: 5
#   Current Replicas: 1
#   Target CPU: 30%
# 
# [14:30:15] Iniciando Stress Test
#   Duração: 60s
#   Concorrência: 50
#   Endpoint: /health
# 
# [14:31:15] Resultados do Stress Test
# ===================================================
# Total de Requisições: 50
# Requisições Bem-sucedidas: 50
# Requisições Falharam: 0
# Taxa de Sucesso: 100.00%
# Duração Média: 0.234s
# Requisições por Segundo: 0.83
```

## 📊 Monitoramento e Métricas

O sistema inclui:
- **Health Checks**: `/health` e `/customer/anonymous`
- **HPA**: Auto-scaling baseado em CPU (30% - 5 réplicas)
- **Métricas**: Prometheus/Grafana (configuração opcional)
- **Logs Estruturados**: Com contexto e níveis configuráveis
- **Readiness/Liveness Probes**: Para Kubernetes

## 🔒 Segurança

- **Autenticação**: Basic Auth para endpoints administrativos
- **Secrets**: Credenciais sensíveis em Kubernetes Secrets
- **ConfigMaps**: Configurações não-sensíveis
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
# Atualizar aplicação no Kubernetes
./infra/scripts/update_app.sh

# Ver logs em tempo real
kubectl logs -f deployment/dpm-app

# Acessar banco de dados
kubectl port-forward svc/postgres 5432:5432

# Executar migrations
kubectl apply -f infra/maintenance/job_dbupdate.yaml
```

## 🤝 Contribuição

Este projeto tem fins educacionais. Pull requests são aceitos apenas dos membros do projeto.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido para o Tech Challenge FASE 02 - Arquitetura de Software**
