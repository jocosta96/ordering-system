# Scripts de Stress Test - Sistema de Fast Food

Este diretório contém scripts para testar e demonstrar o funcionamento do HPA (Horizontal Pod Autoscaler) do sistema de autoatendimento de fast food.

## 📋 Scripts Disponíveis

### `stress_test.py` - Teste Python Avançado
**Script principal para análise técnica e métricas detalhadas**

```bash
# Cenário rápido (IP detectado automaticamente se minikube estiver rodando)
python3 scripts/stress_test.py --scenario quick

# Cenário completo (IP detectado automaticamente se minikube estiver rodando)
python3 scripts/stress_test.py --scenario full

# Cenário customizado (IP detectado automaticamente se minikube estiver rodando)
python3 scripts/stress_test.py --scenario custom --duration 60 --concurrency 20 --endpoint /health
```

**💡 Nota:** O argumento `--api-url` é **opcional** quando usando minikube - o script detecta automaticamente o IP.

**Características:**
- ✅ Métricas detalhadas (RPS, latência, taxa de sucesso)
- ✅ Análise de status do Kubernetes em tempo real
- ✅ Cenários pré-configurados (quick, full, custom)
- ✅ Relatórios técnicos completos
- ✅ Monitoramento automático do HPA
- ✅ Teste de endpoints específicos
- ✅ Configuração flexível de parâmetros

## 🚀 Pré-requisitos

### 1. Kubernetes/Minikube
```bash
# Verificar se Minikube está rodando
minikube status

# Se não estiver, iniciar
minikube start
```

### 2. Aplicação Deployada
```bash
# Deployar a aplicação
./scripts/k8s-deploy.sh

# Verificar se está funcionando
kubectl get pods
```

### 3. Dependências Python
```bash
# Instalar aiohttp para o script de stress test
pip install aiohttp
```

## 📊 Configuração do HPA

O HPA está configurado com os seguintes parâmetros:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: dpm-app
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 30
```

**Parâmetros:**
- **Min Replicas**: 1
- **Max Replicas**: 5
- **Target CPU**: 30%
- **Escala**: Baseada em utilização de CPU

## 🧪 Cenários de Teste

### Cenário 1: Carga Baixa
- **Duração**: 20-30s
- **Requisições**: 200-500
- **Concorrência**: 5-10
- **Resultado Esperado**: Não deve escalar

### Cenário 2: Carga Média
- **Duração**: 30-45s
- **Requisições**: 500-1000
- **Concorrência**: 15-20
- **Resultado Esperado**: Pode escalar para 2-3 réplicas

### Cenário 3: Carga Alta
- **Duração**: 40-60s
- **Requisições**: 1000-2000
- **Concorrência**: 25-30
- **Resultado Esperado**: Deve escalar para 3-4 réplicas

### Cenário 4: Carga Extrema
- **Duração**: 60-90s
- **Requisições**: 2000+
- **Concorrência**: 35-40
- **Resultado Esperado**: Deve escalar para 5 réplicas (máximo)

## 📈 Como Interpretar os Resultados

### 1. Monitoramento do HPA
```bash
kubectl get hpa -w
```

**O que observar:**
- `CURRENT` - Número atual de réplicas
- `TARGETS` - Utilização de CPU atual
- Mudanças em tempo real durante o teste

### 2. Monitoramento dos Pods
```bash
kubectl get pods -l app=dpm-app -w
```

**O que observar:**
- Criação de novos pods (`Pending` → `Running`)
- Status dos pods (`Running`, `Ready`)
- Número total de pods

### 3. Métricas de CPU/Memory
```bash
kubectl top pods -l app=dpm-app
```

**O que observar:**
- Utilização de CPU por pod
- Utilização de Memory por pod
- Distribuição da carga

## 🎯 Endpoints para Teste

### Endpoints Leves (Pouco Processamento)
- `/health` - Health check
- `/customer/anonymous` - Cliente anônimo

### Endpoints Médios (Processamento Moderado)
- `/fastfood/api/product/list` - Lista de produtos
- `/fastfood/api/customer/list` - Lista de clientes

### Endpoints Pesados (Muito Processamento)
- `/fastfood/api/order/list` - Lista de pedidos (com ordenação)
- `/fastfood/api/order/checkout` - Criação de pedido

## 🔍 Comandos Úteis para Análise

### Verificar Status do HPA
```bash
kubectl describe hpa hpa-app
```

### Ver Logs da Aplicação
```bash
kubectl logs -f deployment/dpm-app
```

### Ver Métricas Detalhadas
```bash
kubectl top pods -l app=dpm-app
kubectl top nodes
```

### Verificar Eventos
```bash
kubectl get events --sort-by='.lastTimestamp'
```

## 🚨 Troubleshooting

### HPA não está escalando
1. Verificar se o metrics-server está rodando:
   ```bash
   kubectl get pods -n kube-system | grep metrics-server
   ```

2. Verificar se as métricas estão disponíveis:
   ```bash
   kubectl top pods
   ```

3. Verificar configuração do HPA:
   ```bash
   kubectl describe hpa hpa-app
   ```

### Aplicação não responde
1. Verificar se os pods estão rodando:
   ```bash
   kubectl get pods -l app=dpm-app
   ```

2. Verificar logs da aplicação:
   ```bash
   kubectl logs deployment/dpm-app
   ```

3. Verificar se o service está exposto:
   ```bash
   kubectl get svc
   minikube service svc-app
   ```

## 📝 Exemplo de Uso no Vídeo

```bash
# 1. Mostrar status inicial
kubectl get hpa
kubectl get pods -l app=dpm-app

# 2. Executar demonstração com endpoint pesado (IP detectado automaticamente se minikube estiver rodando)
python3 scripts/stress_test.py --scenario custom \
  --duration 180 \
  --concurrency 100 \
  --endpoint /order/list

# 3. Mostrar resultados
kubectl get hpa
kubectl get pods -l app=dpm-app
kubectl top pods -l app=dpm-app
```

## 🎉 Resultados Esperados

Após executar os stress tests, você deve ver:

1. **HPA funcionando**: Número de réplicas aumentando com a carga
2. **Pods escalando**: Novos pods sendo criados automaticamente
3. **CPU sendo utilizada**: Métricas de CPU próximas ao target (30%)
4. **Performance mantida**: Taxa de sucesso alta mesmo com carga

---

**Scripts criados para o Tech Challenge FASE 02 - Arquitetura de Software** 