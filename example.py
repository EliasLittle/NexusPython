from client import NexusClient

def main():
    # Create client instance
    client = NexusClient(host="box-1", port=50051)
    
    # Store different types of values
    client.store_value("python_test/string", "Hello World")
    client.store_value("python_test/int", 42)
    client.store_value("python_test/float", 3.14)
    #client.store_value("python_test/bool", True)  # Not supported yet
    #client.store_value("python_test/bytes", b"Binary data")  # Not supported yet
    
    # Get a value
    value = client.get_value("python_test/string")
    print(f"Retrieved value: {value}")
    
    # List values
    paths = client.list_values("python_test/")
    print(f"Found paths: {paths}")
    
    # Delete a value
    client.delete_value("python_test/string")

if __name__ == "__main__":
    main()
