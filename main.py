
from config import INSTRUCOES
from agent.core import executar_agente


def main():

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

        if pergunta.lower() == "sair":
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

        except Exception as erro:
            print(f"\nErro na execução do agente: {erro}")


if __name__ == "__main__":
    main()
