# Consumidor
# 0. Acceso Xolo API
# 1. Traer todos los observatorios.
# 2.1 Puede calificar varios observatorios
# 2.2  Acceder a un observatorio.
# 3. Buscar productos
# 3.1 Descarga de producto.
# ________________________________________
# Productor
# 0. Acceso Xolo API
# 1. Crear catalogos
# 2. Crear observatorio
# 3. Registro de productos
# ___________________________________
import requests as R
import json as J
import pandas as pd

def main():
    protocol = "http"
    xolo_addr = "localhost:10001"
    xolo_base_url = "{}://{}".format(protocol,xolo_addr)
    R.post(xolo_base_url)
    


if __name__ =="__main__":
    main()