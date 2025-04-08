from supabase import create_client
import pandas as pd 
import streamlit as st 
import plotly.express as px


API_URL = 'https://vvsontymeeizuhgofmew.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ2c29udHltZWVpenVoZ29mbWV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI1ODAwMjUsImV4cCI6MjA1ODE1NjAyNX0.NXvA9cI3tFgXEAsr_J995FRb3j5ZTZmV_NBiibhjFyM'
supabase = create_client(API_URL, API_KEY)

supabaseList = supabase.table('main_table').select('*').execute().data

# Convert to DataFrame and process datetime
df = pd.DataFrame(supabaseList)
# df['created_at'] = df['created_at'].astype(str)
# df['date'] = df['created_at'].str.split('T').str[0]
# df['time'] = df['created_at'].str.split('T').str[1].str.split('.').str[0]
# df['DateTime'] = pd.to_datetime(df['created_at'])  # Proper datetime conversion

# Convert created_at to datetime directly
df['created_at'] = pd.to_datetime(df['created_at'])

# If needed, extract date and time components
df['date'] = df['created_at'].dt.date
df['time'] = df['created_at'].dt.time

# Sort the DataFrame by created_at
df = df.sort_values(by='created_at')

# Optionally, you can reset the index after sorting
df = df.reset_index(drop=True)

st.set_page_config(page_title="Dashboard",layout='wide', initial_sidebar_state='collapsed')


st.map(df[['latitude', 'longitude']], use_container_width=True)

df = df.tail(30)

# st.markdown(df)

# st.sidebar.header("Visualisation")

# df_sorted = df.sort_values("DateTime").tail(30)

# df = df_sorted

st.markdown('### Voltage')
fig = px.line(df, x="created_at", y="voltage", title='',markers=True, color_discrete_sequence=['red'])

fig.update_traces(marker=dict(color='white'))

# fig.update_layout(
    # xaxis=dict(rangeselector=dict(
        # buttons=list(
            # [   dict(count=30,label="30mn", step="minute",stepmode="backward"),
                # dict(count=1,label="1h", step="hour",stepmode="backward"),     
                # dict(count=5,label="5h", step="hour",stepmode="backward"),
                # dict(count=1,label="1d", step="day",stepmode="backward"), 
                # dict(count=3,label="3d", step="day",stepmode="backward"),             
                # dict(count=7,label="1w", step="day",stepmode="backward"),
                # dict(count=1,label="1m", step="month",stepmode="backward"),
                # dict(count=3,label="3m", step="month",stepmode="backward"),
                # dict(step="all")
            # ]
                    # )
                #  ),
            # rangeslider=dict(visible=False),type="date")
            # )
st.plotly_chart(fig,use_container_width=True, theme="streamlit")

