import streamlit as st
from snowflake.snowpark.context import get_active_session
from config.config import CONFIG, ROLE_TYPES
from utils.helpers import get_fully_qualified_name, log_audit_event, log_role_hierarchy_event

def ui_create_role():
    st.markdown("## Create Role")
    
    with st.form("create_role_form"):
        role_name = st.text_input("Role Name")
        role_type = st.selectbox("Role Type", ROLE_TYPES)
        parent_role = st.text_input("Parent Role (optional)")
        comment = st.text_area("Comment (optional)")
        
        submitted = st.form_submit_button("Create Role")
        
        if submitted:
            if not role_name:
                st.error("Role name is required")
                return
            
            try:
                session = get_active_session()
                
                # Build the CREATE ROLE command
                create_cmd = f"CREATE ROLE {role_name}"
                if comment:
                    create_cmd += f" COMMENT = '{comment}'"
                
                # Execute the command
                session.sql(create_cmd).collect()
                
                # If parent role is specified, grant it
                if parent_role:
                    grant_cmd = f"GRANT ROLE {parent_role} TO ROLE {role_name}"
                    session.sql(grant_cmd).collect()
                
                # Log the events
                log_audit_event(
                    event_type="CREATE_ROLE",
                    object_name=role_name,
                    sql_command=create_cmd,
                    status="SUCCESS"
                )
                
                if parent_role:
                    log_role_hierarchy_event(
                        parent_role=parent_role,
                        child_role=role_name,
                        action="GRANT"
                    )
                
                st.success(f"Role '{role_name}' created successfully!")
                
            except Exception as e:
                st.error(f"Error creating role: {str(e)}")
                log_audit_event(
                    event_type="CREATE_ROLE",
                    object_name=role_name,
                    sql_command=create_cmd,
                    status="FAILED",
                    message=str(e)
                )

def ui_assign_roles():
    st.markdown("## Assign Roles")
    
    try:
        session = get_active_session()
        
        # Get list of existing roles
        roles = session.sql("SHOW ROLES").collect()
        role_list = [row["name"] for row in roles]
        
        with st.form("assign_roles_form"):
            target_role = st.selectbox("Target Role", role_list)
            roles_to_grant = st.multiselect("Roles to Grant", role_list)
            
            submitted = st.form_submit_button("Assign Roles")
            
            if submitted:
                if not roles_to_grant:
                    st.error("Please select at least one role to grant")
                    return
                
                try:
                    for role in roles_to_grant:
                        grant_cmd = f"GRANT ROLE {role} TO ROLE {target_role}"
                        session.sql(grant_cmd).collect()
                        
                        # Log the event
                        log_role_hierarchy_event(
                            parent_role=role,
                            child_role=target_role,
                            action="GRANT"
                        )
                    
                    st.success(f"Roles assigned successfully to '{target_role}'!")
                    
                except Exception as e:
                    st.error(f"Error assigning roles: {str(e)}")
                    
    except Exception as e:
        st.error(f"Error fetching roles: {str(e)}")

def ui_assign_database_roles():
    st.markdown("## Assign Database Roles")
    
    try:
        session = get_active_session()
        
        # Get list of existing roles and databases
        roles = session.sql("SHOW ROLES").collect()
        databases = session.sql("SHOW DATABASES").collect()
        
        role_list = [row["name"] for row in roles]
        database_list = [row["name"] for row in databases]
        
        with st.form("assign_database_roles_form"):
            target_role = st.selectbox("Target Role", role_list)
            database = st.selectbox("Database", database_list)
            
            # Database privileges
            privileges = st.multiselect(
                "Database Privileges",
                ["USAGE", "CREATE SCHEMA", "IMPORT SHARE", "MODIFY", "MONITOR", "OWNERSHIP", "REFERENCE_USAGE"]
            )
            
            submitted = st.form_submit_button("Assign Database Roles")
            
            if submitted:
                if not privileges:
                    st.error("Please select at least one privilege")
                    return
                
                try:
                    for privilege in privileges:
                        grant_cmd = f"GRANT {privilege} ON DATABASE {database} TO ROLE {target_role}"
                        session.sql(grant_cmd).collect()
                        
                        # Log the event
                        log_audit_event(
                            event_type="GRANT_DATABASE_PRIVILEGE",
                            object_name=database,
                            sql_command=grant_cmd,
                            status="SUCCESS"
                        )
                    
                    st.success(f"Database privileges assigned successfully to '{target_role}'!")
                    
                except Exception as e:
                    st.error(f"Error assigning database privileges: {str(e)}")
                    
    except Exception as e:
        st.error(f"Error fetching roles or databases: {str(e)}")

