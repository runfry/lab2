from sqlalchemy import create_engine, Integer, String, ForeignKey, Table, MetaData, Column
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Mapped, mapped_column
from typing import List

# Create engine first
engine = create_engine('postgresql://postgres:8962@localhost:5432/postgres')

# Create base and metadata
Base = declarative_base()
metadata = MetaData()

# Tables for many-to-many relationships
warehouse_sparepart = Table(
    'warehouse_sparepart',
    Base.metadata,  # Use Base.metadata instead of separate metadata
    Column('wars_id', Integer, primary_key=True),
    Column('warehouse_id', Integer, ForeignKey('warehouse.warehouse_id')),
    Column('sparepart_id', Integer, ForeignKey('sparepart.sparepart_id'))
)

supplier_sparepart = Table(
    'supplier_sparepart',
    Base.metadata,  # Use Base.metadata instead of separate metadata
    Column('sups_id', Integer, primary_key=True),
    Column('supplier_id', Integer, ForeignKey('supplier.supplier_id')),
    Column('sparepart_id', Integer, ForeignKey('sparepart.sparepart_id'))
)


class Warehouse(Base):
    __tablename__ = 'warehouse'

    warehouse_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    warehouse_phone: Mapped[int] = mapped_column(Integer)
    available_spareparts: Mapped[int] = mapped_column(Integer)

    # Relationships
    spareparts: Mapped[List["Sparepart"]] = relationship("Sparepart", secondary=warehouse_sparepart,
                                                        back_populates="warehouses")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="warehouse")


class Supplier(Base):
    __tablename__ = 'supplier'

    supplier_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_name: Mapped[str] = mapped_column(String)
    phone_supplier: Mapped[int] = mapped_column(Integer)
    available_quantity: Mapped[int] = mapped_column(Integer)

    # Relationships
    spareparts: Mapped[List["Sparepart"]] = relationship("Sparepart", secondary=supplier_sparepart,
                                                        back_populates="suppliers")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="supplier")


class Sparepart(Base):
    __tablename__ = 'sparepart'

    sparepart_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sparepart_name: Mapped[str] = mapped_column(String)
    sparepart_info: Mapped[str] = mapped_column(String)

    # Relationships
    warehouses: Mapped[List["Warehouse"]] = relationship("Warehouse", secondary=warehouse_sparepart,
                                                       back_populates="spareparts")
    suppliers: Mapped[List["Supplier"]] = relationship("Supplier", secondary=supplier_sparepart,
                                                     back_populates="spareparts")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="sparepart")


class Order(Base):
    __tablename__ = 'order'

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sparepart_id: Mapped[int] = mapped_column(Integer, ForeignKey('sparepart.sparepart_id'))
    warehouse_id: Mapped[int] = mapped_column(Integer, ForeignKey('warehouse.warehouse_id'))
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey('supplier.supplier_id'))

    # Relationships
    sparepart: Mapped["Sparepart"] = relationship("Sparepart", back_populates="orders")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="orders")
    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="orders")


class Model:
    def __init__(self):
        self.engine = engine  # Use the engine defined at module level
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_data(self, table_name: str, data: dict) -> tuple[bool, str]:
        try:
            if table_name == 'sparepart':
                new_record = Sparepart(**data)
            elif table_name == 'warehouse':
                new_record = Warehouse(**data)
            elif table_name == 'supplier':
                new_record = Supplier(**data)
            elif table_name == 'order':
                new_record = Order(**data)
            else:
                return False, "Invalid table name"

            self.session.add(new_record)
            self.session.commit()
            return True, f"Data added successfully with ID: {new_record.sparepart_id if table_name == 'sparepart' else new_record.warehouse_id if table_name == 'warehouse' else new_record.supplier_id if table_name == 'supplier' else new_record.order_id}"
        except Exception as e:
            self.session.rollback()
            return False, f"Failed to add data: {str(e)}"

    def update_data(self, table_name: str, id_column: str, id_value: int, data: dict) -> tuple[bool, str]:
        try:
            if table_name == 'sparepart':
                record = self.session.query(Sparepart).filter_by(sparepart_id=id_value).first()
            elif table_name == 'warehouse':
                record = self.session.query(Warehouse).filter_by(warehouse_id=id_value).first()
            elif table_name == 'supplier':
                record = self.session.query(Supplier).filter_by(supplier_id=id_value).first()
            elif table_name == 'order':
                record = self.session.query(Order).filter_by(order_id=id_value).first()
            else:
                return False, "Invalid table name"

            if not record:
                return False, f"Record with ID {id_value} not found"

            for key, value in data.items():
                setattr(record, key, value)

            self.session.commit()
            return True, "Data updated successfully"
        except Exception as e:
            self.session.rollback()
            return False, f"Update failed: {str(e)}"

    def delete_data(self, table_name: str, id_column: str, id_value: int) -> tuple[bool, str]:
        try:
            if table_name == 'sparepart':
                record = self.session.query(Sparepart).filter_by(sparepart_id=id_value).first()
            elif table_name == 'warehouse':
                record = self.session.query(Warehouse).filter_by(warehouse_id=id_value).first()
            elif table_name == 'supplier':
                record = self.session.query(Supplier).filter_by(supplier_id=id_value).first()
            elif table_name == 'order':
                record = self.session.query(Order).filter_by(order_id=id_value).first()
            else:
                return False, "Invalid table name"

            if not record:
                return False, f"Record with ID {id_value} not found"

            self.session.delete(record)
            self.session.commit()
            return True, "Data deleted successfully"
        except Exception as e:
            self.session.rollback()
            return False, f"Delete failed: {str(e)}"

    def __del__(self):
        self.session.close()