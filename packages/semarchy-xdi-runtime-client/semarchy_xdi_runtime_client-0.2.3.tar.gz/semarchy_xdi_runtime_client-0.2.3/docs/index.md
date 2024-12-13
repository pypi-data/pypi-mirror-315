# semarchy-xdi-runtime-client

This python package allow to remotly launch Semarchy XDI Delivery Job **ASYNCRONOUSLY**, by simply using the runtime url and the job name.
Variables can also be passed to the launch command.

## Installation

```bash
pip install semarchy-xdi-runtime-client
```

## How it works

By using a network capture tool (Wireshark), an unofficial endpoints has been identified : `(runtime-url)/client/1`.  
This endpoint is used by the official start-command.sh command line tool when issuing a `launch delivery` command.

## How to use it

### As a CLI tool

While it's not the initial **objective** of this tool to replace the official CLI tool (start-command.sh), you can use it in script as a CLI.

The [documentation of the CLI](cli/how-to-use.md) details all available options.

### As a Python module

``` python
from semarchy_xdi_runtime_client.client.client import XDIApiClient

client = XDIApiClient(runtime_host="https://runtime-url.example")
session_id = client.launch_delivery(job_name="load-crm-data", job_vars="var ~/date 2024-11-06")
print(session_id)

```