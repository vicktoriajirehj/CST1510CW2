# CST1510CW2
This Repository contains all documentation of Coursework 2
Multi-Domain Intelligence Platform

A Streamlit-based intelligence platform that integrates Cybersecurity, IT Operations, and Data Science dashboards into a single application with secure authentication, CRUD functionality, interactive visualizations, and an AI-powered assistant.

Project Overview

The Multi-Domain Intelligence Platform is designed to provide centralized operational visibility across multiple domains.
It allows authenticated users to:

Monitor and manage cybersecurity incidents

Track and resolve IT operations tickets

Analyze data science datasets

Interact with an AI assistant for cross-domain insights and recommendations

The platform follows a Tier 2 implementation, featuring interactive dashboards, data management (CRUD), and AI-assisted analysis.

Domains Implemented
- Cybersecurity
- IT Operations
- Data Science

System Architecture:

The application follows a Model–View–Controller (MVC) structure:

Model:
CSV-backed data models (Users, Incidents, IT Tickets, Datasets)

View:
Streamlit dashboards and UI components

Controller:
CRUD functions, authentication logic, and AI request handling

Security Features:

- Password hashing using bcrypt

- Role-based access control (admin, it, cyber, data)

- Session-based authentication using Streamlit session state

- No plain-text passwords stored

Dashboards
 Homepage

Application overview

Navigation to dashboards

Description of platform capabilities

Cybersecurity Dashboard:

- Incident severity, status, and category analysis

- Resolution time distribution

- Full CRUD support for incidents

- Interactive Plotly charts

IT Operations Dashboard:

- Ticket management and status tracking

- Department-based workload analysis

- CRUD functionality for IT tickets

Data Science Dashboard:

- Dataset metadata overview

- Department usage insights

- Dataset size and row count visualizations

CRUD support for datasets

AI Assistant

AI Assistant Capabilities

The AI Assistant can:
- Analyze cybersecurity risks
- Identify IT bottlenecks
- Summarize dataset usage trends
- Provide decision-support recommendations

Name: Vicktoria Jimenez
Student ID: M01026849
Program: Cybersecurity CST1510