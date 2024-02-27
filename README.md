# Observatory and Catalog REST - API 

This API allows the manipulation of ```observatory``` objects and ```catalogs``` objects. An observatory has the following structure:
```json
{
    "key": "string",
    "title": "string",
    "catalogs": [
        {
            "level": int,
            "catalog_key": "string"
        }
    ]
}
```

The structure of a ```catalog``` is as follows:
```json
{
    "key": "string",
    "name": "string",
    "display_name": "string",
    "items": [
        {
            "name": "string",
            "display_name": "string",
            "code": "string",
            "description": "string",
            "metadata": {
                "metadata_key(string)": "metadata_value(string)"
            }
        }
    ]
}
```

The structure of a ```product``` is as follows:
```json
{
    "key": "string",
    "description":"string",
    "levels":"List<Level>",
    "product_type":"string",
    "kind":"string",
    "level_index":"int",
    "level_path":"string",
    "profile":"string",
    "product_name":"string"
}
```

A Level is an object with the following structure:
```json
{
    "index":"int",
    "catalog_id":"string",
    "value":"string"
}
```

## Example: Create an observatory

### 1. Create the catalogs
A catalog is a complete enumeration of items arranged sysstematically with descriptive details about the items. In this example we create 3 catalogs: 

- Substances: It containts 4 possible values 1, 2A, 2B, C. 
- States: All mexican states.
- Year: Years from 2000 to 2023.

We need to send the following paylods using the HTTP Method POST:
```json
{
    "key": "iarc",
    "name": "IARC",
    "display_name": "IARC",
    "items": [
        {
            "name": "1",
            "display_name": "1",
            "code": "0",
            "description": "1",
            "metadata": { }
        },
        {
            "name": "2A",
            "display_name": "2A",
            "code": "1",
            "description": "2A",
            "metadata": { }
        },
        {
            "name": "2B",
            "display_name": "2B",
            "code": "2",
            "description": "2B",
            "metadata": { }
        },
        {
            "name": "3",
            "display_name": "3",
            "code": "3",
            "description": "3",
            "metadata": { }
        }
    ]
}
```

To create the mexican states catalog use the following payload example:
```json
{
    "name": "puebla_municipios",
    "display_name": "Municipios de Puebla",
    "items": [
        {
            "name": "ACAJETE",
            "display_name": "Acajete",
            "code": "0",
            "description": "No description yet.",
            "metadata": {
                "cve_ent": "21",
                "cve_mun": "1",
                "entidad": "Puebla"
            }
        },
        {
            "name": "ACATENO",
            "display_name": "Acateno",
            "code": "1",
            "description": "No description yet.",
            "metadata": {
                "cve_ent": "21",
                "cve_mun": "2",
                "entidad": "Puebla"
            }
        },
        {
            "name": "ACATL\u00c1N",
            "display_name": "Acatl\u00e1n",
            "code": "2",
            "description": "No description yet.",
            "metadata": {
                "cve_ent": "21",
                "cve_mun": "3",
                "entidad": "Puebla"
            }
        },
        {
            "name": "ACATZINGO",
            "display_name": "Acatzingo",
            "code": "3",
            "description": "No description yet.",
            "metadata": {
                "cve_ent": "21",
                "cve_mun": "4",
                "entidad": "Puebla"
            }
        }
        More items.... 
    ]
}
```

The last catalog is the years from 2000 to 2023
```json
{
    "name": "years",
    "display_name": "Año",
    "items": [
        {
            "name": "2000",
            "display_name": "2000",
            "code": "0",
            "description": "No description yet.",
            "metadata": {}
        },
        {
            "name": "2001",
            "display_name": "2000",
            "code": "1",
            "description": "No description yet.",
            "metadata": {}
        },
        More items...,
        {
            "name": "2023",
            "display_name": "2023",
            "code": "23",
            "description": "No description yet.",
            "metadata": {}
        },
        

    ]
}
```