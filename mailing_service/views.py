from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Client, MailingList, Log
from .forms import ClientForm, MailingListForm

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)
scheduler.start()


class ClientListView(View):
    def get(self, request):
        clients = Client.objects.all()
        return render(request, 'mailing_service/client_list.html', {'clients': clients})


class ClientCreateView(View):
    def get(self, request):
        form = ClientForm()
        return render(request, 'mailing_service/client_form.html', {'form': form})

    def post(self, request):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, 'mailing_service/client_form.html', {'form': form})


class ClientUpdateView(View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm(instance=client)
        return render(request, 'mailing_service/client_form.html', {'form': form})

    def post(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, 'mailing_service/client_form.html', {'form': form})


class ClientDeleteView(View):
    def get(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        return render(request, 'mailing_service/client_confirm_delete.html', {'client': client})

    def post(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        client.delete()
        return redirect('client_list')


class MailingListListView(View):
    def get(self, request):
        mailing_lists = MailingList.objects.all()
        return render(request, 'mailing_service/mailing_list_list.html', {'mailing_lists': mailing_lists})


class MailingListCreateView(View):
    def get(self, request):
        form = MailingListForm()
        return render(request, 'mailing_service/mailing_list_form.html', {'form': form})

    def post(self, request):
        form = MailingListForm(request.POST)
        if form.is_valid():
            mailing_list = form.save()
            # Регистрируем задачу для отправки рассылки
            @register_job(scheduler, "interval", minutes=1, id=f"mailing_list_{mailing_list.id}")
            def send_scheduled_mailings():
                # Реализуйте логику отправки рассылок по расписанию
                pass
            return redirect('mailing_list_list')
        return render(request, 'mailing_service/mailing_list_form.html', {'form': form})


class MailingListUpdateView(View):
    def get(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        form = MailingListForm(instance=mailing_list)
        return render(request, 'mailing_service/mailing_list_form.html', {'form': form})

    def post(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        form = MailingListForm(request.POST, instance=mailing_list)
        if form.is_valid():
            form.save()
            return redirect('mailing_list_list')
        return render(request, 'mailing_service/mailing_list_form.html', {'form': form})


class LogListView(View):
    def get(self, request):
        logs = Log.objects.all()
        return render(request, 'mailing_service/log_list.html', {'logs': logs})
