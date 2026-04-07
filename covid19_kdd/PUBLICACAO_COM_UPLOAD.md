# 🚀 Guia: Publicar Dashboard COVID-19 com Upload de Arquivo

> **Objetivo:** Colocar seu dashboard no ar em um site gratuito onde os usuários podem fazer upload do arquivo `MICRODADOS.csv` e gerar gráficos.

---

## 📊 Resumo da Solução

✅ **Plataforma:** Streamlit Community Cloud (gratuita)  
✅ **Hospedagem:** GitHub (gratuito)  
✅ **Upload:** Usuários podem fazer upload do arquivo diretamente no site  
✅ **Custo:** $0,00

---

## 🛠️ Passo 1 — Preparar os arquivos

Certifique-se de que sua pasta `covid19_kdd/` tenha:

```
covid19_kdd/
├── app.py                    ← ✨ MODIFICADO (com suporte a upload)
├── requirements.txt          ← dependências (sem mudanças)
├── MICRODADOS.csv           ← opcional (pode ficar de fora no GitHub)
└── GUIA_PUBLICACAO.md       ← referência
```

**Importante:** O novo `app.py` agora permite:
- ✅ Usar arquivo `MICRODADOS.csv` local (se existir)
- ✅ Fazer upload de novo `MICRODADOS.csv` pelo site
- ✅ Gerar gráficos com qualquer arquivo compatível

---

## 🐙 Passo 2 — Criar repositório no GitHub e enviar código

### 2.1 Criar conta e repositório

1. Acesse [github.com/new](https://github.com/new)
2. Preencha:
   - **Repository name:** `covid19-dashboard-es`
   - **Description:** `Dashboard COVID-19 ES — Upload de microdados com Streamlit`
   - Marque **Public**
   - ✅ Marque "Add a README file"
3. Clique em **Create repository**

### 2.2 Enviar seus arquivos (use Git ou GitHub Desktop)

**Opção A: Via terminal (recomendado)**

```bash
cd covid19_kdd

# Inicializar repositório Git
git init

# Adicionar remoto (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/covid19-dashboard-es.git

# Criar arquivo .gitignore para não enviar dados grandes
echo "MICRODADOS.csv" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".ipynb_checkpoints/" >> .gitignore
echo "*.pyc" >> .gitignore

# Enviar arquivo
git add .
git commit -m "feat: dashboard COVID-19 com upload de MICRODADOS"
git branch -M main
git push -u origin main
```

**Opção B: Via GitHub Desktop**
- Faça download: [desktop.github.com](https://desktop.github.com)
- Clique em "Add" → "Create New Repository" → selecione a pasta `covid19_kdd`
- Publish repository como "covid19-dashboard-es"

---

## ☁️ Passo 3 — Publicar no Streamlit Community Cloud (2 minutos)

### 3.1 Acessar Streamlit Cloud

1. Vá para [share.streamlit.io](https://share.streamlit.io)
2. Clique em **Sign in with GitHub** (use sua conta GitHub)

### 3.2 Criar app

1. Clique em **New app** (botão azul, canto superior direito)
2. Preencha:
   | Campo | Valor |
   |-------|-------|
   | **Repository** | `SEU_USUARIO/covid19-dashboard-es` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` |
3. Clique em **Deploy!**
4. ⏳ Aguarde 2-3 minutos — o Streamlit instala tudo automaticamente
5. ✅ Seu app estará disponível em:
   ```
   https://seu-usuario-covid19-dashboard-es.streamlit.app
   ```

---

## 📋 Passo 4 — Usar o app publicado

### Para você (local):
```bash
streamlit run app.py
```

### Para seus usuários (no site):
1. Visitem a URL gerada
2. Clicam em "⬆️ Fazer upload de novo arquivo"
3. Selecionam o arquivo `MICRODADOS.csv` deles
4. Veem os gráficos gerados automaticamente! 📊

---

## 🔄 Passo 5 — Atualizar o app

Se fizer mudanças no código:

```bash
git add app.py
git commit -m "fix: melhorias no dashboard"
git push
```

O Streamlit Community Cloud **detecta automaticamente** as mudanças no GitHub e faz redeploy em ~1 minuto.

---

## 📁 Alternativa: Se o MICRODADOS.csv for muito grande (>100 MB)

Se seu arquivo for grande demais para GitHub, você tem 2 opções:

### Opção 1: Deixar apenas no servidor (recomendado)

Não envie o `MICRODADOS.csv` ao GitHub:
- Já está no `.gitignore` ✅
- Usuários farão upload do arquivo deles pelo site
- Seu app sempre usa a versão local se o arquivo existir

### Opção 2: Usar serviço externo

Use plataformas como AWS S3, Google Cloud Storage ou Hugging Face Datasets para hospedar o arquivo.

---

## 🎯 Checklist Final

- [ ] Arquivo `app.py` modificado com suporte a upload
- [ ] `requirements.txt` contém: `streamlit`, `pandas`, `matplotlib`
- [ ] `.gitignore` criado (não envia `MICRODADOS.csv`)
- [ ] Repositório criado no GitHub
- [ ] Arquivos (`app.py`, `requirements.txt`, etc) enviados ao GitHub
- [ ] App publicado no Streamlit Community Cloud
- [ ] URL compartilhada com usuários ✨

---

## 💡 Dicas

| Dúvida | Resposta |
|--------|----------|
| **Posso alterar a senha de acesso?** | Streamlit Community Cloud ésem autenticação. Se precisar, use `streamlit_authenticator` (avançado) |
| **Qual o limite de tamanho de upload?** | Usuários podem upload até ~200 MB por vez |
| **Como recebo o `MICRODADOS.csv` dos usuários?** | Os dados são processados no servidor, mas não são salvos. Você pode adicionar código para salvar no banco de dados |
| **Preciso de cartão de crédito?** | Não! Streamlit Community Cloud é 100% gratuito |
| **Qual é o SLA (uptime)?** | ~99% para plano gratuito. Streamlit fornece upgrades pagos se precisar |

---

## 🆘 Troubleshooting

### ❌ "Arquivo não encontrado"
→ Verifique se o `requirements.txt` tem todas as dependências

### ❌ "erro ao fazer upload"
→ Tente um arquivo menor ou verifique o encoding (deve ser `latin-1`)

### ❌ "App não aparece após deploy"
→ Aguarde 3-5 minutos e recarregue a página

### ❌ "GitHub não reconhece minhas credenciais"
→ Use token pessoal em vez de senha: [github.com/settings/tokens](https://github.com/settings/tokens)

---

**Pronto!** 🎉 Seu dashboard está no ar e acessível para qualquer pessoa fazer upload e gerar gráficos! 📊
