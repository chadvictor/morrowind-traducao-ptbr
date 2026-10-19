# Compatibilidade

**Alvo desta beta:** Windows 10/11, OpenMW 0.51.0 e Morrowind GOTY em inglês com Tribunal e Bloodmoon, sem outros plugins no perfil selecionado.

Os arquivos reconhecidos são da edição Steam testada. A compra do jogo em outra loja não é um problema por si só: o que determina a compatibilidade técnica são os bytes originais. Ainda não validamos outras edições ou versões. O instalador recusa hashes diferentes antes de escrever os masters traduzidos.

| Arquivo original | SHA-256 |
|---|---|
| `Morrowind.esm` | `5c3c8c2cbd20e25901b59b3ece33d36b7ef0e3d60ad8d11828bcc61a5ead1647` |
| `Tribunal.esm` | `2ace511f23cc2a9ddd5f3aa59c7919789b9378cf4b17c8ae3375dd6b782f3f2b` |
| `Bloodmoon.esm` | `bd27090d0e6ad4c1bf1abc83f1a2dac56fcc82cae7bfe8263c413fb301801357` |

No PowerShell, confira um arquivo com `Get-FileHash -Algorithm SHA256 "D:\Jogos\Morrowind\Data Files\Morrowind.esm"`.

Os recursos MyGUI e a fonte usada no menu também são conferidos. As fontes OpenMW usadas na análise correspondem à revisão `f4bec41444214a7903bebd178389ca22ca13f646`. Todos os hashes exigidos estão em [manifesto.json](../compatibilidade/manifesto.json).

## Por que OpenMW

A tradução altera fontes de scripts recompiladas pelo OpenMW, nomes de tópicos e comandos associados, mantendo outros identificadores e os dados não textuais. Não recompila o bytecode para o executável Bethesda. **Não instale este pacote como se fosse compatível com Morrowind.exe, MWSE ou OpenMW de outra versão.**

Os nomes internos de células são preservados; os rótulos visíveis vêm das tabelas `.cel`. Os arquivos `.top` e `.mrk` cooperam com links explícitos para manter o acesso aos tópicos. Todos esses componentes devem ser instalados em conjunto.

## Saves, mods e atualizações

- Use um jogo novo. Não há migração validada dos tópicos de saves em inglês.
- Esta primeira release exige um perfil sem outros plugins, com Morrowind → Tribunal → Bloodmoon. O instalador não reorganiza seus mods.
- Mods com diálogo, journal, `AddTopic` ou overrides dos mesmos registros precisam de avaliação própria. Mesmo mods sem ESP podem sobrescrever interface e mapas.
- Atualizar OpenMW pode exigir nova validação dos recursos e catálogos Qt. Preserve backups e não edite o manifesto para ignorar incompatibilidades.
- Os scripts de montagem usam Python padrão e podem ser adaptados a outros sistemas, mas o fluxo de instalação e o teste de execução desta release são para Windows.

Para solicitar suporte a uma edição, abra uma issue com versão/loja e os três hashes. **Não anexe masters, arquivos BSA ou executáveis do jogo.**
