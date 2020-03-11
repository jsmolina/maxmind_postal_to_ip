# IP to Postal Code microservice
Simple Quart dockerized service to translate from user IP to a postalcode.

## How to Use:

It expects MAXMIND_URL environment variable to contain full maxmind url.
Where XXXXXXX is your license key from maxmind.com


```bash

docker run --env "MAXMIND_URL=https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=XXXXXXXXX&suffix=tar.gz" \
            -p 8080:8080 CONTAINER_ID
```

```
$ curl -X GET -vv localhost:8080/json/2.152.0.0

{
	"zip_code": "17003",
	"location": {
		"accuracy_radius": 1,
		"latitude": 41.9813,
		"longitude": 2.8257,
		"time_zone": "Europe/Madrid"
	}
}
```
