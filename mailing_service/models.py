from django.db import models


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return self.full_name


class MailingList(models.Model):
    clients = models.ManyToManyField(Client)
    send_time = models.DateTimeField()
    frequency = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')])
    status = models.CharField(max_length=20, choices=[('created', 'Created'), ('started', 'Started'), ('completed', 'Completed')])
    subject = models.CharField(max_length=255)  # Добавлено поле темы письма
    body = models.TextField()  # Добавлено поле тела письма

    def __str__(self):
        return f'Mailing List {self.id}'


class Message(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Log(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE, related_name='logs', verbose_name='Рассылка')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=255, verbose_name='Статус попытки')
    response = models.TextField(blank=True, null=True, verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f'Log {self.id}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['-attempt_time']