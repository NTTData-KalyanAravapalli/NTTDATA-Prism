import streamlit as st
from snowflake.snowpark.context import get_active_session
from config.config import CONFIG
from utils.helpers import get_fully_qualified_name, log_audit_event

def ui_manage_metadata():
    st.markdown("## Metadata Management")
    
    try:
        session = get_active_session()
        
        # Get list of databases
        databases = session.sql("SHOW DATABASES").collect()
        database_list = [row["name"] for row in databases]
        
        selected_database = st.selectbox("Select Database", database_list)
        
        if selected_database:
            # Get schemas in the selected database
            schemas = session.sql(f"SHOW SCHEMAS IN DATABASE {selected_database}").collect()
            schema_list = [row["name"] for row in schemas]
            
            selected_schema = st.selectbox("Select Schema", schema_list)
            
            if selected_schema:
                # Get objects in the selected schema
                objects = session.sql(f"""
                    SELECT 
                        TABLE_NAME as name,
                        TABLE_TYPE as type
                    FROM {selected_database}.INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = '{selected_schema}'
                    UNION ALL
                    SELECT 
                        VIEW_NAME as name,
                        'VIEW' as type
                    FROM {selected_database}.INFORMATION_SCHEMA.VIEWS
                    WHERE TABLE_SCHEMA = '{selected_schema}'
                """).collect()
                
                if objects:
                    # Convert to DataFrame for better display
                    import pandas as pd
                    df = pd.DataFrame(objects)
                    
                    # Display objects
                    st.markdown("### Objects in Schema")
                    st.dataframe(df)
                    
                    # Object details
                    selected_object = st.selectbox("Select Object", df["name"].tolist())
                    
                    if selected_object:
                        # Get object details
                        object_type = df[df["name"] == selected_object]["type"].iloc[0]
                        
                        if object_type in ["BASE TABLE", "VIEW"]:
                            # Get columns
                            columns = session.sql(f"""
                                SELECT 
                                    COLUMN_NAME,
                                    DATA_TYPE,
                                    CHARACTER_MAXIMUM_LENGTH,
                                    IS_NULLABLE,
                                    COLUMN_DEFAULT
                                FROM {selected_database}.INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_SCHEMA = '{selected_schema}'
                                AND TABLE_NAME = '{selected_object}'
                                ORDER BY ORDINAL_POSITION
                            """).collect()
                            
                            if columns:
                                st.markdown("### Column Information")
                                st.dataframe(pd.DataFrame(columns))
                            
                            # Get object properties
                            properties = session.sql(f"""
                                SHOW {object_type}S LIKE '{selected_object}' IN SCHEMA {selected_database}.{selected_schema}
                            """).collect()
                            
                            if properties:
                                st.markdown("### Object Properties")
                                st.dataframe(pd.DataFrame(properties))
                            
                            # Get object grants
                            grants = session.sql(f"""
                                SHOW GRANTS ON {object_type} {selected_database}.{selected_schema}.{selected_object}
                            """).collect()
                            
                            if grants:
                                st.markdown("### Object Grants")
                                st.dataframe(pd.DataFrame(grants))
                        else:
                            st.info(f"Object type {object_type} is not supported for detailed view")
                else:
                    st.info(f"No objects found in schema {selected_schema}")
        else:
            st.info("Please select a database to view metadata")
            
    except Exception as e:
        st.error(f"Error fetching metadata: {str(e)}") 