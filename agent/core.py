
import ollama

from config import MODELO, MAX_ITERACOES
from tools import FERRAMENTAS
from time import perf_counter
from logger import logger


def executar_agente(mensagens: list) -> str:
    """
    Executa o ciclo do agente.

    Consulta o modelo, identifica chamadas de ferramentas,
    executa funções autorizadas e retorna a resposta.
    """

    for _ in range(MAX_ITERACOES):

        resposta = ollama.chat(
            model=MODELO,
            messages=mensagens,
            tools=list(FERRAMENTAS.values()),
            options={"temperature": 0.2}
        )

        mensagens.append(resposta.message)

        chamadas = resposta.message.tool_calls or []

        if not chamadas:
            return resposta.message.content or ""

        for chamada in chamadas:

            nome = chamada.function.name

            if nome not in FERRAMENTAS:
                resultado = "Ferramenta não autorizada."

            else:
                print(f"[Executando: {nome}]")

                logger.info(
                    "FERRAMENTA_INICIADA | %s", nome
                )

                inicio = perf_counter()

                try:
                    resultado = FERRAMENTAS[nome](
                        **chamada.function.arguments
                    )

                    duracao = perf_counter() - inicio

                    logger.info(
                        "FERRAMENTA_CONCLUIDA | %s | %.3fs",
                        nome,
                        duracao
                    )

                except Exception:
                    duracao = perf_counter() - inicio

                    logger.exception(
                        "FERRAMENTA_ERRO | %s | %.3fs",
                        nome,
                        duracao
                    )

                    resultado = (
                        "Não foi possível executar a ferramenta."
                    )

            mensagens.append({
                "role": "tool",
                "tool_name": nome,
                "content": str(resultado)
            })

    return "Limite de etapas atingido."
