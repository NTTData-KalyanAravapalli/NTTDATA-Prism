import streamlit as st
from snowflake.snowpark.context import get_active_session
from config.config import CONFIG
from utils.helpers import get_fully_qualified_name, log_audit_event, configure_dark_mode_charts
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def ui_audit_logs():
    st.markdown("## Audit Logs")
    
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
        
        # Event type filter
        event_types = session.sql("""
            SELECT DISTINCT EVENT_TYPE
            FROM AUDIT_LOG_TABLE
            ORDER BY EVENT_TYPE
        """).collect()
        event_type_list = [row["EVENT_TYPE"] for row in event_types]
        
        selected_event_types = st.multiselect(
            "Event Types",
            event_type_list,
            default=event_type_list
        )
        
        # Build the query
        query = f"""
            SELECT 
                EVENT_ID,
                EVENT_TYPE,
                OBJECT_NAME,
                SQL_COMMAND,
                STATUS,
                MESSAGE,
                USER_NAME,
                ROLE_NAME,
                TIMESTAMP
            FROM AUDIT_LOG_TABLE
            WHERE TIMESTAMP >= '{start_date}'
            AND TIMESTAMP <= '{end_date}'
        """
        
        if selected_event_types:
            event_types_str = "', '".join(selected_event_types)
            query += f" AND EVENT_TYPE IN ('{event_types_str}')"
        
        query += " ORDER BY TIMESTAMP DESC"
        
        # Execute the query
        audit_logs = session.sql(query).collect()
        
        if audit_logs:
            # Convert to DataFrame
            import pandas as pd
            df = pd.DataFrame(audit_logs)
            
            # Display raw logs
            st.markdown("### Audit Logs")
            st.dataframe(df)
            
            # Event type distribution
            st.markdown("### Event Type Distribution")
            event_counts = df["EVENT_TYPE"].value_counts()
            
            fig = px.pie(
                values=event_counts.values,
                names=event_counts.index,
                title="Event Type Distribution"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Status distribution
            st.markdown("### Status Distribution")
            status_counts = df["STATUS"].value_counts()
            
            fig = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Status Distribution"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Events over time
            st.markdown("### Events Over Time")
            df["HOUR"] = pd.to_datetime(df["TIMESTAMP"]).dt.floor("H")
            hourly_events = df.groupby(["HOUR", "EVENT_TYPE"]).size().reset_index(name="COUNT")
            
            fig = px.line(
                hourly_events,
                x="HOUR",
                y="COUNT",
                color="EVENT_TYPE",
                title="Events Over Time"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # User activity
            st.markdown("### User Activity")
            user_activity = df.groupby("USER_NAME").size().reset_index(name="EVENT_COUNT")
            user_activity = user_activity.sort_values("EVENT_COUNT", ascending=False)
            
            fig = px.bar(
                user_activity,
                x="USER_NAME",
                y="EVENT_COUNT",
                title="User Activity"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Role activity
            st.markdown("### Role Activity")
            role_activity = df.groupby("ROLE_NAME").size().reset_index(name="EVENT_COUNT")
            role_activity = role_activity.sort_values("EVENT_COUNT", ascending=False)
            
            fig = px.bar(
                role_activity,
                x="ROLE_NAME",
                y="EVENT_COUNT",
                title="Role Activity"
            )
            configure_dark_mode_charts(fig)
            st.plotly_chart(fig, use_container_width=True)
            
            # Export functionality
            st.markdown("### Export Data")
            if st.button("Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="audit_logs.csv",
                    mime="text/csv"
                )
        else:
            st.info("No audit logs found for the selected criteria")
            
    except Exception as e:
        st.error(f"Error fetching audit logs: {str(e)}") 