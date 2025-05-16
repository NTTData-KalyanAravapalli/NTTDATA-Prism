# NTTDATA-Prism

A comprehensive Snowflake management application built with Streamlit.

## Features

- Database Management
  - Create Database
  - Clone Database
  - Delete Database
- Warehouse Management
  - Create Warehouse
- Role Management
  - Create Role
  - Assign Roles
  - Assign Database Roles
  - Revoke Roles
  - Create Environment Roles
  - Show Role Hierarchy
  - Display RBAC Architecture
- Metadata Management
- Cost Analysis
- Audit Logs

## Prerequisites

- Python 3.8 or higher
- Snowflake account with appropriate permissions
- Streamlit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NTTDATA-Prism.git
cd NTTDATA-Prism
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Snowflake connection:
Create a `.env` file in the project root with your Snowflake credentials:
```
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

## Usage

1. Start the application:
```bash
streamlit run Home.py
```

2. Open your web browser and navigate to `http://localhost:8501`

## Project Structure

```
NTTDATA-Prism/
├── Home.py                 # Main application file
├── config/
│   └── config.py          # Configuration settings
├── pages/
│   ├── about.py           # About page
│   ├── audit.py           # Audit logs page
│   ├── cost.py            # Cost analysis page
│   ├── database.py        # Database management pages
│   ├── metadata.py        # Metadata management page
│   ├── roles.py           # Role management pages
│   └── warehouse.py       # Warehouse management page
├── utils/
│   └── helpers.py         # Utility functions
├── assets/                # Static assets
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Kalyan Aravapalli 