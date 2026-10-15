---
name: conferir-video
description: Use ANTES de dizer que um vídeo está pronto, final, aprovado ou entregável, e sempre que for enviar um corte para o Gabriel. Mede tremor, cor, áudio, legenda e sincronia com o roteiro, e devolve uma tabela de prova. Também use quando o Gabriel reclamar que um take "está tremido", "está amarelado", "está escuro", "vazou voz" ou "faltou legenda".
---

# Conferir vídeo antes de entregar

Nunca dizer "final", "pronto" ou "está no ar" sobre um vídeo sem rodar esta
conferência e **mostrar os números**. Comando que rodou não é prova. Render que
saiu não é prova. A prova é a medição do arquivo entregue.

Todas as falhas listadas aqui já aconteceram de verdade na Vivenda x Pietra.
Elas não são hipóteses.

## A regra de ouro

Meça o **arquivo que você vai mandar**, não o intermediário. Já entreguei vídeo
afirmando que tinha legenda sem abrir o arquivo final para olhar.

## 1. Tremor, take a take

Nunca julgue tremor no olho, nem confie em "parece estável". Meça.

```bash
ffmpeg -hide_banner -loglevel error -ss INI -t DUR -i CLIPE.MOV \
  -vf "scale=960:540,vidstabdetect=shakiness=10:accuracy=15:result=t.trf" -f null -
```

Depois leia o `.trf` e some o deslocamento absoluto por quadro. Rode em TODOS
os candidatos e ordene. Corte usa os mais estáveis; take tremido só entra se
for insubstituível, e aí estabilizado.

**Estabilizar não conserta tudo.** Se o Gabriel disser "não quero que você
estabilize, troque o take", troque. Estabilização come bordas e cria deriva.
E **meça o resultado da estabilização**: já rodei `vidstabtransform` e o tremor
caiu de 36,0 para 34,7, ou seja, não fez nada, e eu entreguei achando que tinha
consertado.

Melhor que estabilizar: **varrer o clipe em janelas e achar o trecho mais
parado**. Um clipe pode ir de 23,5 para 3,6 só mudando o ponto de entrada.

### Duas armadilhas do medidor de borda

1. **Plano em que o movimento enche o quadro** (pés na esteira, esteira andando)
   marca tremor altíssimo sem a câmera ter se mexido. Ali o medidor não vale,
   julgue no olho.
2. **Medir atravessando um corte** dá pico gigante. As durações reais dos
   segmentos diferem das planejadas por arredondamento de quadro, então a
   posição acumulada sai do lugar. Some as durações **reais** dos arquivos, não
   as pretendidas, e deixe folga nas bordas da janela.

## 2. Cor, take a take

Extraia um quadro **já com a LUT** e meça R, G, B médios.

- `G - (R+B)/2 > 0.006` → **verde**. Acontece em plano escuro quando há teal na
  sombra. Foi reclamado duas vezes.
- `R - B > 0.05` → **amarelo demais**. Se a luz do lugar já é quente, não
  empurre âmbar, **neutralize**. Somar âmbar com tungstênio deixa laranja.
- luma média `< 0.13` → escuro demais, o rosto some.

## 3. Áudio: envelope, não transcrição

**Transcrição não prova ausência de som.** O Whisper não transcreveu um "Valeu."
que estava no meio do take, e eu entreguei com a palavra solta. Duas vezes.

Meça o envelope em janelas de 40 ms e olhe onde há energia:

```python
rms = np.sqrt((janela**2).mean()); db = 20*np.log10(rms)
```

Qualquer bloco acima de uns 15 dB do piso de ruído é som. Se houver som onde
você acha que há silêncio, isole aquele trecho e transcreva **só ele**, com
`vad_filter=False` e `condition_on_previous_text=False`.

## 4. Margem de saída da fala

Os tempos do Whisper marcam o **início** da palavra, nunca o fim. Cortar no
início da última palavra come o final dela. Dar **0,4 a 0,5 s depois do início
da última palavra**, e conferir transcrevendo o corte de volta.

