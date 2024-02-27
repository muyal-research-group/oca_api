from typing import Dict
import requests as R
import json as J
import os
from humanfriendly import parse_size

def mictlanfx(
        bucket_id:str,
        file_id:str,
        max_threads:int = 4,
        source_path = "/mictlanx/data",
        chunk_size:str = "1MB"
        ):
    def decorator(func):
        def wrapper(*args, **kwargs ):
            path = "{}/{}".format(source_path,file_id)
            _chunk_size = parse_size(chunk_size)
            bytes_arr = bytearray()
            size = 0
            # if os.path.
            with open(path,"rb") as f:
                while True:
                    chunk = f.read(_chunk_size)
                    if not chunk:
                        break
                    size+= len(chunk)
                    bytes_arr.extend(chunk)
            mem_view = memoryview(bytes_arr)
            return func(
                data = mem_view,
                metadata ={
                    "size":size
                }
            )
        return wrapper
    return decorator



BUCKET_ID = os.environ.get("BUCKET_ID", "bucketid")




# 1. Registro de funciones (template) -> Manual.
# 2. Localizar datos de entrada con decorador.
@mictlanfx(
    bucket_id   = os.environ.get("BUCKET_ID","bucket-x"),
    key         = os.environ.get("KEY","key-x"),
    max_threads = int(os.environ.get("MAX_THREADS","2")),
)
def create_catalogs(
    data:memoryview        = memoryview(b''), # Datos localizados con <KEY>
    metadata:Dict[str,str] = {} , # Metadatos de los datos de la <KEY>
):
    print("DATA",bytes(data[:10]))
    print("METADATA",metadata)
    # Processing stuff goes here.


if __name__ == "__main__":
    create_catalogs()