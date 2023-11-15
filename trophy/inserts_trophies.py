import django
import os
import sys
from django.db import transaction

script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.abspath(os.path.join(script_path, '..'))  # suponiendo que el proyecto está un nivel arriba
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cultucat.settings') 
django.setup()

from trophy.models import Trophy 

@transaction.atomic
def insertar_trofeos():
    trofeos = [
        {
            'nom':"Parlaner",
            'descripcio':"Quants missatges has enviat, no siguis pesat...",
            'punts_nivell1':'10',
            'punts_nivell2':'50',
            'punts_nivell3':'100'
        },
        {
            'nom':"Reviwer",
            'descripcio':"Quants comentaris has escrit",
            'punts_nivell1':'10',
            'punts_nivell2':'50',
            'punts_nivell3':'100'
        },
        {
            'nom':"Més esdeveniments",
            'descripcio':"Quants esdeveniments has assist",
            'punts_nivell1':'10',
            'punts_nivell2':'50',
            'punts_nivell3':'100'
        },
        {
            'nom':"El més amigable",
            'descripcio':"Quants amics tens",
            'punts_nivell1':'10',
            'punts_nivell2':'50',
            'punts_nivell3':'100'
        },
        {
            'nom':"Coleccionista",
            'descripcio':"Quant trofeus tens",
            'punts_nivell1':'1',
            'punts_nivell2':'3',
            'punts_nivell3':'4'
        },
    ]

    for trofeo_data in trofeos:
        Trophy.objects.create(**trofeo_data)


if __name__ == "__main__":
    Trophy.objects.all().delete()
    insertar_trofeos()
