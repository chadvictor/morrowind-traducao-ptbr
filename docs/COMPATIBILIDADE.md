# Compatibilidade

**Alvo desta beta:** Windows 10/11, OpenMW 0.51.0 e Morrowind GOTY em inglês com Tribunal e Bloodmoon, com os três masters originais e `Morrowind_PTBR.esp`, inicialmente sem outros mods no perfil.

Os arquivos reconhecidos são da edição Steam testada. A compra do jogo em outra loja não é um problema por si só: o que determina a compatibilidade técnica são os bytes originais. Ainda não validamos outras edições ou versões. Os geradores Python recusam hashes diferentes. O ESP pronto não executa verificação de hashes: use a edição validada; não force dependências ausentes ou presuma suporte a outra edição.

| Arquivo original | SHA-256 |
|---|---|
| `Morrowind.esm` | `5c3c8c2cbd20e25901b59b3ece33d36b7ef0e3d60ad8d11828bcc61a5ead1647` |
| `Tribunal.esm` | `2ace511f23cc2a9ddd5f3aa59c7919789b9378cf4b17c8ae3375dd6b782f3f2b` |
| `Bloodmoon.esm` | `bd27090d0e6ad4c1bf1abc83f1a2dac56fcc82cae7bfe8263c413fb301801357` |

No PowerShell, confira um arquivo com `Get-FileHash -Algorithm SHA256 "D:\Jogos\Morrowind\Data Files\Morrowind.esm"`.

A reconstrução Python verifica os recursos MyGUI; os recursos da release foram conferidos no OpenMW indicado. As fontes OpenMW usadas na análise correspondem à revisão `f4bec41444214a7903bebd178389ca22ca13f646`. Todos os hashes exigidos estão em [manifesto.json](../compatibilidade/manifesto.json).

## Por que OpenMW

A tradução altera fontes de scripts recompiladas pelo OpenMW, nomes de tópicos e comandos associados, mantendo outros identificadores e os dados não textuais. Não recompila o bytecode para o executável Bethesda. **Não instale este pacote como se fosse compatível com Morrowind.exe, MWSE ou OpenMW de outra versão.**

Os nomes internos de células são preservados; os rótulos visíveis vêm das tabelas `.cel`. Os arquivos `.top` e `.mrk` cooperam com links explícitos para manter o acesso aos tópicos. Todos esses componentes devem ser instalados em conjunto.

## Saves, mods e atualizações

- Use um jogo novo. Não há migração validada dos tópicos de saves em inglês.
- A ordem validada é Morrowind → Tribunal → Bloodmoon → Morrowind_PTBR.esp, sem outros mods. O plugin não reorganiza a lista por você.
- Mods com diálogo, journal, `AddTopic` ou overrides dos mesmos registros precisam de avaliação própria. Mesmo mods sem ESP podem sobrescrever interface e mapas.
- Atualizar OpenMW pode exigir nova validação dos recursos e catálogos Qt. Preserve backups e não edite o manifesto para ignorar incompatibilidades.
- O mod pronto não exige Python. Seu teste de execução foi no Windows; a CI em Linux testa apenas as ferramentas, sem executar o jogo.

Para solicitar suporte a uma edição, abra uma issue com versão/loja e os três hashes. **Não anexe masters, arquivos BSA ou executáveis do jogo.**

O plugin contém exclusões de DIAL seguidas dos grupos reconstruídos, necessárias à renomeação de tópicos. Não remova essas exclusões com ferramentas de limpeza automática: elas evitam tópicos antigos e respostas misturadas. Filtros, scripts e ordem final das respostas são verificados pelo exportador.
