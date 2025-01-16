# %% Import libraries
import folium
import pandas as pd
import plotly.graph_objects as go
from folium.plugins import HeatMap
from streamlit_folium import st_folium

import streamlit as st

# %% Page layout
# Set page config
st.set_page_config(layout="wide")

# %% App functions
def load_data(filepath):
    turtles_data = pd.read_csv(
        rf"{filepath}",
        sep=",",
    )
    turtles_data = turtles_data.loc[turtles_data["date_year"].dropna()]
    return turtles_data.fillna("NA")

def turtle_population_plot(df):
    """Create line graph showing the yearly evolution of Hawksbill sea turtle populations.

    Args:
    ----
    - df (pd.DataFrame): Data containing 'date_year', 'waterBody', and 'count' columns.

    Returns:
    -------
    - fig (plotly.graph_objects.Figure): The line plot figure.

    """
    # Group by year and sum the count of observations
    df_yearly = df.value_counts(["date_year"]).reset_index().sort_values("date_year")
    df_yearly.columns = ["date_year", "count"]
    df_yearly = df_yearly.query("count > 1 and date_year >= 1990")

    # Create the plot
    fig = go.Figure()

    # Add a single line representing total population count over years
    fig.add_trace(
        go.Scatter(
            x=df_yearly["date_year"],
            y=df_yearly["count"],
            mode="lines+markers",
            name="Total Population",
            line={"color": "#0277BD", "width": 3},
            marker={"size": 8},
        ),
    )

    # Add annotations
    fig.add_annotation(
        x=2009,  
        y=df_yearly["count"].max(),  
        text="Surveys from 2007-2009 found hawksbill nesting in 6 eastern Pacific nations, with 80% of nests in El Salvador.",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font={
            "size": 12,
            "color": "#43A047",
        },  
        bgcolor="#002B36", 
        bordercolor="#43A047",  
    )
    fig.add_annotation(
        x=2019, 
        y=df_yearly.query("date_year == 2019")["count"].values[
            0
        ],  
        text=(
            "Hawksbill turtles are currently classified as Critically Endangered by the IUCN.<br>"
            "A major threat to hawksbill turtles is the loss of nesting habitat and coral reefs<br>"
            "due to coastal development, rising seas from climate change, and pollution."
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-50,
        font={
            "size": 12,
            "color": "#E64A19",
        },
        bgcolor="#002B36",  
        bordercolor="#E64A19",  
    )
    # Set layout
    fig.update_layout(
        title="Yearly Evolution of Hawksbill Sea Turtle Population",
        xaxis={"title": "", "showgrid": False, "color": "#FDD835"},
        yaxis={"title": "Observations", "showgrid": False, "color": "#FDD835"},
        plot_bgcolor="#002B36",  # Background color
        paper_bgcolor="#002B36",  # Paper background color
        font={"color": "#FDD835"},  # Text color
        legend={"bgcolor": "#002B36", "font": {"color": "#FDD835"}},
    )

    return fig


def scatter_plot(df):
    """Create scatter plot with dual y-axes for 'sst' (temperature) and 'sss' (salinity) over 'date_year'.

    Args:
    ----
    - df (pd.DataFrame): Data containing 'date_year', 'sst', and 'sss' columns.

    Returns:
    -------
    - fig (plotly.graph_objects.Figure): The scatter plot figure with dual y-axes.

    """
    # Aggregate yearly data by averaging sst and sss values
    df_yearly = df.groupby("date_year")[["sst", "sss"]].mean().reset_index()

    # Create the scatter plot
    fig = go.Figure()

    # Add trace for 'sst' on primary y-axis
    fig.add_trace(
        go.Scatter(
            x=df_yearly["date_year"],
            y=df_yearly["sst"],
            mode="lines+markers",
            name="SST (Temperature)",
            marker={"size": 8, "color": "#FF5722"}, 
            line={"color": "#FF5722", "width": 2},
            yaxis="y",
        ),
    )

    # Add trace for 'sss' on secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=df_yearly["date_year"],
            y=df_yearly["sss"],
            mode="lines+markers",
            name="SSS (Salinity)",
            marker={"size": 8, "color": "#0277BD"},  
            line={"color": "#0277BD", "width": 2},
            yaxis="y2",
        ),
    )

    # Set layout 
    fig.update_layout(
        title="Yearly Evolution of Sea Surface Temperature and Sea Surface Salinity",
        xaxis={"title": "", "showgrid": False, "color": "#FDD835"},
        yaxis={
            "title": "SST (°C)",
            "showgrid": False,
            "color": "#FF5722",
            "side": "left",
        },
        yaxis2={
            "title": "SSS (Salinity)",
            "showgrid": False,
            "color": "#0277BD",
            "overlaying": "y",
            "side": "right",
        },
        plot_bgcolor="#002B36",
        paper_bgcolor="#002B36",
        font={"color": "#FDD835"},
        legend={"bgcolor": "#002B36", "font": {"color": "#FDD835"}},
    )

    return fig


