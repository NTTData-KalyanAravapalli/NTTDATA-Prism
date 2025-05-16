import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.config import *
from utils.helpers import *

# Set page configuration
st.set_page_config(page_title=CONFIG["APP"]["TITLE"], layout="wide")

# Main function
def main():
    # Set page configuration and styling
    st.markdown("""
        <style>
        /* Light mode styles */
        [data-testid="stAppViewContainer"] {
            background-color: #f0f9ff;
        }
        [data-testid="stSidebar"] {
            background-color: #29e5e8;
        }
        .sidebar-content {
            color: white;
        }
        
        /* Dark mode styles */
        @media (prefers-color-scheme: dark) {
            [data-testid="stAppViewContainer"] {
                background-color: #1E1E1E;
            }
            [data-testid="stSidebar"] {
                background-color: #2C2C2C;
            }
            .stMarkdown, .stText {
                color: #FFFFFF !important;
            }
            .stMetric {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Plotly charts in dark mode */
            .js-plotly-plot .plotly {
                background-color: #2C2C2C !important;
            }
            .js-plotly-plot .plotly .main-svg {
                background-color: #2C2C2C !important;
            }
            /* Dataframes/tables in dark mode */
            .stDataFrame {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Select boxes and inputs */
            .stSelectbox, .stTextInput, .stDateInput {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Buttons */
            .stButton button {
                background-color: #4A4A4A !important;
                color: #FFFFFF !important;
            }
            /* Tabs */
            .stTab {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Tab content */
            .stTabContent {
                background-color: #2C2C2C !important;
                color: #FFFFFF !important;
            }
            /* Multiselect */
            .stMultiSelect {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Date input */
            .stDateInput > div {
                background-color: #363636 !important;
                color: #FFFFFF !important;
            }
            /* Links */
            a {
                color: #00CED1 !important;
            }
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #FFFFFF !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image(CONFIG["APP"]["LOGO_URL"], width=500)
        st.image("assets/Prism Designer.jpeg", width=500)
        
        # Account Context
        st.markdown("### Account Context")
        available_accounts = ["PRIMARY", "SECONDARY", "SANDBOX"]
        selected_account = st.selectbox(
            "Select Account:",
            available_accounts,
            key="selected_account",
        )
       
        # Session Information
        st.markdown("### Current Session")
        current_user = get_current_snowflake_user()
        current_role = get_current_snowflake_role()
       
        session_container = st.container()
        with session_container:
            user_col1, user_col2 = st.columns([1, 2])
            with user_col1:
                st.text("User:")
            with user_col2:
                st.text(current_user)
           
            role_col1, role_col2 = st.columns([1, 2])
            with role_col1:
                st.text("Role:")
            with role_col2:
                st.text(current_role)
       
        st.markdown("---")
       
        # Actions section
        st.markdown("### Actions")
        selected_action = st.radio(
            "",
            ACTIONS_LIST,
            key="selected_action_radio"
        )
       
        # Footer information
        st.markdown("---")
        st.markdown("### App Information")
       
        info_container = st.container()
        with info_container:
            ver_col1, ver_col2 = st.columns([1, 2])
            with ver_col1:
                st.text("Version:")
            with ver_col2:
                st.text("1.0.0")
           
            auth_col1, auth_col2 = st.columns([1, 2])
            with auth_col1:
                st.text("Author:")
            with auth_col2:
                st.text("Kalyan Aravapalli")

    # Main content area
    st.title(CONFIG["APP"]["TITLE"])
    st.markdown("---")
   
    # Action Dispatcher
    if selected_action == ABOUT:
        from pages.about import ui_about
        ui_about()
    elif selected_action == CREATE_DATABASE:
        from pages.database import ui_create_database
        ui_create_database()
    elif selected_action == CLONE_DATABASE:
        from pages.database import ui_clone_database
        ui_clone_database()
    elif selected_action == DELETE_DATABASE:
        from pages.database import ui_delete_database
        ui_delete_database()
    elif selected_action == CREATE_WAREHOUSE:
        from pages.warehouse import ui_create_warehouse
        ui_create_warehouse()
    elif selected_action == CREATE_ROLE:
        from pages.roles import ui_create_role
        ui_create_role()
    elif selected_action == ASSIGN_ROLES:
        from pages.roles import ui_assign_roles
        ui_assign_roles()
    elif selected_action == ASSIGN_DATABASE_ROLES:
        from pages.roles import ui_assign_database_roles
        ui_assign_database_roles()
    elif selected_action == REVOKE_ROLES:
        from pages.roles import ui_revoke_roles
        ui_revoke_roles()
    elif selected_action == CREATE_ENVIRONMENT_ROLES:
        from pages.roles import ui_create_environment_roles
        ui_create_environment_roles()
    elif selected_action == SHOW_ROLE_HIERARCHY:
        from pages.roles import ui_show_role_hierarchy
        ui_show_role_hierarchy()
    elif selected_action == DISPLAY_RBAC_ARCHITECTURE:
        from pages.roles import ui_display_rbac_architecture
        ui_display_rbac_architecture()
    elif selected_action == MANAGE_METADATA:
        from pages.metadata import ui_manage_metadata
        ui_manage_metadata()
    elif selected_action == COST_ANALYSIS:
        from pages.cost import ui_cost_analysis
        ui_cost_analysis()
    elif selected_action == AUDIT_LOGS:
        from pages.audit import ui_audit_logs
        ui_audit_logs()
    else:
        st.info("Select an action from the sidebar to get started.")

if __name__ == "__main__":
    main() 