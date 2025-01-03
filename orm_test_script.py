from orm_models import Base, Model, engine, Warehouse, Supplier, Sparepart, Order


def main():
    # Drop all existing tables first
    print("Dropping existing tables...")
    Base.metadata.drop_all(engine)
    print("Tables dropped successfully!")

    # Create all tables
    print("\nCreating tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

    # Create an instance of the Model class
    model = Model()

    # Test adding data
    print("\nTesting data addition:")

    # Add a warehouse first (since it's referenced by sparepart)
    warehouse_data = {
        "warehouse_phone": 123456789,
        "available_spareparts": 10
    }
    success, message = model.add_data("warehouse", warehouse_data)
    print(f"Adding warehouse: {message}")

    # Add a supplier
    supplier_data = {
        "supplier_name": "Test Supplier",
        "phone_supplier": 987654321,
        "available_quantity": 5
    }
    success, message = model.add_data("supplier", supplier_data)
    print(f"Adding supplier: {message}")

    # Add a sparepart
    sparepart_data = {
        "sparepart_name": "Test Part",
        "sparepart_info": "Test Part Description"
    }
    success, message = model.add_data("sparepart", sparepart_data)
    print(f"Adding sparepart: {message}")

    # Add an order
    order_data = {
        "sparepart_id": 1,
        "warehouse_id": 1,
        "supplier_id": 1
    }
    success, message = model.add_data("order", order_data)
    print(f"Adding order: {message}")

    # Test querying data
    print("\nTesting queries:")

    warehouse = model.session.query(Warehouse).first()
    if warehouse:
        print(f"Found warehouse with phone: {warehouse.warehouse_phone}")

    supplier = model.session.query(Supplier).first()
    if supplier:
        print(f"Found supplier: {supplier.supplier_name}")

    sparepart = model.session.query(Sparepart).first()
    if sparepart:
        print(f"Found sparepart: {sparepart.sparepart_name}")

    order = model.session.query(Order).first()
    if order:
        print(f"Found order with ID: {order.order_id}")


if __name__ == "__main__":
    main()