st.markdown('### Current')
fig = px.line(df, x="created_at", y="current", title='',markers=True, color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

st.markdown('### Power')
fig = px.line(df, x="created_at", y="power", title='',markers=True, color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

st.markdown('### Energy')
fig = px.line(df, x="created_at", y="energy", title='',markers=True, color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

st.markdown('### hours')
fig = px.line(df, x="created_at", y="hours",markers=True, title='', color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

# st.area_chart(
    # df,
    # x="DateTime",
    # y="voltage",
    # color="#ffaa00",
# )

# c = alt.Chart(df).mark_area(
    # line={'color':'darkgreen'},
    # color=alt.Gradient(
        # gradient='linear',
        # stops=[alt.GradientStop(color='white', offset=0),
            #    alt.GradientStop(color='darkgreen', offset=1)],
        # x1=1,
        # x2=1,
        # y1=1,
        # y2=0
    # )
# ).encode(
    # alt.X('DateTime'),
    # alt.Y('voltage')
# )

# st.markdown('### Combined Metrics Visualization')
# fig = px.line(
    # df,
    # x="created_at",
    # y=["current", "hours"],  # Corrected spelling of 'voltage'
    # title='current and hours',
    # markers=True
    # , color_discrete_sequence=['red', 'blue']
# )
# fig.update_traces(marker=dict(color='white'))
# st.plotly_chart(fig, use_container_width=True)


# fig = px.line(
    # df,
    # x="created_at",
    # y=["current"],  # Corrected spelling of 'voltage'
    # title='energy and current',
    # color_discrete_sequence=['red', 'green'],
    # markers=True
# )
# fig.add_bar(x=df["created_at"], y=df['energy'])
# fig.update_traces(marker=dict(color='white'))
# st.plotly_chart(fig, use_container_width=True)
# 
# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots

# fig = make_subplots(
    # rows=2, cols=1,shared_xaxes=True,vertical_spacing=0.1,
    # row_heights=[0.6, 0.4], subplot_titles=("Line Chart", "Bar Chart"),
# )
# 
# fig.add_trace(
    # go.Bar(x=df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S'), y=df['energy'],
        #    mode='lines+markers', name='Bar Chart'), row=1, col=1
# )
# 
# fig.add_trace(
    # go.Scatter(x=df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S'), y=df['current'],
            #    mode='lines+markers', name='Line Chart'), row=1, col=1
# )
# 
# fig.update_layout(
    # height=600, showlegend=True, title_text = "Bar Chart Below, Line Chart on Top",
# )
# 
# st.plotly_chart(fig, use_container_width=True)

# fig = make_subplots(
    # rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
    # row_heights=[0.6, 0.4], subplot_titles=("Energy vs. Current", "Line Chart")
# )
# 
# Bar chart with formatted datetime strings
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S'),
        # y=df['energy'],
        # name='Energy',
        # marker_color='blue'
    # ),
    # row=1, col=1
# )
# 
# Line chart
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],
        # y=df['current'],
        # mode='lines+markers',
        # name='Current',
        # line=dict(color='red')
    # ),
    # row=1, col=1
# )
# 
# fig.update_layout(
    # height=600, 
    # title_text="Energy and Current Metrics",
    # showlegend=True
# )
# 
# st.plotly_chart(fig, use_container_width=True)
# 

# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots
# 
# Create figure with secondary y-axis
# fig = make_subplots(specs=[[{"secondary_y": True}]])
# 
# Add bar chart (Energy) - Primary Y-axis
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'],  # Use datetime objects directly
        # y=df['energy'],
        # name='Energy',
        # marker=dict(color='rgba(255, 0, 0, 0.3)'),
        # opacity=0.5
    # ),
    # secondary_y=False
# )
# 
# Add line chart (Current) - Secondary Y-axis
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],  # Use datetime objects directly
        # y=df['current'],
        # name='Current',
        # mode='lines+markers',
        # line=dict(color='blue', width=2),
        # marker=dict(color='white', size=8)
    # ),
    # secondary_y=True
# )
# 
# Configure layout
# fig.update_layout(
    # title_text='Current vs Energy - Dual Axis',
    # height=500,
    # showlegend=True,
    # hovermode='x unified'
# )
# 
# Set axis titles
# fig.update_yaxes(title_text="<b>Energy</b> (kWh)", secondary_y=False)
# fig.update_yaxes(title_text="<b>Current</b> (A)", secondary_y=True)
# 
# st.plotly_chart(fig, use_container_width=True)

# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots
# 
# Create subplots with 2 rows, shared X-axis
# fig = make_subplots(
    # rows=2, cols=1,
    # shared_xaxes=True,
    # vertical_spacing=0.1,
    # row_heights=[0.7, 0.3],  # 70% height for top chart, 30% for bottom
    # subplot_titles=("Current (Line Chart)", "Energy (Bar Chart)")
# )
# 
# Add line chart to top row (row=1)
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],
        # y=df['current'],
        # mode='lines+markers',
        # name='Current',
        # line=dict(color='blue', width=2),
        # marker=dict(color='white', size=8)
    # ),
    # row=1, col=1
# )
# 
# Add bar chart to bottom row (row=2)
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'],
        # y=df['energy'],
        # name='Energy',
        # marker=dict(color='red')
    # ),
    # row=2, col=1
# )
# 
# Update layout
# fig.update_layout(
    # height=600,
    # showlegend=True,
    # title_text="Energy and Current Over Time",
    # hovermode='x unified',
    # margin=dict(t=100),
    # plot_bgcolor='rgba(245,245,245,1)'
# )
# 
# Format axes
# fig.update_yaxes(title_text="Current (A)", row=1, col=1)
# fig.update_yaxes(title_text="Energy (kWh)", row=2, col=1)
# fig.update_xaxes(title_text="Time", row=2, col=1)
# 
# Remove datetime formatting issues
# fig.update_xaxes(rangeslider_visible=False)
# 
# st.plotly_chart(fig, use_container_width=True)

# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots
# 
# Create subplots with adjusted proportions
# fig = make_subplots(
    # rows=2, cols=1,
    # shared_xaxes=True,
    # vertical_spacing=0,  # No space between charts
    # row_heights=[0.8, 0.2],  # 80% for line chart, 20% for bar chart
    # subplot_titles=("Current", "Energy")
# )
# 
# Line chart (Top)
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],
        # y=df['current'],
        # mode='lines+markers',
        # name='Current',
        # line=dict(color='blue', width=2),
        # marker=dict(color='white', size=6)
    # ),
    # row=1, col=1
