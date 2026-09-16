import logging
from collections import namedtuple

import pytest
from fastapi.datastructures import Headers

from core.logging.data_filter import (
    SensitiveDataLoggingFilter,
    SensitiveLogDataMasker,
)


class TestSensitiveLogDataMasker:
    """Test cases for the SensitiveLogDataMasker."""

    MASKED_VALUE = "******"

    @pytest.fixture
    def log_data_masker(self):
        return SensitiveLogDataMasker()

    @pytest.fixture
    def sample_headers(self):
        return Headers({
            'content-type': 'application/json',
            'authorization': 'Bearer secret-token-123',
            'user-agent': 'Mozilla/5.0',
            'x-api-key': 'secret-api-key',
            'host': 'example.com',
            'accept': 'application/json'
        })

    @pytest.fixture
    def sample_dict_data(self):
        return {
            'username': 'john_doe',
            'password': 'DUMMY_PASSWORD',
            'email': 'john@example.com',
            'api_key': 'sk-1234567890',
            'token': 'DUMMY_TOKEN',
            'normal_field': 'safe_value'
        }

    @pytest.fixture
    def sample_string_data(self):
        return "username=john&password=DUMMY_PASSWORD&api_key=sk-1234567890&Bearer DUMMY_TOKEN"

    # ─── filter_request_headers tests ──────────────────────────────────
    def test_filter_request_headers_keeps_safe_headers(self, log_data_masker, sample_headers):
        """Safe headers are preserved."""
        result = log_data_masker.filter_request_headers(sample_headers)

        assert 'content-type' in result
        assert 'user-agent' in result
        assert 'host' in result
        assert 'accept' in result
        assert result['content-type'] == 'application/json'
        assert result['user-agent'] == 'Mozilla/5.0'

    def test_filter_request_headers_removes_sensitive_headers(self, log_data_masker, sample_headers):
        """Sensitive headers are removed."""
        result = log_data_masker.filter_request_headers(sample_headers)

        assert 'authorization' not in result
        assert 'x-api-key' not in result

    def test_filter_request_headers_case_insensitive(self, log_data_masker):
        """Header filtering is case-insensitive."""
        headers = Headers({
            'Content-Type': 'application/json',
            'AUTHORIZATION': 'Bearer token',
            'User-Agent': 'Mozilla/5.0'
        })

        result = log_data_masker.filter_request_headers(headers)

        assert 'content-type' in result
        assert 'user-agent' in result
        assert 'authorization' not in result

    def test_filter_request_headers_empty_headers(self, log_data_masker):
        """Filtering with empty headers returns an empty dict."""
        headers = Headers({})
        result = log_data_masker.filter_request_headers(headers)

        assert result == {}

    # ─── mask_dict tests ──────────────────────────────────
    def test_mask_dict_masks_sensitive_keys(self, log_data_masker, sample_dict_data):
        """Sensitive keys are masked in dictionaries."""
        result = log_data_masker.mask_dict(sample_dict_data)

        assert result['username'] == 'john_doe'
        assert result['password'] == self.MASKED_VALUE
        assert result['email'] == 'john@example.com'
        assert result['api_key'] == self.MASKED_VALUE
        assert result['token'] == self.MASKED_VALUE
        assert result['normal_field'] == 'safe_value'

    def test_mask_dict_case_insensitive_keys(self, log_data_masker):
        """Key masking is case-insensitive."""
        data = {
            'PASSWORD': 'DUMMY_PASSWORD',
            'Api_Key': 'sk-1234567890',
            'TOKEN': 'access_token'
        }

        result = log_data_masker.mask_dict(data)

        assert result['PASSWORD'] == self.MASKED_VALUE
        assert result['Api_Key'] == self.MASKED_VALUE
        assert result['TOKEN'] == self.MASKED_VALUE

    def test_mask_dict_substring_keys(self, log_data_masker):
        """Substring key matching catches realistic compound key names."""
        data = {
            'user_password': 'DUMMY_PASSWORD',
            'apiKey': 'sk-123',
            'x-api-key': 'sk-456',
            'stripe_secret': 'sk_live_x',
            'session_id': 'abc',
            'username': 'john',
        }

        result = log_data_masker.mask_dict(data)

        assert result['user_password'] == self.MASKED_VALUE
        assert result['apiKey'] == self.MASKED_VALUE
        assert result['x-api-key'] == self.MASKED_VALUE
        assert result['stripe_secret'] == self.MASKED_VALUE
        assert result['session_id'] == self.MASKED_VALUE
        assert result['username'] == 'john'

    def test_mask_dict_token_matching(self, log_data_masker):
        """Whole-token matching masks bare and compound key fields but not
        words that merely contain a sensitive substring."""
        data = {
            'key': 'sk-123',
            'private_key': 'PEM_DATA',
            'signing_key': 'hmac-secret',
            'encryptionKey': 'aes-256',
            'monkey': 'banana',
            'bypass': True,
            'author': 'john',
        }

        result = log_data_masker.mask_dict(data)

        assert result['key'] == self.MASKED_VALUE
        assert result['private_key'] == self.MASKED_VALUE
        assert result['signing_key'] == self.MASKED_VALUE
        assert result['encryptionKey'] == self.MASKED_VALUE
        assert result['monkey'] == 'banana'
        assert result['bypass'] is True
        assert result['author'] == 'john'

    def test_mask_dict_benign_key_allowlist(self, log_data_masker):
        """Known-benign identifier fields are not masked despite the "key" token."""
        data = {
            'primary_key': 42,
            'sort_key': 'created_at',
            'foreign_key': 'user_id',
            'primaryKey': 7,  # camelCase normalizes to the same allowlist entry
        }

        result = log_data_masker.mask_dict(data)

        assert result['primary_key'] == 42
        assert result['sort_key'] == 'created_at'
        assert result['foreign_key'] == 'user_id'
        assert result['primaryKey'] == 7

    def test_mask_dict_nested_masking(self, log_data_masker):
        """Nested dictionaries are also masked."""
        data = {
            'user': {
                'name': 'john',
                'password': 'DUMMY_PASSWORD'
            },
            'api_key': 'sk-1234567890'
        }

        result = log_data_masker.mask_dict(data)

        assert result['user']['name'] == 'john'
        assert result['user']['password'] == self.MASKED_VALUE
        assert result['api_key'] == self.MASKED_VALUE

    def test_mask_dict_non_dict_input(self, log_data_masker):
        """Non-dict input is returned unchanged."""
        assert log_data_masker.mask_dict("not a dict") == "not a dict"
        assert log_data_masker.mask_dict(123) == 123

    def test_mask_dict_empty_dict(self, log_data_masker):
        """Masking an empty dictionary returns an empty dict."""
        assert log_data_masker.mask_dict({}) == {}

    def test_mask_dict_with_none_values(self, log_data_masker):
        """None values under sensitive keys are still masked."""
        data = {
            'username': 'john',
            'password': None,
            'api_key': 'sk-1234567890'
        }

        result = log_data_masker.mask_dict(data)

        assert result['username'] == 'john'
        assert result['password'] == self.MASKED_VALUE
        assert result['api_key'] == self.MASKED_VALUE

    def test_mask_dict_non_string_keys(self, log_data_masker):
        """Non-string keys do not crash and are treated as non-sensitive."""
        data = {1: 'one', 2: 'two', ('a', 'b'): 'tuple-key'}

        result = log_data_masker.mask_dict(data)

        assert result[1] == 'one'
        assert result[2] == 'two'
        assert result[('a', 'b')] == 'tuple-key'

    # ─── mask_string tests ──────────────────────────────────
    def test_mask_string_masks_patterns(self, log_data_masker, sample_string_data):
        """Sensitive key=value and Bearer patterns in strings are masked."""
        result = log_data_masker.mask_string(sample_string_data)

        assert f'password={self.MASKED_VALUE}' in result
        assert f'api_key={self.MASKED_VALUE}' in result
        assert f'Bearer {self.MASKED_VALUE}' in result
        assert 'username=john' in result

    def test_mask_string_case_insensitive(self, log_data_masker):
        """String masking is case-insensitive."""
        text = "PASSWORD=DUMMY_PASSWORD&API_KEY=sk-1234567890&BEARER token123"
        result = log_data_masker.mask_string(text)

        assert f'PASSWORD={self.MASKED_VALUE}' in result
        assert f'API_KEY={self.MASKED_VALUE}' in result
        assert f'BEARER {self.MASKED_VALUE}' in result

    def test_mask_string_duplicate_sensitive_keys(self, log_data_masker):
        """Multiple occurrences of a sensitive key are all masked."""
        text = "PASSWORD=DUMMY_PASSWORD&password=DUMMY_PASSWORD"
        result = log_data_masker.mask_string(text)

        assert result == f"PASSWORD={self.MASKED_VALUE}&password={self.MASKED_VALUE}"

    def test_mask_string_json_colon_form(self, log_data_masker):
        """JSON-ish "key": "value" forms are masked, not just key=value."""
        text = '{"username": "john", "password": "DUMMY_PASSWORD"}'
        result = log_data_masker.mask_string(text)

        assert 'DUMMY_PASSWORD' not in result
        assert self.MASKED_VALUE in result
        assert 'john' in result

    def test_mask_string_jwt(self, log_data_masker):
        """Bare JWTs are masked even without a preceding key."""
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NSJ9.abcDEF123"
        text = f"issued token {jwt} to user"
        result = log_data_masker.mask_string(text)

        assert jwt not in result
        assert self.MASKED_VALUE in result

    def test_mask_string_word_boundary(self, log_data_masker):
        """Non-sensitive keys that merely contain a sensitive substring are left alone."""
        text = "monkey=banana&passenger=alice"
        result = log_data_masker.mask_string(text)

        assert result == text

    def test_mask_string_non_string_input(self, log_data_masker):
        """Non-string input is returned unchanged."""
        assert log_data_masker.mask_string(123) == 123

    def test_mask_string_empty_string(self, log_data_masker):
        """Masking an empty string returns an empty string."""
        assert log_data_masker.mask_string("") == ""

    def test_mask_string_no_sensitive_data(self, log_data_masker):
        """A string with no sensitive data is unchanged."""
        text = "username=john&email=john@example.com&age=25"
        assert log_data_masker.mask_string(text) == text

    def test_mask_string_with_special_characters(self, log_data_masker):
        """Special characters in values do not break masking."""
        text = "password=secret!@#$%^&*()&api_key=sk-1234567890"  # NOSONAR
        result = log_data_masker.mask_string(text)

        assert f'password={self.MASKED_VALUE}' in result
        assert f'api_key={self.MASKED_VALUE}' in result

    def test_mask_string_with_multiple_patterns(self, log_data_masker):
        """Multiple sensitive patterns in one string are all masked."""
        text = "password=DUMMY_PASSWORD&api_key=sk-123&token=abc456&Bearer xyz789"
        result = log_data_masker.mask_string(text)

        assert f'password={self.MASKED_VALUE}' in result
        assert f'api_key={self.MASKED_VALUE}' in result
        assert f'token={self.MASKED_VALUE}' in result
        assert f'Bearer {self.MASKED_VALUE}' in result

    # ─── mask_data tests ──────────────────────────────────
    def test_mask_data_with_dict(self, log_data_masker, sample_dict_data):
        """mask_data dispatches dicts to mask_dict."""
        result = log_data_masker.mask_data(sample_dict_data)

        assert result['password'] == self.MASKED_VALUE
        assert result['username'] == 'john_doe'

    def test_mask_data_with_string(self, log_data_masker, sample_string_data):
        """mask_data dispatches strings to mask_string."""
        result = log_data_masker.mask_data(sample_string_data)

        assert f'password={self.MASKED_VALUE}' in result
        assert 'username=john' in result

    def test_mask_data_with_list(self, log_data_masker):
        """mask_data recurses into lists and preserves the list type."""
        data = [
            {'username': 'john', 'password': 'DUMMY_PASSWORD'},
            'password=DUMMY_PASSWORD&api_key=sk-123'
        ]

        result = log_data_masker.mask_data(data)

        assert result[0]['password'] == self.MASKED_VALUE
        assert f'password={self.MASKED_VALUE}' in result[1]
        assert isinstance(result, list)

    def test_mask_data_with_tuple(self, log_data_masker):
        """mask_data recurses into tuples and preserves the tuple type."""
        data = (
            {'username': 'john', 'password': 'DUMMY_PASSWORD'},
            'password=DUMMY_PASSWORD'
        )

        result = log_data_masker.mask_data(data)

        assert result[0]['password'] == self.MASKED_VALUE
        assert f'password={self.MASKED_VALUE}' in result[1]
        assert isinstance(result, tuple)

    def test_mask_data_with_namedtuple(self, log_data_masker):
        """Namedtuples do not crash (built as a plain tuple)."""
        Point = namedtuple("Point", ["x", "password"])
        data = Point(x=1, password="DUMMY_PASSWORD")

        result = log_data_masker.mask_data(data)

        # Returned as a plain tuple; positional order preserved.
        assert isinstance(result, tuple)
        assert result[0] == 1
        # A namedtuple field name is not visible to string/dict masking, so the
        # value passes through unchanged — this documents the boundary.
        assert result[1] == "DUMMY_PASSWORD"

    def test_mask_data_with_object_returned_unchanged(self, log_data_masker):
        """Arbitrary objects are NOT traversed; they are returned as-is."""
        class TestObject:
            def __init__(self):
                self.password = 'DUMMY_PASSWORD'
                self.username = 'john'

        obj = TestObject()
        result = log_data_masker.mask_data(obj)

        assert result is obj
        assert obj.password == 'DUMMY_PASSWORD'  # not mutated

    def test_mask_data_with_primitive_types(self, log_data_masker):
        """Primitive types pass through unchanged."""
        assert log_data_masker.mask_data(123) == 123
        assert log_data_masker.mask_data(True) is True
        assert log_data_masker.mask_data(None) is None

    # ─── _is_sensitive_key tests ──────────────────────────────────
    def test_is_sensitive_key(self, log_data_masker):
        """Key-name detection is token-aware, with word-safe negatives."""
        # Whole-token matches (short/ambiguous words).
        assert log_data_masker._is_sensitive_key("key")
        assert log_data_masker._is_sensitive_key("private_key")
        assert log_data_masker._is_sensitive_key("auth")
        assert log_data_masker._is_sensitive_key("pass")
        # Contains matches (long/unambiguous words, including glued names).
        assert log_data_masker._is_sensitive_key("password")
        assert log_data_masker._is_sensitive_key("user_password")
        assert log_data_masker._is_sensitive_key("mypassword")
        assert log_data_masker._is_sensitive_key("apiKey")
        assert log_data_masker._is_sensitive_key("x-api-key")
        assert log_data_masker._is_sensitive_key("authorization")
        # Negatives: substrings inside a different word do not match.
        assert log_data_masker._is_sensitive_key("monkey") is False
        assert log_data_masker._is_sensitive_key("keyboard") is False
        assert log_data_masker._is_sensitive_key("bypass") is False
        assert log_data_masker._is_sensitive_key("author") is False
        # Benign allowlist overrides the "key" token.
        assert log_data_masker._is_sensitive_key("primary_key") is False
        assert log_data_masker._is_sensitive_key("sort_key") is False
        # Non-string and plain keys.
        assert log_data_masker._is_sensitive_key(123) is False
        assert log_data_masker._is_sensitive_key("username") is False
        assert log_data_masker._is_sensitive_key("email") is False

    def test_safe_headers_configuration(self, log_data_masker):
        """Safe headers allowlist is correct."""
        expected_headers = {
            'content-type', 'content-length', 'user-agent', 'accept',
            'accept-encoding', 'accept-language', 'host', 'referer',
            'x-forwarded-for', 'x-real-ip', 'x-request-id'
        }

        assert log_data_masker.SAFE_HEADERS == expected_headers


