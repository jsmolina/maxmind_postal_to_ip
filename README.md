# IP to Postal Code microservice
Simple Quart dockerized service to translate from user IP to a postalcode.

## How to Use:

It expects MAXMIND_URL environment variable to contain full maxmind url.
Where XXXXXXX is your license key from maxmind.com


```bash

docker run --env "MAXMIND_URL=https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=XXXXXXXXX&suffix=tar.gz" \
            -p 8080:8080 CONTAINER_ID
```
