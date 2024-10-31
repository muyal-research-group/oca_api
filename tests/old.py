import os
import json as J
import unittest as UT
from uuid import uuid4
import pandas as pd
import re 
import json as J
import unicodedata as UD
# from nanoid import nan


class TestsSuit(UT.TestCase):


    @UT.skip("")
    def test_municipios(self):
        # catalog = {
        #     "name":"puebla_municipios",
        #     "display_name": "Municipios de Puebla",
        #     "items":[]
        # }
        
        catalog = {
            "name":"tamps_municipios",
            "display_name": "Municipios de Tamaulipas",
            "items":[]
        }
        # catalog = {
        #     "name":"bc_municipios",
        #     "display_name": "Municipios de Baja California",
        #     "items":[]
        # }
        # with open("./data/puebla_municipios.json","rb") as f:
        # with open("./data/bc_municipios.json","rb") as f:
        with open("./data/tamps_municipios.json","rb") as f:
            x = J.loads(f.read())
            cvt_ent    = x["cve_ent"]
            entidad    = x["entidad"]
            municipios = x["municipios"]
            for i,municipio in enumerate(municipios):
                catalog["items"].append({
                    "name":municipio["municipio"].upper(),
                    "display_name":municipio["municipio"],
                    "code": str(i),
                    "description":"No description yet.",
                    "metadata":{
                        "cve_ent":str(municipio["cve_ent"]),
                        "cve_mun":str(municipio["cve_mun"]),
                        "entidad":entidad
                    }
                })
        print(catalog)
        with open("./data/tamps_municipios_payload.json","w") as f:
            f.write(J.dumps(catalog,indent=4, ensure_ascii=True))



            


            # print(cvt_ent)
            
            # print(x)

        # df = pd.read_csv("./data/puebla_municipios.json")
        
        # for (index,row) in df.iterrows():
            # print(index,row)

   
    @UT.skip("")
    def test_process_catalogs(self):
        with open("./data/semarnat_nra_emisoras.json" ,"rb") as f:
            data = J.loads(f.read())
            catalog = []
            for datum in data:
                # print(datum)
                catalog_entry = {
                    "name":datum["nra"],
                    "display_name":datum["sustancia"].title(),
                    "code": datum["nra"],
                    "description":"DESCRIPTION",
                    "metadata": {
                        # "iarc_group":datum["iarc_group"]
                    }
                }
                catalog.append(catalog_entry)
            x = J.dumps(catalog,indent=4)
            print(type(x))
            with open("./data/semarnat_nra_emisoras_catalog.json" ,"w") as f:
                f.write(x)
        # print(x)
        # print(catalog)

        # print(data)


    @UT.skip("")
    def test_bc_municipiosa(self):
        with open("./data/cve_ent_mun.json","r") as f:
            data = J.loads(f.read())
        bc_mun = data[27]
        print(bc_mun)
        with open("./data/tamps_municipios.json","w") as f:
            f.write(J.dumps(bc_mun,indent=4))
        # with open("./data/bc_municipios.json","w") as f:
        #     f.write(J.dumps(bc_mun,indent=4))

    def test_generate_year_catalog(self):
        items = []
        for k,i in enumerate(range(2004,2023)):
            catalog_item = {
                "value":str(i),
                "display_name":str(i),
                "code":k,
                "description":"Año {}".format(i),
                "metadata":{}
            }
            items.append(catalog_item)
        catalog = {
            "cid":"year20042022",
            "display_name":"Año",
            "items":items,
            "kind":"TEMPORAL"
        }
        with open("./data/year_new.json","w") as f:
            f.write(J.dumps(catalog,indent=4))

    @UT.skip("")
    def test_generate_mun_and_states_catalogs(self):
        items_states         = []
        items_municipalities = []
        with open("./data/cve_ent_mun.json","r") as f:
            data = J.loads(f.read())
        j_global= 0
        for i,x in enumerate(data):
            estado = x["entidad"]
            items_states.append({
                "display_name": estado.title(),
                "code":i,
                "description": "Estado de {} con clave de entidad {}".format(estado,x["cve_ent"]),
                "metadata":{

                },
                "value":estado.upper().replace(" ","")
            })
            for municipio in x["municipios"]:
                municipality = municipio["municipio"]
                cve_mun = municipio["cve_mun"]
                items_municipalities.append({
                    "display_name": municipality.title(),
                    "code":j_global,
                    "description": "Estado de {} con clave de municipio {}".format(estado,municipio["cve_mun"]),
                    "metadata":{
                        "cve_mun":str(cve_mun),
                        "cve_ent":str(municipio["cve_ent"])
                    },
                    "value":municipality.upper().replace(" ","")
                })
                j_global +=1
        states_catalogs = {
            "cid":"states8ce52701ba74",
            "display_name":"Estados",
            "items":items_states
        }
        municipalities_catalogs = {
            "cid":"municipalities4478fa9c66ab",
            "display_name":"Municipios",
            "items":items_municipalities
        }
        with open("./data/states_new.json","w") as f:
            f.write(J.dumps(states_catalogs,indent=4))
        with open("./data/municipalities_new.json","w") as f:
            f.write(J.dumps(municipalities_catalogs,indent=4))

            # print(entidad)
        # print(data)
if __name__ == "__main__":
    UT.main()