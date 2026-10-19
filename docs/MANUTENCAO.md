# Manutenção e fechamento de release

Este repositório mantém somente a tradução, os recursos derivados necessários e os scripts offline. Não acrescente a ferramenta privada de IA, chaves, bancos de trabalho ou masters completos.

## Revisar uma contribuição

1. Confira o contexto linguístico e quais masters/overrides estão envolvidos.
2. Rode `python scripts/mwbr.py validate` e os testes de `tests/`.
3. Mudanças de links, tópicos e scripts exigem revisão técnica coordenada; nunca atualize regras de compatibilidade apenas para esconder uma falha.
4. Monte em uma pasta nova com `--development`, usando os originais suportados.
5. Use um perfil de teste separado. Confira o conteúdo ativo e teste a frase, a missão e os links afetados. Para scripts, compare erros de compilação com os originais.
6. Registre o que foi testado e o que permanece sem teste na descrição do PR.

## Recursos Qt

As fontes `.ts` estão em `interface/qt/`. Os `.qm` distribuídos estão em `conteudo/resources/translations/`. Após editar uma fonte, compile cada catálogo com um `lrelease` Qt compatível, por exemplo:

```powershell
lrelease interface/qt/launcher_pt_BR.ts -qm conteudo/resources/translations/launcher_pt_BR.qm
lrelease interface/qt/wizard_pt_BR.ts -qm conteudo/resources/translations/wizard_pt_BR.qm
lrelease interface/qt/components_pt_BR.ts -qm conteudo/resources/translations/components_pt_BR.qm
```

Confira contexto, plurais, placeholders e carregamento real. A tradução do launcher depende também do locale do sistema. Mantenha as fontes e licença GPL junto dos binários compilados.

## Fechar uma nova versão

O manifesto preserva os hashes da beta inicial. Uma alteração de catálogo passa a aparecer como `versão intacta: False`; isso é esperado durante contribuições. O empacotador recusa publicar uma mistura de fontes alteradas com hashes antigos.

Depois da revisão e dos testes no motor, o mantenedor precisa atualizar **conscientemente**:

- Número da versão em `compatibilidade/manifesto.json`, documentação e notas da release.
- Hashes dos JSONL, recursos e fontes Qt modificados.
- Hashes de saída dos três masters reconstruídos com essa nova versão.
- Regras textuais somente se uma mudança estrutural coordenada tiver sido aprovada e testada.
- Evidências de teste e limitações conhecidas.

Nunca substitua os hashes **de origem** pelos de um master traduzido. Uma nova edição do jogo exige um mapeamento revisado das identidades; os índices binários não são universais entre edições.

## Gerar o ZIP

```powershell
python scripts/mwbr.py validate
python -m unittest discover -s tests -v
python scripts/release.py --check-only
python scripts/release.py
```

O empacotador cria em `dist/` o ZIP completo e `SHA256SUMS.txt`. O mesmo ZIP contém fontes de contribuição e instalador. O diretório `dist/` não entra no Git; os dois arquivos são anexados à release.

O inventário público recusa extensões comerciais/bancos comuns, caminhos pessoais e padrões reconhecidos de credenciais. Isso complementa a revisão manual, não substitui uma auditoria universal de dados sensíveis. Inspecione o ZIP antes do upload.

## Publicar no GitHub

Somente um mantenedor com autorização deve publicar. Faça commit, envie a branch e crie uma tag e release de pré-lançamento apontando para o commit testado. Use as notas da versão em `docs/RELEASE-0.1.0-beta.1.md` como ponto de partida.

O CI roda apenas testes estruturais e sintéticos. Ele não contém nem baixa o jogo. Não use um selo verde do CI como promessa de campanha completa ou revisão humana integral.
