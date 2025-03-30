# Conectando ao Repositório GitHub

Este guia explica como conectar este projeto ao repositório GitHub: https://github.com/davisxavier1984/FPM

## Configuração inicial (execute apenas uma vez)

1. Abra um terminal na pasta raiz do projeto (`/home/davi/Python-Projetos/SMS/FPM`)

2. Inicialize um repositório Git local (se ainda não existir):
   ```bash
   git init
   ```

3. Adicione o repositório GitHub como remoto:
   ```bash
   git remote add origin https://github.com/davisxavier1984/FPM.git
   ```

4. Verifique se o repositório foi adicionado corretamente:
   ```bash
   git remote -v
   ```

## Configuração de autenticação

### Opção 1: Token de Acesso Pessoal (recomendado)

1. No GitHub, vá para Configurações > Configurações do desenvolvedor > Tokens de acesso pessoal
2. Gere um novo token com as permissões necessárias (repo, workflow)
3. Salve o token em um local seguro
4. Use o token como senha quando solicitado (seu nome de usuário continua o mesmo)

### Opção 2: Chaves SSH

1. Gerar uma chave SSH (caso não tenha):
   ```bash
   ssh-keygen -t ed25519 -C "seu_email@example.com"
   ```

2. Adicionar a chave ao ssh-agent:
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. Adicionar a chave pública ao GitHub:
   - Copie o conteúdo do arquivo `~/.ssh/id_ed25519.pub`
   - Vá para GitHub > Configurações > Chaves SSH > Nova chave SSH

4. Altere a URL do remote para SSH:
   ```bash
   git remote set-url origin git@github.com:davisxavier1984/FPM.git
   ```

## Operações comuns do Git

### Baixar arquivos do repositório remoto

```bash
# Baixar arquivos sem mesclar
git fetch origin

# Baixar e mesclar com seu código atual
git pull origin main
```

### Enviar arquivos para o repositório remoto

```bash
# Adicionar arquivos modificados ao stage
git add .

# Criar um commit com mensagem descritiva
git commit -m "Descrição das alterações"

# Enviar para o GitHub
git push origin main
```

### Configuração de usuário (se necessário)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu_email@example.com"
```

## Dicas úteis

- Para verificar o status dos arquivos:
  ```bash
  git status
  ```

- Para visualizar histórico de commits:
  ```bash
  git log --oneline
  ```

- Para desfazer alterações não commitadas:
  ```bash
  git checkout -- .
  ```

- Para criar uma nova branch:
  ```bash
  git checkout -b nome-da-nova-branch
  ```
