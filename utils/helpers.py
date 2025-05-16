import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
from datetime import datetime, timedelta
from config.config import CONFIG

# Helper function to get fully qualified object names
def get_fully_qualified_name(object_name, include_db=True):
    """
    Generate fully qualified name for database objects.
    Args:
        object_name: The name of the table/sequence/procedure
        include_db: Whether to include database name in the path
    Returns:
        Fully qualified name (e.g., "DATABASE.SCHEMA.OBJECT" or "SCHEMA.OBJECT")
    """
    if include_db:
        return f"{CONFIG['DATABASE']['NAME']}.{CONFIG['DATABASE']['SCHEMA']}.{object_name}"
    return f"{CONFIG['DATABASE']['SCHEMA']}.{object_name}"

# Get Snowflake session
def get_snowflake_session():
    try:
        session = get_active_session()
        if session is None:
            st.error("Failed to get active Snowpark session. Ensure you are running this in a Snowflake-connected environment.")
            return None
        return session
    except Exception as e:
        st.error(f"Error establishing Snowflake session: {e}")
        return None

# Get current Snowflake user
def get_current_snowflake_user() -> str:
    """Gets the current Snowflake user."""
    try:
        session = get_snowflake_session()
        if session:
            return session.sql("SELECT CURRENT_USER()").collect()[0][0]
    except Exception:
        pass
    return "UNKNOWN_USER"

# Get current Snowflake role
def get_current_snowflake_role() -> str:
    """Safely get the current role from the session."""
    try:
        session = get_snowflake_session()
        if session:
            return session.sql("SELECT CURRENT_ROLE()").collect()[0][0]
    except Exception:
        pass
    return "UNKNOWN_ROLE"

# Log audit event
def log_audit_event(
    event_type: str,
    object_name: str,
    sql_command: str,
    status: str,
    message: str = "",
    invoked_by_role: str = None,
    invoked_by_user: str = None,
) -> int:
    """Logs an audit event to the AUDIT_LOG_TABLE and returns the event_id."""
    session = get_snowflake_session()
    if not session:
        return None

    if invoked_by_role is None:
        invoked_by_role = get_current_snowflake_role()
    if invoked_by_user is None:
        invoked_by_user = get_current_snowflake_user()

    event_id = None
    try:
        audit_log_sequence = get_fully_qualified_name(CONFIG["TABLES"]["AUDIT_LOG_SEQUENCE"])
        audit_log_table = get_fully_qualified_name(CONFIG["TABLES"]["AUDIT_LOG"])
        
        event_id_result = session.sql(f"SELECT {audit_log_sequence}.NEXTVAL AS ID").collect()
        if not event_id_result:
            st.warning(f"Audit logging failed for '{event_type}': Could not retrieve next event ID from sequence.")
            return None
        event_id = event_id_result[0]["ID"]

        insert_sql = f"""
            INSERT INTO {audit_log_table} (
                EVENT_ID, EVENT_TIME, INVOKED_BY, INVOKED_BY_ROLE, EVENT_TYPE,
                OBJECT_NAME, SQL_COMMAND, STATUS, MESSAGE
            ) VALUES (
                {event_id}, CURRENT_TIMESTAMP(), '{invoked_by_user}', '{invoked_by_role}',
                '{event_type}', '{object_name}', $${sql_command}$$, '{status}', $${message}$$
            )
        """
        session.sql(insert_sql).collect()
        return event_id
    except Exception as e:
        return event_id

# Log role hierarchy event
def log_role_hierarchy_event(
    audit_event_id: int,
    invoked_by: str,
    environment_name: str,
    created_role_name: str,
    created_role_type: str,
    mapped_database_role: str,
    parent_account_role: str,
    sql_command_create_role: str,
    sql_command_grant_db_role: str,
    sql_command_grant_ownership: str,
    status: str,
    message: str = "",
):
    """Logs an event to the ROLE_HIERARCHY_LOG table."""
    session = get_snowflake_session()
    if not session:
        return None

    try:
        role_hierarchy_log_sequence = get_fully_qualified_name(CONFIG["TABLES"]["ROLE_HIERARCHY_LOG_SEQUENCE"])
        role_hierarchy_log_table = get_fully_qualified_name(CONFIG["TABLES"]["ROLE_HIERARCHY_LOG"])
        
        log_id_result = session.sql(f"SELECT {role_hierarchy_log_sequence}.NEXTVAL AS ID").collect()
        if not log_id_result:
            st.warning(f"Role hierarchy logging failed for '{created_role_name}': Could not retrieve LOG_ID from sequence.")
            return
        log_id = log_id_result[0]["ID"]

        insert_sql = f"""
            INSERT INTO {role_hierarchy_log_table} (
                LOG_ID, EVENT_TIME, AUDIT_EVENT_ID, INVOKED_BY, ENVIRONMENT_NAME,
                CREATED_ROLE_NAME, CREATED_ROLE_TYPE, MAPPED_DATABASE_ROLE,
                PARENT_ACCOUNT_ROLE, SQL_COMMAND_CREATE_ROLE, SQL_COMMAND_GRANT_DB_ROLE,
                SQL_COMMAND_GRANT_OWNERSHIP, STATUS, MESSAGE
            ) VALUES (
                {log_id}, CURRENT_TIMESTAMP(), {audit_event_id if audit_event_id else "NULL"},
                '{invoked_by}', '{environment_name}', '{created_role_name}',
                '{created_role_type}', '{mapped_database_role}', '{parent_account_role}',
                $${sql_command_create_role}$$, $${sql_command_grant_db_role}$$,
                $${sql_command_grant_ownership}$$, '{status}', $${message}$$
            )
        """
        session.sql(insert_sql).collect()
    except Exception as e:
        return audit_event_id

# Configure dark mode charts
def configure_dark_mode_charts(fig):
    """Configure charts to be dark-mode friendly"""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#4A4A4A"),
        yaxis=dict(gridcolor="#4A4A4A")
    )
    return fig 