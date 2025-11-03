import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análisis estudiantes - University", layout="wide")
sns.set_theme(style="whitegrid")

st.title("Dashboard - University Student Data")
st.markdown("""
Hecho por:
+ Juan Diego Torregroza
+ Juan Acosta
+ Génesi Barrios
""")

@st.cache_data
def load_data_from_csv(default_path="university_student_data.csv"):
  try:
      df = pd.read_csv(default_path)
  except FileNotFoundError:
      st.info("No se encontró el archivo por defecto. Sube un CSV con la misma estructura.")
      return None
  except Exception as e:
      st.error(f"Error leyendo el archivo por defecto: {e}")
      return None

  df.columns = (
      df.columns
        .str.strip()
        .str.capitalize()
        .str.replace(' ', '_')
        .str.replace('[()%]', '', regex=True)
        .str.replace(r'[^0-9A-Za-z_]+', '', regex=True)
        .str.replace(r'_+', '_', regex=True)
        .str.replace(r'^_|_$', '', regex=True)
  )

  return df

df = load_data_from_csv()

if df is None:
    st.stop()

st.sidebar.markdown(f"Filas, columnas: {df.shape[0]} x {df.shape[1]}")
if st.sidebar.checkbox("Mostrar columnas y tipos"):
    st.sidebar.write(df.dtypes)

years = sorted([int(y) for y in pd.unique(df['Year'].dropna())]) if 'Year' in df.columns else []
terms = sorted(df['Term'].dropna().unique()) if 'Term' in df.columns else []

selected_terms = st.sidebar.multiselect("Seleccionar Term(s)", options=terms, default=terms)
if years:
    selected_years = st.sidebar.multiselect("Seleccionar Año(s)", options=years, default=years)
else:
    selected_years = []

df_filtered = df.copy()
if selected_terms:
    df_filtered = df_filtered[df_filtered['Term'].isin(selected_terms)]
if selected_years:
    df_filtered = df_filtered[df_filtered['Year'].isin(selected_years)]

st.subheader("Datos")

st.markdown("Tabla de datos original")
st.dataframe(df.reset_index(drop=True))

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("Tabla de datos filtrada")
    st.dataframe(df_filtered.reset_index(drop=True))

with col2:
    st.markdown("Resumen rápido")
    st.write(f"Filas (filtradas): {df_filtered.shape[0]}")
    if 'Retention_rate' in df_filtered.columns and 'Student_satisfaction' in df_filtered.columns:
        st.write(df_filtered[['Retention_rate','Student_satisfaction']].agg(['mean','median','std']).round(2))

csv = df_filtered.to_csv(index=False)
st.download_button("📥 Descargar datos filtrados (CSV)", data=csv, file_name="university_student_data_filtered.csv", mime="text/csv")

st.subheader("Visualizaciones")

def plot_to_streamlit(fig):
    st.pyplot(fig, clear_figure=True)

if 'Retention_rate' in df_filtered.columns and 'Year' in df_filtered.columns:
    st.markdown("Retention Rate (%) por Año y Term")
    fig, ax = plt.subplots(figsize=(10,5))
    try:
        sns.lineplot(data=df_filtered, x='Year', y='Retention_rate', hue='Term', marker='o', ax=ax)
        ax.set_title('Retention Rate (%) over Years by Term')
        ax.set_ylabel('Retention Rate (%)')
        ax.set_xticks(sorted(df_filtered['Year'].dropna().unique()))
        ax.grid(True)
        plt.tight_layout()
        plot_to_streamlit(fig)
    except Exception as e:
        st.error(f"No se pudo generar la gráfica de Retention Rate: {e}")

    st.markdown("Promedio por año (ambos términos juntos)")
    try:
        year_avg = df_filtered.groupby('Year')['Retention_rate'].mean().reset_index()
        fig2, ax2 = plt.subplots(figsize=(8,4))
        sns.lineplot(data=year_avg, x='Year', y='Retention_rate', marker='o', ax=ax2)
        ax2.set_title('Average Retention Rate per Year')
        ax2.set_ylabel('Retention Rate (%)')
        plt.tight_layout()
        plot_to_streamlit(fig2)
    except Exception as e:
        st.info("No hay suficientes datos para el promedio por año.")

if 'Student_satisfaction' in df_filtered.columns and 'Year' in df_filtered.columns:
    st.markdown("Student Satisfaction (%) por Año y Term")
    fig3, ax3 = plt.subplots(figsize=(10,5))
    try:
        sns.lineplot(data=df_filtered, x='Year', y='Student_satisfaction', hue='Term', marker='o', ax=ax3)
        ax3.set_title('Student Satisfaction (%) by Year and Term')
        ax3.set_ylabel('Student Satisfaction (%)')
        ax3.set_xticks(sorted(df_filtered['Year'].dropna().unique()))
        plt.tight_layout()
        plot_to_streamlit(fig3)
    except Exception as e:
        st.error(f"No se pudo generar la gráfica de Student Satisfaction: {e}")

    st.markdown("Distribución por Term (boxplot)")
    try:
        fig4, ax4 = plt.subplots(figsize=(6,4))
        sns.boxplot(data=df_filtered, x='Term', y='Student_satisfaction', ax=ax4)
        ax4.set_title('Student Satisfaction distribution by Term')
        plt.tight_layout()
        plot_to_streamlit(fig4)
    except Exception as e:
        st.info("No hay suficientes datos para boxplot.")

st.markdown("Estadísticas por Term")
if all(col in df_filtered.columns for col in ['Retention_rate','Student_satisfaction','Term']):
    try:
        term_stats = df_filtered.groupby('Term')[['Retention_rate','Student_satisfaction']].mean().reset_index().round(2)
        st.dataframe(term_stats)

        fig5, axes = plt.subplots(1,2, figsize=(12,4))
        sns.barplot(data=term_stats, x='Term', y='Retention_rate', ax=axes[0])
        axes[0].set_title('Average Retention Rate by Term')
        sns.barplot(data=term_stats, x='Term', y='Student_satisfaction', ax=axes[1])
        axes[1].set_title('Average Student Satisfaction by Term')
        plt.tight_layout()
        plot_to_streamlit(fig5)
    except Exception as e:
        st.info("No hay suficientes datos para estadísticas por term.")
else:
    st.info("Faltan columnas necesarias para calcular estadísticas por Term (`Retention_rate` y/o `Student_satisfaction`).")

enrolled_cols = [c for c in df_filtered.columns if c.lower().endswith('_enrolled')]
if enrolled_cols and 'Year' in df_filtered.columns:
    st.markdown("Enrolled students por Departamento (stacked) por Año")
    try:
        dept = df_filtered[['Year'] + enrolled_cols].groupby('Year').sum().sort_index()
        fig6, ax6 = plt.subplots(figsize=(10,5))
        dept.plot(kind='bar', stacked=True, ax=ax6)
        ax6.set_title('Enrolled students by Department over Years (stacked)')
        ax6.set_ylabel('Number of enrolled students')
        plt.tight_layout()
        plot_to_streamlit(fig6)
    except Exception as e:
        st.info(f"No se pudo generar la gráfica de departamentos: {e}")
else:
    st.info("No se encontraron columnas de tipo '*_enrolled' para mostrar matriculados por departamento.")

st.subheader("Descripción de columnas")
if st.checkbox("Mostrar descripción completa (describe)"):
    try:
        desc = df.describe(include='all').round(2)
        st.dataframe(desc)
    except Exception as e:
        st.info("No se pudo generar la descripción completa.")

st.markdown("---")