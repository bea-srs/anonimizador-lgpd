# Política de Segurança

Este é um projeto de estudo. Não use com dados pessoais reais em produção sem revisão jurídica e de segurança.

## Versões suportadas

Apenas a branch `main`.

## Como reportar uma vulnerabilidade

Não abra uma issue pública. Acesse a aba Security do repositório, clique em "Report a vulnerability" e descreva o problema e como reproduzi-lo. As respostas são em melhor esforço, em poucos dias.

## O que vale reportar

O objetivo do projeto é que nenhum dado pessoal passe sem anonimização. Por isso, são tratados como vulnerabilidade:

- dado pessoal em um formato suportado que os detectores deixam passar;
- vazamento de dados pessoais em logs, relatórios ou mensagens de erro;
- qualquer caminho em que o texto saia da máquina sem ter sido anonimizado;
- dependências com vulnerabilidades conhecidas.

Formatos fora do escopo, listados em [Limitações](README.md#limitações), não contam como vulnerabilidade.

## Cuidados ao reportar

Não inclua dados pessoais reais no relato. Use dados sintéticos, como os de `data/`.
