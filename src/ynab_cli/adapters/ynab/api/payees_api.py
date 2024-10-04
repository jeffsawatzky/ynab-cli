"""
YNAB API Endpoints

Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.ynab.com

The version of the OpenAPI document: 1.72.1
Generated by OpenAPI Generator (https://openapi-generator.tech)

Do not edit the class manually.
"""

from typing import Annotated, Any

from pydantic import Field, StrictFloat, StrictInt, StrictStr, validate_call

from ynab_cli.adapters.ynab.api_client import ApiClient, RequestSerialized
from ynab_cli.adapters.ynab.api_response import ApiResponse
from ynab_cli.adapters.ynab.models.patch_payee_wrapper import PatchPayeeWrapper
from ynab_cli.adapters.ynab.models.payee_response import PayeeResponse
from ynab_cli.adapters.ynab.models.payees_response import PayeesResponse
from ynab_cli.adapters.ynab.models.save_payee_response import SavePayeeResponse
from ynab_cli.adapters.ynab.rest import RESTResponseType


class PayeesApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_call
    async def get_payee_by_id(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        payee_id: Annotated[StrictStr, Field(description="The id of the payee")],
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> PayeeResponse:
        """Single payee

        Returns a single payee

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param payee_id: The id of the payee (required)
        :type payee_id: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._get_payee_by_id_serialize(
            budget_id=budget_id,
            payee_id=payee_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "PayeeResponse",
            "404": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def get_payee_by_id_with_http_info(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        payee_id: Annotated[StrictStr, Field(description="The id of the payee")],
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[PayeeResponse]:
        """Single payee

        Returns a single payee

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param payee_id: The id of the payee (required)
        :type payee_id: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._get_payee_by_id_serialize(
            budget_id=budget_id,
            payee_id=payee_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "PayeeResponse",
            "404": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def get_payee_by_id_without_preload_content(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        payee_id: Annotated[StrictStr, Field(description="The id of the payee")],
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Single payee

        Returns a single payee

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param payee_id: The id of the payee (required)
        :type payee_id: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._get_payee_by_id_serialize(
            budget_id=budget_id,
            payee_id=payee_id,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "PayeeResponse",
            "404": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        return response_data.response

    def _get_payee_by_id_serialize(
        self,
        budget_id,
        payee_id,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: dict[str, str] = {}

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[str, str | bytes] = {}
        _body_params: bytes | None = None

        # process the path parameters
        if budget_id is not None:
            _path_params["budget_id"] = budget_id
        if payee_id is not None:
            _path_params["payee_id"] = payee_id
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # authentication setting
        _auth_settings: list[str] = ["bearer"]

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/budgets/{budget_id}/payees/{payee_id}",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )

    @validate_call
    async def get_payees(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        last_knowledge_of_server: Annotated[
            StrictInt | None,
            Field(
                description="The starting server knowledge.  If provided, only entities that have changed since `last_knowledge_of_server` will be included."
            ),
        ] = None,
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> PayeesResponse:
        """List payees

        Returns all payees

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param last_knowledge_of_server: The starting server knowledge.  If provided, only entities that have changed since `last_knowledge_of_server` will be included.
        :type last_knowledge_of_server: int
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._get_payees_serialize(
            budget_id=budget_id,
            last_knowledge_of_server=last_knowledge_of_server,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "PayeesResponse",
            "404": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def get_payees_with_http_info(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        last_knowledge_of_server: Annotated[
            StrictInt | None,
            Field(
                description="The starting server knowledge.  If provided, only entities that have changed since `last_knowledge_of_server` will be included."
            ),
        ] = None,
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[PayeesResponse]:
        """List payees

        Returns all payees

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param last_knowledge_of_server: The starting server knowledge.  If provided, only entities that have changed since `last_knowledge_of_server` will be included.
        :type last_knowledge_of_server: int
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._get_payees_serialize(
            budget_id=budget_id,
            last_knowledge_of_server=last_knowledge_of_server,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "PayeesResponse",
            "404": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def get_payees_without_preload_content(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        last_knowledge_of_server: Annotated[
            StrictInt | None,
            Field(
                description="The starting server knowledge.  If provided, only entities that have changed since `last_knowledge_of_server` will be included."
            ),
        ] = None,
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """List payees

        Returns all payees

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param last_knowledge_of_server: The starting server knowledge.  If provided, only entities that have changed since `last_knowledge_of_server` will be included.
        :type last_knowledge_of_server: int
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._get_payees_serialize(
            budget_id=budget_id,
            last_knowledge_of_server=last_knowledge_of_server,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "PayeesResponse",
            "404": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        return response_data.response

    def _get_payees_serialize(
        self,
        budget_id,
        last_knowledge_of_server,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: dict[str, str] = {}

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[str, str | bytes] = {}
        _body_params: bytes | None = None

        # process the path parameters
        if budget_id is not None:
            _path_params["budget_id"] = budget_id
        # process the query parameters
        if last_knowledge_of_server is not None:
            _query_params.append(("last_knowledge_of_server", last_knowledge_of_server))

        # process the header parameters
        # process the form parameters
        # process the body parameter

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # authentication setting
        _auth_settings: list[str] = ["bearer"]

        return self.api_client.param_serialize(
            method="GET",
            resource_path="/budgets/{budget_id}/payees",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )

    @validate_call
    async def update_payee(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        payee_id: Annotated[StrictStr, Field(description="The id of the payee")],
        data: Annotated[PatchPayeeWrapper, Field(description="The payee to update")],
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> SavePayeeResponse:
        """Update a payee

        Update a payee

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param payee_id: The id of the payee (required)
        :type payee_id: str
        :param data: The payee to update (required)
        :type data: PatchPayeeWrapper
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._update_payee_serialize(
            budget_id=budget_id,
            payee_id=payee_id,
            data=data,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "SavePayeeResponse",
            "400": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data

    @validate_call
    async def update_payee_with_http_info(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        payee_id: Annotated[StrictStr, Field(description="The id of the payee")],
        data: Annotated[PatchPayeeWrapper, Field(description="The payee to update")],
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[SavePayeeResponse]:
        """Update a payee

        Update a payee

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param payee_id: The id of the payee (required)
        :type payee_id: str
        :param data: The payee to update (required)
        :type data: PatchPayeeWrapper
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._update_payee_serialize(
            budget_id=budget_id,
            payee_id=payee_id,
            data=data,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "SavePayeeResponse",
            "400": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        await response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )

    @validate_call
    async def update_payee_without_preload_content(
        self,
        budget_id: Annotated[
            StrictStr,
            Field(
                description='The id of the budget. "last-used" can be used to specify the last used budget and "default" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget).'
            ),
        ],
        payee_id: Annotated[StrictStr, Field(description="The id of the payee")],
        data: Annotated[PatchPayeeWrapper, Field(description="The payee to update")],
        _request_timeout: None
        | Annotated[StrictFloat, Field(gt=0)]
        | tuple[Annotated[StrictFloat, Field(gt=0)], Annotated[StrictFloat, Field(gt=0)]] = None,
        _request_auth: dict[StrictStr, Any] | None = None,
        _content_type: StrictStr | None = None,
        _headers: dict[StrictStr, Any] | None = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Update a payee

        Update a payee

        :param budget_id: The id of the budget. \"last-used\" can be used to specify the last used budget and \"default\" can be used if default budget selection is enabled (see: https://api.ynab.com/#oauth-default-budget). (required)
        :type budget_id: str
        :param payee_id: The id of the payee (required)
        :type payee_id: str
        :param data: The payee to update (required)
        :type data: PatchPayeeWrapper
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """

        _param = self._update_payee_serialize(
            budget_id=budget_id,
            payee_id=payee_id,
            data=data,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index,
        )

        _response_types_map: dict[str, str | None] = {
            "200": "SavePayeeResponse",
            "400": "ErrorResponse",
        }
        response_data = await self.api_client.call_api(*_param, _request_timeout=_request_timeout)
        return response_data.response

    def _update_payee_serialize(
        self,
        budget_id,
        payee_id,
        data,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:
        _host = None

        _collection_formats: dict[str, str] = {}

        _path_params: dict[str, str] = {}
        _query_params: list[tuple[str, str]] = []
        _header_params: dict[str, str | None] = _headers or {}
        _form_params: list[tuple[str, str]] = []
        _files: dict[str, str | bytes] = {}
        _body_params: bytes | None = None

        # process the path parameters
        if budget_id is not None:
            _path_params["budget_id"] = budget_id
        if payee_id is not None:
            _path_params["payee_id"] = payee_id
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if data is not None:
            _body_params = data

        # set the HTTP header `Accept`
        if "Accept" not in _header_params:
            _header_params["Accept"] = self.api_client.select_header_accept(["application/json"])

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params["Content-Type"] = _content_type
        else:
            _default_content_type = self.api_client.select_header_content_type(["application/json"])
            if _default_content_type is not None:
                _header_params["Content-Type"] = _default_content_type

        # authentication setting
        _auth_settings: list[str] = ["bearer"]

        return self.api_client.param_serialize(
            method="PATCH",
            resource_path="/budgets/{budget_id}/payees/{payee_id}",
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth,
        )
