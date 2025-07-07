"""
Utility functions for data visualization and analysis
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any

def create_sales_chart(data: List[Dict], title: str = "Sales Chart") -> str:
    """
    Create a sales chart using Plotly
    
    Args:
        data: List of dictionaries containing sales data
        title: Chart title
        
    Returns:
        HTML string for the chart
    """
    if not data:
        return "<p>No data available for chart</p>"
    
    df = pd.DataFrame(data)
    
    if 'month' in df.columns and 'revenue' in df.columns:
        fig = px.line(df, x='month', y='revenue', title=title)
    elif 'category_name' in df.columns and 'revenue' in df.columns:
        fig = px.bar(df, x='category_name', y='revenue', title=title)
    else:
        fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=title)
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="Revenue ($)",
        template="plotly_white"
    )
    
    return fig.to_html(include_plotlyjs='cdn')

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"

def get_color_palette(n: int) -> List[str]:
    """Get a color palette for charts"""
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    return colors[:n] if n <= len(colors) else colors * (n // len(colors) + 1)[:n]
