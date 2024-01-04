from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django_apscheduler.jobstores import DjangoJobStore, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Client, MailingList, Log
from .forms import ClientForm, MailingListForm
from .utils import send_scheduled_mailings

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
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
        return render(request, 'mailing_service/client_form.html', {'form': form, 'client': client})

    def post(self, request, client_id):
        client = get_object_or_404(Client, id=client_id)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
        return render(request, 'mailing_service/client_form.html', {'form': form, 'client': client})


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
        return render(request, 'mailing_service/mailing_list_form.html',
                      {'form': form, 'clients': Client.objects.all()})

    def post(self, request):
        form = MailingListForm(request.POST)
        if form.is_valid():
            mailing_list = form.save(commit=False)
            mailing_list.save()
            form.save_m2m()

            register_job(
                scheduler,
                "interval",
                minutes=1,
                id=f"mailing_list_{mailing_list.id}",
                replace_existing=True,
                func=send_scheduled_mailings,
                args=[mailing_list.id],
            )

            return redirect('mailing_list_list')
        return render(request, 'mailing_service/mailing_list_form.html',
                      {'form': form, 'clients': Client.objects.all()})


class MailingListDetailView(View):
    def get(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        logs = Log.objects.filter(message__mailing_list=mailing_list).order_by('-attempt_time')
        return render(request, 'mailing_service/mailing_list_detail.html', {'mailing_list': mailing_list, 'logs': logs})


class MailingListUpdateView(View):
    def get(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        form = MailingListForm(instance=mailing_list)
        return render(request, 'mailing_service/mailing_list_form.html', {'form': form, 'mailing_list': mailing_list, 'clients': Client.objects.all()})

    def post(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        form = MailingListForm(request.POST, instance=mailing_list)
        if form.is_valid():
            form.save()
            return redirect('mailing_list_list')
        return render(request, 'mailing_service/mailing_list_form.html', {'form': form, 'mailing_list': mailing_list})

    def delete(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        mailing_list.delete()
        return redirect('mailing_list_list')


class MailingListDeleteView(View):
    def get(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        return render(request, 'mailing_service/mailing_list_confirm_delete.html', {'mailing_list': mailing_list})

    def post(self, request, mailing_list_id):
        mailing_list = get_object_or_404(MailingList, id=mailing_list_id)
        mailing_list.delete()
        return redirect('mailing_list_list')


class LogListView(View):
    template_name = 'mailing_service/log_list.html'

    def get(self, request, mailing_list_id=None):
        if mailing_list_id:
            # Обработка, если mailing_list_id передан
            logs = Log.objects.filter(message__mailing_list_id=mailing_list_id).order_by('-attempt_time')
        else:
            # Обработка, если mailing_list_id не передан
            logs = Log.objects.all().order_by('-attempt_time')

        print(logs) # Добавьте эту строку для отладки

        return render(request, self.template_name, {'logs': logs})
