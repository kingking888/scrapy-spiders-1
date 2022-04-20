# Spider for Linkedin (DRAFT)

## Requirements:
* [linkedin-api][ln] (PLEASE READ CAREFULLY BEFORE RUN THIS SPIDER!)
* python >= 3.6

This spider uses an internal Linkedin API called **Voyager** that attended to be
used by their frontend apps.

This spider requires user credentials to be provided into environment:
```
LINKEDIN_USERNAME=<some_name>
LINKEDIN_PASSWORD=<some_password>
```
It depends on data defined in [data.py](data.py) (For testing purposes)

[ln]: https://github.com/tomquirk/linkedin-api
