# Instalação e desinstalação

## Antes de começar

Esta versão foi testada no Windows, com os três masters ingleses da edição Steam GOTY e OpenMW 0.51.0. Abra o jogo original uma vez, configure os caminhos no launcher e confirme que ele funciona. Feche o jogo e o launcher antes de alterar o perfil.

No perfil selecionado, a lista de conteúdo deve conter somente `Morrowind.esm`, `Tribunal.esm` e `Bloodmoon.esm`, nessa ordem. Faça backup dos seus saves e use um jogo novo para testar a tradução. O instalador não apaga saves.

Instale [Python 3.10+ para Windows](https://www.python.org/downloads/windows/) com Tcl/Tk e a opção de adicionar Python ao PATH. A instalação usa somente a biblioteca padrão do Python. Não há `pip install`, download automático de componentes nem acesso a serviços de IA.

## Instalação com dois cliques

1. Baixe o ZIP da tradução na [página de releases](https://github.com/chadvictor/morrowind-traducao-ptbr/releases). Extraia o pacote inteiro, não apenas o `.bat`.
2. Execute `INSTALAR.bat`.
3. Escolha a pasta do jogo, que contém `Data Files`. Também é aceito selecionar diretamente `Data Files`.
4. Escolha a pasta do OpenMW, que contém `resources` e `openmw.exe`. Na Steam, ela pode estar dentro da pasta do Morrowind, mas isso não é obrigatório.
5. Escolha o perfil ativo do OpenMW, identificado pelo arquivo `openmw.cfg`. Normalmente fica em **Documentos → My Games → OpenMW**. Se Documentos foi movido para OneDrive ou se você usa um perfil personalizado, selecione o local real.
6. Escolha uma pasta gravável para o pacote instalado, fora das pastas do jogo e do OpenMW. Será criada a subpasta `Morrowind-PTBR-0.1.0-beta.1`.
7. Confira os caminhos e confirme. A janela de terminal mostra o progresso de montagem dos três masters. Aguarde a mensagem final.
8. Abra o OpenMW como de costume e comece um jogo novo.

O programa valida hashes antes de aplicar as traduções. Uma edição não reconhecida é recusada; não renomeie arquivos ou edite hashes para forçar a instalação. Veja [compatibilidade](COMPATIBILIDADE.md).

O ZIP funciona offline depois de baixar o pacote, Python e OpenMW. A interface de seleção de pastas fica sem interação enquanto a montagem roda; acompanhe o terminal e não feche o processo.

## O que é instalado

O pacote público contém **os campos traduzidos e recursos complementares**. Ele não traz `Morrowind.esm`, `Tribunal.esm`, `Bloodmoon.esm`, arquivos BSA, vídeos, vozes ou o executável do jogo.

Durante a instalação, o programa lê seus masters originais e escreve cópias localizadas em `data/` dentro da pasta escolhida. Copia os recursos do seu OpenMW localmente para `resources/` e acrescenta os catálogos traduzidos. Não há modificação dos arquivos originais.

Na ativação, o perfil passa a usar o novo diretório de dados com prioridade e os recursos locais. São aplicados fallbacks traduzidos, `preferred locales = pt_BR, en` em `[General]` e `subtitles = true` em `[GUI]`. O `launcher.cfg` e as opções da Steam não são alterados.

O backup fica em `backups/morrowind-ptbr-<data-hora>` dentro do perfil. O arquivo `morrowind-ptbr-install.json` registra a instalação. Preserve esses arquivos.

Não mova nem renomeie o diretório instalado enquanto a tradução estiver ativa. Para transferi-lo, desative a tradução, prepare o novo destino e ative novamente.

## Desativar e restaurar

Execute `DESINSTALAR.bat` e selecione o perfil usado na instalação. Quando os arquivos de configuração continuam iguais aos produzidos pelo instalador, o programa restaura a configuração anterior. A pasta da tradução, os backups e todos os saves são preservados.

**Se a configuração mudou depois da instalação**, a reversão automática para para evitar perder mudanças de mods, vídeo ou controles. Nesse caso, feche o jogo e o launcher, faça uma cópia da configuração atual e compare com o backup indicado em `morrowind-ptbr-install.json`:

1. Em `openmw.cfg`, remova o bloco entre `# MORROWIND-PTBR BEGIN` e `# MORROWIND-PTBR END`.
2. Reponha, a partir do backup, a configuração anterior de `resources` e os valores `fallback` que a tradução substituiu. Preserve suas demais alterações recentes.
3. Em `settings.cfg`, restaure as preferências anteriores de idioma e legendas, se desejado.
4. Após conferir os arquivos, remova somente `morrowind-ptbr-install.json`. Mantenha o backup para consulta.

Restaurar os dois arquivos completos do backup é outra possibilidade, mas **também desfaz todas as mudanças posteriores** nesses arquivos. Faça isso apenas se esse for seu objetivo.

## Linha de comando

Para quem prefere terminal, execute na raiz extraída do projeto, substituindo os exemplos pelos seus caminhos:

```powershell
python scripts/mwbr.py validate
python scripts/mwbr.py build --game "D:\Jogos\Morrowind" --openmw "D:\Jogos\OpenMW" --output "D:\Mods\Morrowind-PTBR"
python scripts/mwbr.py activate --bundle "D:\Mods\Morrowind-PTBR" --profile "D:\Perfis\OpenMW"
python scripts/mwbr.py deactivate --profile "D:\Perfis\OpenMW"
```

`build` apenas prepara o pacote; `activate` altera o perfil com backup. Reexecutar o build para um pacote idêntico verifica a integridade e não o sobrescreve. Para uma nova versão, use outro destino e desative a anterior antes de ativar a nova.

## Problemas comuns

| Mensagem ou sintoma | Como proceder |
|---|---|
| Python não encontrado | Instale Python 3.10+ do python.org e habilite PATH; reabra o terminal |
| Erro de `tkinter` | Repare a instalação do Python incluindo Tcl/Tk, ou use os comandos acima |
| Master incompatível | Compare os hashes em `COMPATIBILIDADE.md`; não use masters já modificados |
| Recurso OpenMW incompatível | Use a versão suportada sem substituir seus arquivos de interface |
| Perfil contém outros mods | Crie/configure um perfil limpo com os três masters na ordem indicada |
| Tradução aparece em inglês | Confira o perfil escolhido e se outro diretório de dados está sobrepondo o pacote |
| Launcher continua em inglês | Os catálogos Qt dependem também do locale do sistema; o idioma do jogo é configurado separadamente |
| Jogo não inicia após alteração manual | Restaure a configuração usando o backup e informe a mensagem da falha na issue |
| Save antigo tem tópicos em inglês | Use jogo novo; não há migração validada de saves anteriores |

Leia também a [documentação de instalação oficial do OpenMW](https://openmw.readthedocs.io/en/stable/manuals/installation/index.html).
