# Instalar o mod no OpenMW

**Para jogar: Morrowind GOTY em inglês, com Tribunal e Bloodmoon, e OpenMW 0.51.0. Não precisa de Python, compilador, conta de IA ou chave de API.** O teste desta beta foi feito no Windows com a edição Steam. Confira [compatibilidade](COMPATIBILIDADE.md) para outras edições.

## Baixar e ativar

1. Baixe **`morrowind-ptbr-openmw-mod-0.1.0-beta.2.zip`** em [Releases](https://github.com/chadvictor/morrowind-traducao-ptbr/releases/tag/v0.1.0-beta.2). Os arquivos “Source code” e “fontes-python” são para contribuição/reconstrução.
2. Extraia o ZIP inteiro em uma pasta permanente, por exemplo `D:\Mods\Morrowind-PTBR`. Dentro dela existe **`Data Files`**, contendo `Morrowind_PTBR.esp`, mapas e pastas de recursos. Não copie por cima dos masters originais.
3. No **OpenMW Launcher → Data Files → Data Directories**, use **Append/Adicionar** e escolha **a pasta `Data Files` do mod**. Deixe-a depois da pasta de dados do jogo, para seus recursos terem prioridade.
4. Na lista de conteúdo/plugins, marque **`Morrowind_PTBR.esp`** depois dos três masters. A ordem fica:

```text
Morrowind.esm
Tribunal.esm
Bloodmoon.esm
Morrowind_PTBR.esp
```

5. Abra o jogo e **comece uma partida nova**. Use inicialmente um perfil sem outros mods. Seu atalho habitual ou integração existente com a Steam continua servindo.

Essa é a instalação por pasta de dados e plugin documentada no [guia oficial do OpenMW](https://openmw.readthedocs.io/en/stable/reference/modding/mod-install.html). Copiar arquivos diretamente para o `Data Files` do jogo também é uma prática encontrada na comunidade, mas a pasta separada facilita atualizar e remover sem misturar recursos.

Se preferir configurar manualmente, adicione ao **`openmw.cfg` do usuário**, mantendo os caminhos e masters que já funcionam:

```ini
data="D:\Mods\Morrowind-PTBR\Data Files"
content=Morrowind_PTBR.esp
```

O `data` deve vir depois dos diretórios cujos recursos ele substitui; o `content` depois dos três masters. Use seu caminho real. No launcher, selecione **English / Windows-1252** como codificação dos dados; ou mantenha `encoding=win1252` no `openmw.cfg`. A codificação dos arquivos é independente do idioma exibido.

## Completar a interface do OpenMW

O ESP traduz os registros do jogo. Alguns textos pertencem às configurações do motor e exigem estes ajustes adicionais, sem Python. Feche jogo e launcher e faça cópia de `openmw.cfg` e `settings.cfg` antes de editar. No Windows, normalmente ficam em **Documentos → My Games → OpenMW**; perfis personalizados podem usar outro lugar.

### Idioma dos menus modernos

Em **`settings.cfg`**, localize a seção `[General]` e ajuste:

```ini
[General]
preferred locales = pt_BR, en
```

Se desejar legendas, ajuste `subtitles = true` em `[GUI]`. O arquivo `Extras/settings-idioma.cfg` contém esses exemplos. **Mescle as opções nas seções existentes; não substitua todo o seu settings.cfg nem duplique seções.**

### Perguntas de classe, mensagens de nível e calendário

Abra **`Extras/openmw-fallbacks.cfg`** e copie suas linhas para o **`openmw.cfg` do usuário**. Se já existir uma linha `fallback=` com a mesma chave, substitua-a pela traduzida, em vez de deixar duplicatas. Preserve os demais fallbacks e opções. O arquivo é um fragmento; não deve substituir todo o `openmw.cfg`.

São 63 textos configurados separadamente pelo motor. Sem essa etapa, essas mensagens podem continuar em inglês, mesmo com os diálogos e itens já traduzidos.

### Launcher e assistente (opcional)

Com os aplicativos fechados, copie os três arquivos `.qm` de **`Extras/launcher/translations`** para **`resources/translations` da instalação do OpenMW 0.51.0**. Se já houver arquivos com os mesmos nomes, guarde uma cópia deles antes. Isso pode solicitar permissão do Windows se o OpenMW estiver em Program Files. O locale do sistema precisa permitir a seleção de pt-BR.

Esse extra traduz o programa de configuração e o assistente; não é necessário para os textos dentro do jogo. As fontes Qt e a licença GPL acompanham o pacote. Não copie a pasta `fontes-qt` para `Data Files`.

## Atualizar da beta.1 ou do pacote antigo

A beta.1 construía masters localizados numa pasta separada. **Não deixe essa pasta ativa junto com o ESP.** Use `DESINSTALAR.bat` do pacote antigo, ou a [reversão manual](RECONSTRUCAO-PYTHON.md#desativar-e-restaurar), para restaurar o perfil antes de instalar o mod novo. A desativação antiga pode precisar de Python; a instalação nova não precisa.

Confirme que `Morrowind.esm`, `Tribunal.esm` e `Bloodmoon.esm` vêm da sua instalação original. Desative outras traduções e comece um jogo novo. Não há migração validada de saves da beta.1.

## Desativar

Desmarque `Morrowind_PTBR.esp` no launcher e remova o diretório do mod da lista de dados. Retire também as linhas traduzidas de fallback ou restaure seus valores anteriores; reverta as opções de idioma se desejar. Se instalou os `.qm` opcionais, restaure os anteriores ou remova apenas os três adicionados. Os backups preservam o estado anterior.

Não carregue uma partida dependente da tradução esperando migração automática para inglês. Preserve os saves. Só apague a pasta do mod depois de desativá-la.

## Problemas comuns

| Sintoma | Verificação |
|---|---|
| ESP não aparece | Adicionou a pasta que contém o `.esp`, ou apenas a pasta acima dela? |
| Textos do jogo em inglês | Confira marcação do ESP, ordem e conflitos com outras traduções/mods |
| Alguns menus em inglês | Configure `preferred locales`; confira os extras de fallback e launcher |
| Acentos incorretos | Use `encoding=win1252`, não UTF-8, para os dados TES3 |
| Faltam Tribunal/Bloodmoon | Os três masters originais são obrigatórios nesta versão |
| Problema numa missão | Registre NPC, missão, texto, versão e mods na issue; esta beta ainda não tem campanha completa validada |

## Para quem quer reconstruir ou contribuir

Python fica restrito às ferramentas de desenvolvimento e à [opção avançada de reconstrução](RECONSTRUCAO-PYTHON.md). Veja [CONTRIBUTING.md](../CONTRIBUTING.md) para editar textos e gerar um ESP local.
