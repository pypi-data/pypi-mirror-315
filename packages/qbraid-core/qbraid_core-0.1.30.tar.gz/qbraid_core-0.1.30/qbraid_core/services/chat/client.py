# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module providing client for interacting with the qBraid chat service.

"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator, Literal, Optional, Union

from qbraid_core.client import QbraidClient
from qbraid_core.exceptions import RequestsApiError
from qbraid_core.registry import register_client

from .exceptions import ChatServiceRequestError

if TYPE_CHECKING:
    from requests import Response


@register_client()
class ChatClient(QbraidClient):
    """Client for interacting with qBraid chat service."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
        response_format: Optional[Literal["text", "code", "json"]] = None,
    ) -> dict[str, Any]:
        """Fetch the full chat response as a dictionary.

        Args:
            prompt (str): The prompt to send to the chat service.
            model (str, optional): The model to use for the chat response.
            response_format (str, optional): The format of the response. Defaults to 'text'.

        Returns:
            dict[str, Any]: The complete response as a dictionary.

        Raises:
            ChatServiceRequestError: If the chat request fails.
        """
        response_format = response_format or "json"
        response = self._post_chat_request(
            prompt, model, stream=False, response_format=response_format
        )
        response_json = response.json()
        if response_format == "json":
            return response_json
        return response_json["content"]

    def chat_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        response_format: Optional[Literal["text", "code"]] = None,
    ) -> Generator[str, None, None]:
        """Stream chat response chunks.

        Args:
            prompt (str): The prompt to send to the chat service.
            model (str, optional): The model to use for the chat response.
            response_format (str, optional): The format of the response. Defaults to 'text'.

        Returns:
            Generator[str, None, None]: A generator that yields chunks of the response.

        Raises:
            ChatServiceRequestError: If the chat request fails.
        """
        response_format = response_format or "text"
        response = self._post_chat_request(
            prompt, model, stream=True, response_format=response_format
        )
        yield from response.iter_content(decode_unicode=True)

    def _post_chat_request(
        self,
        prompt: str,
        model: Optional[str],
        stream: bool,
        response_format: Literal["text", "code", "json"],
    ) -> Response:
        """Send a POST request to the chat endpoint with error handling.

        Args:
            prompt (str): The prompt to send to the chat service.
            model (str, optional): The model to use for the chat response.
            stream (bool): Whether the response should be streamed.

        Returns:
            Response: The response object from the POST request.

        Raises:
            ChatServiceRequestError: If the chat request fails.
        """
        if response_format == "code":
            prompt += " Return only raw code. Do not include any text outside of code blocks."

        payload = {"prompt": prompt, "stream": stream}
        if model:
            payload["model"] = model

        try:
            return self.session.post("/chat", json=payload, stream=stream)
        except RequestsApiError as err:
            raise ChatServiceRequestError(f"Failed to get chat response: {err}") from err

    def get_models(
        self, params: Optional[dict[str, Any]] = None
    ) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """Fetch available models or details of a specific model.

        Args:
            params (dict[str, Any], optional): Optional parameters to filter models.

        Returns:
            list[dict[str, Any]] | dict[str, Any]: A list of models or a specific model.

        Raises:
            ChatServiceRequestError: If the request fails or the model is not found.
        """
        try:
            response = self.session.get("/chat/models", params=params)
            return response.json()
        except RequestsApiError as err:
            raise ChatServiceRequestError(f"Failed to get models: {err}") from err

    def add_model(self, model: str, description: str, pricing: dict[str, float]) -> dict[str, Any]:
        """Add a new chat model to the service.

        Args:
            model (str): The unique identifier for the chat model.
            description (str): A description of the chat model.
            pricing (dict[str, float]): Pricing information with 'input' and 'output' keys.

        Returns:
            dict[str, Any]: The response from the service.

        Raises:
            ChatServiceRequestError: If the request fails.
        """
        payload = {"model": model, "description": description, "pricing": pricing}
        try:
            response = self.session.post("/chat/models", json=payload)
            return response.json()
        except RequestsApiError as err:
            raise ChatServiceRequestError(f"Failed to add model: {err}") from err
