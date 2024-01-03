# utils.py
from .models import MailingList, Log


def send_scheduled_mailings(mailing_list_id):
    mailing_list = MailingList.objects.get(id=mailing_list_id)

    # Реализуйте здесь логику отправки рассылок
    # И сохраните результаты в журнале (Log)

    # Пример сохранения лога:
    log = Log.objects.create(mailing_list=mailing_list, message="Рассылка успешно отправлена")
    log.save()
