import logging
from datetime import timedelta

from django.db import transaction
from django.conf import settings
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from payment_config.api_calls import get_bcv
from orders.models import Order
from orders.utils import cancel_old_in_progress_orders


logger = logging.getLogger(__name__)


@util.close_old_connections
def cancel_old_in_progress_orders_job():

    cancel_old_in_progress_orders()


@util.close_old_connections
def get_bcv_job():
    data = get_bcv()
    if data['status_code'] == 200:
        print('La tasa de cambio del USD/VED ha sido actualizada')
        print('Tasa actual:', data['obj'].value)
    else:
        print("No se pudo obtener la tasa de cambio")
        print("Codigo de error: ", data["status_code"])


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Este trabajo elimina las entradas de ejecución del trabajo de APScheduler anteriores a `max_age` de la base de datos.
    Ayuda a evitar que la base de datos se llene con registros históricos antiguos que ya no existen.
    ya no es útil.
    
    :param max_age: el período máximo de tiempo para conservar los registros históricos de ejecución de trabajos.
                    El valor predeterminado es 7 días.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            get_bcv_job,
            trigger=CronTrigger(day="*"),
            id="get_bcv_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        scheduler.add_job(
            cancel_old_in_progress_orders_job,
            trigger=CronTrigger(day="*"),
            id="cancel_old_in_progress_orders",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                    day_of_week="mon", hour="00", minute="00"
                ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")