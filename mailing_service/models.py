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

    def __str__(self):
        return f'Mailing List {self.id}'


class Message(models.Model):
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Log(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    response = models.TextField()

    def __str__(self):
        return f'Log {self.id}'
