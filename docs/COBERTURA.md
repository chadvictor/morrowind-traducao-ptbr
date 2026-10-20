# Cobertura e estado da tradução

## O que os números significam

O catálogo de trabalho reuniu **52.190 entradas** dos três masters e das interfaces, dividido em **52.380 segmentos**. A aprovação desses segmentos é um estado do processo de tradução e revisão com IA. Não significa revisão humana de todas as frases.

A publicação usa o resultado final da reinserção: **43.694 campos realmente modificados**, separados em arquivos JSONL. Entradas sem alterações, partes de um mesmo script, tabelas de localização e recursos da interface não têm correspondência de um para um com esse total. Os catálogos guardam só alterações. No mod pronto, cada registro sobrescrito inclui também os campos estruturais necessários; os masters do jogador continuam fornecendo o restante do jogo.

| Categoria no patch | Morrowind | Tribunal | Bloodmoon |
|---|---:|---:|---:|
| Diálogos | 19.348 | 3.930 | 4.040 |
| Journal | 1.217 | 421 | 2.393 |
| Livros | 532 | 48 | 42 |
| Nomes e descrições | 5.745 | 721 | 877 |
| Scripts com alterações | 1.261 | 318 | 182 |
| Tópicos modificados | 1.298 | 213 | 187 |
| Interface GMST | 876 | 0 | 45 |

Essas contagens incluem overrides das expansões. Não representam uma contagem de falas únicas ou de missões.

Além dos campos acima, o pacote cobre mapas para **1.423 nomes de locais**, um conjunto coordenado de **2.098 tópicos**, **455 valores YAML**, **23 valores MyGUI**, **529 mensagens Qt** e **63 fallbacks**. Os botões principais possuem **21 imagens novas**. Os números detalhados estão em [cobertura.json](cobertura.json).

## Evidência técnica disponível

Na instalação de origem, usando OpenMW 0.51.0:

- Foram conferidas **3.223 condições no motor**, incluindo registros, recursos e carregamento do jogador em Seyda Neen.
- **15.570 de 15.570 scripts de diálogo** compilaram.
- **1.206 de 1.207 scripts gerais** compilaram. A falha do script `Museum` foi reproduzida com os masters originais; não foi introduzida pela tradução.
- O menu principal foi renderizado e o perfil instalado passou pelo teste de abertura.
- Os masters originais mantiveram os hashes.

O instalador público reconstrói os masters com os mesmos hashes do pacote usado nesses testes. Também é testado com entradas sintéticas para detectar campos truncados, fontes erradas e falhas de reversão. Os testes automáticos do GitHub não incluem os arquivos comerciais do jogo nem executam uma campanha.

O pacote reconstruído pelo instalador público também foi ativado em um perfil separado e executado no motor: as 3.223 conferências e a compilação dos 15.570 scripts de diálogo passaram novamente. A desativação restaurou o arquivo de configuração de teste exatamente; uma fonte incompatível foi recusada antes da criação do destino.

## Limitações visíveis

- Não houve playthrough completo, revisão humana integral, teste de todos os finais ou validação de todos os mods.
- Vozes, filmes e demais imagens com texto continuam no idioma original. Legendas existentes no catálogo podem ser traduzidas; não foram criadas legendas novas para todo áudio ou vídeo.
- O sistema de links preserva as descobertas derivadas do texto original. **9.508 respostas/entradas têm rótulos adicionais de tópicos**, normalmente entre colchetes, quando não foi encontrado um encaixe literal na tradução. Esse recurso prioriza o funcionamento; pode precisar de refinamento editorial em contexto.
- Tópicos armazenados em saves anteriores podem permanecer em inglês. Recomendamos jogo novo.
- A renomeação coordenada dos tópicos e dos comandos `AddTopic` pode conflitar com mods em inglês. Não há promessa de compatibilidade automática.
- Nomes próprios e termos de lore podem permanecer no original por escolha editorial; isso não significa necessariamente uma tradução ausente.

## Como ajudar na próxima versão

Revise diálogos no contexto de quem fala, teste missões do início ao fim, confira links e títulos do diário, reporte cortes de texto e proponha um vocabulário consistente. Registre o nome do NPC, local, missão, versão e uma captura quando possível. Evite declarar “tudo funciona” com base somente em o jogo abrir.

## Mod convencional da beta.2

O ESP de 16.122.012 bytes foi gerado dos mesmos catálogos. Os três masters originais mais o plugin produziram, na comparação estrutural, os mesmos registros efetivos e os mesmos **2.884 grupos de diálogo / 31.822 INFOs** dos masters localizados. A ordenação de respostas, filtros, IDs e scripts foi comparada; somente os ponteiros PNAM/NNAM foram normalizados para representar a ordem consolidada.

Em perfil de teste isolado, com a pasta dos masters originais e o novo ESP, passaram novamente **3.223 verificações** e a compilação de **15.570/15.570 scripts de diálogo**. O erro preexistente `Museum` continua sendo a única falha entre 1.207 scripts gerais. O parser independente `esmtool` também leu o plugin. Isso não substitui testar missões do início ao fim.

A interface completa nesse teste usou `preferred locales = pt_BR, en` e o fragmento de fallbacks. Na instalação do jogador, esses são ajustes adicionais descritos no guia. Os `.qm` do launcher são opcionais e separados.
