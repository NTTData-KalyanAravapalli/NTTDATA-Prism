# Configuration dictionary
CONFIG = {
    "APP": {
        "TITLE": "Portal for Role Integration, Security & Management",
        "LOGO_URL": "assets/NTT-Data-Logo.png"
    },
    "DATABASE": {
        "NAME": "SECURITY",  # Change this for your environment
        "SCHEMA": "ACCESS_CONTROL"  # Change this for your environment
    },
    "TABLES": {
        "ENVIRONMENTS": "ENVIRONMENTS",
        "ROLE_METADATA": "FUNCTIONAL_TECHNICAL_ROLE_METADATA",
        "AUDIT_LOG": "AUDIT_LOG",
        "AUDIT_LOG_SEQUENCE": "SEQ_AUDIT_LOG",
        "ROLE_HIERARCHY_LOG": "ROLE_HIERARCHY_LOG",
        "ROLE_HIERARCHY_LOG_SEQUENCE": "SEQ_ROLE_HIERARCHY_LOG"
    },
    "STORED_PROCEDURES": {
        "DATABASE_CONTROLLER": "SP_DATABASE_CONTROLLER",
        "ENVIRONMENT_ROLE_CONTROLLER": "SP_ENVIRONMENT_ROLE_CONTROLLER",
        "MANAGE_FUNCTIONAL_TECHNICAL_ROLES": "SP_MANAGE_FUNCTIONAL_TECHNICAL_ROLES_CONTROLLER"
    }
}

# Actions
CREATE_DATABASE = "Create a Database"
CLONE_DATABASE = "Clone a Database"
DELETE_DATABASE = "Delete a Database"
CREATE_WAREHOUSE = "Create a Warehouse"
CREATE_ROLE = "Create a Role"
CREATE_ENVIRONMENT_ROLES = "Create Environment Roles"  
SHOW_ROLE_HIERARCHY = "Show Role Hierarchy"
DISPLAY_RBAC_ARCHITECTURE = "Display RBAC Architecture"
MANAGE_METADATA = "Manage Metadata"
AUDIT_LOGS = "Audit Logs"
ASSIGN_ROLES = "Assign Roles"
ASSIGN_DATABASE_ROLES = "Assign Database Roles"
REVOKE_ROLES = "Revoke Roles"  
COST_ANALYSIS = "Cost Analysis"
ABOUT = "About PRISM"

ACTIONS_LIST = [
    ABOUT,
    CREATE_DATABASE,
    CLONE_DATABASE,
    DELETE_DATABASE,
    CREATE_WAREHOUSE,
    CREATE_ROLE,
    ASSIGN_ROLES,
    ASSIGN_DATABASE_ROLES,
    REVOKE_ROLES, 
    CREATE_ENVIRONMENT_ROLES,
    SHOW_ROLE_HIERARCHY,
    DISPLAY_RBAC_ARCHITECTURE,
    MANAGE_METADATA,
    COST_ANALYSIS,
    AUDIT_LOGS, 
]

# Role Types
FUNCTIONAL_ROLE = "Functional"
TECHNICAL_ROLE = "Technical" 