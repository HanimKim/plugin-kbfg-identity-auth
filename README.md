# plugin-kbfg-sso

Plugin for KBFG SSO Connector


# Configuration

~~~python
options(dict) = {
	'auth_type': 'kbfg_sso',
	'agent_id': 'YOUR AGENT ID',
	'auth_url': 'YOUR AUTH SERVER URL, ex http://1.1.1.1:8080'
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
    auth_url: http://1.1.1.1:8080
  plugin_id: plugin-kbfg-identity-auth
  version: '1.0'
~~~

# Auth.init

If you init plugin, the response metadata looks like

~~~
{'metadata':
	{
	'authorization_endpoint': 'http://1.1.1.1:8080/sso/sigin,
	'token_endpoint': 'http://1.1.1.1:8080/sso/validateTicket'
	}
}
~~~

***authrizat_endpoint*** is for ticket creation in a browser.
***token_endpoint*** is for auth plugin.

# Release Note

## Version 0.2

Support New Auth API
* Auth.init
* Auth.verify
* Auth.find (NOT SUPPORT)
* Auth.login
