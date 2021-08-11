# plugin-kbfg-sso

Plugin for KBFG SSO Connector


# Configuration

~~~python
options(dict) = {
	'auth_type': 'kbfg_sso',
	...
	}

~~~


## Example

To enable kbfg-sso plugin,
use identity.Domain.change_auth_plugin API.


~~~bash
spacectl exec change_auth_plugin identity.Domain -f keycloak.yaml
~~~

Example YAML file

~~~yaml
plugin_info:
  options:
    auth_type: kbfg_sso
  plugin_id: plugin-kbfg-sso
  version: '1.0'
~~~

# Auth.init

If you init plugin, the response looks like

~~~
{'metadata': {
              }
	 }
~~~

# Release Note

## Version 1.0

Support New Auth API
* Auth.init
* Auth.verify
* Auth.find
* Auth.login