def pie_plot(df, field, colors=None):
    """Create a pie plot segmented by a specified field.

    Args:
    ----
    - df (pd.DataFrame): Data containing 'date_year' and the specified field.
    - field (str): Column name to segment the pie plot (e.g., 'waterBody').
    - colors (list): Custom color palette for the pie chart segments.

    Returns:
    -------
    - fig (plotly.graph_objects.Figure): The pie plot figure.

    """
    # Filter data for date_year >= 2000
    filtered_data = df.query("date_year >= 2000")

    # Count occurrences of the specified field
    field_counts = filtered_data[field].value_counts().reset_index()
    field_counts.columns = [field, "count"]
    field_counts = field_counts.query("count > 1")

    # Default color scheme if none provided
    if colors is None:
        colors = ["#1A1D26", "#43A047", "#00ACC1", "#FDD835"]

    # Create pie plot
    fig = go.Figure(
        go.Pie(
            labels=field_counts[field],
            values=field_counts["count"],
            marker={
                "colors": colors,
                "line": {"color": "#002B36", "width": 1},
            },
            textinfo="percent+label",
            hole=0.3,
        ),
    )

    # Set layout
    fig.update_layout(
        title=f"Habitat by {field.capitalize()} (2000 - 2019)",
        plot_bgcolor="#002B36",
        paper_bgcolor="#002B36",
        font={"color": "#FDD835"},
    )

    return fig


def map_heatmap(turtles_data):
    """Generate a heatmap on a satellite map using folium, from the turtle observations data.

    Args:
    ----
        turtles_data (pd.DataFrame): Hawksbill sea turtles dataframe.

    Returns:
    -------
        folium.Map: A folium Map.

    """
    heat_data = (
        turtles_data[["decimalLatitude", "decimalLongitude"]]
        .dropna()
        .to_numpy()
        .tolist()
    )

    # Calculate map center
    center_lat = turtles_data["decimalLatitude"].mean()
    center_lon = turtles_data["decimalLongitude"].mean()

    # Create the map
    heatmap = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=2,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
    )

    # Add the heatmap
    HeatMap(heat_data, radius=15).add_to(heatmap)

    return heatmap


# Define data filtering function
def filter_turtle_data(turtles_data, year):
    """Filter turtle data based on a selected date.

    Args:
    ----
        turtles_data (pd.DataFrame): Hawksbill sea turtles dataframe.

    Returns:
    -------
        pd.DataFrame: Filtered turtle data.

    """
    filtered_data = turtles_data[turtles_data["date_year"] >= year]
    filtered_data["date_year"] = filtered_data["date_year"].astype(int)
    return filtered_data[["date_year", "decimalLatitude", "decimalLongitude"]]

# %% Data
turtles_data = load_data("Resources/seaturtles.csv")
# Get the first and last years from the filtered data
filtered_years = turtles_data[turtles_data["date_year"].astype(int) >= 1992]
first_date = filtered_years["date_year"].astype(int).min()
last_date = filtered_years["date_year"].astype(int).max()

# %% App
col1, col2 = st.columns([0.9, 9])
with col1:
    st.image(
        "Resources/Turtle+no+background.png",
        width=100,
    )
with col2:
    st.title("Hawksbill Sea Turtles Data Visualization")
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Population decline",
        "Environmental conditions",
        "Habitat",
        "Population distribution",
    ],
)

with tab1:
    st.plotly_chart(turtle_population_plot(turtles_data), use_container_width=True)

with tab2:
    st.plotly_chart(scatter_plot(turtles_data), use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(pie_plot(turtles_data, "waterBody"))
    with col2:
        st.plotly_chart(
            pie_plot(turtles_data, "country", ["#004D91", "#1A1D26", "#81D4FA"]),
        )
with tab4:
    # Add a slider
    selected_date = st.slider(
        "",
        min_value=first_date,
        max_value=last_date,
        value=first_date,
    )

    # Filter data based on the slider
    filtered_data = filter_turtle_data(turtles_data, selected_date)
    st_folium(map_heatmap(filtered_data), width=1400, height=400)
