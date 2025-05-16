import streamlit as st
from snowflake.snowpark.context import get_active_session
from config.config import CONFIG
from utils.helpers import get_fully_qualified_name, log_audit_event

def ui_create_warehouse():
    st.markdown("## Create Warehouse")
    
    with st.form("create_warehouse_form"):
        warehouse_name = st.text_input("Warehouse Name")
        
        # Warehouse size options
        warehouse_size = st.selectbox(
            "Warehouse Size",
            ["XSMALL", "SMALL", "MEDIUM", "LARGE", "XLARGE", "2XLARGE", "3XLARGE", "4XLARGE"]
        )
        
        # Auto-suspend options
        auto_suspend = st.number_input(
            "Auto-suspend (seconds)",
            min_value=60,
            max_value=86400,
            value=300,
            step=60
        )
        
        # Auto-resume options
        auto_resume = st.checkbox("Auto-resume", value=True)
        
        # Scaling policy
        scaling_policy = st.selectbox(
            "Scaling Policy",
            ["STANDARD", "ECONOMY"]
        )
        
        # Comment
        comment = st.text_area("Comment (optional)")
        
        submitted = st.form_submit_button("Create Warehouse")
        
        if submitted:
            if not warehouse_name:
                st.error("Warehouse name is required")
                return
            
            try:
                session = get_active_session()
                
                # Build the CREATE WAREHOUSE command
                create_cmd = f"""
                CREATE WAREHOUSE {warehouse_name}
                WAREHOUSE_SIZE = {warehouse_size}
                AUTO_SUSPEND = {auto_suspend}
                AUTO_RESUME = {str(auto_resume).upper()}
                SCALING_POLICY = {scaling_policy}
                """
                
                if comment:
                    create_cmd += f" COMMENT = '{comment}'"
                
                # Execute the command
                session.sql(create_cmd).collect()
                
                # Log the event
                log_audit_event(
                    event_type="CREATE_WAREHOUSE",
                    object_name=warehouse_name,
                    sql_command=create_cmd,
                    status="SUCCESS"
                )
                
                st.success(f"Warehouse '{warehouse_name}' created successfully!")
                
            except Exception as e:
                st.error(f"Error creating warehouse: {str(e)}")
                log_audit_event(
                    event_type="CREATE_WAREHOUSE",
                    object_name=warehouse_name,
                    sql_command=create_cmd,
                    status="FAILED",
                    message=str(e)
                ) 