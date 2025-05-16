import streamlit as st
from config.config import CONFIG

def ui_about():
    st.markdown("## About NTTDATA-Prism")
    st.markdown("""
    NTTDATA-Prism is a comprehensive Snowflake management application that provides a user-friendly interface
    for managing various aspects of your Snowflake environment.
    """)
    
    st.markdown("### Key Features")
    
    # Database Management
    st.markdown("#### Database Management")
    st.markdown("""
    - Create new databases with custom configurations
    - Clone existing databases for testing or development
    - Delete databases when no longer needed
    """)
    
    # Warehouse Management
    st.markdown("#### Warehouse Management")
    st.markdown("""
    - Create and configure warehouses
    - Set up warehouse parameters for optimal performance
    """)
    
    # Role Management
    st.markdown("#### Role Management")
    st.markdown("""
    - Create and manage roles
    - Assign roles to users and other roles
    - Manage database-specific roles
    - View and maintain role hierarchy
    - Implement RBAC (Role-Based Access Control) architecture
    """)
    
    # Additional Features
    st.markdown("#### Additional Features")
    st.markdown("""
    - Metadata management for better organization
    - Cost analysis tools for budget tracking
    - Comprehensive audit logging
    """)
    
    st.markdown("### Technology Stack")
    st.markdown("""
    - **Frontend**: Streamlit
    - **Backend**: Python
    - **Database**: Snowflake
    - **Visualization**: Plotly
    """)
    
    st.markdown("### Version Information")
    st.markdown(f"""
    - **Current Version**: 1.0.0
    - **Last Updated**: {CONFIG["APP"]["LAST_UPDATED"]}
    """)
    
    st.markdown("### Contact")
    st.markdown("""
    For support or inquiries, please contact:
    - **Author**: Kalyan Aravapalli
    """) 