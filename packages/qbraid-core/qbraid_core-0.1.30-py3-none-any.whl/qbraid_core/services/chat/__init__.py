# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module providing client for interacting with qBraid chat service.

.. currentmodule:: qbraid_core.services.chat

Classes
--------

.. autosummary::
   :toctree: ../stubs/

   ChatClient

Exceptions
------------

.. autosummary::
   :toctree: ../stubs/

   ChatServiceRequestError
   ChatServiceRuntimeError

"""
from .client import ChatClient
from .exceptions import ChatServiceRequestError, ChatServiceRuntimeError

__all__ = [
    "ChatClient",
    "ChatServiceRequestError",
    "ChatServiceRuntimeError",
]
