# Starlyng SSH Connection Library

A Python library for checking server availability and managing server configurations via SSH.

## Features

- Check multiple servers' SSH availability in parallel using `ping_servers`
- Execute commands across multiple servers using `run_command_on_servers` 
- Server configuration management through `Server` dataclass
- Parallel execution using threading
- Comprehensive error handling and logging
- Utility functions for server management:
  - `get_hostname`: Generate hostnames from IP/port
  - `get_host_id`: Generate host IDs
  - `get_ip_for_ssh`: Format IPs for SSH connections

## Prerequisites

Before you begin, ensure you have:
* Python 3.9 or higher installed
* SSH access to target servers
* SSH key authentication configured (optional)

## Installation
```bash
pip install starlyng-ssh-connection
```

## Usage

### Creating Servers

```python
from ssh_connection.models import Server

# Create server instances for local network
servers = [
    Server(
        hostname="server01",
        ip="192.168.1.100",
        public_ip=False,
        ssh_key_path="~/.ssh/id_rsa",
        ssh_port=22,
        ssh_user="admin",
        ssh_vlan_id=10
    ),
    Server(
        hostname="server02",
        ip="192.168.1.101",
        public_ip=False,
        ssh_key_path="~/.ssh/id_rsa",
        ssh_port=22,
        ssh_user="admin",
        ssh_vlan_id=10
    )
]

# Create a public server instance
public_server = Server(
    hostname="public-server01",
    ip="203.0.113.10",
    public_ip=True,
    ssh_key_path="~/.ssh/id_rsa",
    ssh_port=12345,
    ssh_user="admin",
    ssh_vlan_id=0  # Not used for public IPs
)
```

### Checking Server Availability

```python
from ssh_connection.connections import ping_servers

# Check which servers are offline
offline_servers = ping_servers(servers)
if offline_servers:
    print("Offline servers:", offline_servers)
else:
    print("All servers are online!")
```

### Running Commands on Servers

```python
from ssh_connection.connections import run_command_on_servers

# Run a single command on all servers
results = run_command_on_servers(servers, "uptime")
for hostname, result in results.items():
    if result['error']:
        print(f"{hostname} error: {result['error']}")
    else:
        print(f"{hostname} output: {result['output']}")
```

### Running Multiple Commands on Servers

```python
from ssh_connection.connections import run_command_on_servers

# Run multiple commands in sequence
commands = [
    "hostname",
    "uptime",
    "df -h"
]
results = run_command_on_servers(servers, commands)
for hostname, result in results.items():
    if result['error']:
        print(f"{hostname} error: {result['error']}")
    else:
        print(f"{hostname} output: {result['output']}")
```

### Working with Local Network Servers

```python
from ssh_connection.utils import get_hostname, get_ip_for_ssh

# Generate hostname for a local server
hostname = get_hostname("server", "192.168.1.20", 22, public_ip=False)
print(f"Generated hostname: {hostname}")  # Output: server10

# Get SSH IP address with VLAN
ssh_ip = get_ip_for_ssh("192.168.1.100", vlan_id=10, public_ip=False)
print(f"SSH IP: {ssh_ip}")  # Output: 192.168.10.100
```

### Working with Public Servers

```python
from ssh_connection.utils import get_hostname, get_ip_for_ssh

# Generate hostname for a public server (uses port number)
public_hostname = get_hostname("server", "203.0.113.10", 12345, public_ip=True)
print(f"Public server hostname: {public_hostname}")  # Output: server45

# Get SSH IP for public server
public_ssh_ip = get_ip_for_ssh("203.0.113.10", vlan_id=0, public_ip=True)
print(f"Public SSH IP: {public_ssh_ip}")  # Output: 203.0.113.10
```

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## Contact

If you have any questions, please contact:

- GitHub: [@justinsherwood](https://github.com/justinsherwood)
