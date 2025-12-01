#!/usr/bin/env python3
"""Unit and integration tests for client"""

import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), {"login": org_name})
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        client = GithubOrgClient("test")
        with patch.object(client, "org", return_value={"repos_url": "url"}):
            self.assertEqual(client._public_repos_url, "url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        client = GithubOrgClient("test")
        mock_get_json.return_value = [{"name": "repo1", "license": {"key": "apache-2.0"}}]
        with patch.object(client, "_public_repos_url", "url"):
            self.assertEqual(client.public_repos(), ["repo1"])
            mock_get_json.assert_called_once()

    def test_has_license(self):
        repo = {"license": {"key": "my_license"}}
        self.assertTrue(GithubOrgClient.has_license(repo, "my_license"))
        self.assertFalse(GithubOrgClient.has_license(repo, "other_license"))

@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), [
    (org_payload, repos_payload, expected_repos, apache2_repos)
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.return_value.json.side_effect = [cls.org_payload, cls.repos_payload]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos_integration(self):
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos(license_key="apache-2.0"), self.apache2_repos)
