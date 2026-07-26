from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Mahasiswa, Dosen, Laboratorium, Kunci
from .forms import MahasiswaForm, DosenForm, LaboratoriumForm, KunciForm


class MahasiswaListView(LoginRequiredMixin, ListView):
    model = Mahasiswa
    template_name = 'master_data/mahasiswa_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama__icontains=search) | Q(nim__icontains=search)
            )
        return qs


class MahasiswaCreateView(LoginRequiredMixin, CreateView):
    model = Mahasiswa
    form_class = MahasiswaForm
    template_name = 'master_data/mahasiswa_form.html'
    success_url = reverse_lazy('mahasiswa_list')


class MahasiswaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mahasiswa
    form_class = MahasiswaForm
    template_name = 'master_data/mahasiswa_form.html'
    success_url = reverse_lazy('mahasiswa_list')


class MahasiswaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mahasiswa
    success_url = reverse_lazy('mahasiswa_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('mahasiswa_list')
        return context


class DosenListView(LoginRequiredMixin, ListView):
    model = Dosen
    template_name = 'master_data/dosen_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama__icontains=search) | Q(nidn__icontains=search)
            )
        return qs


class DosenCreateView(LoginRequiredMixin, CreateView):
    model = Dosen
    form_class = DosenForm
    template_name = 'master_data/dosen_form.html'
    success_url = reverse_lazy('dosen_list')


class DosenUpdateView(LoginRequiredMixin, UpdateView):
    model = Dosen
    form_class = DosenForm
    template_name = 'master_data/dosen_form.html'
    success_url = reverse_lazy('dosen_list')


class DosenDeleteView(LoginRequiredMixin, DeleteView):
    model = Dosen
    success_url = reverse_lazy('dosen_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('dosen_list')
        return context


class LaboratoriumListView(LoginRequiredMixin, ListView):
    model = Laboratorium
    template_name = 'master_data/laboratorium_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama_lab__icontains=search) | Q(kode_lab__icontains=search)
            )
        return qs


class LaboratoriumCreateView(LoginRequiredMixin, CreateView):
    model = Laboratorium
    form_class = LaboratoriumForm
    template_name = 'master_data/laboratorium_form.html'
    success_url = reverse_lazy('laboratorium_list')


class LaboratoriumUpdateView(LoginRequiredMixin, UpdateView):
    model = Laboratorium
    form_class = LaboratoriumForm
    template_name = 'master_data/laboratorium_form.html'
    success_url = reverse_lazy('laboratorium_list')


class LaboratoriumDeleteView(LoginRequiredMixin, DeleteView):
    model = Laboratorium
    success_url = reverse_lazy('laboratorium_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('laboratorium_list')
        return context


class KunciListView(LoginRequiredMixin, ListView):
    model = Kunci
    template_name = 'master_data/kunci_list.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('laboratorium')
        search = self.request.GET.get('search')
        lab = self.request.GET.get('lab')
        if search:
            qs = qs.filter(nomor_kunci__icontains=search)
        if lab:
            qs = qs.filter(laboratorium_id=lab)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_list'] = Laboratorium.objects.all()
        return context


class KunciCreateView(LoginRequiredMixin, CreateView):
    model = Kunci
    form_class = KunciForm
    template_name = 'master_data/kunci_form.html'
    success_url = reverse_lazy('kunci_list')


class KunciUpdateView(LoginRequiredMixin, UpdateView):
    model = Kunci
    form_class = KunciForm
    template_name = 'master_data/kunci_form.html'
    success_url = reverse_lazy('kunci_list')


class KunciDeleteView(LoginRequiredMixin, DeleteView):
    model = Kunci
    success_url = reverse_lazy('kunci_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('kunci_list')
        return context
