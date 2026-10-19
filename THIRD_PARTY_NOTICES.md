# Licenças e conteúdo de terceiros

## Arquivos originais do projeto

Os scripts offline em `scripts/`, testes, documentação e contribuições autorais são disponibilizados sob a MIT, conforme [LICENSE](LICENSE). A licença cobre apenas os direitos de que os colaboradores dispõem. Ela não altera os direitos de terceiros sobre obras preexistentes.

## The Elder Scrolls III: Morrowind

Morrowind, Tribunal, Bloodmoon, seus textos originais, personagens, marcas e demais conteúdos pertencem aos respectivos titulares, incluindo Bethesda Softworks/ZeniMax. Esta é uma tradução de fã não oficial. O projeto não afirma patrocínio, aprovação ou afiliação com os titulares.

Os catálogos contêm textos traduzidos para aplicação aos originais do próprio jogador. Não distribuímos masters completos, BSA, executáveis, filmes ou vozes. A licença MIT do nosso código não concede licença para o jogo ou para o conteúdo subjacente às traduções. É necessário possuir uma cópia do jogo. O uso de um formato de patch não equivale a uma declaração de autorização dos titulares.

## OpenMW

Origem: [OpenMW](https://github.com/OpenMW/openmw), revisão `f4bec41444214a7903bebd178389ca22ca13f646`, versão 0.51.0. Copyright dos contribuidores do OpenMW; veja os [créditos upstream](https://github.com/OpenMW/openmw/blob/f4bec41444214a7903bebd178389ca22ca13f646/AUTHORS.md).

Arquivos derivados/modificados em `conteudo/data/mygui/`, `conteudo/data/l10n/` e `interface/qt/` mantêm a **GNU GPL versão 3**. As alterações consistem em traduções pt-BR e normalizações de XML necessárias à leitura. A licença está em [LICENSES/GPL-3.0.txt](LICENSES/GPL-3.0.txt).

Os `.qm` em `conteudo/resources/translations/` são compilações dos `.ts` correspondentes em `interface/qt/`; esses fontes editáveis são incluídos no mesmo pacote público. Para reconstruir, use o comando Qt `lrelease arquivo.ts -qm arquivo.qm`. A instrução detalhada está em `docs/MANUTENCAO.md`. Os binários do OpenMW e Qt não são distribuídos aqui.

## Fonte MysticCards e imagens do menu

Os 21 botões em `conteudo/data/textures/` foram desenhados para este projeto com a fonte MysticCards distribuída pelo OpenMW; não são cópias dos botões comerciais. A fonte é de OpenMW Team (2022), baseada em Pelagiad de Isak Larborn (2015), sob SIL Open Font License 1.1. O aviso integral está em [LICENSES/MysticCards-OFL-1.1.txt](LICENSES/MysticCards-OFL-1.1.txt).

Não distribuímos o arquivo da fonte no repositório ou ZIP. A cópia local de recursos feita pelo instalador vem da instalação OpenMW do jogador. A licença da fonte não exige aplicar OFL aos documentos/imagens gerados com ela.

## Ferramentas utilizadas durante o desenvolvimento

O trabalho usou o parser PE do REA como apoio à investigação, parsers de TES3, ferramentas OpenMW e modelos de IA via OpenRouter. Esses serviços não são dependências da instalação. Nenhum código do cliente privado de IA, credencial, banco de trabalho ou pacote REA é incluído nesta publicação.
