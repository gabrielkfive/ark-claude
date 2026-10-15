---
name: edicao-cinematografica
description: Use ao editar ou colorizar vídeo de cliente a partir de captação bruta (baixar material do Drive, escolher takes, criar look e LUT, limpar locução, legendar, mixar e renderizar). Também use quando o Gabriel mandar uma pasta de captação, pedir "monta o vídeo", "coloriza", "faz o corte" ou mandar uma referência visual de filme. Traz o método que funcionou na Vivenda x Pietra, com os comandos reais.
---

# Edição cinematográfica a partir de bruto

Método construído na captação Vivenda x Pietra (Clube.Co, 26/08/2026), 49 clipes
4K 10 bits de Fujifilm X-T3, entregue em sete versões. Cada regra aqui custou um
erro real.

## A ordem que funciona

1. Baixar tudo e conferir a contagem
2. Ler o roteiro técnico, se existir
3. Mapear a locução palavra por palavra
4. Varrer os clipes: conteúdo, tremor, cor
5. Desenhar o look e gerar a LUT
6. Montar bloco a bloco, casando plano com fala
7. Limpar a voz, mixar, legendar
8. Rodar a skill `conferir-video` **antes** de dizer que está pronto

## 1. Baixar do Drive

O conector do Drive **mente por omissão**: só indexa arquivo que o usuário já
abriu. Numa pasta de 49 vídeos ele devolveu 2, e eu afirmei ao Gabriel que a
cobertura não existia. Nunca use listagem de conector como prova de ausência.

```bash
python -m gdown --folder "https://drive.google.com/drive/folders/ID" -O .
```

O gdown enumera tudo mas **para por volta de 29 arquivos** (limite do Google).
O log traz `Processing file <id> <nome>` para os 49: extraia os que faltam e
baixe um a um por id. Confira a contagem no fim.

## 2. Varrer o material

Folha de contato **já com a LUT**, 2 a 3 quadros por clipe, rótulo com o número
em cada tile. Sem rótulo você não consegue referenciar depois.

```bash
ffmpeg -y -ss T -i CLIPE.MOV -frames:v 1 \
  -vf "lut3d=file=look.cube,scale=320:-1,drawtext=text='0217':x=6:y=4:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.8:boxborderw=4" q.jpg
# depois: renomear em sequencia f%03d.jpg e tile=6x5  (esta build nao tem glob)
```

## 3. Tremor: medir e escolher a janela

Não escolha ponto de entrada no olho. Varra o clipe inteiro em janelas de 1,6 s
e pegue a mais parada. Ganho real observado: um clipe caiu de 23,5 para 3,6 só
mudando o segundo de entrada. Método e armadilhas estão em `conferir-video`.

## 4. O look

**Meça a referência e meça o bruto.** Nunca copie números de uma referência
gravada em outro lugar: um Reel à luz de vela tem luma 39 de 255, e forçar isso
num ginásio em luz do dia apaga o rosto da pessoa. A referência serve para
**linguagem e composição**, a cor tem que servir à locação.

Diagnósticos que decidem o look:
- saturação do bruto abaixo da metade do alvo, material log, saturação **sobe**
- saturação de todos os clusters entre 0 e 0,08, a locação **não tem cor**;
  construa com **luminância**, não com saturação, senão você multiplica ruído de
  compressão e a janela vira mancha verde
- luz do lugar já quente, **neutralize**, não empurre âmbar. Âmbar somado a
  tungstênio dá laranja, e o Gabriel reclama com razão
- verde nas sombras vem de teal positivo no `colorbalance`. Deixe `gs` e `gm`
  **negativos** em todas as LUTs

### Gerar .cube a partir de uma cadeia de filtros

Permite iterar rápido no ffmpeg e levar o resultado exato para o Resolve. Monta
a treliça identidade, passa pelo filtro, grava o cubo:

