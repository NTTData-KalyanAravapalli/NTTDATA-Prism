import streamlit as st
from snowflake.snowpark import Session
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_snowflake_session():
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }
    return Session.builder.configs(connection_parameters).create()

def test_snowflake_connection():
    st.title("Snowflake Connection Test")
    
    # Display current environment variables (without sensitive data)
    st.write("### Environment Variables Check")
    st.write(f"SNOWFLAKE_ACCOUNT: {os.getenv('SNOWFLAKE_ACCOUNT', 'Not set')}")
    st.write(f"SNOWFLAKE_USER: {os.getenv('SNOWFLAKE_USER', 'Not set')}")
    st.write(f"SNOWFLAKE_ROLE: {os.getenv('SNOWFLAKE_ROLE', 'Not set')}")
    st.write(f"SNOWFLAKE_WAREHOUSE: {os.getenv('SNOWFLAKE_WAREHOUSE', 'Not set')}")
    st.write(f"SNOWFLAKE_DATABASE: {os.getenv('SNOWFLAKE_DATABASE', 'Not set')}")
    st.write(f"SNOWFLAKE_SCHEMA: {os.getenv('SNOWFLAKE_SCHEMA', 'Not set')}")
    
    # Test connection
    st.write("### Connection Test")
    try:
        session = get_snowflake_session()
        if session:
            st.success("✅ Successfully connected to Snowflake!")
            
            # Test basic queries
            st.write("### Testing Basic Queries")
            
            # Get current user
            current_user = session.sql("SELECT CURRENT_USER()").collect()[0][0]
            st.write(f"Current User: {current_user}")
            
            # Get current role
            current_role = session.sql("SELECT CURRENT_ROLE()").collect()[0][0]
            st.write(f"Current Role: {current_role}")
            
            # Get current warehouse
            current_warehouse = session.sql("SELECT CURRENT_WAREHOUSE()").collect()[0][0]
            st.write(f"Current Warehouse: {current_warehouse}")
            
            # Get current database
            current_database = session.sql("SELECT CURRENT_DATABASE()").collect()[0][0]
            st.write(f"Current Database: {current_database}")
            
    except Exception as e:
        st.error(f"❌ Failed to connect to Snowflake: {str(e)}")
        st.write("### Troubleshooting Tips:")
        st.write("1. Check if your .env file exists and contains all required credentials")
        st.write("2. Verify your Snowflake account identifier format (e.g., xy12345.us-east-1)")
        st.write("3. Ensure your user has the correct role and warehouse access")
        st.write("4. Check if your IP is whitelisted in Snowflake")

if __name__ == "__main__":
    test_snowflake_connection() 