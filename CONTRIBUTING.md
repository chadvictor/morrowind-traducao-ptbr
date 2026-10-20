# Contribuindo com Morrowind PT-BR

Obrigado por ajudar a melhorar a tradução. Revisão de linguagem, testes de missões, correções de interface e documentação são contribuições úteis, mesmo sem conhecimento de programação.

## Reportar sem editar arquivos

Abra uma [issue](https://github.com/chadvictor/morrowind-traducao-ptbr/issues/new/choose). Informe a versão da tradução e do OpenMW, NPC/local/missão, texto atual, sugestão e o que aconteceu. Uma captura ajuda a localizar a frase. Se houver mods, liste-os. Não publique chaves, logs com informações pessoais, saves privados ou arquivos comerciais.

## Dependências para editar e testar

Para editar pelo GitHub e abrir PR, basta o navegador. Para validar e gerar um mod local, use **Python 3.10+** (biblioteca padrão), os três masters originais compatíveis e OpenMW 0.51.0 para o teste no motor. Qt `lrelease` só é necessário ao editar os catálogos Qt. **Jogadores não precisam dessas ferramentas.**

## Corrigir um texto e abrir PR

1. Faça um fork e crie uma branch, por exemplo `revisao-dialogo-fargoth`.
2. Procure a frase nos arquivos de `traducoes/`, usando a busca do GitHub ou do seu editor. Os catálogos são organizados por `Morrowind`, `Tribunal`, `Bloodmoon` e categoria.
3. Altere somente o valor de **`text`** na entrada encontrada. Cada linha é um objeto JSON completo. Preserve o `id` e todos os campos de identidade.
4. Consulte a [orientação editorial](docs/GUIA-EDITORIAL.md) e confira o contexto no jogo. Se o mesmo registro tiver override em uma expansão, verifique também essa ocorrência.
5. Execute `python scripts/mwbr.py validate` e `python -m unittest discover -s tests -v`.
6. Abra um PR explicando o problema, o motivo da escolha e o que testou. Não inclua masters gerados, backups, bancos de IA ou a pasta local de instalação.

**Não precisa usar IA nem possuir chave de API para contribuir.** A ferramenta que produziu a tradução inicial não faz parte deste repositório.

## Como ler uma entrada

`id` identifica master, índice do registro e índice do campo na versão original suportada. `type`, `field`, `record_id` e, nos diálogos, `topic` ajudam a localizar o contexto. `source_sha256` valida a fonte. `trailing_nuls` preserva o formato binário. **Esses campos não são texto a traduzir.**

O inglês integral não é duplicado nos catálogos do jogo. Quem possui os originais pode consultar uma entrada localmente:

```powershell
python scripts/mwbr.py context "ID_COPIADO_DA_ENTRADA" --game "D:\Jogos\Morrowind"
```

O comando mostra o campo original e a tradução, sem gravar ou enviar dados à rede. Use o ID real do JSONL no lugar do exemplo.

Em JSON, quebras de linha são `\n`, aspas dentro do texto são `\"` e barras invertidas são `\\`. Não divida um objeto em várias linhas no formato JSONL. Arquivos UTF-8; os textos destinados aos masters precisam ser representáveis em Windows-1252. Evite emojis e caracteres fora desse encoding.

## O que não deve ser alterado isoladamente

- **Links `@rótulo#`:** preservam navegação e descoberta de tópicos. Mudar o rótulo exige atualizar o mapa `.top` e verificar as referências.
- **Nomes de tópicos, scripts e títulos de quest:** alterações podem afetar outros masters e agrupar ou separar entradas do diário. Solicite revisão técnica no PR.
- **Scripts:** altere somente o literal exibido; não traduza comandos, IDs, arquivos de áudio, variáveis ou números das opções `Choice`.
- **Marcadores:** preserve tokens como `%PCName`, formatos de mensagens e marcação dos livros. Não substitua um placeholder por uma tradução literal.
- **Identidades/hashes/regras em `compatibilidade/`:** não os atualize só para silenciar um teste que falhou. Explique mudanças estruturais e inclua evidência de teste.

A validação automática é uma primeira barreira. Ela não prova que a frase é boa, que o lore está correto ou que uma missão pode ser concluída.

## Interface e imagens

| Arquivo | Como contribuir |
|---|---|
| `conteudo/data/l10n/*/pt_BR.yaml` | Edite valores; preserve chaves e argumentos ICU |
| `conteudo/fallbacks.json` | Edite valores; não deixe entradas vazias |
| `conteudo/data/mygui/*.layout` | Mudança de XML exige revisão de layout; preserve atributos funcionais |
| `interface/qt/*_pt_BR.ts` | Edite traduções no Qt Linguist ou XML; preserve contexto, disambiguation e plurais |
| `conteudo/data/*.cel`, `.top`, `.mrk` | Mapas técnicos em Windows-1252, separados por TAB; coordenar com os masters |
| `conteudo/data/textures/menu_*.dds` | Imagens autorais do menu; preservar tamanho, transparência e os três estados |

Os arquivos derivados do OpenMW mantêm sua licença original. Não introduza assets de outro mod sem verificar e registrar a licença e os créditos.

## Testar uma alteração no jogo

```powershell
python scripts/build_mod.py --development --game "D:\Jogos\Morrowind" --output "D:\Mods\MWBR-teste-da-minha-correcao"
```

O modo `--development` permite textos editados; continua exigindo originais compatíveis e preservação de identidades. Ele **não substitui validação de links e scripts no motor**. Teste em perfil separado, com backups; adicione a pasta `Data Files` gerada e marque `Morrowind_PTBR.esp` como documentado em [INSTALACAO.md](docs/INSTALACAO.md).

Se alterou `.ts`, recompile os `.qm` em `conteudo/resources/translations/` com Qt `lrelease` antes de gerar o mod, conforme o guia de manutenção. O gerador do mod copia esses catálogos compilados; não invoca Qt automaticamente. Mantenedores devem regenerar os hashes de release somente após os testes descritos em [MANUTENCAO.md](docs/MANUTENCAO.md).

## Licenciamento das contribuições

Ao abrir um PR, envie apenas conteúdo que você tem direito de contribuir. As contribuições originais seguem a MIT; alterações em arquivos derivados do OpenMW seguem a licença desses arquivos. Não reivindicamos direitos sobre o conteúdo original de Morrowind. Veja [LICENSE](LICENSE) e [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
