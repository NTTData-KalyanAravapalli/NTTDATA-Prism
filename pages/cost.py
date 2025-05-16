import streamlit as st
from snowflake.snowpark.context import get_active_session
from config.config import CONFIG
from utils.helpers import get_fully_qualified_name, log_audit_event, configure_dark_mode_charts
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def ui_cost_analysis():
    st.markdown("## Cost Analysis")
    
    try:
        session = get_active_session()
        
        # Date range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                datetime.now() - timedelta(days=30)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                datetime.now()
            )
        
        # Warehouse usage analysis
        st.markdown("### Warehouse Usage Analysis")
        
        warehouse_usage = session.sql(f"""
            SELECT 
                WAREHOUSE_NAME,
                DATE_TRUNC('HOUR', START_TIME) as HOUR,
                SUM(CREDITS_USED) as CREDITS_USED
            FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
            WHERE START_TIME >= '{start_date}'
            AND START_TIME <= '{end_date}'
            GROUP BY WAREHOUSE_NAME, HOUR
            ORDER BY HOUR
        """).collect()
        
        if warehouse_usage:
            # Convert to DataFrame
            import pandas as pd
            df = pd.DataFrame(warehouse_usage)
            
            # Create line chart
            fig = px.line(
                df,
                x="HOUR",
                y="CREDITS_USED",
                color="WAREHOUSE_NAME",
                title="Warehouse Credit Usage Over Time"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            st.markdown("### Summary Statistics")
            summary = df.groupby("WAREHOUSE_NAME").agg({
                "CREDITS_USED": ["sum", "mean", "max"]
            }).round(2)
            summary.columns = ["Total Credits", "Average Credits", "Max Credits"]
            st.dataframe(summary)
        
        # Storage usage analysis
        st.markdown("### Storage Usage Analysis")
        
        storage_usage = session.sql(f"""
            SELECT 
                DATABASE_NAME,
                SCHEMA_NAME,
                ACTIVE_BYTES,
                TIME_TRAVEL_BYTES,
                FAILSAFE_BYTES,
                STORAGE_BYTES
            FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE
            WHERE USAGE_DATE >= '{start_date}'
            AND USAGE_DATE <= '{end_date}'
            ORDER BY STORAGE_BYTES DESC
        """).collect()
        
        if storage_usage:
            # Convert to DataFrame
            df_storage = pd.DataFrame(storage_usage)
            
            # Convert bytes to GB
            for col in ["ACTIVE_BYTES", "TIME_TRAVEL_BYTES", "FAILSAFE_BYTES", "STORAGE_BYTES"]:
                df_storage[col] = df_storage[col] / (1024 * 1024 * 1024)
            
            # Create bar chart
            fig = px.bar(
                df_storage,
                x="DATABASE_NAME",
                y="STORAGE_BYTES",
                title="Storage Usage by Database (GB)"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Storage breakdown
            st.markdown("### Storage Breakdown")
            storage_breakdown = df_storage.melt(
                id_vars=["DATABASE_NAME", "SCHEMA_NAME"],
                value_vars=["ACTIVE_BYTES", "TIME_TRAVEL_BYTES", "FAILSAFE_BYTES"],
                var_name="Storage Type",
                value_name="Size (GB)"
            )
            
            fig = px.bar(
                storage_breakdown,
                x="DATABASE_NAME",
                y="Size (GB)",
                color="Storage Type",
                title="Storage Breakdown by Type (GB)"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        # Query history analysis
        st.markdown("### Query History Analysis")
        
        query_history = session.sql(f"""
            SELECT 
                DATE_TRUNC('HOUR', START_TIME) as HOUR,
                WAREHOUSE_NAME,
                COUNT(*) as QUERY_COUNT,
                AVG(EXECUTION_TIME) as AVG_EXECUTION_TIME,
                SUM(CREDITS_USED) as CREDITS_USED
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
            WHERE START_TIME >= '{start_date}'
            AND START_TIME <= '{end_date}'
            GROUP BY HOUR, WAREHOUSE_NAME
            ORDER BY HOUR
        """).collect()
        
        if query_history:
            # Convert to DataFrame
            df_queries = pd.DataFrame(query_history)
            
            # Create line chart for query count
            fig = px.line(
                df_queries,
                x="HOUR",
                y="QUERY_COUNT",
                color="WAREHOUSE_NAME",
                title="Query Count Over Time"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Create line chart for average execution time
            fig = px.line(
                df_queries,
                x="HOUR",
                y="AVG_EXECUTION_TIME",
                color="WAREHOUSE_NAME",
                title="Average Query Execution Time Over Time"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            st.markdown("### Query Summary Statistics")
            summary = df_queries.groupby("WAREHOUSE_NAME").agg({
                "QUERY_COUNT": "sum",
                "AVG_EXECUTION_TIME": "mean",
                "CREDITS_USED": "sum"
            }).round(2)
            summary.columns = ["Total Queries", "Average Execution Time", "Total Credits"]
            st.dataframe(summary)
            
    except Exception as e:
        st.error(f"Error analyzing costs: {str(e)}") 