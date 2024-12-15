# adb-wifi-py

`adb-wifi-py` is a tool for pairing Android 11 and newer devices for wireless debugging directly through a terminal using QR code.

It leverages the `python-zeroconf` library for multicast DNS service discovery and the `qrcode` library for QR code generation.

## Installation

To install `adb-wifi-py`, run the following command:

### pip

```bash
pip install adb-wifi-py
```

### pipx

```bash
pipx install adb-wifi-py
```

### rye

```bash
rye tools install adb-wifi-py
```

### uv

```bash
uv tool install adb-wifi-py
```

## Usage

To use `adb-wifi-py`, run the following command:

```bash
adb-wifi
```

Follow the on-screen instructions to pair your device.

## License

This project is licensed under the GPL-3.0 License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [chanzmao](https://github.com/benigumocom) for the idea and [original code](https://gist.github.com/benigumocom/a6a87fc1cb690c3c4e3a7642ebf2be6f).
- [python-zeroconf](https://github.com/python-zeroconf/python-zeroconf) for multicast DNS service discovery.
- [qrcode](https://github.com/lincolnloop/python-qrcode) for QR code generation.
