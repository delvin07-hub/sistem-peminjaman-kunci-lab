from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import PenanggungJawabForm
from .mixins import admin_required, AdminRequiredMixin
from .models import PenanggungJawab


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_superuser:
                messages.error(
                    request,
                    'Akses ditolak. Hanya admin yang dapat menggunakan web ini.',
                )
            else:
                login(request, user)
                messages.success(request, 'Selamat datang, ' + user.username)
                return redirect('dashboard')
        else:
            messages.error(request, 'Username atau password salah!')
    return render(request, 'authentication/login.html')


@admin_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Anda telah logout.')
    return redirect('login')


class PenanggungJawabListView(AdminRequiredMixin, ListView):
    model = PenanggungJawab
    template_name = 'authentication/penanggung_jawab_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        qs = super().get_queryset().select_related('user')
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama_lengkap__icontains=search) |
                Q(telepon__icontains=search) |
                Q(user__username__icontains=search)
            )
        return qs


class PenanggungJawabCreateView(AdminRequiredMixin, CreateView):
    model = PenanggungJawab
    form_class = PenanggungJawabForm
    template_name = 'authentication/penanggung_jawab_form.html'
    success_url = reverse_lazy('penanggung_jawab_list')


class PenanggungJawabUpdateView(AdminRequiredMixin, UpdateView):
    model = PenanggungJawab
    form_class = PenanggungJawabForm
    template_name = 'authentication/penanggung_jawab_form.html'
    success_url = reverse_lazy('penanggung_jawab_list')


class PenanggungJawabDeleteView(AdminRequiredMixin, DeleteView):
    model = PenanggungJawab
    success_url = reverse_lazy('penanggung_jawab_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('penanggung_jawab_list')
        return context
