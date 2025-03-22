# rTor: Tor Reverse Proxy

rTor is a lightweight reverse proxy application designed to facilitate access to Tor hidden services (.onion sites) through a standard HTTP interface. It acts as an intermediary between regular web browsers and the Tor network, eliminating the need for end users to configure Tor directly.

## Features

- Proxies HTTP requests to Tor hidden services
- Configurable SOCKS proxy settings for Tor connectivity
- Customizable local port binding
- Simple command-line interface

## Usage

The application can be launched via command line with various configuration options:

```
python tor_reverse_proxy.py --help
usage: tor_reverse_proxy.py [-h] [--socks-port SOCKS_PORT] [--socks-host SOCKS_HOST] [--port PORT] --onion-url ONION_URL

options:
  -h, --help            show this help message and exit
  --socks-port SOCKS_PORT
                        Tor SOCKS port (default: 9050)
  --socks-host SOCKS_HOST
                        Tor SOCKS host (default: 127.0.0.1)
  --port PORT           Port to run the proxy server on (default: 8080)
  --onion-url ONION_URL
                        Target .onion URL (without http:// prefix)
```

## Requirements

- Python 3.x
- Running Tor service
- Network connectivity

## Example

To proxy requests to a specific .onion site through a local Tor instance:

```bash
python tor_reverse_proxy.py --onion-url explorerzydxu5ecjrkwceayqybizmpjjznk5izmitf2modhcusuqlid.onion --port 8080
```

This will start a local HTTP server on port 8080 that forwards all requests to the blockstream.info website hrough the Tor network.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
