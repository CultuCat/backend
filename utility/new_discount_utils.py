from user.models import Perfil
from discount.models import Discount
from trophy.models import Trophy

import string
import random

def verificar_y_otorgar_descuento(user_id, trofeo_nombre, count_check):
    t_comments = Trophy.objects.get(nom=trofeo_nombre)
    new_points = 0
        
    if count_check == t_comments.punts_nivell1:
        nivell = 1
        new_points = 10
    elif count_check == t_comments.punts_nivell2:
        nivell = 2
        new_points = 50
    elif count_check == t_comments.punts_nivell3:
        nivell = 3
        new_points = 100
    else:
        nivell = None
        
    if nivell is not None:
        #se suman los puntos
        u = Perfil.objects.get(id=user_id) 
        u.puntuacio += new_points
        u.save()
        
        caracteres_validos_codigo = string.ascii_uppercase + string.digits
        codigo_descuento= ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
        while Discount.objects.filter(codi=codigo_descuento).exists():
            codigo_descuento = ''.join(random.choice(caracteres_validos_codigo) for _ in range(8))
                
        Discount.objects.create(codi=codigo_descuento,userDiscount=Perfil.objects.get(id=user_id),nivellTrofeu=nivell,nomTrofeu=trofeo_nombre,usat=False)