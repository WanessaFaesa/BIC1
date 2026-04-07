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
# CARREGAMENTO DOS DADOS (SEM CACHE PARA EVITAR ERRO COM ARQUIVOS GRANDES)
# ─────────────────────────────────────────────
def carregar_dados_chunked(caminho_ou_buffer, nome_arquivo="arquivo", usar_amostra=False) -> pd.DataFrame:
    """
    Lê CSV em chunks para lidar com arquivos grandes (>1GB).
    SEM CACHE para evitar erro ao serializar dados grandes.
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    chunks = []
    total_linhas = 0
    chunk_size = 50000  # Aumentado para 50k = mais rápido
    chunk_num = 0
    
    try:
        # Se buffer, reset para leitura
        if hasattr(caminho_ou_buffer, 'seek'):
            caminho_ou_buffer.seek(0)
        
        # Lê em chunks
        for chunk in pd.read_csv(
            caminho_ou_buffer,
            sep=';',
            encoding='latin-1',
            low_memory=False,
            chunksize=chunk_size,
            on_bad_lines='skip'  # Ignora linhas malformadas
        ):
            chunk_num += 1
            total_linhas += len(chunk)
            
            # Atualiza barra de progresso
            progress = min(chunk_num / 100, 0.95)  # Max 95%
            progress_bar.progress(progress)
            status_text.text(f"✓ Lidas {total_linhas:,} linhas...")
            
            # Se usar amostra e já leu o suficiente, pare
            if usar_amostra and total_linhas > 500000:  # Máx 500k
                status_text.text(f"⏹️ Usando amostra dos primeiros {total_linhas:,} registros")
                break
            
            chunks.append(chunk)
        
        progress_bar.progress(1.0)
        status_text.empty()
        
        # Concatena todos os chunks
        if chunks:
            dados = pd.concat(chunks, ignore_index=True)
        else:
            st.error("❌ Nenhum dado foi lido do arquivo")
            return None
        
        # Tenta converter data de notificação
        col_data = next(
            (c for c in dados.columns 
             if 'ata' in c.lower() and 'otifica' in c.lower()), 
            None
        )
        if col_data:
            try:
                dados['data_convertida'] = pd.to_datetime(
                    dados[col_data], 
                    errors='coerce', 
                    dayfirst=True
                )
                dados['ano_mes'] = dados['data_convertida'].dt.to_period('M').astype(str)
            except:
                pass  # Se falhar, continua sem coluna de data
        
        return dados
        
    except MemoryError:
        st.error("❌ Arquivo muito grande para memória disponível")
        st.info("💡 Tente: 1) Usar percentual menor, 2) Comprimir arquivo em ZIP, 3) Dividir em partes")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao ler arquivo: {str(e)}")
        status_text.empty()
        return None

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
        with st.spinner("📂 Carregando arquivo local..."):
            df = carregar_dados_chunked(CAMINHO_CSV, usar_amostra=False)
        if df is not None:
            st.success(f"✅ Dataset local carregado: **{len(df):,} registros** × {df.shape[1]} colunas")
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo local: {str(e)}")

elif opcao_dados == "⬆️ Fazer upload de novo arquivo":
    st.info("💡 **Dica:** Para arquivos muito grandes (>1GB), comprima em ZIP ou divida em partes")
    
    arquivo_upload = st.file_uploader(
        "Selecione um arquivo CSV (MICRODADOS.csv)",
        type="csv",
        help="Arquivo pode estar em formato CSV com separador ';' e encoding 'latin-1'"
    )
    
    if arquivo_upload is not None:
        col_botao1, col_botao2 = st.columns(2)
        
        with col_botao1:
            usar_amostra_upload = st.checkbox(
                "Usar apenas amostra (~500k linhas)",
                value=True,
                help="Reduz muito a memória usada"
            )
        
        with col_botao2:
            if st.button("▶️ Processar arquivo", use_container_width=True):
                st.info("🔄 Processando... aguarde")
                df = carregar_dados_chunked(arquivo_upload, arquivo_upload.name, usar_amostra=usar_amostra_upload)
                
                if df is not None:
                    st.success(f"✅ Arquivo carregado com sucesso!")
                    st.success(f"📊 {len(df):,} registros × {df.shape[1]} colunas prontos para análise")
                else:
                    st.error("❌ Não foi possível carregar o arquivo")

# Se nenhum arquivo foi carregado, parar
if df is None:
    st.warning("⚠️ Nenhum dados disponíveis. Faça upload de um arquivo para continuar.")
    st.stop()

st.divider()

# ─────────────────────────────────────────────
# FILTRAGEM INICIAL - REDUZIR TAMANHO PARA ARQUIVOS GRANDES
# ─────────────────────────────────────────────
st.subheader("🎯 Amostra de Dados")

tamanho_original = len(df)

# Se arquivo for grande, ofereça opções de amostra manual
if tamanho_original > 100000:
    col_amostra1, col_amostra2 = st.columns(2)
    
    with col_amostra1:
        usar_amostra = st.checkbox(
            "📊 Aplicar amostra manual",
            value=False,
            help="Para análises mais rápidas, selecione uma porcentagem dos dados"
        )
    
    with col_amostra2:
        if usar_amostra:
            percentual = st.slider(
                "% de dados para análise",
                min_value=1,
                max_value=100,
                value=50,
                step=5,
                help="Quanto maior o percentual, mais memória será usada"
            )
            df = df.sample(frac=percentual/100, random_state=42)
            st.info(f"📈 Usando {percentual}% dos dados: {len(df):,} registros (de {tamanho_original:,} originais)")
else:
    st.success(f"✅ Todos os {tamanho_original:,} registros estão sendo utilizados")

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
