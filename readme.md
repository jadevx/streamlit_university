# Dashboard de Análisis de Estudiantes - University

Aplicación interactiva creada con **Streamlit** para analizar datos universitarios, visualizar métricas de retención y satisfacción estudiantil, y explorar tendencias por año, término y facultad.

---

## Autores
- **Juan Diego Torregroza**
- **Juan Acosta**
- **Génesi Barrios**

---

## Descripción General

Este dashboard permite:
- Filtrar datos por **Año** y **Termino (Term)**.
- Visualizar:
  - Tasa de retención estudiantil (`Retention Rate`).
  - Nivel de satisfacción de estudiantes (`Student Satisfaction`).
  - Distribución por facultad (`Engineering`, `Business`, `Arts`, `Science`).
- Obtener estadísticas resumen y descargar los datos filtrados.
- Explorar descripciones estadísticas de todas las columnas del dataset.

---

## Dataset

El dataset utilizado contiene información sobre el desempeño académico y retención de estudiantes universitarios.

### Ejemplo de las primeras filas (`head`):

| Year | Term   | Applications | Admitted | Enrolled | Retention Rate (%) | Student Satisfaction (%) | Engineering Enrolled | Business Enrolled | Arts Enrolled | Science Enrolled |
|------|--------|---------------|-----------|-----------|--------------------|--------------------------|----------------------|------------------|---------------|------------------|
| 2015 | Spring | 2500          | 1500      | 600       | 85                 | 78                       | 200                  | 150              | 125           | 125              |
| 2015 | Fall   | 2500          | 1500      | 600       | 85                 | 78                       | 200                  | 150              | 125           | 125              |
| 2016 | Spring | 2600          | 1550      | 625       | 86                 | 79                       | 210                  | 160              | 130           | 125              |
| 2016 | Fall   | 2600          | 1550      | 625       | 86                 | 79                       | 210                  | 160              | 130           | 125              |
| 2017 | Spring | 2700          | 1600      | 650       | 87                 | 80                       | 225                  | 165              | 135           | 125              |

---

## Instalación local

### Clonar el repositorio
```bash
git clone https://github.com/jadevx/streamlit_university.git
cd streamlit_university
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar localmente
```bash
streamlit run app.py
```

### Streamlit Link
https://datasetmineria-e8pkvhxm2qwedmutsqj2kn.streamlit.app/
