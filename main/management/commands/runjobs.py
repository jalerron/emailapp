import logging
import smtplib
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from emailapp import settings
from main.models import Mailings, Logs

logger = logging.getLogger(__name__)


def get_task(task, time_now):
    if task.end_time.timestamp() > time_now.timestamp() >= task.start_time.timestamp() \
            and task.status == task.SendStatus.CREATED:
        task.status = task.SendStatus.LAUNCHED
        task.save()
        emails_list = get_client(task)
        print(emails_list)
        task.status = task.SendStatus.COMPLETED
        task.save()


def get_client(task):
    emails_list = []
    for client in task.clients.all():
        emails_list.append(client.email)

    send_mail(
        subject=task.message.topic,
        message=task.message.body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails_list
    )

    print(emails_list)
    return emails_list


def my_job():
    time_now = timezone.now()
    print(time_now)
    mailing_tasks = Mailings.objects.all()

    for task in mailing_tasks:
        print(task)
        if task.is_active:
            try:

                if task.frequency == task.Periodicity.DAILY:
                    get_task(task, time_now)

                if task.frequency == task.Periodicity.WEEKLY:
                    get_task(task, time_now)

                if task.frequency == task.Periodicity.MONTHLY:
                    get_task(task, time_now)

                if task.frequency == task.Periodicity.DAILY or task.frequency == task.Periodicity.WEEKLY or task.frequency == task.Periodicity.MONTHLY:

                    log = Logs.objects.create(message_title=task, time=time_now, status=Logs.LogStatus.OK,
                                          response='Successful')
                    log.save()

            except smtplib.SMTPException:
                log = Logs.objects.create(message_title=task, time=time_now, status=Logs.LogStatus.FAILED,
                                          response='Error')
                log.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/25"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено задание: 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено еженедельное задание: 'delete_old_job_executions'.")

        try:
            logger.info(" Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик остановлен успешно!")
