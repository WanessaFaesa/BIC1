# 🚀 Guia de Publicação — Dashboard COVID-19 ES

> **Objetivo:** Publicar o dashboard Streamlit na internet de forma gratuita usando **GitHub** + **Streamlit Community Cloud**.

---

## 📋 Pré-requisitos

| Item | Como verificar |
|---|---|
| Conta no **GitHub** | [github.com](https://github.com) |
| Conta no **Streamlit Cloud** | [share.streamlit.io](https://share.streamlit.io) (gratuito, login com GitHub) |
| Git instalado | `git --version` no terminal |
| Python 3.9+ | `python --version` no terminal |

---

## Passo 1 — Estrutura dos arquivos do projeto

Certifique-se de que a pasta do projeto contém estes arquivos:

```
covid19_kdd/
├── app.py                ← dashboard principal
├── requirements.txt      ← dependências Python
├── MICRODADOS.csv        ← dataset (NÃO enviar ao GitHub se for grande!)
└── analise_covid19.ipynb ← notebook de análise (opcional)
```

> ⚠️ **IMPORTANTE:** O arquivo `MICRODADOS.csv` pode ser grande demais para o GitHub (limite de 100 MB por arquivo e 1 GB por repositório). Veja a Seção 5 para alternativas.

---

## Passo 2 — Criar o repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Preencha:
   - **Repository name:** `covid19-dashboard-es`
   - **Description:** `Dashboard COVID-19 Espírito Santo — KDD`
   - Marque **Public**
   - ✅ Marque "Add a README file"
3. Clique em **Create repository**

---

## Passo 3 — Enviar os arquivos para o GitHub

Abra o terminal na pasta do projeto (`covid19_kdd/`) e execute:

```bash
# 1. Inicializa o repositório Git local
git init

# 2. Conecta ao repositório remoto criado (substitua SEU_USUARIO pelo seu username)
git remote add origin https://github.com/SEU_USUARIO/covid19-dashboard-es.git

# 3. Cria o arquivo .gitignore para não enviar arquivos desnecessários
echo "MICRODADOS.csv" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".ipynb_checkpoints/" >> .gitignore
echo "*.pyc" >> .gitignore

# 4. Adiciona todos os arquivos ao staging
git add .

# 5. Faz o commit inicial
git commit -m "feat: dashboard COVID-19 ES com Streamlit"

# 6. Envia para o GitHub
git branch -M main
git push -u origin main
```

Confirme no navegador que os arquivos aparecem no repositório.

---

## Passo 4 — Publicar no Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io) e clique em **Sign in with GitHub**
2. Clique em **New app** (botão azul no canto superior direito)
3. Preencha o formulário:

   | Campo | Valor |
   |---|---|
   | **Repository** | `SEU_USUARIO/covid19-dashboard-es` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` |

4. Clique em **Deploy!**
5. Aguarde ~2 minutos — o Streamlit instalará as dependências automaticamente via `requirements.txt`
6. Seu app estará disponível em uma URL do tipo:
   ```
   https://seu-usuario-covid19-dashboard-es-app-XXXXX.streamlit.app
   ```

---

## Passo 5 — Como lidar com o arquivo MICRODADOS.csv

Como o CSV pode ultrapassar o limite do GitHub, existem 3 opções:

### Opção A — Upload direto no Streamlit (recomendado para arquivo ≤ 200 MB)

Adicione um uploader no `app.py` para o usuário carregar o arquivo:

```python
# Substitua o bloco de carregamento no app.py por:
arquivo = st.file_uploader(
    "📂 Faça upload do arquivo MICRODADOS.csv",
    type=["csv"]
)

if arquivo is None:
    st.info("⬆️ Aguardando upload do arquivo MICRODADOS.csv...")
    st.stop()

df = carregar_dados(arquivo)
```

E ajuste a função `carregar_dados` para aceitar `UploadedFile`:

```python
@st.cache_data
def carregar_dados(arquivo) -> pd.DataFrame:
    dados = pd.read_csv(arquivo, sep=';', encoding='latin-1', low_memory=False)
    col_data = next((c for c in dados.columns if 'ata' in c.lower() and 'otifica' in c.lower()), None)
    if col_data:
        dados['data_convertida'] = pd.to_datetime(dados[col_data], errors='coerce', dayfirst=True)
        dados['ano_mes'] = dados['data_convertida'].dt.to_period('M').astype(str)
    return dados
```

### Opção B — Git LFS (Large File Storage)

```bash
git lfs install
git lfs track "*.csv"
git add .gitattributes MICRODADOS.csv
git commit -m "add: dataset via Git LFS"
git push
```

> Requer conta GitHub Pro ou organização para arquivos > 1 GB.

### Opção C — Hospedar o CSV externamente (Google Drive / OneDrive)

Publique o CSV como link direto e carregue via URL no app:

```python
URL_CSV = "https://drive.google.com/uc?id=SEU_FILE_ID"
df = pd.read_csv(URL_CSV, sep=';', encoding='latin-1', low_memory=False)
```

---

## Passo 6 — Atualizar o app após mudanças

Sempre que fizer alterações no código, execute no terminal:

```bash
git add .
git commit -m "fix: descrição da mudança"
git push
```

O Streamlit Cloud detecta automaticamente o push e atualiza o app em ~30 segundos.

---

## Passo 7 — Acessar logs de erro (Troubleshooting)

Se o app der erro após o deploy:

1. No painel do [share.streamlit.io](https://share.streamlit.io), clique no seu app
2. Clique em **⋮ (Menu)** → **Manage app** → **Logs**
3. Leia a mensagem de erro e corrija no código local
4. Faça `git push` para redesplojar

### Erros comuns:

| Erro | Causa | Solução |
|---|---|---|
| `ModuleNotFoundError` | Biblioteca não listada | Adicionar ao `requirements.txt` |
| `FileNotFoundError: MICRODADOS.csv` | CSV não enviado | Usar Opção A (uploader) |
| `UnicodeDecodeError` | Encoding incorreto | Manter `encoding='latin-1'` |
| App travado no carregamento | CSV muito grande | Usar `@st.cache_data` e filtrar colunas |

---

## ✅ Checklist Final

- [ ] `app.py` funcionando localmente com `streamlit run app.py`
- [ ] `requirements.txt` atualizado com todas as dependências
- [ ] Repositório criado no GitHub
- [ ] Arquivos enviados com `git push`
- [ ] App publicado no Streamlit Cloud
- [ ] URL do app anotada e compartilhada

---

> 🎓 **Parabéns!** Seu dashboard COVID-19 ES está publicado e acessível para qualquer pessoa no mundo com o link.  
> 📌 Guarde a URL e compartilhe com professores, colegas e no seu portfólio!
