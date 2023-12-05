import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

volcano_df_raw = load_data(path="./data/volcano_ds_pop.csv")
volcano_df = deepcopy(volcano_df_raw)


st.title('Intro to Streamlit')
st.header('Volcanoes Around the World')

left_column, middle_column, right_column = st.columns([3, 1, 1])

volcano_df['Country'] = volcano_df['Country'].replace({
    'United States': 'United States of America',
    'Tanzania': 'United Republic of Tanzania',
    'Martinique': 'Martinique',
    'Sao Tome & Principe': 'Sao Tome and Principe',
    'Guadeloupe': 'Guadeloupe',
    'Wallis & Futuna': 'Wallis and Futuna'
})

with open('./data/countries.geojson') as file:
    volcano_geojson = json.load(file)

if st.checkbox("Show Volcano Data"):
    st.subheader("This is my volcanoes dataset:")
    st.dataframe(data=volcano_df)

types = ["All"]+sorted(pd.unique(volcano_df['Type']))
volcano_type = left_column.selectbox("Choose a Type", types)

show_population = middle_column.radio(
    label='Show Population', options=['Yes', 'No'])

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

if volcano_type == "All":
    alt_volcano_df = volcano_df
else:
    alt_volcano_df = volcano_df[volcano_df["Type"] == volcano_type]

url = "https://public.opendatasoft.com/explore/dataset/significant-volcanic-eruption-database/table/"
st.write("Data Source:", url)

st.subheader("MatplotLib Map")

# Matplotlib
m_volcano_fig, ax_volcano = plt.subplots(figsize=(10, 8))
ax_volcano.scatter(alt_volcano_df['Longitude'], alt_volcano_df['Latitude'], alpha=0.7)

ax_volcano.set_title("Volcano Locations Around the Globe")
ax_volcano.set_xlabel('Longitude')
ax_volcano.set_ylabel('Latitude')

st.subheader("Plotly Map")

volcano_df.head()

fig = px.scatter_mapbox(volcano_df,
                        lat='Latitude',
                        lon='Longitude',
                        color='Type',
                        hover_name='Volcano Name',
                        hover_data=['Type', 'Country', 'Region', 'Status'],
                        zoom=1.5,
                        title="<b>'Volcanoes Around the Globe'</b>",
                        color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(
                    title={"font_size":20,
                         "xanchor":"center", "x":0.38,
                        "yanchor":"bottom", "y":0.95},
                    title_font=dict(size=32, color='Navy', family='Times Roman, sans-serif'),
                    height=1500,
                    width=2300,
                    autosize=True,
                    hovermode='closest',
                    mapbox=dict(
                        style='open-street-map'
                    ),
                    legend_title_text='Volcano Type'
)

if plot_type == "Matplotlib":
    st.pyplot(m_volcano_fig)
else:
    st.plotly_chart(fig)