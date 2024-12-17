from http import HTTPStatus
from typing import Any, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_log import ResourceLog
from ...types import Response


def _get_kwargs(
    function_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/functions/{function_name}/logs",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ResourceLog"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ResourceLog.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ResourceLog"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[List["ResourceLog"]]:
    """
    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ResourceLog']]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    function_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[List["ResourceLog"]]:
    """
    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ResourceLog']
    """

    return sync_detailed(
        function_name=function_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    function_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[List["ResourceLog"]]:
    """
    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ResourceLog']]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    function_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[List["ResourceLog"]]:
    """
    Args:
        function_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ResourceLog']
    """

    return (
        await asyncio_detailed(
            function_name=function_name,
            client=client,
        )
    ).parsed
