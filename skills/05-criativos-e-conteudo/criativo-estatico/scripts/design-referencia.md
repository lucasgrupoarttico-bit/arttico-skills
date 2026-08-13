# Regras de Design — Referência

> Replica o layout de um anúncio enviado pelo usuário, mas adaptado ao design
> guide do cliente. Copia a ESTRUTURA da referência, nunca a cor ou o estilo do
> concorrente.

---

## Conceito

O usuário manda um anúncio que funcionou (do concorrente ou de outra marca) e
pede "faz parecido". A skill lê o esqueleto — onde fica o texto, onde fica a
imagem, que tipo de banner/tag existe — e reconstrói com a identidade do cliente.
O resultado tem a mesma lógica de composição, mas as cores, fontes e logo são
sempre da marca do cliente.

---

## Dimensões

- **Story:** 1080×1920 (`criativo.html`)
- **Feed:** 1080×1440 (`criativo-feed.html`)

---

## Como usar a referência

1. Analisar o anúncio enviado e identificar o esqueleto:
   - Onde está o texto principal (topo, meio, base)
   - Se tem imagem e onde (lateral, fundo, rodapé)
   - Se tem banner/tag de atenção e onde
   - Como o CTA aparece
2. **Extrair só a estrutura de composição** — não copiar cor, fonte nem estilo
   visual do original
3. Reconstruir cada bloco com a identidade do cliente (cores, logo, fonte do
   design guide)

---

## Visual (adaptado ao cliente)

- **Fundo:** cor primária do cliente — **nunca preto ou cor genérica**, nunca a
  cor do anúncio original
- **Com imagem:** foto no lado direito inferior; overlay
  `linear-gradient(to right, [cor-primária] 25%, rgba([rgb], 0.25) 100%)`
- **Sem imagem:** fundo sólido na cor primária
- **Banner de atenção:** pílula/tag uppercase com fundo semitransparente no topo
  do conteúdo (`rgba(255,255,255,0.15)`)
- **Logo:** topo do frame, base64 embedded

---

## CTA

- Dentro do bloco de conteúdo, logo abaixo do subtítulo (`margin-top: 24px`)
- **Nunca no rodapé separado** do texto principal
- Estilo sugerido: outlined (`border: 3px solid #FFFFFF; color: #FFFFFF;
  background: transparent`) ou fundo branco com texto na cor primária

---

## Cores

- **Fundo:** cor primária do cliente
- **Texto:** branco ou cor de alto contraste sobre a primária
- **Banner:** `rgba(255,255,255,0.15)` (semitransparente)
- **CTA:** branco (outlined ou preenchido)

Toda a paleta vem do design guide do cliente. A referência define só o "onde",
não o "com qual cor".

---

## Regras

- **Copiar estrutura, nunca cor/estilo do original** — o criativo tem que parecer
  do cliente, não do concorrente
- Fundo sempre na cor primária do cliente, nunca preto genérico
- CTA dentro do bloco de conteúdo, nunca no rodapé separado
- Banner de atenção semitransparente no topo do conteúdo
- Logo base64, nunca `src` relativo ou com espaços
- Imagem base64 ou caminho absoluto `file:///`. Nunca relativo
- Sem travessões em nenhum texto

---

## Adaptação por cliente

1. Ler o design guide pra cor primária (fundo), cores de texto e logo
2. Ler o anúncio de referência só pra tirar o esqueleto de composição
3. Reescrever headline/subtítulo/CTA no tom do cliente
4. Se a referência tiver imagem, usar foto real do cliente na mesma posição

---

## O que ajustar

- **Ficou parecido demais com o original:** trocar cores/fonte pela identidade do
  cliente — só a estrutura deve coincidir
- **Sem imagem na referência:** fundo sólido na cor primária
- **Banner competindo com o texto:** baixar a opacidade do fundo do banner
- **CTA solto no rodapé:** mover pra dentro do bloco de conteúdo (`margin-top: 24px`)

Pede pro Claude: "muda a regra X no design referência" e ele edita este arquivo.
