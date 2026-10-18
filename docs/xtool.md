# xtool: app de iPhone feito pelo Claude Code

Do Reel do @billyia_ (18/10/2026): https://github.com/xtool-org/xtool (licença MIT, ativo em 18/10/2026).
O xtool substitui o Xcode na linha de comando: compila um projeto SwiftPM como app de iPhone, assina e
instala no aparelho. Como tudo é por terminal, o Claude Code escreve o código, recompila e manda pro
celular. Documentação oficial: https://xtool.sh/documentation/xtooldocs

## No Mac (caminho mais curto)

1. Instale o Xcode pela App Store e abra uma vez (aceite os termos). Confira:
   `xcrun -sdk iphoneos -show-sdk-path`
2. `brew install xtool-org/tap/xtool` (o `instalar-ferramentas.sh` já faz isso).
3. `xtool setup` e escolha o login:
   - **0, API Key:** recomendado se você pagar o Apple Developer Program (US$ 99/ano).
     Crie uma Team Key com papel App Manager no App Store Connect.
   - **1, Senha:** funciona com qualquer Apple ID, mas usa API privada da Apple. A própria
     documentação sugere um Apple ID separado. A senha vai só para a Apple.
4. Plugue o iPhone no cabo, destrave e confie no computador.

## No PC (Windows, pelo WSL, dá mais trabalho)

1. Instale o WSL: `wsl --install`, como admin, e reinicie o PC.
2. USB para o WSL com o usbipd: https://learn.microsoft.com/windows/wsl/connect-usb
   Se der `AFCClient.Error.muxError`, use o atalho do iTunes descrito em
   https://github.com/xtool-org/xtool/issues/19#issuecomment-2898986718
3. Dentro do WSL:
   - Instale o Swift 6.4 seguindo https://swift.org/install/linux
   - Rode `sudo apt-get install usbmuxd libimobiledevice-utils`.
4. Baixe o **Xcode 27 (.xip)** pelo navegador, logado no Apple ID:
   https://developer.apple.com/download/all/?q=Xcode
5. Instale o xtool:
   ```bash
   curl -fL "https://github.com/xtool-org/xtool/releases/latest/download/xtool-$(uname -m).AppImage" -o xtool
   chmod +x xtool && sudo mv xtool /usr/local/bin/
   xtool setup   # login e caminho do Xcode .xip
   swift sdk list   # tem que aparecer "darwin"
   ```

## Primeiro app (cole no Claude Code)

> Use o xtool já instalado. Crie um app SwiftUI chamado [NOME] que [O QUE FAZ]. Três telas,
> componentes nativos do iOS, modo escuro. Rode `xtool new`, depois `xtool dev` para compilar e
> instalar no meu iPhone. Se der erro, leia a mensagem, corrija e rode de novo.

## Onde isso serve na ARK

- **Aprovar pelo celular** a fila do Flow v2. Um app pequeno com notificação, que fala com o
  painel. Antes disso, teste o Remote Control oficial do Claude, que já faz parte disso.
- **Protótipo de app para cliente** (Vivenda, por exemplo) no mesmo dia, para mostrar na reunião.
- **WorkFlowArk na App Store** continua no plano Capacitor (`gest-odeagencia/docs/APPLE-STORE.md`).
  O xtool não embrulha PWA; ele serve para app nativo em Swift.

## Limites

- Com Apple ID gratuito, a Apple deixa o app instalado por pouco tempo e limita quantos apps
  ficam no aparelho. Para uso contínuo ou para publicar na loja, é preciso a conta paga.
- O xtool **não foi instalado nem testado** nesta máquina. Ele precisa do seu Apple ID, do
  Xcode baixado com o seu login e do iPhone no cabo.