```python
N=33; v=np.linspace(0,1,N)
lat=[(r,g,b) for b in v for g in v for r in v]        # r varia mais rapido
cru=(np.array(lat)*65535).round().astype("<u2").tobytes()
p=subprocess.run(["ffmpeg","-f","rawvideo","-pix_fmt","rgb48le","-s","%dx%d"%(N*N,N),
   "-i","-","-vf",CADEIA,"-f","rawvideo","-pix_fmt","rgb48le","-"],input=cru,capture_output=True)
# escrever LUT_3D_SIZE 33 e as linhas "r g b"
```

Depois **confirme** aplicando a LUT e comparando com a cadeia original: a
diferença tem que ficar abaixo de 0,004.

Faça uma LUT por ambiente (base, claro, escuro, neutro), não uma só para tudo.

## 5. Locução

`faster-whisper` com `word_timestamps=True` dá o mapa dos takes. A pessoa erra e
regrava: escolha o take bom, não o primeiro.

**Os tempos marcam o INÍCIO da palavra.** Cortar ali come o fim dela. Dê 0,4 a
0,5 s depois do início da última palavra.

**Limpeza de ruído de ventilação**, o que funcionou de verdade (ganho de 11,4 dB
de relação sinal ruído, contra 5 dB do `afftdn`):

```
highpass=f=80, asplit -> arnndn=m=bd.rnnn -> amix seco 0,18 / limpo 0,82
-> compand=attacks=0.02:decays=0.30:points=-80/-88|-52/-66|-38/-38|0/0
```

Modelo: `https://raw.githubusercontent.com/GregorR/rnnoise-models/master/beguiling-drafter-2018-08-30/bd.rnnn`

**Áudio de ambiente de academia não serve de trilha**: tem conversa de direção e
ruído. Use no máximo nos primeiros segundos.

## 6. Trilha

Sem faixa licenciada, sintetize um leito e **avise que é provisório**. O que
soou bem: progressão Lá menor, Fá, Dó, Sol resolvendo em Dó, com pad de cinco
vozes, arpejo em colcheias entrando aos 9 s, pulso grave a 90 bpm crescendo, e
brilho no agudo a partir dos 14 s. Arco geral crescendo até o bloco do produto.

Mixagem: voz manda, o resto abaixa sozinho.

```
[bed][voz]sidechaincompress=threshold=0.045:ratio=8:attack=20:release=420
-> amix com a voz -> loudnorm=I=-15:TP=-1.5:LRA=11
```

## 7. Legendas

Montserrat não vem no Windows. Pegue os TTF reais pela API do Google Fonts
(`fonts.googleapis.com/css2?family=...` e siga as URLs de `fonts.gstatic.com`).
Baixar de `github.com/google/fonts/raw/...` devolve página de erro de 304 KB com
assinatura `0a0a0a0a`: **confira a assinatura**, que tem que ser `00010000`.

ASS com `subtitles=arquivo.ass:fontsdir=fonts`. Corpo **62 em 1080p**, 54 não lê
no celular. Quebre linha em fronteira de frase, nunca terminando em preposição
ou artigo. Corrija nome de marca que o Whisper escreve minúsculo.

## 8. Armadilhas de ferramenta

- **Caminho MSYS dentro de filtro do ffmpeg não funciona.** `lut3d=file=/c/...`
  falha calado. Entre na pasta e use caminho relativo.
- **Dois pontos em `drawtext`** quebra o parser. Troque por vírgula ou hífen.
- **`zoompan` duplica quadro** quando a fonte é 29,97 e a saída 30. Feche a
  cadeia com `trim=0:DUR,setpts=PTS-STARTPTS`.
- **Concat acumula deriva** de arredondamento: 27 segmentos perderam 0,55 s.
  Some as durações **reais** dos arquivos e absorva a diferença no último plano.
- `ffprobe` de duração em arquivo com stream de dados imprime duas linhas.

## 9. Antes de entregar

