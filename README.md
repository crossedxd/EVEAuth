# EVEAuth

Authenticate via EVE Online's sign-in service and establish a session
using a given config file, or the default config file if none is specified.

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
auth = Auth()  # Initializes the Auth object
auth.session()  # The first session() will trigger authorize() to be called
auth.session()  # Subsequent calls will reuse the same Session() object
```
