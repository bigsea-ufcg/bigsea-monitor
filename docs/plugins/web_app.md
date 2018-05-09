# Web Application

## Request example
`POST /monitoring/web-app-01`

Request body:
```javascript
{
	"plugin": "web_app",
	"plugin_info": {
			"host_ip":"10.57.4.1",
			"host_username": "ubuntu",
			"log_path":"/var/log/web-app.log"
	}
}
```
