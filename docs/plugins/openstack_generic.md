# Openstack Generic

## Request example
`POST /monitoring/os-generic-s8bc3`

Request body:
```javascript
{
	"plugin": "os_generic",
	"info_plugin": {"host_ip":"10.57.4.1",
			"expected_time": 360,
			"log_path":"/var/log/web-app.log"
	}
}
```
