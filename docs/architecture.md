👤 Autor

Projeto desenvolvido por Marcos (Aurion System)

# 🏗️ 2. architecture.md


# 🧠 Arquitetura da Lyra

## Estrutura Geral

A Lyra é baseada em arquitetura modular orientada a agentes.

### Camadas

- Core → Configuração global
- Routes → Endpoints da API
- Services → Lógica de negócio
- Data → Persistência
- Schemas → Validação

---

## Fluxo principal

1. Usuário envia mensagem
2. Sistema identifica intenção
3. Orchestrator seleciona agentes
4. Agentes processam contexto
5. Supervisor gera resposta final

---

## Componentes-chave

### 🧩 Agents
Entidades especializadas com comportamento próprio.

### 🧠 Memory
- Histórico
- Resumo
- Tags
- Objetivos

### 🎯 Orchestrator
Responsável por:
- selecionar agentes
- montar equipe
- coordenar respostas

### 👁 Supervisor
Refina e consolida resposta final