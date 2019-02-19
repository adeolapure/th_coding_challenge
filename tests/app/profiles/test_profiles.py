import unittest
from unittest import mock

import requests
import responses

from app.profiles.profiles import (
    BitbucketProfileSummary,
    GitProfileSummary,
    GitHubProfileSummary,
    exc
)


class GitProfileSummaryTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch.object(GitProfileSummary, '__abstractmethods__', new=set())
        self.patcher.start()

    def doCleanups(self):
        self.patcher.stop()
        return super().doCleanups()


class GitProfileSummaryResetTestCase(GitProfileSummaryTestCase):
    def test_clears_state(self):
        profile = GitProfileSummary('someone')
        profile._loaded_state = {'some': 'stuff', 'goes': ['h', 'e', 'r', 'e']}

        profile.reset()
        self.assertDictEqual(profile._loaded_state, {})


class GitProfileSummaryValidateUsernameTestCase(GitProfileSummaryTestCase):
    @responses.activate
    def test_valid_username(self):
        responses.add(responses.HEAD, 'https://example.com', status=200)
        mock_validation_url = mock.PropertyMock(return_value='https://example.com')

        with mock.patch.object(GitProfileSummary, '_username_validation_url', new_callable=mock_validation_url):
            self.assertTrue(GitProfileSummary('someone').validate_username())

    @responses.activate
    def test_invalid_username_raises_error(self):
        responses.add(responses.HEAD, 'https://example.com', status=404)
        mock_validation_url = mock.PropertyMock(return_value='https://example.com')
        with mock.patch.object(GitProfileSummary, '_username_validation_url', new_callable=mock_validation_url):

            with self.assertRaises(exc.ProfileNotFoundError) as ctx:
                GitProfileSummary('someone').validate_username()

        self.assertEqual(
            str(ctx.exception),
            f'{GitProfileSummary.PROVIDER} could not find a profile for user: someone'
        )


class GitProfileSummaryHandleResponseTestCase(GitProfileSummaryTestCase):
    def test_returns_response_with_acceptable_status_code(self):
        response = requests.Response()
        response.status_code = 201

        self.assertIs(
            GitProfileSummary('someone')._handle_response(response, (200, 201)),
            response
        )

    def test_raises_UpstreamRateLimit_when_unexpected_403_encountered(self):
        response = requests.Response()
        response.status_code = 403

        profile = GitProfileSummary('someone')
        with self.assertRaises(exc.UpstreamRateLimit) as ctx:
            profile._handle_response(response)

        self.assertEqual(str(ctx.exception), str(profile.PROVIDER))

    def test_raises_APIError_when_unexpected_400_encountered(self):
        response = requests.Response()
        response.status_code = 400
        response.request = requests.Request('GET', 'https://example.com')

        profile = GitProfileSummary('someone')
        with self.assertRaises(exc.APIError) as ctx:
            profile._handle_response(response)

        self.assertEqual(
            str(ctx.exception),
            'Received unexpected response for GET request to https://example.com: 400'
        )
