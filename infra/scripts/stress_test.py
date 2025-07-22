#!/usr/bin/env python3
"""
Stress Test Script para Sistema de Autoatendimento de Fast Food
Demonstra o funcionamento do HPA (Horizontal Pod Autoscaler)
"""

import asyncio
import aiohttp
import time
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict
import argparse


class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    NC = "\033[0m"  # No Color


class StressTest:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.results = []
        self.start_time = None
        self.end_time = None

    def print_status(self, message: str, color: str = Colors.NC):
        """Imprime mensagem com cor e timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {message}{Colors.NC}")

    def get_k8s_status(self) -> Dict:
        """Obtém status atual do Kubernetes"""
        try:
            # Obter status do HPA
            hpa_result = subprocess.run(
                ["kubectl", "get", "hpa", "-o", "json"], capture_output=True, text=True
            )
            hpa_data = json.loads(hpa_result.stdout)

            # Obter status dos pods
            pods_result = subprocess.run(
                ["kubectl", "get", "pods", "-l", "app=dpm-app", "-o", "json"],
                capture_output=True,
                text=True,
            )
            pods_data = json.loads(pods_result.stdout)

            return {"hpa": hpa_data, "pods": pods_data}
        except Exception as e:
            self.print_status(f"Erro ao obter status K8s: {e}", Colors.RED)
            return {}

    def show_current_status(self):
        """Mostra status atual do sistema"""
        self.print_status("Status Atual do Sistema", Colors.BLUE)
        print("=" * 50)

        status = self.get_k8s_status()

        if status:
            # Mostrar HPA
            hpa = status["hpa"]["items"][0] if status["hpa"]["items"] else {}
            if hpa:
                spec = hpa.get("spec", {})
                status_info = hpa.get("status", {})

                print(f"HPA: {hpa['metadata']['name']}")
                print(f"  Min Replicas: {spec.get('minReplicas', 'N/A')}")
                print(f"  Max Replicas: {spec.get('maxReplicas', 'N/A')}")
                print(
                    f"  Current Replicas: {status_info.get('currentReplicas', 'N/A')}"
                )
                print(
                    f"  Target CPU: {spec.get('metrics', [{}])[0].get('resource', {}).get('target', {}).get('averageUtilization', 'N/A')}%"
                )

            # Mostrar Pods
            pods = status["pods"]["items"]
            print(f"\nPods ({len(pods)}):")
            for pod in pods:
                name = pod["metadata"]["name"]
                status = pod["status"]["phase"]
                ready = "Ready" if pod["status"].get("ready", False) else "Not Ready"
                print(f"  {name}: {status} ({ready})")

        print("=" * 50)

    async def make_request(self, session: aiohttp.ClientSession, endpoint: str) -> Dict:
        """Faz uma requisição HTTP"""
        start_time = time.time()
        try:
            async with session.get(f"{self.api_url}{endpoint}") as response:
                end_time = time.time()
                return {
                    "status": response.status,
                    "duration": end_time - start_time,
                    "success": response.status == 200,
                    "endpoint": endpoint,
                }
        except Exception as e:
            end_time = time.time()
            return {
                "status": 0,
                "duration": end_time - start_time,
                "success": False,
                "error": str(e),
                "endpoint": endpoint,
            }

    async def stress_test(
        self, duration: int, concurrency: int, endpoint: str = "/health"
    ):
        """Executa stress test"""
        self.print_status("Iniciando Stress Test", Colors.YELLOW)
        self.print_status(f"  Duração: {duration}s")
        self.print_status(f"  Concorrência: {concurrency}")
        self.print_status(f"  Endpoint: {endpoint}")
        print()

        self.start_time = time.time()

        # Criar sessão HTTP
        timeout = aiohttp.ClientTimeout(total=duration + 10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Criar tarefas
            tasks = []
            for _ in range(concurrency):
                task = asyncio.create_task(self.make_request(session, endpoint))
                tasks.append(task)

            # Executar tarefas
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Processar resultados
            for result in results:
                if isinstance(result, dict):
                    self.results.append(result)

        self.end_time = time.time()

    def calculate_metrics(self) -> Dict:
        """Calcula métricas dos resultados"""
        if not self.results:
            return {}

        successful_requests = [r for r in self.results if r.get("success", False)]
        failed_requests = [r for r in self.results if not r.get("success", False)]

        durations = [r["duration"] for r in self.results if "duration" in r]

        return {
            "total_requests": len(self.results),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(self.results) * 100
            if self.results
            else 0,
            "avg_duration": sum(durations) / len(durations) if durations else 0,
            "min_duration": min(durations) if durations else 0,
            "max_duration": max(durations) if durations else 0,
            "total_duration": self.end_time - self.start_time
            if self.start_time and self.end_time
            else 0,
        }

    def print_results(self):
        """Imprime resultados do stress test"""
        self.print_status("Resultados do Stress Test", Colors.GREEN)
        print("=" * 50)

        metrics = self.calculate_metrics()

        if metrics:
            print(f"Total de Requisições: {metrics['total_requests']}")
            print(f"Requisições Bem-sucedidas: {metrics['successful_requests']}")
            print(f"Requisições Falharam: {metrics['failed_requests']}")
            print(f"Taxa de Sucesso: {metrics['success_rate']:.2f}%")
            print(f"Duração Média: {metrics['avg_duration']:.3f}s")
            print(f"Duração Mínima: {metrics['min_duration']:.3f}s")
            print(f"Duração Máxima: {metrics['max_duration']:.3f}s")
            print(f"Duração Total: {metrics['total_duration']:.2f}s")

            if metrics["total_requests"] > 0:
                rps = metrics["total_requests"] / metrics["total_duration"]
                print(f"Requisições por Segundo: {rps:.2f}")

        print("=" * 50)

    async def run_scenario(
        self, name: str, duration: int, concurrency: int, endpoint: str = "/health"
    ):
        """Executa um cenário de teste"""
        self.print_status(f"Executando Cenário: {name}", Colors.PURPLE)
        print("-" * 40)

        # Mostrar status antes
        self.show_current_status()

        # Executar stress test
        await self.stress_test(duration, concurrency, endpoint)

        # Mostrar resultados
        self.print_results()

        # Aguardar um pouco para o HPA reagir
        self.print_status("Aguardando HPA reagir...", Colors.YELLOW)
        await asyncio.sleep(10)

        # Mostrar status depois
        self.show_current_status()
        print()


async def main():
    parser = argparse.ArgumentParser(
        description="Stress Test para Sistema de Fast Food"
    )

    # Verificar se kubectl está disponível
    try:
        subprocess.run(
            ["kubectl", "version", "--client"], check=True, capture_output=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}kubectl não está instalado ou não está no PATH{Colors.NC}")
        sys.exit(1)

    # Verificar se Minikube está rodando e obter IP
    minikube_ip = None
    try:
        result = subprocess.run(["minikube", "ip"], capture_output=True, text=True)
        if result.returncode == 0:
            minikube_ip = result.stdout.strip()
    except FileNotFoundError:
        pass

    # Definir URL padrão baseada no IP do minikube ou localhost
    if minikube_ip:
        default_api_url = f"http://{minikube_ip}:30080"
    else:
        default_api_url = "http://localhost:30080"

    parser.add_argument(
        "--api-url",
        default=default_api_url,
        help="URL da API (detecta automaticamente se minikube estiver rodando)",
    )
    parser.add_argument(
        "--scenario",
        choices=["quick", "full", "custom"],
        default="quick",
        help="Cenário de teste",
    )
    parser.add_argument("--duration", type=int, default=30, help="Duração em segundos")
    parser.add_argument(
        "--concurrency", type=int, default=10, help="Número de conexões concorrentes"
    )
    parser.add_argument("--endpoint", default="/health", help="Endpoint para testar")

    args = parser.parse_args()

    stress_test = StressTest(args.api_url)

    print(
        f"{Colors.BLUE}Stress Test - Sistema de Autoatendimento de Fast Food{Colors.NC}"
    )
    print(
        f"{Colors.BLUE}===================================================={Colors.NC}"
    )
    print()
    print(f"{Colors.GREEN}API URL: {args.api_url}{Colors.NC}")
    print()

    if args.scenario == "quick":
        # Cenário rápido para demonstração
        scenarios = [
            ("Carga Baixa", 20, 5, "/health"),
            ("Carga Média", 30, 15, "/health"),
            ("Carga Alta", 40, 25, "/health"),
        ]
    elif args.scenario == "full":
        # Cenário completo
        scenarios = [
            ("Carga Baixa", 30, 5, "/health"),
            ("Carga Média", 45, 15, "/health"),
            ("Carga Alta", 60, 25, "/health"),
            ("Carga Extrema", 90, 40, "/health"),
            ("Teste Endpoint Pesado", 60, 20, "/fastfood/api/order/list"),
        ]
    else:
        # Cenário customizado
        scenarios = [
            (
                f"Custom ({args.duration}s, {args.concurrency} conc)",
                args.duration,
                args.concurrency,
                args.endpoint,
            )
        ]

    for name, duration, concurrency, endpoint in scenarios:
        await stress_test.run_scenario(name, duration, concurrency, endpoint)

    print(f"{Colors.GREEN}Stress Test Concluído!{Colors.NC}")
    print()
    print(f"{Colors.BLUE}Dicas para análise:{Colors.NC}")
    print("1. Verifique se o HPA escalou: kubectl get hpa")
    print("2. Monitore os pods: kubectl get pods -l app=dpm-app")
    print("3. Veja as métricas: kubectl top pods -l app=dpm-app")
    print("4. Analise os logs: kubectl logs -f deployment/dpm-app")


if __name__ == "__main__":
    asyncio.run(main())
