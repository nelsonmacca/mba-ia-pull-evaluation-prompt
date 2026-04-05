# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Visão geral

Este projeto implementa o fluxo completo de engenharia de prompts proposto no desafio:

1. pull do prompt inicial de baixa qualidade a partir do LangSmith Hub
2. criação de uma versão otimizada do prompt
3. validação local com testes em `pytest`
4. push do prompt otimizado para o LangSmith Hub
5. avaliação automática com LangSmith + métricas customizadas
6. iteração contínua com base nos resultados

O prompt trabalhado neste desafio foi:

- `bug_to_user_story_v1` → versão inicial
- `bug_to_user_story_v2` → versão otimizada

---

## Objetivo do desafio

Converter relatos de bugs em User Stories com melhor qualidade, aplicando técnicas de Prompt Engineering e validando os resultados por meio de avaliação automatizada.

O fluxo e os critérios do projeto estão definidos no template do desafio e nos scripts de avaliação do repositório. As métricas efetivamente utilizadas no `evaluate.py` são:

- Helpfulness
- Correctness
- F1-Score
- Clarity
- Precision :contentReference[oaicite:0]{index=0}

---

## Estrutura do projeto

```text
mba-ia-pull-evaluation-prompt/
├── .env.example
├── README.md
├── requirements.txt
├── datasets/
│   └── bug_to_user_story.jsonl
├── prompts/
│   ├── bug_to_user_story_v1.yml
│   └── bug_to_user_story_v2.yml
├── src/
│   ├── pull_prompts.py
│   ├── push_prompts.py
│   ├── evaluate.py
│   ├── metrics.py
│   └── utils.py
└── tests/
    └── test_prompts.py