# Regras de Design — Preço Topo

> Comparação de preço COM × SEM a marca, com os dois valores em destaque no topo
> e a foto do produto full-bleed embaixo. Formato agressivo e direto de oferta 2x1.
> Nasceu de referências validadas da Prime Gourmet (Casa Moscou).

---

## Conceito

Bate o olho e vê o preço pela metade. O benefício não é abstrato ("economize"),
é numérico e brutal: **você paga X, sem a marca pagaria 2X**. Ideal pra clube de
desconto, cupom, cashback, 2x1, combo — qualquer oferta onde o número é o
argumento. A foto do produto (comida, hospedagem, serviço) gera desejo antes da
leitura do preço.

---

## Dimensões

- **Story:** 1080×1920 (`layout-a-story.html`)
- **Feed:** 1080×1440 (`layout-a-feed.html`)

Mesma base nos dois; no feed a foto full-bleed fica mais compacta (escala ~0.9).

---

## Estrutura

```
body (flex-direction: column, bg: cor primária escura da marca, position: relative)
  ├── .top (padding, text-align: center, flex-shrink: 0)
  │     ├── .brand-logo   ← logo da marca no topo, ~88px, circular, centralizado
  │     ├── .headline     ← "COM O [MARCA]" / "✕ SEM O [MARCA]" — Montserrat 800 ~84px
  │     │                    o "✕" na cor de acento; duas linhas, uppercase
  │     └── .subtarja     ← PÍLULA cor de acento, texto na cor do fundo, uppercase ~21px
  │                          "na compra de dois [item] no [parceiro]"
  ├── .prices (display: flex, gap ~22px, flex-shrink: 0)
  │     ├── .col.com  → .plabel "COM [MARCA] VOCÊ PAGA" (branco) + .pcard.com
  │     │                .pcard.com: fundo cor de acento, texto escuro, preço ~82px
  │     └── .col.sem  → .plabel "SEM [MARCA] VOCÊ PAGA" (branco) + .pcard.sem
  │                      .pcard.sem: fundo claro (#f4f2ee), texto escuro, preço ~82px
  ├── .photo (flex: 1, overflow: hidden)
  │     ├── .photo-img    ← foto do produto, object-fit: cover
  │     └── ::after       ← gradiente sutil: escurece topo e base pra fundir com o preto
  └── .footer            ← "*Valores aproximados", pequeno, centralizado na base
```

---

## Preços (o destaque principal)

- Preço **exagerado**: `font-family: Montserrat 800; font-size: ~82px` (story).
  O cifrão "R$" menor (~36px) e elevado (`vertical-align`)
- **Card COM** = fundo cor de acento cheia, texto na cor do fundo (escuro)
- **Card SEM** = fundo claro `#f4f2ee`, texto escuro. É o "caro", mas não riscar
  nem apagar demais — o contraste com o card de acento já entrega a mensagem
- `.plabel` (COM/SEM ... VOCÊ PAGA): branco, ~27px, weight 700, uppercase
- `border-radius: 12px`, sombra escura sutil `0 12px 40px rgba(0,0,0,0.5)`

---

## Tarja de contexto

- **Pílula na cor de acento**, texto na cor do fundo (escuro), uppercase ~21px,
  weight 700, `border-radius: 6px`
- Diz onde a conta bate: "na compra de dois [item] no [parceiro]"
- É o gatilho de credibilidade — sempre citar o **parceiro real** e a **condição**

---

## Cores

- **Fundo:** cor primária escura da marca (ex: Prime `#010300`)
- **Acento:** cor de destaque da marca (ex: dourado `#F1B835`) — no "✕", tarja e card COM
- **Card SEM:** claro `#f4f2ee` (quase branco quente)
- **Texto headline/labels:** branco

O acento aparece em 3 pontos (X, tarja, card COM) — sem espalhar mais que isso.

---

## Regras gerais

- **Preços movidos a dado real** — precisa de: parceiro, preço COM, preço SEM
- Foto do produto full-bleed embaixo; base64 via script Node (nunca caminho
  relativo/com espaços). Se não houver foto, placeholder escuro marcando o lugar
- Gradiente `::after` na foto: escurece só topo e base pra fundir com o fundo,
  sem lavar a cor do produto
- Logo da marca base64 embutida
- Sem travessões em nenhum texto
- Footer "*valores aproximados" quando o preço for estimado

---

## Adaptação por cliente

1. Ler o design guide pra cor primária (fundo) e cor de acento (X, tarja, card COM)
2. Trocar "[MARCA]" pelo nome do clube/marca ("COM O PRIME × SEM O PRIME")
3. Preencher parceiro + os dois preços + o item ("dois hambúrgueres", "duas diárias")
4. Foto real do produto do parceiro na área full-bleed
5. Reaproveitável: é só trocar parceiro + foto + valores pros próximos criativos

---

## O que ajustar

- **Preço pouco visível:** aumentar `.pcard .val` e `.plabel` (queixa comum — exagerar)
- **Sem foto ainda:** o build cai no placeholder; dropar `foto-parceiro.jpg` (ou
  imagem em `marca/`) e re-rodar o script
- **Item específico:** trocar "dois pratos" pelo item real ("dois hambúrgueres")

Pede pro Claude: "muda a regra X no design preço topo" e ele edita este arquivo.
