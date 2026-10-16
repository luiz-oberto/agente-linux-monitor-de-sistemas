
import json

import ollama
import psutil


MODELO = "qwen3:4b"


def consultar_cpu() -> str:
    """Consulta o percentual atual de utilização da CPU."""
    return json.dumps({
        "cpu_percentual": psutil.cpu_percent(interval=1),
        "nucleos_logicos": psutil.cpu_count()
    })


def consultar_memoria() -> str:
    """Consulta o consumo atual de memória RAM."""
    memoria = psutil.virtual_memory()

    return json.dumps({
        "total_gb": round(memoria.total / 1024**3, 2),
        "disponivel_gb": round(memoria.available / 1024**3, 2),
        "uso_percentual": memoria.percent
    })


def consultar_disco() -> str:
    """Consulta o uso do disco da partição raiz."""
    disco = psutil.disk_usage("/")

    return json.dumps({
        "total_gb": round(disco.total / 1024**3, 2),
        "livre_gb": round(disco.free / 1024**3, 2),
        "uso_percentual": disco.percent
    })

def consultar_sistema() -> str:
    """
    Consulta em tempo real CPU, memória RAM
    e disco para elaborar um diagnóstico geral.
    """

    cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage("/")

    dados = {
        "cpu_percentual": cpu,
        "cpu_nucleos_logicos": psutil.cpu_count(),
        "ram_percentual": memoria.percent,
        "ram_disponivel_gb": round(
            memoria.available / 1024**3, 2
        ),
        "disco_percentual": disco.percent,
        "disco_livre_gb": round(
            disco.free / 1024**3, 2
        )
    }

    return json.dumps(dados)


def listar_processos_memoria() -> str:
    """Lista os cinco processos que mais consomem memória RAM."""

    processos = []

    for processo in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            info = processo.info
            memoria = info["memory_info"]

            if memoria is None:
                continue

            processos.append({
                "pid": info["pid"],
                "nome": info["name"],
                "ram_mb": round(memoria.rss / 1024**2, 2)
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processos.sort(
        key=lambda p: p["ram_mb"],
        reverse=True
    )

    return json.dumps(processos[:5])


def listar_processos_cpu() -> str:
    """Lista cinco processos com maior consumo de CPU em uma amostra."""

    processos = []

    for processo in psutil.process_iter(["pid", "name"]):
        try:
            processo.cpu_percent(interval=None)
            processos.append(processo)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    import time
    time.sleep(1)

    resultados = []

    for processo in processos:
        try:
            uso_cpu = processo.cpu_percent(interval=None)

            resultados.append({
                "pid": processo.pid,
                "nome": processo.name(),
                "cpu_percentual": round(uso_cpu, 2)
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    resultados.sort(
        key=lambda p: p["cpu_percentual"],
        reverse=True
    )

    return json.dumps(resultados[:5])


FERRAMENTAS = {
    "consultar_cpu": consultar_cpu,
    "consultar_memoria": consultar_memoria,
    "consultar_disco": consultar_disco,
    "consultar_sistema": consultar_sistema,
    "listar_processos_memoria": listar_processos_memoria,
    "listar_processos_cpu": listar_processos_cpu
}


def main():
    mensagens = [{
        "role": "system",
        "content": (
            "Você é um agente de monitoramento Linux. "
            "Responda em português brasileiro. "
            "Use as ferramentas para consultar métricas atuais. "
            "Não invente medições. "
            "Você não pode modificar o sistema."
            "Quando o usuário solicitar informações atuais, "
            "consulte novamente as ferramentas, mesmo que "
            "existam resultados anteriores no histórico. "
            "Para diagnóstico geral, utilize consultar_sistema. "
            "Quando o usuário solicitar investigação de processos, "
            "utilize as ferramentas de listagem de CPU e memória. "
            "Não encerre processos nem altere configurações."
        )
    }]

    print("Agente Linux iniciado. Digite 'sair' para encerrar.")

    while True:
        pergunta = input("\nVocê: ").strip()

        if pergunta.lower() == "sair":
            break

        if not pergunta:
            continue

        mensagens.append({
            "role": "user",
            "content": pergunta
        })

        for _ in range(5):
            resposta = ollama.chat(
                model=MODELO,
                messages=mensagens,
                tools=list(FERRAMENTAS.values()),
                options={"temperature": 0.2}
            )

            mensagens.append(resposta.message)

            chamadas = resposta.message.tool_calls or []

            if not chamadas:
                print("\nAgente:", resposta.message.content)
                break

            for chamada in chamadas:
                nome = chamada.function.name

                if nome not in FERRAMENTAS:
                    resultado = "Ferramenta não autorizada."
                else:
                    print(f"[Executando: {nome}]")
                    try:
                        resultado = FERRAMENTAS[nome](
                            **chamada.function.arguments
                        )
                    except Exception as erro:
                        resultado = f"Erro ao consultar: {erro}"

                mensagens.append({
                    "role": "tool",
                    "tool_name": nome,
                    "content": str(resultado)
                })
        else:
            print("Limite de etapas atingido.")


if __name__ == "__main__":
    main()

