from datetime import date
from . import refresh


def run():
    today = date.today()
    # Definim el where
    t_day = avui.strftime('%Y-%m-%d') + 'T00:00:00'
    refresh.getEventsDadesObertes("data_inici>='" + data_avui + "'")