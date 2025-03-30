# Resolver erro de push Git

Para resolver o erro `src refspec main does not match any`, siga estes passos:

## 1. Verificar branches existentes

```bash
git branch
```

Se não aparecer nenhuma branch ou não existir uma branch "main", você precisa criar seu primeiro commit.

## 2. Adicionar arquivos ao Git

```bash
# Adicionar todos os arquivos
git add .
```

## 3. Criar o primeiro commit

```bash
git commit -m "Commit inicial"
```

## 4. Criar e mudar para a branch "main" (se necessário)

Se sua branch principal for "master" (padrão antigo do Git):

```bash
# Renomear master para main (se existir)
git branch -m master main
```

Ou se não tiver nenhuma branch ainda:

```bash
# Criar branch main
git checkout -b main
```

## 5. Tentar o push novamente

```bash
git push -u origin main
```

O parâmetro `-u` configura o upstream, assim nas próximas vezes você pode usar apenas `git push`.

## Resolução de problemas comuns

### Se receber erro de autenticação:
- Digite seu usuário do GitHub quando solicitado
- Use um token de acesso pessoal como senha (não sua senha do GitHub)

### Se o repositório remoto já tiver conteúdo:
```bash
# Primeiro, puxe as alterações remotas
git pull origin main --allow-unrelated-histories
# Resolva conflitos se necessário, depois faça o push
git push origin main
```
