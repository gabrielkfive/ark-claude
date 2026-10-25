# Máquina nova: roteiro para o Claude da máquina

Você é o Claude recém instalado num PC ou notebook formatado do Gabriel (ARK). Ele não é técnico e fala por voz. Faça tudo sozinho, em pt-BR, frases curtas, sem traço nem travessão.

1. Baixe e rode o diagnóstico em PowerShell:
   `irm https://raw.githubusercontent.com/gabrielkfive/ark-claude/master/maquina-nova.ps1 -OutFile $env:TEMP\mn.ps1; powershell -ExecutionPolicy Bypass -File $env:TEMP\mn.ps1 -Verificar`
2. Leia o resultado e resolva primeiro o que veio marcado com [!!]:
   - Chromebook: drivers do CoolStar (coolstar.org/chromebook/windows-install.html) para touchpad, teclado e som. Firmware só se ele autorizar.
   - Dispositivo sem driver: procure o driver pelo modelo no site do fabricante ou pelo Windows Update (Atualizações opcionais).
   - Disco eMMC ou HDD: avise que a lentidão vem do disco; desligue apps de inicialização e a indexação de busca.
3. Rode o script sem `-Verificar` (como admin) para instalar a base: Git, Node, Python 3.13, gh, jq, Chrome e Claude Code.
4. Peça para ele rodar `gh auth login` (é ele quem faz login), depois clone `gabrielkfive/ark-claude` e `gabrielkfive/ark-jarvis` em `%USERPROFILE%` e rode `ark-claude\instalar-ferramentas.ps1` e `ark-jarvis\instalar.ps1`.
   No Windows 10 o app Claude Desktop é MSIX e esconde o que é gravado em AppData\Roaming (pip --user, uv tool, config do gh). Rode esses instaladores e o `gh auth login` num PowerShell aberto fora do app.
5. Python aqui é `python`, nunca `python3`.
6. Ação destrutiva (formatar, firmware, apagar partição) só com o ok dele.
7. No fim, rode o `-Verificar` de novo e mostre a ele o antes e o depois.
