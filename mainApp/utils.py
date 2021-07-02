import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# C:\\Users\\Fabricio\\Documents\\Django Projects\\docs\\src\\mainApp\\mainApp\
#podria mejorar la funcion para que me tome el titulo del archivo, haga un slug y con eso sepa que escribir
# si le paso una imagen la sube lo mismo, pero el encoding esta mal porque la escribi como un txt
def handle_uploaded_file(f):
    print("escribiendo...")
    with open(BASE_DIR / 'subido.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
