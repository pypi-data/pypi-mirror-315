"""Module containing the MobileVikingsClient class for interacting with the Mobile Vikings API."""

from datetime import datetime, timedelta, timezone
import logging

import httpx

from .const import BASE_URL, CLIENT_ID, CLIENT_SECRET

_LOGGER = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Exception raised for authentication errors."""

    pass


class MobileVikingsClient:
    """Asynchronous client for interacting with the Mobile Vikings API."""

    def __init__(self, username, password, tokens=None):
        """Initialize the MobileVikingsClient.

        Parameters
        ----------
        username : str
            The username for authenticating with the Mobile Vikings API.
        password : str
            The password for authenticating with the Mobile Vikings API.
        tokens : dict, optional
            A dictionary containing token information (refresh_token, access_token, expiry).

        """
        self.username = username
        self.password = password
        self.refresh_token = None
        self.access_token = None
        self.expires_in = None
        self.access_token_expiry = None
        self.client = httpx.AsyncClient()

        if tokens:
            self.refresh_token = tokens.get("refresh_token")
            self.access_token = tokens.get("access_token")
            self.expires_in = tokens.get("expires_in")
            if self.expires_in:
                self.access_token_expiry = datetime.fromisoformat(str(self.expires_in))

    async def close(self):
        """Close the HTTPX client."""
        await self.client.aclose()

    async def authenticate(self):
        """Authenticate with the Mobile Vikings API."""
        if self._is_token_valid():
            self.client.headers["Authorization"] = f"Bearer {self.access_token}"
        else:
            if self.refresh_token:
                _LOGGER.debug("Access token renewal with refresh token")
                await self._request_token(
                    {
                        "refresh_token": self.refresh_token,
                        "grant_type": "refresh_token",
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                    }
                )
            else:
                _LOGGER.debug("Requesting new access token")
                await self._request_token(
                    {
                        "username": self.username,
                        "password": self.password,
                        "grant_type": "password",
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                    }
                )

        if self._is_token_valid():
            self.client.headers["Authorization"] = f"Bearer {self.access_token}"
            return {
                "refresh_token": self.refresh_token,
                "access_token": self.access_token,
                "expires_in": self.expires_in,
            }
        else:
            return False

    def _is_token_valid(self):
        """Check if the current access token is valid."""
        return (
            self.access_token
            and self.access_token_expiry
            and datetime.now() < self.access_token_expiry
        )

    async def _request_token(self, payload):
        """Request an access token with the given payload."""
        response = await self.handle_request(
            "/oauth2/token/", payload, "POST", True, True
        )

        data = response.json()
        if response.status_code == 200:
            self.access_token = data.get("access_token")
            self.expires_in = data.get("expires_in")
            self.access_token_expiry = datetime.now() + timedelta(
                seconds=self.expires_in
            )
            self.refresh_token = data.get("refresh_token")
        elif response.status_code == 400 and payload.get("grant_type") == "password":
            raise AuthenticationError(
                f"Invalid grant_type - {data.get('error_description')}"
            )
        elif (
            response.status_code == 401 and payload.get("grant_type") == "refresh_token"
        ):
            raise AuthenticationError(f"Unauthorized - {data.get('error_description')}")
        else:
            raise AuthenticationError("Failed to authenticate")

    async def handle_request(
        self,
        endpoint,
        payload=None,
        method="GET",
        return_raw_response=False,
        authenticate_request=False,
    ):
        """Handle the HTTP request by logging the request details and handling the response."""
        # Ensure access token is valid before making the request
        if authenticate_request is False:
            await self.authenticate()

        url = BASE_URL + endpoint
        request_details = f"{method} request to: {url}"

        # Anonymize sensitive information like passwords
        if payload and ("password" in payload or "client_secret" in payload):
            anonymized_payload = {
                key: "********" if key in {"password", "client_secret"} else value
                for key, value in payload.items()
            }
            request_details += f", Payload: {anonymized_payload}"
        elif payload:
            request_details += f", Payload: {payload}"

        _LOGGER.debug(request_details)

        # Determine the appropriate method to call based on the HTTP method
        if method == "GET":
            response = await self.client.get(url)
        elif method == "POST":
            response = await self.client.post(url, data=payload)
        # Add support for other HTTP methods if needed
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if return_raw_response:
            _LOGGER.debug(f"Response data: {response.text}")
            return response

        if response.status_code == 200:
            data = response.json()
            _LOGGER.debug(f"Response data: {data}")
            return data
        elif response.status_code == 404:
            error_data = response.json()
            _LOGGER.debug(f"404 Error: {error_data}")
            return error_data
        elif str(response.status_code).startswith("4"):
            error_data = response.json()
            _LOGGER.debug(f"{response.status_code} Error: {error_data}")
            return False
        else:
            error_message = f"Request failed. Status code: {response.status_code}"
            try:
                error_data = response.json()
                error_message += f", Error: {error_data}"
            except Exception:
                pass
            raise Exception(error_message)

    async def get_customer_info(self):
        """Fetch customer information from the Mobile Vikings API.

        Returns
        -------
        dict or None: A dictionary containing customer information, or None if request fails.

        """
        return await self.handle_request("/customers/me")

    async def get_loyalty_points_balance(self):
        """Fetch loyalty points balance from the Mobile Vikings API.

        Returns
        -------
        dict or None: A dictionary containing loyalty points balance, or None if request fails.

        """
        return await self.handle_request("/loyalty-points/balance")

    async def get_subscriptions(self):
        """Fetch subscriptions from the Mobile Vikings API.

        Returns
        -------
        dict
            A dictionary containing subscription information.

        """
        subscriptions = await self.handle_request("/subscriptions?state=enabled")
        for subscription in subscriptions:
            subscription_id = subscription.get("id")
            if subscription.get("type") == "fixed-internet":
                subscription["modem_settings"] = await self.handle_request(
                    f"/subscriptions/{subscription_id}/modem/settings"
                )
            else:
                balance = await self.handle_request(
                    f"/subscriptions/{subscription_id}/balance"
                )
                subscription["balance"] = self.add_percentage_to_balance(balance)
        return subscriptions

    def add_percentage_to_balance(self, balance):
        """Calculate and add validity and usage percentages to each bundle in a balance.

        This function iterates through a list of bundles within the given `balance` and calculates:
        1. The validity percentage, which indicates how much of the bundle's validity period has elapsed.
        2. The used percentage, which shows how much of the total bundle has been consumed.

        The calculated percentages are added as new keys (`period_percentage` and `used_percentage`) to each bundle.

        Args:
        ----
            balance (dict): A dictionary containing the balance information with a key `bundles`,
                        which is a list of dictionaries. Each bundle dictionary must have the following keys:
                        - `valid_from` (str): Start of the validity period in ISO 8601 format (e.g., "YYYY-MM-DDTHH:MM:SS+ZZ:ZZ").
                        - `valid_until` (str): End of the validity period in ISO 8601 format.
                        - `total` (float): The total amount of the bundle.
                        - `used` (float): The amount of the bundle that has been used.

        Returns:
        -------
            dict: The updated balance dictionary with added percentages for each bundle.

        Raises:
        ------
            ValueError: If any required key is missing or if `valid_from` and `valid_until` are not properly formatted.

        """
        # Parse the current time and make it timezone-aware
        current_time = datetime.now(timezone.utc)

        # Loop through each bundle to calculate and add percentages
        for bundle in balance["bundles"]:
            try:
                valid_from = datetime.strptime(
                    bundle["valid_from"], "%Y-%m-%dT%H:%M:%S%z"
                )
                valid_until = datetime.strptime(
                    bundle["valid_until"], "%Y-%m-%dT%H:%M:%S%z"
                )
            except ValueError as e:
                raise ValueError(f"Invalid date format in bundle: {e}")

            # Calculate validity percentage
            validity_period = (valid_until - valid_from).total_seconds()
            elapsed_time = (current_time - valid_from).total_seconds()
            period_percentage = max(
                0, min((elapsed_time / validity_period) * 100, 100)
            )  # Clamp between 0 and 100

            # Calculate used percentage
            total = bundle["total"]
            used = bundle["used"]
            used_percentage = (used / total) * 100 if total > 0 else 0

            # Add percentages to the bundle
            # Rounding to two decimal places ensures consistent formatting and precision for display purposes
            bundle["period_percentage"] = round(period_percentage, 2)
            bundle["used_percentage"] = round(used_percentage, 2)

        return balance

    async def get_invoices(self):
        """Fetch subscriptions from the Mobile Vikings API.

        Returns
        -------
        dict
            A dictionary containing subscription information.

        """
        invoices = await self.handle_request(
            "/invoices?status=accepted,bad_dept,created,issued,partially_paid,pending_payment,review,unknown"
        )
        return invoices.get("results")

    async def get_data(self):
        """Fetch customer info, loyalty points balance, and subscriptions from the Mobile Vikings API.

        Returns
        -------
        dict
            A dictionary containing customer info, loyalty points balance, subscriptions, and unpaid invoices.

        Notes
        -----
            Errors in individual API calls will result in an error message being included in the respective section of the returned dictionary.

        """
        try:
            customer_info = await self.get_customer_info()
        except Exception as e:
            customer_info = {"error": str(e)}

        try:
            loyalty_points_balance = await self.get_loyalty_points_balance()
        except Exception as e:
            loyalty_points_balance = {"error": str(e)}

        try:
            subscriptions = await self.get_subscriptions()
        except Exception as e:
            subscriptions = {"error": str(e)}

        try:
            unpaid_invoices = await self.get_invoices()
        except Exception as e:
            unpaid_invoices = {"error": str(e)}

        return {
            "timestamp": datetime.now().isoformat(),
            "customer_info": customer_info,
            "loyalty_points_balance": loyalty_points_balance,
            "subscriptions": subscriptions,
            "unpaid_invoices": unpaid_invoices,
            "tokens": {
                "refresh_token": self.refresh_token,
                "access_token": self.access_token,
                "expires_in": self.expires_in,
            },
        }