class TestSensitiveDataLoggingFilter:
    """Test cases for the logging.Filter integration."""

    MASKED_VALUE = "******"

    @pytest.fixture
    def filter_instance(self):
        return SensitiveDataLoggingFilter()

    def _make_record(self, msg, args=None):
        return logging.LogRecord(
            name="app",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg=msg,
            args=args,
            exc_info=None,
        )

    def test_filter_returns_true(self, filter_instance):
        """The filter always delivers the record."""
        record = self._make_record("nothing sensitive here")
        assert filter_instance.filter(record) is True

    def test_filter_masks_plain_message(self, filter_instance):
        """A sensitive key=value in the message text is masked."""
        record = self._make_record("login password=DUMMY_PASSWORD ok")
        filter_instance.filter(record)

        assert "DUMMY_PASSWORD" not in record.getMessage()
        assert self.MASKED_VALUE in record.getMessage()

    def test_filter_masks_structured_args(self, filter_instance):
        """A sensitive value passed via %-args is masked before rendering."""
        record = self._make_record("request body: %s", args=({"password": "DUMMY_PASSWORD"},))
        filter_instance.filter(record)

        rendered = record.getMessage()
        assert "DUMMY_PASSWORD" not in rendered
        assert self.MASKED_VALUE in rendered
        # args are cleared after rendering.
        assert record.args is None

    def test_filter_masks_object_via_rendering(self, filter_instance):
        """An object arg is scrubbed at the string level, not by traversal."""
        class Body:
            def __repr__(self):
                return "Body(password=DUMMY_PASSWORD)"

        record = self._make_record("body=%s", args=(Body(),))
        filter_instance.filter(record)

        assert "DUMMY_PASSWORD" not in record.getMessage()

    def test_filter_cyclic_object_arg_does_not_hang(self, filter_instance):
        """A cyclic object in args must not cause infinite recursion."""
        class Node:
            def __repr__(self):
                return "Node(secret=DUMMY)"

        a = Node()
        b = Node()
        a.b = b
        b.a = a

        record = self._make_record("node=%s", args=(a,))
        assert filter_instance.filter(record) is True

    def test_filter_fails_closed_on_error(self, filter_instance, monkeypatch):
        """If masking raises, the message is withheld but the record is delivered."""
        def boom(_text):
            raise RuntimeError("mask failure")

        monkeypatch.setattr(filter_instance.masker, "mask_string", boom)

        record = self._make_record("password=DUMMY_PASSWORD")
        result = filter_instance.filter(record)

        assert result is True
        assert record.msg == SensitiveDataLoggingFilter.PLACEHOLDER
        assert "DUMMY_PASSWORD" not in str(record.msg)