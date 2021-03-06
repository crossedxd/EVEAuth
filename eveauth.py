import base64
import json
import webbrowser

import requests


class Auth:
    '''
    Authenticate via EVE Online's sign-in service and establish a session using
    a given config file, or the default config file if none is specified.

    The accompanying config file should be a JSON file containing the settings
    from the EVE Online Developers application registration page.  The config
    file (auth_config.json) should be in the following format:

    {
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "callback_url": "your_callback_url",
        "prompt_type": "input",
        "scopes": [
            "sample_scope_1.v1",
            "sample_scope_2.v1"
        ]
    }

    Valid prompt types are:
    * "input" - command line input()
    * "modal" - a wxPython TextEntryDialog() popup window

    Usage:
    import requests
    from eveauth import Auth

    session = Auth().session()
    '''

    def __init__(self, filepath='auth_config.json'):
        '''Initializes an Auth object with information from a config file.'''
        with open(filepath, 'r') as config_file:
            config = json.loads(config_file.read())

        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.callback_url = config['callback_url']
        self.scopes = '+'.join(config['scopes']) + '+'
        self.prompt_type = config['prompt_type']
        self.token = base64.b64encode(bytes('{}:{}'.format(self.client_id,
                                                           self.client_secret),
                                            'utf-8')).decode('utf-8')
        self._session = None

    def session(self):
        '''Returns current session, establishing one if it doesn't exist.'''
        if self._session is None:
            self.authorize()
        return self._session

    def authorize(self):
        '''Authorizes and establishes a session with the current config.'''
        url = 'https://login.eveonline.com/oauth/authorize/?response_type=code'
        url += '&client_id=' + self.client_id
        url += '&redirect_uri=' + self.callback_url
        url += '&scope=' + self.scopes
        webbrowser.open(url[0:-1])
        auth_input = None
        if self.prompt_type == 'modal':
            import wx
            dlg = wx.TextEntryDialog(
                None,
                'Login via SSO and paste the Auth code URL here:',
                'Input Auth URL')
            dlg.SetValue('')
            if dlg.ShowModal() == wx.ID_OK:
                auth_input = dlg.GetValue()
        elif self.prompt_type == 'input':
            auth_input = input(
                'Login via SSO and paste the Auth code URL here:\n')
        auth_code = auth_input.split(self.callback_url + '/?code=')[1]
        authorization = 'Basic {}'.format(self.token)
        response = requests.post('https://login.eveonline.com/oauth/token',
                                 headers={'Authorization': authorization},
                                 data={'grant_type': 'authorization_code',
                                       'code': auth_code})
        token = response.json()
        self._session = requests.Session()
        self._session.headers.update(
            {'Authorization': 'Bearer ' + token['access_token']})