# )
# 
# Bar chart (Bottom)
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'],
        # y=df['energy'],
        # name='Energy',
        # marker=dict(color='red', opacity=0.7)
    # ),
    # row=2, col=1
# )
# 
# Update layout
# fig.update_layout(
    # height=700,  # Increased total height
    # showlegend=False,
    # margin=dict(t=40, b=20, l=40, r=20),
    # plot_bgcolor='white'
# )
# 
# Axis formatting
# fig.update_yaxes(title_text="Current (A)", row=1, col=1, showgrid=False)
# fig.update_yaxes(title_text="Energy (kWh)", row=2, col=1, showgrid=False)
# fig.update_xaxes(showticklabels=False, row=1, col=1)  # Hide x-axis on top chart
# fig.update_xadf = df.tail(30)

# st.set_page_config(page_title="Visualisation", layout="wide")

# st.markdown(df)

# st.sidebar.header("Visualisation")

# df_sorted = df.sort_values("DateTime").tail(30)

# df = df_sorted

# fig.update_layout(
    # xaxis=dict(rangeselector=dict(
        # buttons=list(
            # [   dict(count=30,label="30mn", step="minute",stepmode="backward"),
                # dict(count=1,label="1h", step="hour",stepmode="backward"),     
                # dict(count=5,label="5h", step="hour",stepmode="backward"),
                # dict(count=1,label="1d", step="day",stepmode="backward"), 
                # dict(count=3,label="3d", step="day",stepmode="backward"),             
                # dict(count=7,label="1w", step="day",stepmode="backward"),
                # dict(count=1,label="1m", step="month",stepmode="backward"),
                # dict(count=3,label="3m", step="month",stepmode="backward"),
                # dict(step="all")
            # ]
                    # )
                #  ),
            # rangeslider=dict(visible=False),type="date")
            # )
st.plotly_chart(fig,use_container_width=True, theme="streamlit")

