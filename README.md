# Raio-X do TEOT

Mapeamento questão a questão das provas **TARO (2014, 2016–2026)** e **TEOT (2021, 2023–2026)** da SBOT, usado na preparação para o TEOT.
São 1.770 questões (1.765 válidas), classificadas por grande tema, região, subtema, tipo de cobrança, questão de detalhe e referência oficial.

Site publicado pelo GitHub Pages a partir de `index.html` no branch `main`.

Este repositório público contém apenas a página. A base de questões classificadas (pasta `data/`) fica fora dele; por isso os scripts de `pipeline/` não rodam sozinhos aqui.

## Estrutura

```
index.html                     site (GitHub Pages), documento HTML completo — gerado
artifact.html                  mesma página no formato do artifact do Claude — gerado
page/
  head.html                    <title> e fontes
  style.html                   CSS (tokens de cor, tema claro/escuro)
  body.html                    HTML + JavaScript; /*DATA*/ é substituído pelos dados
pipeline/
  build_page.py                gera index.html a partir de page/ + data/base.json
  build_base.py                junta classificação + referências + enunciados em data/base.json
  teot_split.py, teot_refs.py, teot_build.py, taro_split.py   extração do texto dos PDFs
```

## Formato da classificação (`.tsv`)

`questão|tema|região|idade|subtema|tipo|detalhe`

- **tema**: `TA` trauma adulto · `TP` trauma pediátrico · `OP` ortopedia pediátrica · `BAS` básicas · `OC` ombro e cotovelo · `MAO` mão · `COL` coluna · `QUA` quadril · `JOE` joelho · `PE` pé e tornozelo · `ONC` oncologia · `ANUL` anulada
- **região**: `OC` · `MAO` · `COL` · `QUA` · `JOE` · `PE` · `GER` (geral/sistêmico)
- **idade**: `A` adulto · `P` pediátrico
- **tipo**: `DIA` diagnóstico · `CON` conduta · `FIS` fisiopatologia/biomecânica · `ANA` anatomia/via de acesso · `CLA` classificação · `CPX` complicação/prognóstico · `EPI` epidemiologia
- **detalhe**: `1` quando a resposta depende de número secundário, epônimo de técnica pouco usual ou fato isolado de entidade rara

## Fluxo para atualizar

1. Classificar a nova prova num `.tsv` em `data/classificacao/`.
2. Ajustar e rodar `pipeline/build_base.py` (os caminhos dos scripts de extração ainda apontam para o ambiente original e precisam ser adaptados).
3. Rodar `python3 pipeline/build_page.py` para regenerar `index.html` e `artifact.html`.
4. Fazer commit e push: o GitHub Pages atualiza o site em 1–2 minutos.

## Regras de classificação

- Trauma do adulto fica em “Trauma adulto”, com a região anotada; trauma da criança em “Trauma pediátrico”.
- Doenças pediátricas ficam em “Ortopedia pediátrica”, exceto escoliose/Scheuermann (Coluna), mão congênita e plexo obstétrico (Mão).
- Questões de anatomia entram na região da estrutura, no subtema “Anatomia e vias de acesso”.
- Referência só é atribuída quando a prova, a tabela oficial ou a correção com referência oficial a informam. Nenhum livro é inferido.

## Lacunas conhecidas

TARO 2015, TEOT 2022 e o caderno de anatomia do TEOT 2024 não estão na base. TARO 2023, TEOT 2023 e TEOT 2026 não informam referência por questão.

## Direitos

As provas são da SBOT. Este repositório não contém enunciados nem os PDFs originais.