Chame a skill `conferir-video`. Ela existe porque eu já disse "final" para um
vídeo com palavra cortada, voz vazando e take tremido.

## 10. Mais armadilhas de ferramenta

- **`tile` do ffmpeg exige quadros do mesmo tamanho.** Com `scale=N:-1` cada
  clipe vira uma altura diferente e o `tile` devolve **um único quadro**, sem
  erro. Normalize com `scale=W:H:force_original_aspect_ratio=decrease,pad=...`
  antes, ou monte a folha com PIL, que é determinístico.
- **Duração de áudio no cabeçalho mente.** O `ffprobe` informou 28,8 s para uma
  faixa que tinha 58,6 s de verdade. Decodifique e conte amostras.
- **Rótulo do `filter_complex` só pode ser consumido uma vez.** Usar `[vo]` no
  `sidechaincompress` e de novo no `amix` dá "matches no streams". Use `asplit`.
- **Monte o áudio como arquivo próprio e confira antes de multiplexar.** Numa
  cadeia longa de filtros a mixagem saiu 6 s mais curta que o vídeo e a vinheta
  ficou muda. Gerar `MIX.wav`, medir, e só então casar com a imagem.

## 11. Trave o labial no tempo acumulado real

Quando o corte volta para o rosto depois de cobertura, o ponto de entrada na
fonte tem que ser `offset + soma dos quadros REAIS já montados`, não a posição
pretendida. Renderize cada plano com `-frames:v N` exato e vá somando. Um clipe
de cobertura que rendeu 2,80 s em vez de 3,50 empurra tudo depois dele e a boca
sai do lugar sem que nenhuma medição de imagem acuse.

## 0. Antes de tudo: inventário e transcrição (aprendido a ferro em 30 e 31/08)

Ordem que NÃO pode ser invertida, porque foi invertida oito vezes em dois dias
(ver memória `feedback-revisao-30-31-ago-erros-repetidos`):

1. **Inventário do material.** `CLIENTES\<cliente>\` inteira (BRUTO, COLORIDOS,
   INSTAGRAM, ENTREGA), `Documents\ARK CONTENT\_NOVOS_MIKE`, `.claude\uploads\`,
   zips e os 8 vídeos do Instagram da ARK (memória `ark-acervo-instagram-portfolio`).
   Escrever a lista com duração, resolução e uma linha do que mostra. "Não
   existe" só depois de duas ferramentas de natureza diferente.
2. **Transcrever a locução palavra por palavra** (faster-whisper large-v3,
   `word_timestamps=True`) e montar a tabela segundo x fala x plano. Cada linha
   nomeia o arquivo e o ponto de entrada. Sem essa tabela não há render.
3. **Lista de vetados da peça**: marca de terceiro legível, pessoa tapando a
   lente, take que o Gabriel já mandou tirar, logo de outro cliente atrás do
   apresentador. Conferida antes de cada render, não caçada caso a caso.
4. **Material profissional antes de bastidor.** Reel publicado e bruto 4K
   primeiro; take de celular só onde a fala pede bastidor, e nunca com pele
   amarela de luz de laboratório ou touca em primeiro plano.
5. **Cor: casar com o que ele já aprovou.** COLORIDOS do cliente, Reel
   publicado ou grade dele no Resolve são a referência. Material que já está
   bom recebe só contraste leve. Se a câmera é Fujifilm X-T3 o bruto pode ser
   F-Log, mas testar bloco a bloco: o material da feira não era.
6. **Gimbal: taxa nativa (60 fps), sem estabilizar, sem zoompan.** Movimento
   de linguagem não é tremor.
7. Só então os passos 1 a 11 acima, e `conferir-video` no arquivo final.

Regra do Gabriel para o criativo institucional: "faz algo bom e real", "não
inventa de mexer muito em color", "toma liberdade de usar os vídeos que mandei",
"somos uma produtora". Trilha sintetizada continua provisória: avisar sempre.
