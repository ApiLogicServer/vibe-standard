<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Northwind Database Analysis Project Instructions

This is a Python project for analyzing the Northwind sample database with the following characteristics:

## Project Context
- **Database**: SQLite Northwind database with tables for customers, orders, products, categories, suppliers, employees, and shippers
- **Framework**: Flask web application with SQLAlchemy ORM
- **Visualization**: Plotly, Matplotlib, and Seaborn for charts and graphs
- **Analysis**: Jupyter notebooks for exploratory data analysis

## Code Style Guidelines
- Use SQLAlchemy ORM models for database interactions
- Follow Flask best practices for route organization
- Use type hints for function parameters and return values
- Implement proper error handling and logging
- Write descriptive docstrings for classes and functions

## Database Conventions
- Use snake_case for database column names
- Implement proper relationships between models using SQLAlchemy
- Use database migrations for schema changes
- Validate data integrity with constraints

## Web Development Patterns
- Separate business logic into service classes
- Use templates for consistent HTML structure
- Implement responsive design with Bootstrap or similar
- Add proper CSRF protection for forms

## Data Analysis Best Practices
- Use pandas for data manipulation and analysis
- Create reusable visualization functions
- Document analysis methodology in notebooks
- Include statistical summaries and insights