st.markdown('### Current')
fig = px.line(df, x="created_at", y="current", title='',markers=True, color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

st.markdown('### Power')
fig = px.line(df, x="created_at", y="power", title='',markers=True, color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

st.markdown('### Energy')
fig = px.line(df, x="created_at", y="energy", title='',markers=True, color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

st.markdown('### hours')
fig = px.line(df, x="created_at", y="hours",markers=True, title='', color_discrete_sequence=['red'])
fig.update_traces(marker=dict(color='white'))
st.plotly_chart(fig,use_container_width=True)

# st.area_chart(
    # df,
    # x="DateTime",
    # y="voltage",
    # color="#ffaa00",
# )

# c = alt.Chart(df).mark_area(
    # line={'color':'darkgreen'},
    # color=alt.Gradient(
        # gradient='linear',
        # stops=[alt.GradientStop(color='white', offset=0),
            #    alt.GradientStop(color='darkgreen', offset=1)],
        # x1=1,
        # x2=1,
        # y1=1,
        # y2=0
    # )
# ).encode(
    # alt.X('DateTime'),
    # alt.Y('voltage')
# )

# st.markdown('### Combined Metrics Visualization')
# fig = px.line(
    # df,
    # x="created_at",
    # y=["current", "hours"],  # Corrected spelling of 'voltage'
    # title='current and hours',
    # markers=True
    # , color_discrete_sequence=['red', 'blue']
# )
# fig.update_traces(marker=dict(color='white'))
# st.plotly_chart(fig, use_container_width=True)


# fig = px.line(
    # df,
    # x="created_at",
    # y=["current"],  # Corrected spelling of 'voltage'
    # title='energy and current',
    # color_discrete_sequence=['red', 'green'],
    # markers=True
# )
# fig.add_bar(x=df["created_at"], y=df['energy'])
# fig.update_traces(marker=dict(color='white'))
# st.plotly_chart(fig, use_container_width=True)
# 
# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots

# fig = make_subplots(
    # rows=2, cols=1,shared_xaxes=True,vertical_spacing=0.1,
    # row_heights=[0.6, 0.4], subplot_titles=("Line Chart", "Bar Chart"),
# )
# 
# fig.add_trace(
    # go.Bar(x=df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S'), y=df['energy'],
        #    mode='lines+markers', name='Bar Chart'), row=1, col=1
# )
# 
# fig.add_trace(
    # go.Scatter(x=df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S'), y=df['current'],
            #    mode='lines+markers', name='Line Chart'), row=1, col=1
# )
# 
# fig.update_layout(
    # height=600, showlegend=True, title_text = "Bar Chart Below, Line Chart on Top",
# )
# 
# st.plotly_chart(fig, use_container_width=True)

# fig = make_subplots(
    # rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
    # row_heights=[0.6, 0.4], subplot_titles=("Energy vs. Current", "Line Chart")
# )
# 
# Bar chart with formatted datetime strings
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S'),
        # y=df['energy'],
        # name='Energy',
        # marker_color='blue'
    # ),
    # row=1, col=1
# )
# 
# Line chart
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],
        # y=df['current'],
        # mode='lines+markers',
        # name='Current',
        # line=dict(color='red')
    # ),
    # row=1, col=1
# )
# 
# fig.update_layout(
    # height=600, 
    # title_text="Energy and Current Metrics",
    # showlegend=True
# )
# 
# st.plotly_chart(fig, use_container_width=True)
# 

# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots
# 
# Create figure with secondary y-axis
# fig = make_subplots(specs=[[{"secondary_y": True}]])
# 
# Add bar chart (Energy) - Primary Y-axis
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'],  # Use datetime objects directly
        # y=df['energy'],
        # name='Energy',
        # marker=dict(color='rgba(255, 0, 0, 0.3)'),
        # opacity=0.5
    # ),
    # secondary_y=False
# )
# 
# Add line chart (Current) - Secondary Y-axis
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],  # Use datetime objects directly
        # y=df['current'],
        # name='Current',
        # mode='lines+markers',
        # line=dict(color='blue', width=2),
        # marker=dict(color='white', size=8)
    # ),
    # secondary_y=True
# )
# 
# Configure layout
# fig.update_layout(
    # title_text='Current vs Energy - Dual Axis',
    # height=500,
    # showlegend=True,
    # hovermode='x unified'
# )
# 
# Set axis titles
# fig.update_yaxes(title_text="<b>Energy</b> (kWh)", secondary_y=False)
# fig.update_yaxes(title_text="<b>Current</b> (A)", secondary_y=True)
# 
# st.plotly_chart(fig, use_container_width=True)

# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots
# 
# Create subplots with 2 rows, shared X-axis
# fig = make_subplots(
    # rows=2, cols=1,
    # shared_xaxes=True,
    # vertical_spacing=0.1,
    # row_heights=[0.7, 0.3],  # 70% height for top chart, 30% for bottom
    # subplot_titles=("Current (Line Chart)", "Energy (Bar Chart)")
# )
# 
# Add line chart to top row (row=1)
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],
        # y=df['current'],
        # mode='lines+markers',
        # name='Current',
        # line=dict(color='blue', width=2),
        # marker=dict(color='white', size=8)
    # ),
    # row=1, col=1
