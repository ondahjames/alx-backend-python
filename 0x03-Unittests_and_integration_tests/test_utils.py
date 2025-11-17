#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"a": {"b": 2}}["a"]),   # or {"b": 2}
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected results."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
      #!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"a": {"b": 2}}["a"]),   # or {"b": 2}
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected results."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

from unittest.mock import patch

class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test that get_json returns expected JSON payload."""
        mock_get.return_value.json.return_value = {"payload": True}

        from utils import get_json
        result = get_json("http://example.com")

        self.assertEqual(result, {"payload": True})
        mock_get.assert_called_once_with("http://example.com")
class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method results."""
        class TestClass:
            def a_method(self):
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            obj.a_property
            obj.a_property

            mock_method.assert_called_once()
#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns correct value."""
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"org": org_name})

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
    def test_public_repos_url(self):
        """Test the _public_repos_url property."""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}

            client = GithubOrgClient("example")
            result = client._public_repos_url

            self.assertEqual(result, "http://example.com/repos")
    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos method."""
        mock_repos_url.return_value = "http://example.com/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        client = GithubOrgClient("example")
        repos = client.public_repos()

        self.assertEqual(repos, ["repo1"])
        mock_get_json.assert_called_once_with("http://example.com/repos")
    @parameterized.expand([
        ([{"name": "repo1"}], ["repo1"]),
        ([], []),
    ])
    def test_public_repos_param(self, payload, expected):
        """Parameterize repo result outputs."""
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            with patch("client.get_json") as mock_json:
                mock_url.return_value = "http://example.com/repos"
                mock_json.return_value = payload

                client = GithubOrgClient("example")
                self.assertEqual(client.public_repos(), expected)
    def test_has_license(self):
        """Test has_license method correctly matches licenses."""
        client = GithubOrgClient("example")

        repo1 = {"license": {"key": "abc"}}
        repo2 = {"license": {"key": "xyz"}}

        self.assertTrue(client.has_license(repo1, "abc"))
        self.assertFalse(client.has_license(repo2, "abc"))

