from sqlalchemy import create_engine, Column, String, Integer, Date, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from tkinter import messagebox

# Khởi tạo Base để định nghĩa các bảng
Base = declarative_base()

# Định nghĩa các bảng trong cơ sở dữ liệu

class Inventory(Base):
    __tablename__ = 'inventory'
    Product_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Product_Name = Column(String(255), nullable=False)
    Category_ID = Column(String(255), ForeignKey('inventory_category.Category_ID'), nullable=False)
    Supplier_ID = Column(String(255), ForeignKey('suppliers.Supplier_ID'), nullable=False)

    # Quan hệ
    category = relationship("InventoryCategory", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    transaction_details = relationship("InventoryTransactionDetail", back_populates="product")
    inventory_balances = relationship("InventoryBalance", back_populates="product")


class InventoryCategory(Base):
    __tablename__ = 'inventory_category'
    Category_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Category_Name = Column(String(255), nullable=False)
    Description = Column(String(255))

    # Quan hệ
    products = relationship("Inventory", back_populates="category")


class InventoryTransaction(Base):
    __tablename__ = 'inventory_transaction'
    Transaction_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Transaction_Type = Column(String(255), nullable=False)
    Warehouse_ID = Column(String(255), ForeignKey('warehouses.Warehouse_ID'), nullable=False)
    To_Warehouse_ID = Column(String(255), ForeignKey('warehouses.Warehouse_ID'), nullable=True)
    Employee_ID = Column(String(255), ForeignKey('employees.Employee_ID'), nullable=False)
    Transaction_Date = Column(Date, nullable=False)

    # Quan hệ
    details = relationship("InventoryTransactionDetail", back_populates="transaction")
    employee = relationship("Employee", back_populates="transactions")


class InventoryTransactionDetail(Base):
    __tablename__ = 'inventory_transaction_detail'
    Detail_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Transaction_ID = Column(String(255), ForeignKey('inventory_transaction.Transaction_ID'), nullable=False)
    Product_ID = Column(String(255), ForeignKey('inventory.Product_ID'), nullable=False)
    Product_Name = Column(String(255), nullable=True)
    Unit_Type = Column(String(255), nullable=True)
    Quantity = Column(Integer, nullable=False)
    Unit_Price = Column(DECIMAL, nullable=True)
    Total_Price = Column(DECIMAL, nullable=True)
    Description = Column(String(255), nullable=True)

    # Quan hệ
    transaction = relationship("InventoryTransaction", back_populates="details")
    product = relationship("Inventory", back_populates="transaction_details")


class InventoryBalance(Base):
    __tablename__ = 'inventory_balance'
    Inventory_Balance_ID = Column(String(255), primary_key=True, nullable=False)
    Warehouse_ID = Column(String(255), ForeignKey('warehouses.Warehouse_ID'), nullable=False)
    Product_ID = Column(String(255), ForeignKey('inventory.Product_ID'), nullable=False)
    Date = Column(Date, nullable=False)
    Product_Name = Column(String(255), nullable=True)
    Unit_Type = Column(String(255), nullable=True)
    initial_stock = Column(Integer, nullable=True, default=0)
    quantity_imported = Column(Integer, nullable=True, default=0)
    export_quantity = Column(Integer, nullable=True, default=0)
    Unit_Price = Column(DECIMAL, nullable=True)
    Total_Price = Column(DECIMAL, nullable=True)
    Unit_Price_Import = Column(DECIMAL, nullable=True)
    Total_Price_Import = Column(DECIMAL, nullable=True)
    Unit_Price_Export = Column(DECIMAL, nullable=True)
    Total_Price_Export = Column(DECIMAL, nullable=True)

    __table_args__ = (
        UniqueConstraint('Inventory_Balance_ID', 'Warehouse_ID', 'Product_ID', name='uix_inventory_balance'),
    )

    # Quan hệ
    warehouse = relationship("Warehouse", back_populates="inventory_balances")
    product = relationship("Inventory", back_populates="inventory_balances")


class Warehouse(Base):
    __tablename__ = 'warehouses'
    Warehouse_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Name = Column(String(255), nullable=False)
    Location = Column(String(255), nullable=True)

    # Quan hệ
    inventory_balances = relationship("InventoryBalance", back_populates="warehouse")


class Supplier(Base):
    __tablename__ = 'suppliers'
    Supplier_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Supplier_Name = Column(String(255), nullable=False)
    Contact_Name = Column(String(255), nullable=True)
    Phone = Column(String(15), nullable=True)
    Address = Column(String(255), nullable=True)

    # Quan hệ
    products = relationship("Inventory", back_populates="supplier")


class Employee(Base):
    __tablename__ = 'employees'
    Employee_ID = Column(String(255), primary_key=True, unique=True, nullable=False)
    Employee_Name = Column(String(255), nullable=False)
    Position = Column(String(255), nullable=True)
    Phone = Column(String(15), nullable=True)
    Email = Column(String(255), nullable=True)
    Department = Column(String(255), nullable=True)

    # Quan hệ
    transactions = relationship("InventoryTransaction", back_populates="employee")


class User(Base):
    __tablename__ = 'users'
    username = Column(String(20), primary_key=True, unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    account_type = Column(String(10), nullable=False)
    Employee_ID = Column(String(255), ForeignKey('employees.Employee_ID'), nullable=True)


# Kết nối cơ sở dữ liệu SQLite
engine = create_engine('sqlite:///inventory_management_system.db')

# Tạo bảng nếu chưa tồn tại
Base.metadata.create_all(engine)

# Tạo session để tương tác với cơ sở dữ liệu
Session = sessionmaker(bind=engine)
session = Session()

print("Database created successfully!")
