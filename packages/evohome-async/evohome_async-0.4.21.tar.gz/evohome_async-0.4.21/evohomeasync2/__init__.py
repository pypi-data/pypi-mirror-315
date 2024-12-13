#!/usr/bin/env python3
"""evohomeasync2 provides an async client for the *updated* Evohome API.

It is (largely) a faithful port of https://github.com/watchforstock/evohome-client

Further information at: https://evohome-client.readthedocs.io
"""

from .base import EvohomeClient  # noqa: F401
from .broker import Broker  # noqa: F401
from .controlsystem import ControlSystem  # noqa: F401
from .exceptions import (  # noqa: F401
    AuthenticationFailed,
    DeprecationError,
    EvohomeError,
    InvalidParameter,
    InvalidSchedule,
    InvalidSchema,
    NoSingleTcsError,
    RateLimitExceeded,
    RequestFailed,
)
from .gateway import Gateway  # noqa: F401
from .hotwater import HotWater  # noqa: F401
from .location import Location  # noqa: F401
from .zone import Zone  # noqa: F401

__version__ = "0.4.21"
