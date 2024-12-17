# circlemind-sdk

Developer-friendly & type-safe Python SDK specifically catered to leverage *circlemind-sdk* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=circlemind-sdk&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />

<!-- Start Summary [summary] -->
## Summary


<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [circlemind-sdk](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#circlemind-sdk)
  * [SDK Installation](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#sdk-example-usage)
  * [Available Resources and Operations](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#retries)
  * [Error Handling](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#error-handling)
  * [Server Selection](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#custom-http-client)
  * [Authentication](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#authentication)
  * [Debugging](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#debugging)
* [Development](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#development)
  * [Maturity](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#maturity)
  * [Contributions](https://github.com/circlemind-ai/circlemind-sdk/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install circlemind-sdk
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add circlemind-sdk
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
from circlemind_sdk import CirclemindSDK
import os

with CirclemindSDK(
    api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
) as circlemind_sdk:

    res = circlemind_sdk.get_user_plan_plan_get()

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from circlemind_sdk import CirclemindSDK
import os

async def main():
    async with CirclemindSDK(
        api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
    ) as circlemind_sdk:

        res = await circlemind_sdk.get_user_plan_plan_get_async()

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [CirclemindSDK](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md)

* [get_user_plan_plan_get](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#get_user_plan_plan_get) - User plan
* [get_graph_configuration](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#get_graph_configuration) - Graph configuration (get)
* [set_graph_configuration](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#set_graph_configuration) - Graph configuration (set)
* [list_graphs](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#list_graphs) - List graphs
* [create_graph](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#create_graph) - Create new graph
* [delete_graph](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#delete_graph) - Delete existing graph
* [download_graphml](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#download_graphml) - Download graphml
* [query](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#query) - Query memory
* [get_query_status](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#get_query_status) - Check query request status
* [add](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#add) - Add memory
* [add_from_files](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#add_from_files) - Add memory (from files)
* [get_add_status](https://github.com/circlemind-ai/circlemind-sdk/blob/master/docs/sdks/circlemindsdk/README.md#get_add_status) - Check add request status

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from circlemind_sdk import CirclemindSDK
from circlemind_sdk.utils import BackoffStrategy, RetryConfig
import os

with CirclemindSDK(
    api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
) as circlemind_sdk:

    res = circlemind_sdk.get_user_plan_plan_get(,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from circlemind_sdk import CirclemindSDK
from circlemind_sdk.utils import BackoffStrategy, RetryConfig
import os

with CirclemindSDK(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
) as circlemind_sdk:

    res = circlemind_sdk.get_user_plan_plan_get()

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.SDKError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `get_graph_configuration_async` method may raise the following exceptions:

| Error Type                 | Status Code | Content Type     |
| -------------------------- | ----------- | ---------------- |
| models.HTTPValidationError | 422         | application/json |
| models.SDKError            | 4XX, 5XX    | \*/\*            |

### Example

```python
from circlemind_sdk import CirclemindSDK, models
import os

with CirclemindSDK(
    api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
) as circlemind_sdk:
    res = None
    try:

        res = circlemind_sdk.get_graph_configuration(graph_name="<value>")

        # Handle response
        print(res)

    except models.HTTPValidationError as e:
        # handle e.data: models.HTTPValidationErrorData
        raise(e)
    except models.SDKError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from circlemind_sdk import CirclemindSDK
import os

with CirclemindSDK(
    server_url="https://api.circlemind.co",
    api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
) as circlemind_sdk:

    res = circlemind_sdk.get_user_plan_plan_get()

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from circlemind_sdk import CirclemindSDK
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = CirclemindSDK(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from circlemind_sdk import CirclemindSDK
from circlemind_sdk.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = CirclemindSDK(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name             | Type   | Scheme  | Environment Variable           |
| ---------------- | ------ | ------- | ------------------------------ |
| `api_key_header` | apiKey | API key | `CIRCLEMINDSDK_API_KEY_HEADER` |

To authenticate with the API the `api_key_header` parameter must be set when initializing the SDK client instance. For example:
```python
from circlemind_sdk import CirclemindSDK
import os

with CirclemindSDK(
    api_key_header=os.getenv("CIRCLEMINDSDK_API_KEY_HEADER", ""),
) as circlemind_sdk:

    res = circlemind_sdk.get_user_plan_plan_get()

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from circlemind_sdk import CirclemindSDK
import logging

logging.basicConfig(level=logging.DEBUG)
s = CirclemindSDK(debug_logger=logging.getLogger("circlemind_sdk"))
```

You can also enable a default debug logger by setting an environment variable `CIRCLEMINDSDK_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=circlemind-sdk&utm_campaign=python)
