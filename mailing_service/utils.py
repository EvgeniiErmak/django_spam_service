from django.core.mail import send_mail
from django.utils import timezone
from decouple import config  # Импорт из библиотеки python-decouple
from .models import MailingList, Log


def send_scheduled_mailings(mailing_list_id):
    mailing_list = MailingList.objects.get(id=mailing_list_id)

    try:
        # Ваша логика для формирования сообщения и адресатов
        subject = mailing_list.message.subject
        body = mailing_list.message.body

        if mailing_list.select_all_clients:
            recipients = [client.email for client in mailing_list.clients.all()]
        else:
            recipients = [client.email for client in mailing_list.clients.filter(is_subscribed=True)]

        # Отправка электронной почты
        send_mail(subject, body, config('EMAIL_HOST_USER'), recipients, fail_silently=False)

        # Сохранение успешного лога
        log = Log.objects.create(
            mailing_list=mailing_list,
            attempt_time=timezone.now(),
            status="success",
            response="Рассылка успешно отправлена"
        )
        log.save()

        print(f"Log saved for mailing_list_id={mailing_list_id}")

    except Exception as e:
        # Сохранение неудачного лога
        log = Log.objects.create(
            mailing_list=mailing_list,
            attempt_time=timezone.now(),
            status="error",
            response=f"Ошибка при отправке рассылки: {str(e)}"
        )
        log.save()

