<div align="center">

![Morrowind em português do Brasil — tradução gratuita para OpenMW](docs/imagens/capa.svg)

# Morrowind em português do Brasil

### Vvardenfell tem muita história para contar. Agora, em português.

**Morrowind + Tribunal + Bloodmoon · OpenMW 0.51.0 · Gratuito · Beta comunitária**

[![Baixar tradução](https://img.shields.io/badge/BAIXAR-TRADU%C3%87%C3%83O_PT--BR-c5a87b?style=for-the-badge)](https://github.com/chadvictor/morrowind-traducao-ptbr/releases)
[![Contribuir](https://img.shields.io/badge/CONTRIBUIR-REVIS%C3%83O_E_TESTES-56715c?style=for-the-badge)](CONTRIBUTING.md)

[Instalação](docs/INSTALACAO.md) · [O que está traduzido](docs/COBERTURA.md) · [Compatibilidade](docs/COMPATIBILIDADE.md) · [Reportar problema](https://github.com/chadvictor/morrowind-traducao-ptbr/issues/new/choose)

</div>

Uma tradução de fã para jogar **The Elder Scrolls III: Morrowind** em português brasileiro pelo **OpenMW**. O projeto reúne os textos traduzidos, os recursos de interface e um instalador offline, com arquivos abertos para revisão e contribuição da comunidade.

**Primeira versão pública: `0.1.0-beta.1`.** A tradução inicial foi produzida com auxílio de IA, revisão automatizada, decisões editoriais pontuais e validação técnica. **Ainda não houve revisão humana integral nem teste completo da campanha.** Precisamos de jogadores para aperfeiçoar a linguagem e conferir missões em contexto.

## Quero jogar

Você precisa de:

- **Morrowind GOTY em inglês**, com **Tribunal e Bloodmoon**, instalado e comprado por você. Esta beta reconhece os hashes da edição Steam usada nos testes; outras edições ainda precisam de validação.
- **OpenMW 0.51.0**, configurado e funcionando com o jogo original, em um perfil sem outros mods.
- **Windows 10/11** e **Python 3.10 ou superior**, com Tcl/Tk (incluído no instalador padrão do [python.org](https://www.python.org/downloads/windows/)).
- Uma pasta gravável fora de `Program Files` para guardar a tradução. **Não precisa de conta, chave de API, OpenRouter ou pagamento.**

1. Abra [Releases](https://github.com/chadvictor/morrowind-traducao-ptbr/releases) e baixe **`morrowind-ptbr-openmw-0.1.0-beta.1.zip`**. Escolha esse arquivo; ele é o pacote de instalação da versão.
2. Extraia o ZIP inteiro para uma pasta. Feche o OpenMW e seu launcher.
3. Execute **`INSTALAR.bat`**. Se faltar Python, instale-o com a opção **Add python.exe to PATH** e execute novamente.
4. Selecione as quatro pastas solicitadas: **Morrowind**, **OpenMW**, **perfil com `openmw.cfg`** e **local onde ficará a tradução**.
5. Ao receber a confirmação de instalação, abra o OpenMW pelo seu atalho habitual ou pela integração que você já usa na Steam. **Comece um jogo novo.**

O instalador confere os originais, monta cópias traduzidas em uma pasta separada e cria backup antes de ativar a tradução. **Não substitui os arquivos originais, não altera saves e não muda suas opções de inicialização da Steam.** Não mova a pasta instalada depois da ativação.

Para desativar, execute **`DESINSTALAR.bat`** e selecione o mesmo perfil. Se você tiver alterado a configuração depois da instalação, o programa preserva suas mudanças e orienta a [reversão manual](docs/INSTALACAO.md#desativar-e-restaurar).

> **Leia antes de instalar:** esta beta usa mudanças coordenadas de tópicos de diálogo e scripts. Saves antigos e mods em inglês podem conflitar. O executável original `Morrowind.exe`, MWSE e outras versões do OpenMW **não são alvos validados**. [Detalhes de compatibilidade →](docs/COMPATIBILIDADE.md)

## O que está traduzido

| Área | Nesta beta |
|---|---|
| Diálogos e tópicos | Textos extraídos dos três masters; links de diálogo preservados pelo pacote |
| Missões e diário | Entradas de journal e títulos de missões |
| Livros e descrições | Conteúdo textual extraído e marcação preservada |
| Mundo e inventário | Nomes exibidos de locais, itens, magias, criaturas, personagens e outros registros do catálogo |
| Interface | Mensagens, menus textuais, calendário, perguntas da criação de personagem e recursos OpenMW |
| Launcher e assistente | Catálogos Qt em pt-BR; a seleção de idioma também depende do idioma do sistema |
| Botões do menu principal | 21 imagens tipográficas novas, nos estados normal, selecionado e pressionado |
| Vozes, filmes e demais imagens | **Não traduzidos**; sem dublagem, legendagem nova de vídeos ou tradução de todos os textos em texturas |

O trabalho de origem abrangeu **52.190 entradas**, divididas em **52.380 segmentos aprovados no processo de tradução**. Esses números descrevem o catálogo processado; não significam que todas as superfícies do jogo foram traduzidas ou que cada frase recebeu revisão humana.

O repositório distribui **43.694 campos modificados** dos masters, além dos mapas e recursos de interface. Campos inalterados são reutilizados da instalação original. Uma entrada do catálogo de trabalho não corresponde necessariamente a um campo final do patch. [Cobertura e limitações →](docs/COBERTURA.md)

<details>
<summary>Prévia dos botões traduzidos</summary>

![Botões Voltar, Novo Jogo, Salvar Jogo, Carregar Jogo, Opções, Créditos e Sair do Jogo nos três estados](docs/imagens/menu-ptbr.png)

Prévia das imagens geradas para o menu; não é uma captura de uma campanha jogada.

</details>

## Ajude a melhorar

**Você pode contribuir sem programar.** Encontrou uma frase estranha, termo inconsistente, problema com acentos ou missão que não avança? Abra uma issue com o texto, o contexto e, se possível, uma captura da tela.

Para corrigir diretamente, edite o campo `text` nos catálogos em `traducoes/`, rode a validação e abra um pull request. O [guia de contribuição](CONTRIBUTING.md) explica como localizar a frase, consultar o original da sua instalação, testar uma alteração e preservar os marcadores usados pelo jogo.

Prioridades: revisão linguística em contexto, padronização de termos, testes de missões, legibilidade da interface e documentação de novas edições compatíveis. Sugestões são bem-vindas; não há promessa de prazo de resposta.

## Organização do repositório

```text
traducoes/          # Campos editáveis, separados por master e categoria
conteudo/          # Mapas de localização, interface e imagens traduzidas
interface/qt/      # Fontes editáveis dos catálogos Qt (.ts)
compatibilidade/   # Hashes, identidades e regras estruturais
scripts/           # Montagem offline, instalação, validação e empacotamento
tests/             # Testes do instalador e da preservação de dados
docs/              # Instalação, cobertura, compatibilidade e manutenção
.github/           # Validação automática, modelos de issues e de PR
LICENSES/          # Licenças dos componentes de terceiros
```

**Este repositório não contém a ferramenta privada de tradução por IA**, prompts, clientes de API, chaves, checkpoints financeiros, bancos de trabalho ou executáveis comerciais. Os scripts publicados servem exclusivamente para aplicar, validar e distribuir os arquivos da tradução.

## Licença e créditos

O código original de instalação, documentação e contribuições autorais deste projeto são disponibilizados sob a [licença MIT](LICENSE), na extensão dos direitos dos colaboradores. Os arquivos derivados do OpenMW mantêm a licença GPL-3.0; os avisos e atribuições estão em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

**A MIT não licencia Morrowind, sua história, seus personagens, marcas ou outros conteúdos da Bethesda.** Este é um projeto de fãs independente, não oficial e sem afiliação com Bethesda ou com a equipe do OpenMW. É necessário possuir o jogo original.

Projeto mantido por [chadvictor](https://github.com/chadvictor), com espaço aberto para os créditos de futuras contribuições. [Créditos e origem do trabalho →](docs/CREDITOS.md)
