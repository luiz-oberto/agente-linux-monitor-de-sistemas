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

from .servicos import (
    consultar_servico,
    listar_servicos_falhos
)

FERRAMENTAS = {
    "consultar_cpu": consultar_cpu,
    "consultar_memoria": consultar_memoria,
    "consultar_disco": consultar_disco,
    "consultar_sistema": consultar_sistema,
    "listar_processos_memoria": listar_processos_memoria,
    "listar_processos_cpu": listar_processos_cpu,
    "consultar_servico": consultar_servico,
    "listar_servicos_falhos": listar_servicos_falhos
}