# )
# 
# Add bar chart to bottom row (row=2)
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'],
        # y=df['energy'],
        # name='Energy',
        # marker=dict(color='red')
    # ),
    # row=2, col=1
# )
# 
# Update layout
# fig.update_layout(
    # height=600,
    # showlegend=True,
    # title_text="Energy and Current Over Time",
    # hovermode='x unified',
    # margin=dict(t=100),
    # plot_bgcolor='rgba(245,245,245,1)'
# )
# 
# Format axes
# fig.update_yaxes(title_text="Current (A)", row=1, col=1)
# fig.update_yaxes(title_text="Energy (kWh)", row=2, col=1)
# fig.update_xaxes(title_text="Time", row=2, col=1)
# 
# Remove datetime formatting issues
# fig.update_xaxes(rangeslider_visible=False)
# 
# st.plotly_chart(fig, use_container_width=True)

# import plotly.graph_objects as go 
# from plotly.subplots import make_subplots
# 
# Create subplots with adjusted proportions
# fig = make_subplots(
    # rows=2, cols=1,
    # shared_xaxes=True,
    # vertical_spacing=0,  # No space between charts
    # row_heights=[0.8, 0.2],  # 80% for line chart, 20% for bar chart
    # subplot_titles=("Current", "Energy")
# )
# 
# Line chart (Top)
# fig.add_trace(
    # go.Scatter(
        # x=df['created_at'],
        # y=df['current'],
        # mode='lines+markers',
        # name='Current',
        # line=dict(color='blue', width=2),
        # marker=dict(color='white', size=6)
    # ),
    # row=1, col=1
# )
# 
# Bar chart (Bottom)
# fig.add_trace(
    # go.Bar(
        # x=df['created_at'],
        # y=df['energy'],
        # name='Energy',
        # marker=dict(color='red', opacity=0.7)
    # ),
    # row=2, col=1
# )
# 
# Update layout
# fig.update_layout(
    # height=700,  # Increased total height
    # showlegend=False,
    # margin=dict(t=40, b=20, l=40, r=20),
    # plot_bgcolor='white'
# )
# 
# Axis formatting
# fig.update_yaxes(title_text="Current (A)", row=1, col=1, showgrid=False)
# fig.update_yaxes(title_text="Energy (kWh)", row=2, col=1, showgrid=False)
# fig.update_xaxes(showticklabels=False, row=1, col=1)  # Hide x-axis on top chart
# fig.update_xaxes(title_text="Time", row=2, col=1)
# 
# Tight layout adjustments
# fig.update_layout(
    # annotations=[
        # dict(
            # x=0.5,
            # y=-0.15,
            # showarrow=False,
            # text="Time",
            # xref="paper",
            # yref="paper"
        # )
    # ]
# )
# 
# st.plotly_chart(fig, use_container_width=True)

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

# Create subplots with Streamlit's theme colors
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0,
    row_heights=[0.8, 0.8],
    # subplot_titles=("Current", "Energy")
)

# Line chart (Top)
fig.add_trace(
    go.Scatter(
        x=df['created_at'],
        y=df['current'],
        mode='lines+markers',
        name='Current',
        line=dict(
            color='red',  # Streamlit's primary purple
            width=2.5
        ),
        marker=dict(
            color='#FFFFFF',  # White
            # size=8,
            line=dict(
                color='#FFFFFF',  # Purple border
                width=1.5
            )
        )
    ),
    row=1, col=1
)

