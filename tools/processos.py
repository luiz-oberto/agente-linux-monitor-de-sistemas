import json
import psutil
import time

# INVESTIGAÇÃO DE PROCESSOS
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
