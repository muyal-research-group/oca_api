# Observatory - API 
An observatory is an object that contain N catalogs. This object is used in the user interface to create a page dinamically. The catalogs are use to match products that are listed in the UI. We can use the values in the catalogs to create queries. You can se an example of an observatory at [here](https://muyal.tamps.cinvestav.mx/observatories). You need to have an account please contact me a at jesus.castillo.b@cinvestav.mx to request your account.

So in code an observatory has a simple structure like this: 
```python
class Observatory:
    obid:str
    title: str
    image_url:str
    description:str
    catalogs:List[LevelCatalog]
    disabled:bool 
```

You can create one of this using this [endpoint](https://alpha.tamps.cinvestav.mx/ocapi/redoc#operation/create_observatory_observatories_post). 

# Catalog - API 

A catalog is a collection of values. Catalogs has an special attribute that define its ```kind```. We use this attribute to perform advanced queries.
```python
class Catalog:
    cid:str
    display_name:str 
    items: List[CatalogItem]
    kind:str 
```

You can create a catalog using this [endpoint](https://alpha.tamps.cinvestav.mx/ocapi/redoc#operation/create_catalogs_catalogs_post). ⚠️ The supported ```kind``` values are the followin: ```TEMPORAL```, ```SPATIAL```, ```INTEREST```, ```INTEREST_NUMERIC```. 

# Product - API 
A product can be anything you want, you defined like this:
```python
class Product(BaseModel):
    pid:str # Product unique identifier
    description:str # A simple description
    levels:List[Level] # levels defined later
    product_type: str # the type of the product
    level_path:str # xD the name of the levels (e.g CIE10.SEXO)
    profile:str # The value of the levels (e.g C50.MUJER)
    product_name: str # Name of the product xd 
    tags:List[str] # Tags for advancing permission control
```

The product has levels, this are defined like this:
```python
class Level(BaseModel):
    index:int # this value determines the position in the user interface.
    cid:str # The unique identifier of the catalog for this level.
    value:str # The value in the catalog
    kind:str # the kind of the level maybe spatial, temporal, and so on.
```

You can create may products in bulk using the next [endpoint](https://alpha.tamps.cinvestav.mx/ocapi/redoc#operation/create_products_products_post). 


# Getting started

You can run this service locally in your computer or in a server using the docker image:

```bash
docker pull nachocode/oca:api
```

Now you can clone this repo:
```bash
git clone git@github.com:muyal-research-group/oca_api.git
```

You need to be inside the folder ```oca_api```
```bash
cd oca_api
```

Execute the next command:
```sh
docker compose up -f ./oca.yml  up -d 
```


<!-- This API allows the manipulation of ```observatory``` objects and ```catalogs``` objects. An observatory has the following structure:
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
``` -->