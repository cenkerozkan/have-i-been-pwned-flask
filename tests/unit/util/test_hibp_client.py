# tests/unit/util/test_hibp_client.py
import os
import pytest
from unittest.mock import patch, MagicMock

from util.hibp_client import HibpClient
from exceptions.no_hibp_key_found_exception import NoHibpKeyFoundException
from exceptions.hibp_could_not_be_verified_exception import (
    HibpCouldNotBeVerifiedException,
)
from model.hibp_breached_site_model import HibpBreachedSiteModel


@pytest.fixture
def hibp_client():
    """Create a fresh instance of HibpClient for each test"""
    # Reset singleton for testing
    HibpClient._instance = None
    return HibpClient()


@pytest.fixture
def mock_env_with_key(monkeypatch):
    """Mock environment with HIBP API key"""
    monkeypatch.setenv("HIBP_API_KEY", "test_api_key")


@pytest.fixture
def mock_env_without_key(monkeypatch):
    """Mock environment without HIBP API key"""
    monkeypatch.delenv("HIBP_API_KEY", raising=False)


@pytest.fixture
def sample_breach_response():
    """Sample breach response data from HIBP API"""
    return [
        {
            "Name": "Dailymotion",
            "Title": "Dailymotion",
            "Domain": "dailymotion.com",
            "BreachDate": "2016-10-20",
            "AddedDate": "2017-08-07T02:51:12Z",
            "ModifiedDate": "2017-08-07T02:51:12Z",
            "PwnCount": 85176234,
            "Description": 'In October 2016, the video sharing platform <a href="http://thehackernews.com/2016/12/dailymotion-video-hacked.html" target="_blank" rel="noopener">Dailymotion suffered a data breach</a>. The attack led to the exposure of more than 85 million user accounts and included email addresses, usernames and bcrypt hashes of passwords.',
            "LogoPath": "https://logos.haveibeenpwned.com/Dailymotion.png",
            "Attribution": None,
            "DisclosureUrl": None,
            "DataClasses": ["Email addresses", "Passwords", "Usernames"],
            "IsVerified": True,
            "IsFabricated": False,
            "IsSensitive": False,
            "IsRetired": False,
            "IsSpamList": False,
            "IsMalware": False,
            "IsSubscriptionFree": False,
            "IsStealerLog": False,
        }
    ]


class TestHibpClient:
    def test_api_version_property(self, hibp_client):
        """Test API version property getter and setter"""
        assert hibp_client.api_version == "v3"

        hibp_client.api_version = "v3"
        assert hibp_client.api_version == "v3"
        assert hibp_client._BASE_URL == "https://haveibeenpwned.com/api/v3"

    def test_get_breached_accounts_no_api_key(self, hibp_client, mock_env_without_key):
        """Test exception is raised when no API key is found"""
        with pytest.raises(NoHibpKeyFoundException):
            hibp_client.get_breached_accounts("test@example.com")

    @patch("requests.get")
    def test_get_breached_accounts_success(
        self, mock_get, hibp_client, mock_env_with_key, sample_breach_response
    ):
        """Test successful retrieval of breached accounts"""

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = sample_breach_response
        mock_get.return_value = mock_response

        result = hibp_client.get_breached_accounts("test@example.com")

        # Verify the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert (
            "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com"
            in args[0]
        )
        assert kwargs["headers"] == {"hibp-api-key": "test_api_key"}

        assert len(result) == 1
        assert isinstance(result[0], HibpBreachedSiteModel)
        assert result[0].title == "Dailymotion"
        assert result[0].domain == "dailymotion.com"
        assert result[0].breach_date == "2016-10-20"
        assert result[0].pwn_count == 85176234
        assert len(result[0].data_classes) == 3
        assert "Email addresses" in result[0].data_classes
        assert result[0].is_verified is True
        assert result[0].is_malware is False

    @patch("requests.get")
    def test_get_breached_accounts_truncate_param(
        self, mock_get, hibp_client, mock_env_with_key
    ):
        """Test truncate parameter is passed correctly"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        hibp_client.get_breached_accounts("test@example.com", truncate_response=True)

        args, kwargs = mock_get.call_args
        assert "truncateResponse=true" in args[0]

        hibp_client.get_breached_accounts("test@example.com", truncate_response=False)

        args, kwargs = mock_get.call_args
        assert "truncateResponse=false" in args[0]

    @patch("requests.get")
    def test_get_breached_accounts_no_breaches(
        self, mock_get, hibp_client, mock_env_with_key
    ):
        """Test when no breaches are found"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = hibp_client.get_breached_accounts("test@example.com")
        assert result is None

    @patch("requests.get")
    def test_get_breached_accounts_unauthorized(
        self, mock_get, hibp_client, mock_env_with_key
    ):
        """Test unauthorized API key"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with pytest.raises(HibpCouldNotBeVerifiedException):
            hibp_client.get_breached_accounts("test@example.com")

    @patch("requests.get")
    def test_get_breached_accounts_unexpected_status(
        self, mock_get, hibp_client, mock_env_with_key
    ):
        """Test unexpected status code"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Server error")
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Server error"):
            hibp_client.get_breached_accounts("test@example.com")

    @patch("requests.get")
    def test_get_breached_accounts_request_exception(
        self, mock_get, hibp_client, mock_env_with_key
    ):
        """Test request exception handling"""
        mock_get.side_effect = Exception("Connection error")

        with pytest.raises(Exception, match="Connection error"):
            hibp_client.get_breached_accounts("test@example.com")

    @patch("requests.get")
    def test_get_breached_accounts_multiple_breaches(
        self, mock_get, hibp_client, mock_env_with_key
    ):
        """Test handling multiple breaches in response"""
        # Mock response with multiple breaches
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "Name": "Dailymotion",
                "Title": "Dailymotion",
                "Domain": "dailymotion.com",
                "BreachDate": "2016-10-20",
                "AddedDate": "2017-08-07T02:51:12Z",
                "ModifiedDate": "2017-08-07T02:51:12Z",
                "PwnCount": 85176234,
                "Description": "Breach description",
                "LogoPath": "https://logos.haveibeenpwned.com/Dailymotion.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": ["Email addresses"],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False,
            },
            {
                "Name": "Wattpad",
                "Title": "Wattpad",
                "Domain": "wattpad.com",
                "BreachDate": "2020-06-29",
                "AddedDate": "2020-07-19T22:49:19Z",
                "ModifiedDate": "2020-07-19T22:49:19Z",
                "PwnCount": 268765495,
                "Description": "Breach description",
                "LogoPath": "https://logos.haveibeenpwned.com/Wattpad.png",
                "Attribution": None,
                "DisclosureUrl": None,
                "DataClasses": ["Email addresses", "Passwords"],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": False,
                "IsStealerLog": False,
            },
        ]
        mock_get.return_value = mock_response

        result = hibp_client.get_breached_accounts("test@example.com")

        assert len(result) == 2
        assert result[0].name == "Dailymotion"
        assert result[1].name == "Wattpad"
        assert result[1].pwn_count == 268765495
