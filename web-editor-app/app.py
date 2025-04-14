import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from io import BytesIO

# Título do app
st.set_page_config(page_title="Editor de Arquivo Web", layout="wide")
st.title("📄 Editor de Arquivos CSV / Excel")

# Upload do arquivo
uploaded_file = st.file_uploader("Envie seu arquivo CSV ou Excel:", type=["csv", "xlsx"])

if uploaded_file:
    # Carrega os dados no DataFrame
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("Arquivo carregado com sucesso!")

    st.subheader("🧾 Tabela com Edição Interativa")

    # Configura a tabela para edição
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, resizable=True)
    gb.configure_grid_options(domLayout='normal')
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        theme="material",
        fit_columns_on_grid_load=True
    )

    edited_df = pd.DataFrame(grid_response["data"])

    # Sessão para modificação extra
    st.markdown("### ➕➖ Adicionar ou Remover Linhas/Colunas")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Adicionar Linha Vazia"):
            edited_df.loc[len(edited_df)] = [""] * len(edited_df.columns)

        col_name = st.text_input("Nome da nova coluna:")
        if st.button("➕ Adicionar Coluna"):
            if col_name:
                edited_df[col_name] = ""
            else:
                st.warning("Digite um nome para a nova coluna.")

    with col2:
        if st.button("➖ Remover Última Linha"):
            if not edited_df.empty:
                edited_df = edited_df.iloc[:-1]
            else:
                st.warning("Nada para remover!")

        drop_col = st.selectbox("Selecionar coluna para remover", options=edited_df.columns)
        if st.button("➖ Remover Coluna Selecionada"):
            edited_df.drop(columns=[drop_col], inplace=True)

    # Exibe DataFrame final
    st.subheader("📋 Visualização Final dos Dados")
    st.dataframe(edited_df, use_container_width=True)

    # Exportar como CSV
    def convert_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Baixar Arquivo CSV Modificado",
        data=convert_to_csv(edited_df),
        file_name="arquivo_modificado.csv",
        mime="text/csv"
    )

else:
    st.info("📂 Envie um arquivo para começar.")
