from django.core.management.base import BaseCommand, CommandError

from payment_config.api_calls import get_bcv


class Command(BaseCommand):
    help = 'Obtiene la ultima tasa de cambio del bcv'

    def handle(self, *args, **options):

        data = get_bcv()
        if data['status_code'] == 200:
            print('La tasa de cambio del USD/VED ha sido actualizada')
            print('Tasa actual:', data['obj'].value)
        else:
            raise CommandError('No se pudo obtener la tasa de cambio del bcv')

