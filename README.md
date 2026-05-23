# Inventory Management System (IMS)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-blueviolet.svg)

A real-time, modern **CustomTkinter desktop application** designed to manage warehouse inventories, suppliers, products, and handle transaction approvals with absolute precision.

## Overview

The Inventory Management System (IMS) provides warehouse administrators and employees with a robust platform to track stock levels, manage inbound/outbound shipments, and monitor system activities. It integrates SQLite with SQLAlchemy ORM to provide reliable data storage, paired with an elegant, responsive desktop interface.

### Key Features

*   **Workflow Approval System:** Inbound and Outbound shipments are initially created in a Draft status, which does not affect actual stock balances. Administrators review and approve these transactions in the Transactions tab to transition them to Completed and commit the inventory changes.
*   **Collapsible Responsive Sidebar:** Features a hamburger menu button (☰) that dynamically collapses the navigation sidebar to display only minimal representations, maximizing screen estate for complex tables and data.
*   **Real-time Dynamic Filtering:** Search bars in the Products and Inventory tabs automatically filter and update displayed records as you type, providing instantaneous visual feedback.
*   **Smooth Toast Notifications:** Intrusive popup alert dialogs are replaced with native-looking sliding Toast notifications that gracefully slide into view and auto-dismiss after 3 seconds, preserving the user's workflow.
*   **Permanent Audit Trail:** Complete audit trail of all sensitive user actions (login, product creation, transaction approvals, user updates) stored with high-precision timestamps for rigorous compliance.
*   **Inventory Valuation:** Automatically calculates warehouse asset valuations using the Weighted Average Cost method, giving real-time asset insights on the main dashboard.
*   **Mica/Acrylic Effect:** Applies translucent background styling on Windows platforms for premium visual aesthetics.

## Target Audience (User Roles)

The system tracks actions and delegates privileges based on two distinct roles:
*   **Admin:** Complete system control, including inventory valuation metrics, transaction approvals, audit log inspection, and user account management.
*   **Employee:** Restricted access enabling creation of inbound/outbound drafts, transfer of stock, and product views.

## Architecture & Technical Stack

*   **Framework:** CustomTkinter (GUI Frontend)
*   **Window Effects:** pywinstyles (Mica/Acrylic glassmorphism)
*   **Database & ORM:** SQLite & SQLAlchemy (Declarative Base)
*   **Image Processing:** Pillow (PIL)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LQP-CTER/Inventory-Management-System.git
   cd Inventory-Management-System
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## Security Notice

*   **Data Privacy:** The local SQLite database (`inventory_management_system.db`) and python cache folders are strictly ignored via `.gitignore` to prevent accidental exposure of confidential storage and transaction data.
*   **Internal Use Only:** Designed for internal deployment to streamline corporate inventory control.

---
*Developed by LQP-CTER*
