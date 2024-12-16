# SMSActivatePy Library

A Python library for interacting with the [SMSActivate API](https://sms-activate.org/api2). This tool allows you to integrate SMS activation services seamlessly into your projects.

## Installation

To install the library, run the following command:

```sh
pip install smsactivatepy
```

## Requirements

- `requests`
- `json`

## Usage Example

```python
from smsactivatepy.api import SMSActivateAPI

# Initialize the API with your key
sa = SMSActivateAPI(APIKEY)

# Enable debug mode (optional, for troubleshooting)
sa.debug_mode = True
```

## Features

This library provides an interface for accessing the SMSActivate service. You can use it for operations such as:
- Requesting a virtual phone number
- Managing SMS activations
- Checking account balance

Detailed functionality is described in the official [SMSActivate API documentation](https://sms-activate.org/api2).

## Author

Developed by Gabriel Lima  
Email: [gabrielmrts@yahoo.com](mailto:gabrielmrts@yahoo.com)
