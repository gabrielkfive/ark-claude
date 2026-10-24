Claude, instala no meu PC as skills e plugins de design que o Gabriel usa. Rode um por um, pule o que já estiver instalado e no fim me mostre o que deu certo e o que falhou.

1. Skills do Emil Kowalski (acabamento, animação, estilo Apple, protótipos):
   npx skills@latest add emilkowalski/skills
   Repo: https://github.com/emilkowalski/skills

2. Hallmark (tira a "cara de IA" do design, e copia estilo de print ou site):
   npx skills@latest add nutlope/hallmark
   Repo: https://github.com/Nutlope/hallmark

3. UI UX Pro Max (paletas, combinações de fonte e estilos prontos):
   npx skills@latest add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max
   Repo: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

4. Plugins oficiais da Anthropic (rodar dentro do Claude Code):
   /plugin install frontend-design@claude-plugins-official
   /plugin install superpowers@claude-plugins-official

5. ECC (design-system, make-interfaces-feel-better, frontend-slides):
   /plugin marketplace add https://github.com/affaan-m/ECC
   /plugin install ecc@ecc
   Instale só por esse link oficial, cópia de terceiro pode ter vírus.

6. Skills da ARK (replica-fiel, carrossel no padrão ARK):
   git clone https://github.com/gabrielkfive/ark-claude ~/ark-claude
   cd ~/ark-claude && bash instalar.sh
   (se já tiver a pasta: cd ~/ark-claude && git pull && bash instalar.sh)

Depois feche e abra o Claude Code pra carregar tudo.

Como usar no dia a dia:
- Tem uma referência pra copiar? Peça "usa a replica-fiel" e mande o print.
- Peça nova do zero? Peça "usa o hallmark".
- Sempre confira o resultado em imagem antes de entregar, não só o código.
