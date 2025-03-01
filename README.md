# Nexus Python Client

A Python client for interacting with the Nexus service.

## Installation

WIP

## Usage

```python
from client import NexusClient

client = NexusClient()

# Store a value
client.store_value("my/path", "Hello World")

# Get a value
value = client.get_value("my/path")

# List values
paths = client.list_values("my/")

# Delete a value
client.delete_value("my/path")
```