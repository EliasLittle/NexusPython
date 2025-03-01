import grpc
from typing import Optional, Union
import proto.nexus_pb2 as nexus_pb2
import proto.nexus_pb2_grpc as nexus_grpc

class NexusClient:
    def __init__(self, host: str = 'localhost', port: int = 50051):
        """Initialize a Nexus client.
        
        Args:
            host: The server hostname (default: localhost)
            port: The server port (default: 50051)
        """
        self.server_addr = f'{host}:{port}'
        self.channel = grpc.insecure_channel(self.server_addr)
        self.stub = nexus_grpc.NexusServiceStub(self.channel)
    
    def __del__(self):
        """Cleanup the gRPC channel on deletion."""
        self.channel.close()

    def store_value(self, path: str, value: Union[str, int, float, bool, bytes]) -> None:
        """Store a value on the nexus server.
        
        Args:
            path: The path to store the value under
            value: The value to store (can be string, int, float, bool, or bytes)
        """
        try:
            request = nexus_pb2.StoreValueRequest()
            request.path = path
            
            # Set the appropriate value field based on type
            if isinstance(value, str):
                request.string_value.value = value
            elif isinstance(value, int):
                request.int_value.value = value
            elif isinstance(value, float):
                request.float_value.value = value
            elif isinstance(value, bool):
                raise ValueError("Boolean values are not supported yet")
                # request.bool_value.value = value
            elif isinstance(value, bytes):
                raise ValueError("Bytes values are not supported yet")
                # request.bytes_value.value = value
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
            
            response = self.stub.StoreValue(request)
            print(f"Successfully stored value at {path}. Response: {response}")
            
        except grpc.RpcError as e:
            print(f"Failed to store value: {e.details()}")

    def get_value(self, path: str) -> Optional[Union[str, int, float, bool, bytes]]:
        """Retrieve a value from the nexus server.
        
        Args:
            path: The path to retrieve the value from
            
        Returns:
            The value if found, None if not found or error
        """
        try:
            request = nexus_pb2.GetPathRequest()
            request.path = path
            
            response = self.stub.GetNode(request)
            
            # Determine which value field is set and return it
            which_oneof = response.WhichOneof('value')
            if which_oneof == 'string_value':
                return response.string_value.value
            elif which_oneof == 'int_value':
                return response.int_value.value
            elif which_oneof == 'float_value':
                return response.float_value.value
            elif which_oneof == 'bool_value':
                return response.bool_value.value
            elif which_oneof == 'bytes_value':
                return response.bytes_value.value
            return None
            
        except grpc.RpcError as e:
            print(f"Failed to get value: {e.details()}")
            return None

    def delete_value(self, path: str) -> bool:
        """Delete a value from the nexus server.
        
        Args:
            path: The path to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            request = nexus_pb2.DeletePathRequest()
            request.path = path
            
            response = self.stub.DeletePath(request)
            print(f"Successfully deleted value at {path}. Response: {response}")
            return True
            
        except grpc.RpcError as e:
            print(f"Failed to delete value: {e.details()}")
            return False

    def list_values(self, path: str = "") -> list[str]:
        """List all values under a prefix.
        
        Args:
            path: The path to list values under (default: "" for all values)
            
        Returns:
            List of paths found under the prefix
        """
        try:
            request = nexus_pb2.GetChildrenRequest()
            request.path = path
            
            response = self.stub.GetChildren(request)
            return list(response.children)
            
        except grpc.RpcError as e:
            print(f"Failed to list values: {e.details()}")
            return []

def main():
    # Example usage
    client = NexusClient()
    
    # Store different types of values
    client.store_value("python_test/string", "Hello World")
    client.store_value("python_test/int", 42)
    client.store_value("python_test/float", 3.14)
    #client.store_value("python_test/bool", True)
    #client.store_value("python_test/bytes", b"Binary data")
    
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
