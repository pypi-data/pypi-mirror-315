# togai-client
![PyPI](https://img.shields.io/pypi/v/togai-client)

[Togai](https://www.togai.com/) is an end to end pricing infrastructure that enable you with metering, aggregating, pricing and billing for your application.

This is an official Typescript client library for using [Togai APIs](https://docs.togai.com/reference).

- API version: 1.0
- Package version: 1.0.3
For more information, please visit [https://docs.togai.com](https://docs.togai.com)

## Requirements.

Python 3.8+

## Installation & Usage
### pip install

```sh
pip install togai-client
```
(you may need to run `pip` with root permission: `sudo pip install togai-client`)

Then import the package:
```python
import togai_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import togai_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:
You will need a API_TOKEN to use the API. You can get one from your Togai Account

```python

import time
import togai_client
from pprint import pprint
from togai_client.api import accounts_api
from datetime import datetime
from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Optional, Union
from typing_extensions import Annotated
from togai_client.models.account import Account
from togai_client.models.account_aliases_paginated_response import AccountAliasesPaginatedResponse
from togai_client.models.account_paginated_response import AccountPaginatedResponse
from togai_client.models.add_account_aliases_request import AddAccountAliasesRequest
from togai_client.models.base_success_response import BaseSuccessResponse
from togai_client.models.create_account_request import CreateAccountRequest
from togai_client.models.create_proposal_request import CreateProposalRequest
from togai_client.models.create_purchase_request import CreatePurchaseRequest
from togai_client.models.edit_pricing_schedule_request import EditPricingScheduleRequest
from togai_client.models.get_proposal_response import GetProposalResponse
from togai_client.models.get_purchase_response import GetPurchaseResponse
from togai_client.models.pricing_schedule_paginated_response import PricingSchedulePaginatedResponse
from togai_client.models.proposal import Proposal
from togai_client.models.proposals_paginated_response import ProposalsPaginatedResponse
from togai_client.models.purchase import Purchase
from togai_client.models.purchase_paginated_list_data import PurchasePaginatedListData
from togai_client.models.remove_account_aliases_request import RemoveAccountAliasesRequest
from togai_client.models.update_account_request import UpdateAccountRequest
from togai_client.models.update_pricing_schedule_request_with_actions import UpdatePricingScheduleRequestWithActions
from togai_client.models.update_pricing_schedule_response import UpdatePricingScheduleResponse
from togai_client.models.update_proposal_status import UpdateProposalStatus
# Defining the host is optional and defaults to https://api.togai.com
# See configuration.py for a list of all supported configuration parameters.
configuration = togai_client.Configuration(
    host = "https://api.togai.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (Bearer <credential>): bearerAuth
configuration = togai_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)


# Enter a context with an instance of the API client
with togai_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)
    account_id = 'ACC00001' # str | account_id corresponding to an account
    add_account_aliases_request = togai_client.AddAccountAliasesRequest() # AddAccountAliasesRequest | Payload to add aliases to account

    try:
        # Add Aliases to account
        api_response = api_instance.add_aliases(account_id, add_account_aliases_request)
        pprint(api_response)
    except togai_client.ApiException as e:
        print("Exception when calling AccountsApi->add_aliases: %s\n" % e)
```

You can get a detailed step-by-step guide for a sample ingestion and metering at [examples directory](https://github.com/zuora/togai-python-client/tree/main/examples)
For a more detailed documentation for every api and models, please refer to the [docs directory](https://github.com/zuora/togai-python-client/tree/main/docs)

## Author

engg@togai.com


