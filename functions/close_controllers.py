def close_controllers(clients):
    """Close every open MODBUS TCP connection."""
    for name, client in clients.items():
        client.close()
        print(f"Closed connection to {name}")
