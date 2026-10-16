
from config import INSTRUCOES
from agent.core import executar_agente
from logger import logger

COMANDOS_SAIDA = {
    "sair",
    "saiir",
    "exit",
    "quit",
    "q",
    "encerrar"
}

def main():

    logger.info("AGENTE_INICIADO")

    mensagens = [
        {
            "role": "system",
            "content": INSTRUCOES
        }
    ]

    print(
        "Agente Linux iniciado. "
        "Digite 'sair' para encerrar."
    )

    while True:

        try:
            pergunta = input("\nVocê: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando agente...")
            break

        if pergunta.lower() in COMANDOS_SAIDA:
            print("\nAté logo! \nEncerrando agente...")
            break

        if not pergunta:
            continue

        mensagens.append({
            "role": "user",
            "content": pergunta
        })

        try:
            resposta = executar_agente(mensagens)
            print("\nAgente:", resposta)

        except Exception:
            logger.exception("ERRO_EXECUCAO_AGENTE")
            print("\nOcorreu um erro na execução do agente.")

    logger.info("AGENTE_ENCERRADO")

if __name__ == "__main__":
    main()
