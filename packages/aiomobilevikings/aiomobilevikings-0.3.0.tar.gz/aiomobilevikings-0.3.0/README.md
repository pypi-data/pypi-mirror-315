# aiomobilevikings

Asynchronous library to communicate with the Mobile Vikings API

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20an%20Omer-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/QhvcnzjYzA)

[![MIT License](https://img.shields.io/github/license/geertmeersman/aiomobilevikings?style=flat-square)](https://github.com/geertmeersman/aiomobilevikings/blob/master/LICENSE)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/aiomobilevikings)](https://github.com/geertmeersman/aiomobilevikings/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/aiomobilevikings.svg)](http://isitmaintained.com/project/geertmeersman/aiomobilevikings)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/aiomobilevikings.svg)](http://isitmaintained.com/project/geertmeersman/aiomobilevikings)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/aiomobilevikings/pulls)

[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/aiomobilevikings/search?l=python)

[![github release](https://img.shields.io/github/v/release/geertmeersman/aiomobilevikings?logo=github)](https://github.com/geertmeersman/aiomobilevikings/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/aiomobilevikings)](https://github.com/geertmeersman/aiomobilevikings/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/aiomobilevikings)](https://github.com/geertmeersman/aiomobilevikings/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/aiomobilevikings)](https://github.com/geertmeersman/aiomobilevikings/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/aiomobilevikings?logo=github)](https://github.com/geertmeersman/aiomobilevikings/commits/main)

## Mobile Vikings API - Available Endpoints

### 1. **Authenticate**

- **Description**: Authenticates with the Mobile Vikings API to obtain an access token.
- **Input**:
  - `username` (string): Mobile Vikings account username.
  - `password` (string): Mobile Vikings account password.
- **Output**:
  - `refresh_token` (string): Token for refreshing the access token.
  - `access_token` (string): Token for accessing other endpoints.
  - `expires_in` (int): Time in seconds until the access token expires.

---

### 2. **Get Customer Info**

- **Description**: Fetches customer details from the API.
- **Input**: None.
- **Output**:
  - `id` (string): Customer ID.
  - `name` (string): Customer name.
  - `email` (string): Email address.

---

### 3. **Get Loyalty Points Balance**

- **Description**: Retrieves the loyalty points balance of the customer.
- **Input**: None.
- **Output**:
  - `points` (int): Total loyalty points.
  - `valid_until` (string, ISO 8601): Expiry date of points.

---

### 4. **Get Subscriptions**

- **Description**: Lists active subscriptions with additional details like modem settings or balance.
- **Input**: None.
- **Output**:
  - `subscriptions` (list of objects):
    - `id` (string): Subscription ID.
    - `type` (string): Type of subscription (e.g., "mobile", "fixed-internet").
    - `balance` (object): Balance details including:
      - `used` (float): Data/usage consumed.
      - `total` (float): Total data/usage.
      - `period_percentage` (float): Percentage of validity period elapsed.
      - `used_percentage` (float): Percentage of usage consumed.

---

### 5. **Get Invoices**

- **Description**: Retrieves unpaid and pending invoices.
- **Input**: None.
- **Output**:
  - `invoices` (list of objects):
    - `id` (string): Invoice ID.
    - `amount` (float): Invoice amount.
    - `status` (string): Invoice status (e.g., "pending_payment", "accepted").

---

### 6. **Get All Data**

- **Description**: Aggregates customer info, loyalty points, subscriptions, and unpaid invoices in one call.
- **Input**: None.
- **Output**:
  - `customer_info` (object): Customer details (see Get Customer Info).
  - `loyalty_points_balance` (object): Loyalty points balance (see Get Loyalty Points Balance).
  - `subscriptions` (list of objects): Subscriptions (see Get Subscriptions).
  - `unpaid_invoices` (list of objects): Invoices (see Get Invoices).
  - `timestamp` (string, ISO 8601): Time of data retrieval.

## Mobile Vikings API Example Script

This example script demonstrates how to utilize the `MobileVikingsClient` class from the `aiomobilevikings` module to interact with the Mobile Vikings API. It showcases various functionalities available within the client class to retrieve different types of data from the API.

### Usage

1. **Installation:** Ensure the `aiomobilevikings` module is installed. If not, install it using `pip install aiomobilevikings`.

2. **Configuration:** Replace the placeholder details within the script with actual values.

3. **Execution:** Run the script, and it will sequentially call these functions, displaying the retrieved data for each function.

### Important Notes

- Replace placeholder values (user, password) with your actual Mobile Vikings account details.
- Make sure you have appropriate access rights and permissions for the Mobile Vikings API endpoints being accessed.

Feel free to modify the script as needed, adding error handling, logging, or additional functionalities based on your requirements and the Mobile Vikings API's capabilities.

```python
"""
Example Script: Accessing Mobile Vikings API with aiomobilevikings

Requirements:
- aiomobilevikings library (installed via pip)

Usage:
Run the script and observe the output displaying various data from the Mobile Vikings API.
"""

from aiomobilevikings import MobileVikingsClient
import logging
import asyncio
import json

# Set the logging level to DEBUG for the root logger
logging.basicConfig(level=logging.ERROR)

# Create a logger for the aiomobilevikings module
_LOGGER = logging.getLogger("aiomobilevikings")
_LOGGER.setLevel(logging.DEBUG)  # Set the logging level to DEBUG for this logger


async def main():
    """Run the main function."""
    # Initialize the MobileVikingsClient with credentials
    client = MobileVikingsClient(
        username="xxxxxx@xxxxx.com", # Replace with actual username
        password="xxxxxxxxxxxxxxxx", # Replace with actual password
    )

    try:
        # Fetch customer information
        data = await client.get_data()
        print(json.dumps(data, indent=2))
    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the client session
        await client.close()
```
