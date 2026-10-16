
import json
import re
import subprocess


def consultar_servico(nome: str) -> str:
    """Consulta o estado atual de um serviço systemd pelo nome."""

    if not re.fullmatch(r"[A-Za-z0-9_.@-]{1,100}", nome):
        return json.dumps({
            "erro": "Nome de serviço inválido."
        })

    unidade = (
        nome if nome.endswith(".service")
        else f"{nome}.service"
    )

    try:
        resultado = subprocess.run(
            [
                "systemctl", "show", unidade,
                "--property=LoadState,ActiveState,SubState,Description",
                "--no-pager"
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )

        if resultado.returncode != 0:
            return json.dumps({
                "erro": resultado.stderr.strip()
                or "Não foi possível consultar o serviço."
            })

        dados = {"servico": unidade}

        for linha in resultado.stdout.splitlines():
            if "=" in linha:
                chave, valor = linha.split("=", 1)
                dados[chave] = valor

        return json.dumps(dados, ensure_ascii=False)

    except (subprocess.TimeoutExpired, OSError) as erro:
        return json.dumps({"erro": str(erro)})


def listar_servicos_falhos() -> str:
    """Lista serviços systemd que estão em estado failed."""

    try:
        resultado = subprocess.run(
            [
                "systemctl", "list-units",
                "--type=service",
                "--state=failed",
                "--no-legend",
                "--plain",
                "--no-pager"
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )

        if resultado.returncode != 0:
            return json.dumps({
                "erro": resultado.stderr.strip()
                or "Falha ao listar serviços."
            })

        return json.dumps({
            "servicos_falhos": resultado.stdout.strip()
        }, ensure_ascii=False)

    except (subprocess.TimeoutExpired, OSError) as erro:
        return json.dumps({"erro": str(erro)})
