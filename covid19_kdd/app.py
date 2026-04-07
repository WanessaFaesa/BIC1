"""
=============================================================
  Dashboard COVID-19 - Espírito Santo
  Desenvolvido com Streamlit
=============================================================
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19 ES — Dashboard",
    page_icon="🦠",
    layout="wide"
)

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
st.title("🦠 Dashboard COVID-19 — Espírito Santo")
st.markdown("""
> **Projeto KDD** | Análise exploratória dos microdados de notificações de COVID-19.  
> Fonte: Secretaria Estadual de Saúde do ES — `MICRODADOS.csv`
""")
st.divider()

# ─────────────────────────────────────────────
# CARREGAMENTO DOS DADOS (cache para performance)
# ─────────────────────────────────────────────
@st.cache_data
def carregar_dados(caminho_ou_buffer, nome_arquivo="arquivo") -> pd.DataFrame:
    """Lê o CSV e faz conversões básicas."""
    dados = pd.read_csv(caminho_ou_buffer, sep=';', encoding='latin-1', low_memory=False)

    # Tenta converter data de notificação
    col_data = next((c for c in dados.columns if 'ata' in c.lower() and 'otifica' in c.lower()), None)
    if col_data:
        dados['data_convertida'] = pd.to_datetime(dados[col_data], errors='coerce', dayfirst=True)
        dados['ano_mes'] = dados['data_convertida'].dt.to_period('M').astype(str)

    return dados

# ─────────────────────────────────────────────
# SEÇÃO DE UPLOAD E CARREGAMENTO
# ─────────────────────────────────────────────
import os

CAMINHO_CSV = 'MICRODADOS.csv'
arquivo_local_existe = os.path.exists(CAMINHO_CSV)

st.subheader("📥 Carregue ou use dados locais")

if arquivo_local_existe:
    opcao_dados = st.radio(
        "Escolha a fonte de dados:",
        ["📁 Usar arquivo local (MICRODADOS.csv)", "⬆️ Fazer upload de novo arquivo"],
        label_visibility="collapsed"
    )
else:
    opcao_dados = "⬆️ Fazer upload de novo arquivo"
    st.info("💡 Nenhum arquivo local encontrado. Use o uploader abaixo para forneceder seus dados.")

df = None

if opcao_dados == "📁 Usar arquivo local (MICRODADOS.csv)" and arquivo_local_existe:
    try:
        df = carregar_dados(CAMINHO_CSV)
        st.success(f"✅ Dataset local carregado: **{len(df):,} registros** × {df.shape[1]} colunas")
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo local: {str(e)}")

elif opcao_dados == "⬆️ Fazer upload de novo arquivo":
    arquivo_upload = st.file_uploader(
        "Selecione um arquivo CSV (MICRODADOS.csv)",
        type="csv",
        help="Arquivo deve estar em formato CSV com separador ';' e encoding 'latin-1'"
    )
    
    if arquivo_upload is not None:
        try:
            df = carregar_dados(arquivo_upload, arquivo_upload.name)
            st.success(f"✅ Arquivo '{arquivo_upload.name}' carregado: **{len(df):,} registros** × {df.shape[1]} colunas")
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
            st.info("💡 Verifique se o arquivo é um CSV válido com separador ';' e encoding 'latin-1'")

# Se nenhum arquivo foi carregado, parar
if df is None:
    st.warning("⚠️ Nenhum dados disponíveis. Faça upload de um arquivo para continuar.")
    st.stop()

st.divider()

# ─────────────────────────────────────────────
# BARRA LATERAL — FILTROS
# ─────────────────────────────────────────────
st.sidebar.header("⚙️ Filtros")

# Filtro de Município
municipios = sorted(df['Municipio'].dropna().unique().tolist())
municipios_sel = st.sidebar.multiselect(
    "🏙️ Município",
    options=municipios,
    default=[],
    placeholder="Todos os municípios"
)

# Filtro de Classificação
classificacoes = sorted(df['Classificacao'].dropna().unique().tolist())
class_sel = st.sidebar.multiselect(
    "🏷️ Classificação",
    options=classificacoes,
    default=[],
    placeholder="Todas as classificações"
)

# Filtro de Sexo
sexos = sorted(df['Sexo'].dropna().unique().tolist())
sexo_sel = st.sidebar.multiselect(
    "👥 Sexo",
    options=sexos,
    default=[],
    placeholder="Todos os sexos"
)

# ── Aplica filtros ──
df_filtrado = df.copy()

if municipios_sel:
    df_filtrado = df_filtrado[df_filtrado['Municipio'].isin(municipios_sel)]

if class_sel:
    df_filtrado = df_filtrado[df_filtrado['Classificacao'].isin(class_sel)]

if sexo_sel:
    df_filtrado = df_filtrado[df_filtrado['Sexo'].isin(sexo_sel)]

st.sidebar.markdown(f"**📋 Registros exibidos:** {len(df_filtrado):,}")

# ─────────────────────────────────────────────
# MÉTRICAS RESUMIDAS
# ─────────────────────────────────────────────
st.subheader("📊 Resumo dos Dados Filtrados")

col1, col2, col3, col4 = st.columns(4)

total = len(df_filtrado)
confirmados = df_filtrado['Classificacao'].str.contains('Confirmado', case=False, na=False).sum()
obitos = df_filtrado['Evolucao'].str.contains('bito', case=False, na=False).sum()
taxa = round(obitos / confirmados * 100, 2) if confirmados > 0 else 0.0

col1.metric("📋 Total Notificações", f"{total:,}")
col2.metric("✅ Confirmados", f"{confirmados:,}")
col3.metric("💀 Óbitos COVID", f"{obitos:,}")
col4.metric("📉 Letalidade", f"{taxa}%")

st.divider()

# ─────────────────────────────────────────────
# GRÁFICO 1 — Distribuição por Classificação
# ─────────────────────────────────────────────
st.subheader("📊 1. Distribuição por Classificação")

contagem_class = df_filtrado['Classificacao'].value_counts()
fig1, ax1 = plt.subplots(figsize=(10, 4))
cores = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
ax1.barh(contagem_class.index, contagem_class.values,
         color=cores[:len(contagem_class)], edgecolor='white')
for barra in ax1.patches:
    ax1.text(barra.get_width() + contagem_class.max() * 0.01,
             barra.get_y() + barra.get_height() / 2,
             f'{int(barra.get_width()):,}', va='center', fontsize=10)
ax1.set_xlabel("Quantidade")
ax1.set_title("Distribuição por Classificação", fontweight='bold')
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()
st.pyplot(fig1)

st.divider()

# ─────────────────────────────────────────────
# GRÁFICO 2 — Top 10 Municípios
# ─────────────────────────────────────────────
st.subheader("🏙️ 2. Top 10 Municípios com Mais Notificações")

top10 = df_filtrado['Municipio'].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(11, 5))
cores2 = ['#e74c3c'] + ['#2980b9'] * 9
ax2.bar(top10.index, top10.values, color=cores2[:len(top10)], edgecolor='white')
for barra in ax2.patches:
    ax2.text(barra.get_x() + barra.get_width() / 2,
             barra.get_height() + top10.max() * 0.01,
             f'{int(barra.get_height()):,}', ha='center', fontsize=9, fontweight='bold')
ax2.set_xlabel("Município")
ax2.set_ylabel("Notificações")
ax2.set_title("Top 10 Municípios por Notificações", fontweight='bold')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
st.pyplot(fig2)

st.divider()

# ─────────────────────────────────────────────
# GRÁFICO 3 — Distribuição por Sexo
# ─────────────────────────────────────────────
st.subheader("👥 3. Distribuição por Sexo")

sexo_count = df_filtrado['Sexo'].value_counts(dropna=True)
fig3, ax3 = plt.subplots(figsize=(6, 6))
ax3.pie(sexo_count.values, labels=sexo_count.index,
        autopct='%1.1f%%',
        colors=['#3498db', '#e91e63', '#95a5a6'][:len(sexo_count)],
        explode=[0.05] * len(sexo_count), startangle=140,
        textprops={'fontsize': 12})
ax3.set_title("Distribuição por Sexo", fontweight='bold')
plt.tight_layout()
col_g3, _ = st.columns([1, 1])
with col_g3:
    st.pyplot(fig3)

st.divider()

# ─────────────────────────────────────────────
# GRÁFICO 4 — Evolução Temporal
# ─────────────────────────────────────────────
st.subheader("📈 4. Evolução Mensal de Notificações")

if 'ano_mes' in df_filtrado.columns:
    evolucao = df_filtrado.groupby('ano_mes').size().sort_index()
    fig4, ax4 = plt.subplots(figsize=(13, 5))
    ax4.plot(evolucao.index, evolucao.values,
             color='#2980b9', linewidth=2.5, marker='o', markersize=4)
    ax4.fill_between(range(len(evolucao)), evolucao.values, alpha=0.15, color='#2980b9')
    ax4.set_xlabel("Mês")
    ax4.set_ylabel("Notificações")
    ax4.set_title("Evolução Mensal de Notificações", fontweight='bold')
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig4)
else:
    st.warning("⚠️ Coluna de data não identificada para gráfico temporal.")

st.divider()

# ─────────────────────────────────────────────
# TABELA DE DADOS BRUTOS (opcional)
# ─────────────────────────────────────────────
with st.expander("🗂️ Ver tabela de dados filtrados (primeiras 200 linhas)"):
    st.dataframe(df_filtrado.head(200), use_container_width=True)

# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("🎓 Projeto KDD — Análise de Dados COVID-19 ES | Desenvolvido com Python + Streamlit")
