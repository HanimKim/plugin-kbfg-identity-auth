# plugin-kbfg-sso

Plugin for KBFG SSO Connector


# Configuration

~~~python
options(dict) = {
  'auth_type': 'kbfg_sso',
  'agent_id': 'YOUR AGENT ID',
  'auth_endpoint': 'YOUR AUTH SERVER ENDPOINT, ex http://1.1.1.1:8080'
  '...': '...'
}
~~~


## Example

To enable kbfg-sso plugin,
use identity.Domain.change_auth_plugin API.


~~~bash
spacectl exec change_auth_plugin identity.Domain -f change_auth_plugin.yaml
~~~

Example YAML file

~~~yaml
plugin_info:
  options:
    auth_type: kbfg_sso
    agent_id: 123456
    authorization_endpoint: http://1.1.1.1:8080/sso/sigin
    validate_token_endpoint: http://1.1.1.1:8080/sso/validateTicket
    check_server_endpoint: http://1.1.1.1:8080/api/v1/sso/checkserver
  plugin_id: plugin-kbfg-identity-auth
~~~

# Auth.init

If you init plugin, the response metadata looks like

~~~
{
  'metadata': {
    'authorization_endpoint': 'http://1.1.1.1:8080/sso/sigin,
    'validate_token_endpoint': 'http://1.1.1.1:8080/sso/validateTicket',
    'check_server_endpoint': 'http://1.1.1.1:8080/api/v1/sso/checkserver'
  }
}
~~~

***authrizat_endpoint*** is for ticket creation in a browser.
***validate_token_endpoint*** is for auth plugin.
***check_server_endpoint***is for check server

# Release Note

## Version 0.2

Support New Auth API
* Auth.init
* Auth.verify
* Auth.find (NOT SUPPORT)
* Auth.login
