# 🦠 Dashboard COVID-19 — Espírito Santo

> **Análise exploratória interativa dos microdados de notificações de COVID-19**  
> Projeto KDD com visualizações em tempo real

---

## 🎯 Sobre o Projeto

Dashboard desenvolvido em **Python + Streamlit** para análise de dados de COVID-19 do estado do Espírito Santo (ES).

**Funcionalidades principais:**
- 📊 Visualizações de notificações por município, classificação e sexo
- 📈 Evolução temporal mensal de casos
- 💀 Cálculo de taxa de letalidade
- 🔍 Filtros interativos por município, classificação e sexo
- ⬆️ Upload de arquivo CSV (até 2GB com amostragem)
- 📱 Interface responsiva e intuitiva

---

## 🌐 Acesso Online

**🔗 Link do Dashboard:** [https://bic1covid19.streamlit.app/](https://bic1covid19.streamlit.app/)

Nenhuma instalação necessária! Faça upload do seu `MICRODADOS.csv` e comece a análise.

---

## 📋 Pré-requisitos

| Item | Versão |
|------|--------|
| Python | 3.9+ |
| Streamlit | 1.32.0+ |
| Pandas | 2.0.0+ |
| Matplotlib | 3.7.0+ |

---

## 🚀 Como Usar (Online)

1. Visite: **[bic1covid19.streamlit.app](https://bic1covid19.streamlit.app/)**
2. Clique em **"Selecione um arquivo CSV"**
3. Escolha seu `MICRODADOS.csv` (com colunas: `Municipio`, `Classificacao`, `Sexo`, `Evolucao`)
4. Clique em **"▶️ Processar arquivo"**
5. ✨ Explore os gráficos e filtros!

---

## 💻 Como Rodar Localmente

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/WanessaFaesa/BIC1.git
cd BIC1
```

### 2️⃣ Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute o app

```bash
streamlit run app.py
```

O app abrirá em: `http://localhost:8501`

---

## 📁 Estrutura do Projeto

```
covid19_kdd/
├── app.py                      # 🎯 Aplicação principal Streamlit
├── requirements.txt            # 📦 Dependências Python
├── MICRODADOS.csv             # 📊 Dataset (não incluído, faça upload)
├── analise_covid19.ipynb      # 📓 Notebook de análise
├── GUIA_PUBLICACAO.md         # 📝 Guia de publicação
├── PUBLICACAO_COM_UPLOAD.md   # 📝 Guia com suporte a upload
└── README.md                   # 📋 Este arquivo
```

---

## 📊 Formato do Arquivo CSV

O `MICRODADOS.csv` deve conter as colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `data_notificacao` | Data da notificação | 2020-01-15 |
| `Municipio` | Município ES | Vitória |
| `Classificacao` | Confirmado/Suspeito/Descartado | Confirmado |
| `Sexo` | M/F/Indefinido | M |
| `Evolucao` | Óbito/Recuperado/Internado | Recuperado |

**Separador:** `;` (ponto-e-vírgula)  
**Encoding:** `latin-1`

---

## 🛠️ Tecnologias

- **[Streamlit](https://streamlit.io/)** — Framework web para data apps
- **[Pandas](https://pandas.pydata.org/)** — Manipulação de dados
- **[Matplotlib](https://matplotlib.org/)** — Visualizações
- **[GitHub](https://github.com/)** — Versionamento
- **[Streamlit Cloud](https://streamlit.io/cloud)** — Deploy gratuito

---

## ⚡ Performance

- ✅ Processamento em **chunks** para arquivos >1GB
- ✅ Cache automático para gráficos
- ✅ Amostragem opcional (~500k linhas)
- ✅ Carregamento: ~10-30 segundos (arquivo 1.8GB)

---

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| "Arquivo muito grande" | Use amostra (checkbox) ou comprima em ZIP |
| "Coluna não encontrada" | Verifique nomes/encoding do CSV |
| "Erro de memória" | Divida arquivo em partes ou use moins % de amostra |

---

## 📝 Licença

Este projeto é de código aberto. Usado para fins educacionais — Projeto KDD.

---

## 👤 Autor

**Wanessa Faesa** — Análise de Dados & Desenvolvimento

---

## 🤝 Contribuições

Melhorias são bem-vindas! Faça um fork, crie uma branch e envie um Pull Request.

```bash
git checkout -b minha-melhoria
git commit -m "feat: adiciona nova funcionalidade"
git push origin minha-melhoria
```
