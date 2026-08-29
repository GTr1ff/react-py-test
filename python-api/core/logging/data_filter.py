import re
import logging
from typing import Any

from fastapi.datastructures import Headers

logger = logging.getLogger("app")


class SensitiveDataLoggingFilter(logging.Filter):
    """Logging filter that uses SensitiveLogDataMasker to redact sensitive data from log records."""

    PLACEHOLDER = "[log message withheld: masking failed]"

    def __init__(self):
        super().__init__()
        self.masker = SensitiveLogDataMasker()

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter and redact sensitive data from a log record."""
        try:
            # Mask structured args by key/value (e.g. a dict body with a
            # "password" field) BEFORE the message is rendered.
            if record.args:
                record.args = self.masker.mask_data(record.args)

            # Render the final message and scrub key/value + token patterns
            # in the text, then clear args since it is now baked into msg.
            record.msg = self.masker.mask_string(record.getMessage())
        except Exception:
            record.msg = self.PLACEHOLDER
        record.args = None
        return True


class SensitiveLogDataMasker:
    """Contains sensitive data masking and filtering logic."""

    MASKED_VALUE = "******"

    def __init__(self):
        # Headers that are safe to log. Everything not in this allowlist is
        # dropped by filter_request_headers. Add or remove as needed.
        self.SAFE_HEADERS = {
            'content-type', 'content-length', 'user-agent', 'accept',
            'accept-encoding', 'accept-language', 'host', 'referer',
            'x-forwarded-for', 'x-real-ip', 'x-request-id'
        }

        # Key-name detection is token-aware: the field name is split on "_",
        # "-", whitespace and camelCase boundaries, and each token is compared
        # exactly. This catches "key", "apiKey", "private_key" and
        # "signing_key" without masking "monkey", "bypass" or "author".
        self.KEY_TOKEN_SPLIT = re.compile(r"[_\-\s]+|(?<=[a-z0-9])(?=[A-Z])")

        # Short/ambiguous words: match only as whole tokens.
        self.SENSITIVE_KEY_TOKENS = {"key", "pwd", "pass", "auth", "csrf", "bearer"}

        # Long, unambiguous words: match anywhere in the name, so glued
        # names like "mypassword" or "APIKey" are caught. Keep each keyword
        # in exactly one of these two structures.
        self.SENSITIVE_KEY_PATTERN = re.compile(
            r"password|passwd|secret|token|credential|api[-_]?key"
            r"|session[-_]?id|authorization|authentication",
            re.IGNORECASE,
        )

        # Known safe names containing a sensitive token, compared against
        # the normalized snake_case form of the field name.
        self.SAFE_KEYS = {"primary_key", "sort_key", "foreign_key"}

        # Keywords used to build the in-text key=value / key: value patterns.
        keywords = (
            r"password|passwd|pwd|secret|secret[-_]?key|api[-_]?key|access[-_]?token"
            r"|refresh[-_]?token|csrf[-_]?token|token|credentials?|authorization"
            r"|authentication|session[-_]?id"
        )

        # Regex patterns for sensitive data appearing inside rendered text.
        self.SENSITIVE_PATTERNS = [
            # key=value, key: value and "key": "value" 
            (re.compile(rf'\b({keywords})\b(["\']?\s*[:=]\s*["\']?)([^&\s;,"\']+)', re.IGNORECASE),
             rf'\1\2{self.MASKED_VALUE}'),
            # Authorization scheme prefixes.
            (re.compile(r'\b(Bearer|Basic)\s+[a-z0-9\-._~+/]+=*', re.IGNORECASE),
             rf'\1 {self.MASKED_VALUE}'),
            # JWTs (header.payload.signature, base64url).
            (re.compile(r'\beyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'),
             self.MASKED_VALUE),
        ]

    def filter_request_headers(self, headers: Headers) -> dict:
        """Remove sensitive headers for logging purposes (allowlist)."""
        return {
            key: value for key, value in headers.items()
            if key.lower() in self.SAFE_HEADERS
        }

    def _is_sensitive_key(self, key: Any) -> bool:
        """Return True if a mapping key name looks sensitive."""
        name = str(key)
        tokens = [t.lower() for t in self.KEY_TOKEN_SPLIT.split(name) if t]
        if "_".join(tokens) in self.SAFE_KEYS:
            return False
        if set(tokens) & self.SENSITIVE_KEY_TOKENS:
            return True
        return bool(self.SENSITIVE_KEY_PATTERN.search(name))

    def mask_data(self, data: Any) -> Any:
        """Mask sensitive data in supported types only."""
        if isinstance(data, dict):
            return self.mask_dict(data)
        elif isinstance(data, str):
            return self.mask_string(data)
        elif isinstance(data, tuple):
            return tuple(self.mask_data(item) for item in data)
        elif isinstance(data, list):
            return [self.mask_data(item) for item in data]
        else:
            return data

    def mask_dict(self, data: dict) -> Any:
        """Mask sensitive data in a dictionary (non-mutating)."""
        if not isinstance(data, dict):
            return data

        masked_data = {}
        for key, value in data.items():
            if self._is_sensitive_key(key):
                masked_data[key] = self.MASKED_VALUE
            else:
                masked_data[key] = self.mask_data(value)
        return masked_data

    def mask_string(self, text: str) -> Any:
        """Mask sensitive data in a string."""
        if not isinstance(text, str):
            return text

        masked_text = text
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            masked_text = pattern.sub(replacement, masked_text)
        return masked_text


log_data_masker = SensitiveLogDataMasker()