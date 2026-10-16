import json
import psutil

# CONSULTAS
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