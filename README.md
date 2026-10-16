# Agente Linux - monitor de sistema
Este projeto tem o objetivo de implementar um agente local utilizando Ollama com o modelo **Qwen3 4B** e **python** para monitora os recursos da minha máquina local. Futuramente pretendo implementar melhorias na qual ele será capaz de se conectar um servidor/máquina remotamente e poderá fazer as análises de consumo dos recursos de cada máquina.

**monitoramento Linux | seleção de ferramentas por IA | arquitetura modular | rastreabilidade das operações**

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

## LISTA DE FUNÇÕES
### Consulta de consumo dos recursos da máquina
- [x] consulta cpu
- [x] consulta memoria
- [x] consulta disco
- [x] consulta geral

### Consulta de serviços da máquina
- [x] consulta serviço
- [x] listar serviços falhos

### Listar processos e respectivas informações de consumo dos recursos
- [x] listar processos da memória
- [x] listar processos da CPU

### Consultar registros do ```journalctl```
- [ ] Consultar registros do journalctl
