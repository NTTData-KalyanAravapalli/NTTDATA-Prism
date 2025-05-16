import streamlit as st
from snowflake.snowpark.context import get_active_session
from config.config import CONFIG
from utils.helpers import get_fully_qualified_name, log_audit_event

def ui_create_database():
    st.markdown("## Create Database")
    
    with st.form("create_database_form"):
        database_name = st.text_input("Database Name")
        clone_source = st.text_input("Clone From (optional)")
        comment = st.text_area("Comment (optional)")
        
        submitted = st.form_submit_button("Create Database")
        
        if submitted:
            if not database_name:
                st.error("Database name is required")
                return
            
            try:
                session = get_active_session()
                
                # Build the CREATE DATABASE command
                create_cmd = f"CREATE DATABASE {database_name}"
                if clone_source:
                    create_cmd += f" CLONE {clone_source}"
                if comment:
                    create_cmd += f" COMMENT = '{comment}'"
                
                # Execute the command
                session.sql(create_cmd).collect()
                
                # Log the event
                log_audit_event(
                    event_type="CREATE_DATABASE",
                    object_name=database_name,
                    sql_command=create_cmd,
                    status="SUCCESS"
                )
                
                st.success(f"Database '{database_name}' created successfully!")
                
            except Exception as e:
                st.error(f"Error creating database: {str(e)}")
                log_audit_event(
                    event_type="CREATE_DATABASE",
                    object_name=database_name,
                    sql_command=create_cmd,
                    status="FAILED",
                    message=str(e)
                )

def ui_clone_database():
    st.markdown("## Clone Database")
    
    try:
        session = get_active_session()
        
        # Get list of existing databases
        databases = session.sql("SHOW DATABASES").collect()
        database_list = [row["name"] for row in databases]
        
        with st.form("clone_database_form"):
            source_database = st.selectbox("Source Database", database_list)
            new_database_name = st.text_input("New Database Name")
            comment = st.text_area("Comment (optional)")
            
            submitted = st.form_submit_button("Clone Database")
            
            if submitted:
                if not new_database_name:
                    st.error("New database name is required")
                    return
                
                try:
                    # Build the CLONE DATABASE command
                    clone_cmd = f"CREATE DATABASE {new_database_name} CLONE {source_database}"
                    if comment:
                        clone_cmd += f" COMMENT = '{comment}'"
                    
                    # Execute the command
                    session.sql(clone_cmd).collect()
                    
                    # Log the event
                    log_audit_event(
                        event_type="CLONE_DATABASE",
                        object_name=new_database_name,
                        sql_command=clone_cmd,
                        status="SUCCESS"
                    )
                    
                    st.success(f"Database '{new_database_name}' cloned successfully from '{source_database}'!")
                    
                except Exception as e:
                    st.error(f"Error cloning database: {str(e)}")
                    log_audit_event(
                        event_type="CLONE_DATABASE",
                        object_name=new_database_name,
                        sql_command=clone_cmd,
                        status="FAILED",
                        message=str(e)
                    )
                    
    except Exception as e:
        st.error(f"Error fetching databases: {str(e)}")

def ui_delete_database():
    st.markdown("## Delete Database")
    
    try:
        session = get_active_session()
        
        # Get list of existing databases
        databases = session.sql("SHOW DATABASES").collect()
        database_list = [row["name"] for row in databases]
        
        with st.form("delete_database_form"):
            database_to_delete = st.selectbox("Select Database to Delete", database_list)
            confirm_delete = st.checkbox("I confirm that I want to delete this database")
            
            submitted = st.form_submit_button("Delete Database")
            
            if submitted:
                if not confirm_delete:
                    st.error("Please confirm the deletion")
                    return
                
                try:
                    # Build the DROP DATABASE command
                    drop_cmd = f"DROP DATABASE {database_to_delete}"
                    
                    # Execute the command
                    session.sql(drop_cmd).collect()
                    
                    # Log the event
                    log_audit_event(
                        event_type="DELETE_DATABASE",
                        object_name=database_to_delete,
                        sql_command=drop_cmd,
                        status="SUCCESS"
                    )
                    
                    st.success(f"Database '{database_to_delete}' deleted successfully!")
                    
                except Exception as e:
                    st.error(f"Error deleting database: {str(e)}")
                    log_audit_event(
                        event_type="DELETE_DATABASE",
                        object_name=database_to_delete,
                        sql_command=drop_cmd,
                        status="FAILED",
                        message=str(e)
                    )
                    
    except Exception as e:
        st.error(f"Error fetching databases: {str(e)}") 