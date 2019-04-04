# EVEAuth

Authenticate via EVE Online's sign-in service and establish a session
using a specified config file, or the default config file if none is specified.

The accompanying config file should be a JSON file containing the settings
from the EVE Online Developers application registration page.  The config
file should be in the following format:

```
{
  "client_id":"your_client_id",
  "client_secret":"your_client_secret",
  "callback_url":"your_callback_url",
  "scopes":[
	 "sample_scope_1.v1",
	 "sample_scope_2.v1"
  ]
}
```

Usage:
```
import requests
from eveauth import Auth

session = Auth().session()
```