Entre takes a pessoa fala com a equipe ("Bom?", "Valeu", "É isso", "Eu estou
subindo o microfone"). Confira sempre o que existe **antes e depois** da fala.

## 5. Legenda

Se prometeu legenda, **prove que ela está queimada no arquivo final**:

```bash
ffmpeg -y -ss T -i FINAL.mp4 -frames:v 1 -vf "crop=iw:220:0:ih-230" prova.jpg
```

Olhe a imagem em pelo menos quatro momentos diferentes. Confira também a fonte
pedida, o corpo (62 em 1080p lê no celular, 54 não) e a quebra de linha: nunca
terminar linha em preposição ou artigo solto.

## 6. Repetição e continuidade

Liste os clipes na ordem do corte. **Dois cortes seguidos do mesmo clipe ou do
mesmo enquadramento leem como repetição**, mesmo sendo ações diferentes.
Verifique também: a pessoa abre a boca para falar num take que é só imagem? Ela
olha para fora de quadro para a equipe? Aparece parte do corpo que foge do tom?

## 7. Sincronia com o roteiro

O plano tem que casar com a fala. Se a locução diz "a minha profissão", o plano
da profissão (jaleco, consultório) entra **ali**, não trinta segundos depois.
Monte a tabela fala por bloco contra plano por bloco antes de renderizar.

## 8. O arquivo final

- duração de vídeo e de áudio batem
- existe faixa de áudio, em 48 kHz
- loudness perto de menos 15 LUFS, pico abaixo de menos 1 dB
- transcreva o **filme finalizado** e compare com o roteiro, palavra por palavra
- gere folha de contato de 20 quadros e **olhe**

## Como reportar

Tabela com medida, valor, limite e situação. Sem adjetivo sem número ao lado.
Se algo não foi conferido, dizer que não foi conferido, em vez de omitir.

## 9. Legenda que invade o bloco seguinte

Dar folga no fim de cada bloco (o clássico "+0,3 s para respirar") **sem cortar
no início do próximo** faz os eventos do ASS se empilharem. O renderizador
desenha os dois ao mesmo tempo e o texto aparece **fora de ordem**:

```
mil reais e que tem interesse em
Você empresário que fatura
mais de 50
```

No criativo institucional da ARK, **24 dos 28 blocos** estavam nesse estado. Não
era um caso isolado, era o filme inteiro, e nenhuma medição de cor, áudio ou
tremor pega isso. Só o quadro extraído pega.

**Como aplicar:** o fim de cada bloco é `min(fim natural, início do próximo menos
0,02 s)`. Depois conferir por programa que não sobrou sobreposição, e ainda assim
**olhar quatro quadros**. Se a legenda queimada do cliente lê melhor que a sua, a
sua está pequena: em 1080x1920 o corpo 70 lê, 58 não.

## 10. Material do cliente já vem com legenda queimada

Trabalho publicado da agência costuma ter legenda gravada no vídeo. Se você puser
a sua no mesmo lugar, ficam duas legendas brigando. Solução que funcionou: **subir
a sua para o topo** só na janela em que aparece material publicado, com um estilo
`Alignment=8`. Fica lendo como decisão de design, não como conserto.

## 11. O seu próprio movimento entra na conta do tremor

`zoompan` soma de 2 a 3 pontos na métrica de borda. Um plano mediu **5,91 na
fonte e 8,25 já no filme**, e a diferença era o zoom que eu mesmo pus.

**Meça a FONTE para escolher o take** e use a medição do filme só para achar
plano fora da curva. Senão você fica perseguindo o seu próprio movimento.
Separe também o que é **movimento de linguagem** (drone, slider, caminhada de
cobertura de evento) do que é câmera trêmula: os dois marcam igual e só um é erro.

## 12. Alerta em material já aprovado não é alerta

Ao intercalar trabalho que a agência já entregou e o cliente já publicou, a
métrica de cor acusa "amarelo" no look quente que **é** o look aprovado.
Recolorir aquilo seria passar por cima de decisão de quem assinou a peça.

Separe as duas listas antes de reportar: **a minha grade** (corrijo) e **look
aprovado de terceiro** (declaro isento e digo por quê). Nunca esconda o número,
mostre com a justificativa do lado.

## 13. Container com tarja: meça a imagem, não o quadro

Material "vertical" entregue por filmmaker costuma vir como **container
horizontal com a imagem no meio e tarja preta dos lados**. Na Royal Face eram
3840x2160 com a imagem real em 1215x2160 a partir de x=1312, dois terços do
quadro eram preto.

Isso envenena TODA medição: a luma média deu **0,161 medindo o quadro inteiro e
0,376 medindo só a imagem**. Eu quase clareei um material bem exposto.

**Como aplicar:** antes de qualquer medida, decodifique um quadro em cinza e ache
as colunas e linhas que não são pretas. Confirme em 5 ou 6 clipes, porque a
janela costuma ser a mesma em todos. Só então meça e corte.

## 14. O transcritor erra o tempo da PRIMEIRA palavra

Duas vezes na mesma sessão o Whisper marcou a primeira palavra em lugar errado:
disse 0,92 quando o som começava em 0,12, e disse 0,00 quando havia meio segundo
de folga. Ele preenche o começo do segmento com o silêncio anterior, ou grampeia
em zero.

**Como aplicar:** para achar onde a fala começa, use o **envelope**. Para saber se
o que está ali é fala ou respiração, **isole o trecho e transcreva desacelerado**:
se o modelo não devolve nada, é respiração. Foi assim que eu ganhei meio segundo
de gancho num anúncio de 19 segundos.

## 15. Marca de terceiro no quadro

Em anúncio pago, embalagem de fornecedor legível trava na revisão e a decisão de
exibir é do cliente, não sua. Na Royal Face o mesmo frasco aparecia em **quatro**
clipes e a caixa de outro fabricante em mais dois; tirei um e ele voltou por
outro clipe no vídeo seguinte.

**Como aplicar:** faça a **lista de vetados uma vez**, com o número do clipe e o
que aparece, e confira essa lista antes de cada montagem. Caçar caso a caso
garante que um escapa.

## 16. Tremor se julga pela razão saída sobre fonte

Limite absoluto (6,0) aprovou vídeos que o Gabriel rejeitou por tremor (Royal
Face, 31/08 13:45). O certo: medir o mesmo trecho na FONTE e no FILME e reportar
a razão. Acima de 1,3x, o meu pipeline piorou o take (conversão 60 para 30 fps,
`zoompan`, estabilização em material de gimbal). Material de gimbal entrega na
taxa nativa, sem estabilizar e sem zoom.

## 17. Áudio: envelope em TODA a duração, inclusive a vinheta

`-an` num render parcial e `-shortest` no mux deixaram a vinheta muda (menos 180
dBFS do segundo 58 ao 64) e cortaram o fim. Medir o envelope do arquivo final do
primeiro ao último segundo e comparar com a duração do vídeo.

## 18. Um take, um uso, e a folha a 1 fps

No criativo da ARK v10 o mesmo take de tablet entrou duas vezes em 4 segundos e o
estande apareceu quatro vezes. Antes de entregar, listar clipe por bloco e
recusar qualquer repetição de arquivo ou de enquadramento. A folha de contato a
1 fps com rótulo de tempo (`fps=1,tile=8xN,drawtext`) mostra isso em um olhar.

## 19. Defeito conhecido não vai no rodapé

A v9 foi entregue com "quatro coisas que ainda não estão certas" e a v10 com
"dois pendentes". Resposta dele: "tudo errado". Se há defeito conhecido, ou se
conserta ou não se entrega; a lista de pendentes é para o que depende dele.

## 20. A tabela de prova sai em UTC menos 3

Os carimbos de sessão são UTC. "Passei das 17h" foi dito às 15:58 de Brasília.
Ler o relógio do Windows antes de falar de prazo.
