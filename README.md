# XCP-NG Automation scripts

## Description
Set of scripts for simple automation task on XCP-NG hypervisor. Each script outputs structured JSON for easy integration with scripts and automation workflows.
Example: 
Run:
```python
python vm_get_network.py
```
Expected output: 
```bash
{
  "success": true,
  "vm": {
    "name": "Example-VM",
    "uuid": "11111111-2222-4333-8444-555555555555"
  },
  "vifs": [
    {
      "device": "eth0",
      "device_number": 0,
      "uuid": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
      "mac_address": "02:00:00:00:00:01",
      "network": {
        "name": "public-network",
        "uuid": "11111111-aaaa-4bbb-8ccc-222222222222"
      },
      "currently_attached": true,
      "mtu": 1500
    }
  ],
  "guest_networks": {
    "0/ip": "192.0.2.10",
    "0/ipv4/0": "192.0.2.10",
    "0/ipv4/1": "192.0.2.11",
    "1/ip": "198.51.100.10",
    "1/ipv4/0": "198.51.100.10"
  },
  "guest_tools_available": true
}
```

## Run inside a container
```bash
# Build a python environment image 
podman build -t xcp-automation-scripts .
podman run --env-file -v "$PWD":/scripts:ro .env localhost/xcp-automation-scripts:latest <script-file-name>
```

## Scripts
-  vm_get_network: retrieves virtual machine network interface details and guest IP information from an XCP-ng host using the VM UUID.


