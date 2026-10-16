# Agente Linux - monitor de sistema
Este projeto tem o objetivo de implementar um agente local utilizando Ollama com o modelo Qwen3 4B e python para monitora os recursos da minha máquina local. Futuramente pretendo implementar melhorias na qual ele será capaz de se conectar um servidor/máquina remotamente e poderá fazer as análises de consumo dos recursos de cada máquina.

### esquema do projeto

```
agente-linux/
├── main.py
├── config.py
├── agent/
│   ├── __init__.py
│   └── core.py
├── tools/
│   ├── __init__.py
│   ├── sistema.py
│   └── processos.py
├── logs/
├── requirements.txt
└── .venv/
```