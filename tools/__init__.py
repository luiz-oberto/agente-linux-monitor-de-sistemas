from .sistema import (
    consultar_cpu,
    consultar_memoria,
    consultar_disco,
    consultar_sistema
)


from .processos import (
    listar_processos_cpu,
    listar_processos_memoria
)

FERRAMENTAS = {
    "consultar_cpu": consultar_cpu,
    "consultar_memoria": consultar_memoria,
    "consultar_disco": consultar_disco,
    "consultar_sistema": consultar_sistema,
    "listar_processos_memoria": listar_processos_memoria,
    "listar_processos_cpu": listar_processos_cpu
}