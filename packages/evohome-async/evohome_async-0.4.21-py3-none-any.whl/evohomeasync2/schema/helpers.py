#!/usr/bin/env python3
"""evohomeasync2 schema - shared helpers."""

from __future__ import annotations


def camel_case(s: str) -> str:
    """Convert a PascalCase string to camelCase."""
    return s[:1].lower() + s[1:]


def pascal_case(s: str) -> str:
    """Convert a camelCase string to PascalCase."""
    return s[:1].upper() + s[1:]
