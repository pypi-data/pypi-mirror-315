from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_not_found_error import HTTPNotFoundError
from ...models.http_validation_error import HTTPValidationError
from ...models.wkt import WKT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search_term_kw: str,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    is_clean_formatting: Union[None, Unset, bool] = True,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["search_term_kw"] = search_term_kw

    params["limit"] = limit

    params["offset"] = offset

    json_is_clean_formatting: Union[None, Unset, bool]
    if isinstance(is_clean_formatting, Unset):
        json_is_clean_formatting = UNSET
    else:
        json_is_clean_formatting = is_clean_formatting
    params["is_clean_formatting"] = json_is_clean_formatting

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/ws/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPNotFoundError, HTTPValidationError, List["WKT"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = WKT.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = HTTPNotFoundError.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPNotFoundError, HTTPValidationError, List["WKT"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_term_kw: str,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    is_clean_formatting: Union[None, Unset, bool] = True,
) -> Response[Union[HTTPNotFoundError, HTTPValidationError, List["WKT"]]]:
    """Search a WKT by keyword

     Search a WKT by keyword

    Args:
        search_term_kw (str):
        limit (Union[Unset, int]): Number of records to display Default: 50.
        offset (Union[Unset, int]): Number of records from which we start to display Default: 0.
        is_clean_formatting (Union[None, Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPNotFoundError, HTTPValidationError, List['WKT']]]
    """

    kwargs = _get_kwargs(
        search_term_kw=search_term_kw,
        limit=limit,
        offset=offset,
        is_clean_formatting=is_clean_formatting,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search_term_kw: str,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    is_clean_formatting: Union[None, Unset, bool] = True,
) -> Optional[Union[HTTPNotFoundError, HTTPValidationError, List["WKT"]]]:
    """Search a WKT by keyword

     Search a WKT by keyword

    Args:
        search_term_kw (str):
        limit (Union[Unset, int]): Number of records to display Default: 50.
        offset (Union[Unset, int]): Number of records from which we start to display Default: 0.
        is_clean_formatting (Union[None, Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPNotFoundError, HTTPValidationError, List['WKT']]
    """

    return sync_detailed(
        client=client,
        search_term_kw=search_term_kw,
        limit=limit,
        offset=offset,
        is_clean_formatting=is_clean_formatting,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_term_kw: str,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    is_clean_formatting: Union[None, Unset, bool] = True,
) -> Response[Union[HTTPNotFoundError, HTTPValidationError, List["WKT"]]]:
    """Search a WKT by keyword

     Search a WKT by keyword

    Args:
        search_term_kw (str):
        limit (Union[Unset, int]): Number of records to display Default: 50.
        offset (Union[Unset, int]): Number of records from which we start to display Default: 0.
        is_clean_formatting (Union[None, Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPNotFoundError, HTTPValidationError, List['WKT']]]
    """

    kwargs = _get_kwargs(
        search_term_kw=search_term_kw,
        limit=limit,
        offset=offset,
        is_clean_formatting=is_clean_formatting,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search_term_kw: str,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    is_clean_formatting: Union[None, Unset, bool] = True,
) -> Optional[Union[HTTPNotFoundError, HTTPValidationError, List["WKT"]]]:
    """Search a WKT by keyword

     Search a WKT by keyword

    Args:
        search_term_kw (str):
        limit (Union[Unset, int]): Number of records to display Default: 50.
        offset (Union[Unset, int]): Number of records from which we start to display Default: 0.
        is_clean_formatting (Union[None, Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPNotFoundError, HTTPValidationError, List['WKT']]
    """

    return (
        await asyncio_detailed(
            client=client,
            search_term_kw=search_term_kw,
            limit=limit,
            offset=offset,
            is_clean_formatting=is_clean_formatting,
        )
    ).parsed