def ui_revoke_roles():
    st.markdown("## Revoke Roles")
    
    try:
        session = get_active_session()
        
        # Get list of existing roles
        roles = session.sql("SHOW ROLES").collect()
        role_list = [row["name"] for row in roles]
        
        with st.form("revoke_roles_form"):
            target_role = st.selectbox("Target Role", role_list)
            roles_to_revoke = st.multiselect("Roles to Revoke", role_list)
            
            submitted = st.form_submit_button("Revoke Roles")
            
            if submitted:
                if not roles_to_revoke:
                    st.error("Please select at least one role to revoke")
                    return
                
                try:
                    for role in roles_to_revoke:
                        revoke_cmd = f"REVOKE ROLE {role} FROM ROLE {target_role}"
                        session.sql(revoke_cmd).collect()
                        
                        # Log the event
                        log_role_hierarchy_event(
                            parent_role=role,
                            child_role=target_role,
                            action="REVOKE"
                        )
                    
                    st.success(f"Roles revoked successfully from '{target_role}'!")
                    
                except Exception as e:
                    st.error(f"Error revoking roles: {str(e)}")
                    
    except Exception as e:
        st.error(f"Error fetching roles: {str(e)}")

def ui_create_environment_roles():
    st.markdown("## Create Environment Roles")
    
    with st.form("create_environment_roles_form"):
        environment = st.selectbox("Environment", ["DEV", "TEST", "PROD"])
        role_prefix = st.text_input("Role Prefix")
        
        submitted = st.form_submit_button("Create Environment Roles")
        
        if submitted:
            if not role_prefix:
                st.error("Role prefix is required")
                return
            
            try:
                session = get_active_session()
                
                # Create environment-specific roles
                roles = [
                    f"{role_prefix}_{environment}_ADMIN",
                    f"{role_prefix}_{environment}_DEVELOPER",
                    f"{role_prefix}_{environment}_ANALYST",
                    f"{role_prefix}_{environment}_VIEWER"
                ]
                
                for role in roles:
                    create_cmd = f"CREATE ROLE {role}"
                    session.sql(create_cmd).collect()
                    
                    # Log the event
                    log_audit_event(
                        event_type="CREATE_ENVIRONMENT_ROLE",
                        object_name=role,
                        sql_command=create_cmd,
                        status="SUCCESS"
                    )
                
                st.success(f"Environment roles created successfully for {environment}!")
                
            except Exception as e:
                st.error(f"Error creating environment roles: {str(e)}")

def ui_show_role_hierarchy():
    st.markdown("## Role Hierarchy")
    
    try:
        session = get_active_session()
        
        # Get role hierarchy data
        hierarchy_data = session.sql("""
            SELECT 
                GRANTED_TO as role,
                GRANTEE_NAME as granted_role
            FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
            WHERE GRANTED_TO != GRANTEE_NAME
            ORDER BY role, granted_role
        """).collect()
        
        if hierarchy_data:
            # Convert to DataFrame for better display
            import pandas as pd
            df = pd.DataFrame(hierarchy_data)
            st.dataframe(df)
            
            # Create a hierarchical view
            st.markdown("### Hierarchical View")
            for role in df["role"].unique():
                st.markdown(f"#### {role}")
                granted_roles = df[df["role"] == role]["granted_role"].tolist()
                for granted_role in granted_roles:
                    st.markdown(f"- {granted_role}")
        else:
            st.info("No role hierarchy data available")
            
    except Exception as e:
        st.error(f"Error fetching role hierarchy: {str(e)}")

def ui_display_rbac_architecture():
    st.markdown("## RBAC Architecture")
    
    st.markdown("""
    ### Role-Based Access Control (RBAC) Architecture
    
    The RBAC architecture in this application follows a hierarchical structure:
    
    1. **System Roles**
       - ACCOUNTADMIN
       - SECURITYADMIN
       - USERADMIN
       - SYSADMIN
    
    2. **Environment Roles**
       - {prefix}_DEV_*
       - {prefix}_TEST_*
       - {prefix}_PROD_*
    
    3. **Functional Roles**
       - ADMIN
       - DEVELOPER
       - ANALYST
       - VIEWER
    
    4. **Database Roles**
       - Database-specific privileges
       - Schema-level access
    
    ### Role Hierarchy Rules
    
    1. System roles are at the top of the hierarchy
    2. Environment roles inherit from system roles
    3. Functional roles inherit from environment roles
    4. Database roles are assigned to functional roles
    
    ### Best Practices
    
    1. Always use the principle of least privilege
    2. Regularly audit role assignments
    3. Document role hierarchies
    4. Use role naming conventions
    5. Implement role-based security policies
    """) 