# Bar chart (Bottom)
fig.add_trace(
    go.Bar(
        x=df['created_at'],
        y=df['hours'],
        name='Hours',
        marker=dict(
            color='blue',  # Streamlit's secondary blue
            opacity=0.9,
            # line=dict(
                # color='blue',
                # width=5
            # )
        )
    ),
    row=2, col=1
)

# Update layout to match Streamlit's theme
fig.update_layout(
    height=650,
    showlegend=False,
    margin=dict(t=40, b=20, l=40, r=20),
    plot_bgcolor="#000000",  # Match Streamlit's canvas
    paper_bgcolor="#000000",
    font=dict(
        family='Source Sans Pro, sans-serif',  # Streamlit's font
        color="#FFFFFF"  # Streamlit's text color
    ),
    hoverlabel=dict(
        bgcolor="#000000",
        font_size=14,
        font_family='Source Sans Pro, sans-serif'
    )
)

# Axis styling
fig.update_yaxes(
    title_text="Current (A)", 
    row=1, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_yaxes(
    title_text="Hours", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_xaxes(
    showticklabels=False, 
    row=1, 
    col=1, 
    linecolor='#31333F',
    showline=False,    # Remove axis line
)

fig.update_xaxes(
    title_text="Time", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color='#31333F'),
    tickfont=dict(color='#FFFFFF')
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

# Create subplots with Streamlit's theme colors
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0,
    row_heights=[0.8, 0.8],
    # subplot_titles=("Current", "Energy")
)

# Line chart (Top)
fig.add_trace(
    go.Scatter(
        x=df['created_at'],
        y=df['current'],
        mode='lines+markers',
        name='Current',
        line=dict(
            color='red',  # Streamlit's primary purple
            width=2.5
        ),
        marker=dict(
            color='#FFFFFF',  # White
            # size=8,
            line=dict(
                color='#FFFFFF',  # Purple border
                width=1.5
            )
        )
    ),
    row=1, col=1
)

# Bar chart (Bottom)
fig.add_trace(
    go.Bar(
        x=df['created_at'],
        y=df['power'],
        name='Power',
        marker=dict(
            color='blue',  # Streamlit's secondary blue
            opacity=0.9,
            # line=dict(
                # color='blue',
                # width=5
            # )
        )
    ),
    row=2, col=1
)

# Update layout to match Streamlit's theme
fig.update_layout(
    height=650,
    showlegend=False,
    margin=dict(t=40, b=20, l=40, r=20),
    plot_bgcolor="#000000",  # Match Streamlit's canvas
    paper_bgcolor="#000000",
    font=dict(
        family='Source Sans Pro, sans-serif',  # Streamlit's font
        color="#FFFFFF"  # Streamlit's text color
    ),
    hoverlabel=dict(
        bgcolor="#000000",
        font_size=14,
        font_family='Source Sans Pro, sans-serif'
    )
)

# Axis styling
fig.update_yaxes(
    title_text="Current (A)", 
    row=1, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_yaxes(
    title_text="Power (w)", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_xaxes(
    showticklabels=False, 
    row=1, 
    col=1, 
    linecolor='#31333F',
    showline=False,    # Remove axis line
)

fig.update_xaxes(
    title_text="Time", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color='#31333F'),
    tickfont=dict(color='#FFFFFF')
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit", row=2, col=1)
# 
# Tight layout adjustments
# fig.update_layout(
    # annotations=[
        # dict(
            # x=0.5,
            # y=-0.15,
            # showarrow=False,
            # text="Time",
            # xref="paper",
            # yref="paper"
        # )
    # ]
# )
# 
# st.plotly_chart(fig, use_container_width=True)

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

# Create subplots with Streamlit's theme colors
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0,
    row_heights=[0.8, 0.8],
    # subplot_titles=("Current", "Energy")
)

# Line chart (Top)
fig.add_trace(
    go.Scatter(
        x=df['created_at'],
        y=df['current'],
        mode='lines+markers',
        name='Current',
        line=dict(
            color='red',  # Streamlit's primary purple
            width=2.5
        ),
        marker=dict(
            color='#FFFFFF',  # White
            # size=8,
            line=dict(
                color='#FFFFFF',  # Purple border
                width=1.5
            )
        )
    ),
    row=1, col=1
)

# Bar chart (Bottom)
fig.add_trace(
    go.Bar(
        x=df['created_at'],
        y=df['hours'],
        name='Hours',
        marker=dict(
            color='blue',  # Streamlit's secondary blue
            opacity=0.9,
            # line=dict(
                # color='blue',
                # width=5
            # )
        )
    ),
    row=2, col=1
)

# Update layout to match Streamlit's theme
fig.update_layout(
    height=650,
    showlegend=False,
    margin=dict(t=40, b=20, l=40, r=20),
    plot_bgcolor="#000000",  # Match Streamlit's canvas
    paper_bgcolor="#000000",
    font=dict(
        family='Source Sans Pro, sans-serif',  # Streamlit's font
        color="#FFFFFF"  # Streamlit's text color
    ),
    hoverlabel=dict(
        bgcolor="#000000",
        font_size=14,
        font_family='Source Sans Pro, sans-serif'
    )
)

# Axis styling
fig.update_yaxes(
    title_text="Current (A)", 
    row=1, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_yaxes(
    title_text="Hours", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_xaxes(
    showticklabels=False, 
    row=1, 
    col=1, 
    linecolor='#31333F',
    showline=False,    # Remove axis line
)

fig.update_xaxes(
    title_text="Time", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color='#31333F'),
    tickfont=dict(color='#FFFFFF')
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")

import plotly.graph_objects as go 
from plotly.subplots import make_subplots

# Create subplots with Streamlit's theme colors
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0,
    row_heights=[0.8, 0.8],
    # subplot_titles=("Current", "Energy")
)

# Line chart (Top)
fig.add_trace(
    go.Scatter(
        x=df['created_at'],
        y=df['current'],
        mode='lines+markers',
        name='Current',
        line=dict(
            color='red',  # Streamlit's primary purple
            width=2.5
        ),
        marker=dict(
            color='#FFFFFF',  # White
            # size=8,
            line=dict(
                color='#FFFFFF',  # Purple border
                width=1.5
            )
        )
    ),
    row=1, col=1
)

# Bar chart (Bottom)
fig.add_trace(
    go.Bar(
        x=df['created_at'],
        y=df['power'],
        name='Power',
        marker=dict(
            color='blue',  # Streamlit's secondary blue
            opacity=0.9,
            # line=dict(
                # color='blue',
                # width=5
            # )
        )
    ),
    row=2, col=1
)

# Update layout to match Streamlit's theme
fig.update_layout(
    height=650,
    showlegend=False,
    margin=dict(t=40, b=20, l=40, r=20),
    plot_bgcolor="#000000",  # Match Streamlit's canvas
    paper_bgcolor="#000000",
    font=dict(
        family='Source Sans Pro, sans-serif',  # Streamlit's font
        color="#FFFFFF"  # Streamlit's text color
    ),
    hoverlabel=dict(
        bgcolor="#000000",
        font_size=14,
        font_family='Source Sans Pro, sans-serif'
    )
)

# Axis styling
fig.update_yaxes(
    title_text="Current (A)", 
    row=1, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_yaxes(
    title_text="Power (w)", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color="#FFFFFF"),
    tickfont=dict(color="#FFFFFF")
)

fig.update_xaxes(
    showticklabels=False, 
    row=1, 
    col=1, 
    linecolor='#31333F',
    showline=False,    # Remove axis line
)

fig.update_xaxes(
    title_text="Time", 
    row=2, 
    col=1, 
    gridcolor='#31333F',
    title_font=dict(color='#31333F'),
    tickfont=dict(color='#FFFFFF')
)

st.plotly_chart(fig, use_container_width=True, theme="streamlit")
