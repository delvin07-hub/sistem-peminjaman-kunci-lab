from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.authentication.mixins import AdminRequiredMixin
from django.db.models import Q
from .models import Mahasiswa, Dosen, Laboratorium, Kunci
from .forms import MahasiswaForm, DosenForm, LaboratoriumForm, KunciForm


def _next_kode_ruangan():
    n = 1
    while Laboratorium.objects.filter(kode_lab=f'R{n}').exists():
        n += 1
    return f'R{n}'


def _next_nomor_kunci(ruangan):
    n = 1
    while Kunci.objects.filter(
        laboratorium=ruangan, nomor_kunci=f'K{n}'
    ).exists():
        n += 1
    return f'K{n}'


def _renumber_kunci(ruangan):
    """Renumber semua kunci ruangan jadi kontigu K1..Kn (urut id)."""
    daftar = list(Kunci.objects.filter(laboratorium=ruangan).order_by('id'))
    for i, k in enumerate(daftar, start=1):
        k.nomor_kunci = f'TMP{i}'
        k.save(update_fields=['nomor_kunci'])
    for i, k in enumerate(daftar, start=1):
        k.nomor_kunci = f'K{i}'
        k.save(update_fields=['nomor_kunci'])


class MahasiswaListView(AdminRequiredMixin, ListView):
    model = Mahasiswa
    template_name = 'master_data/mahasiswa_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama__icontains=search) | Q(nim__icontains=search)
            )
        return qs


class MahasiswaCreateView(AdminRequiredMixin, CreateView):
    model = Mahasiswa
    form_class = MahasiswaForm
    template_name = 'master_data/mahasiswa_form.html'
    success_url = reverse_lazy('mahasiswa_list')


class MahasiswaUpdateView(AdminRequiredMixin, UpdateView):
    model = Mahasiswa
    form_class = MahasiswaForm
    template_name = 'master_data/mahasiswa_form.html'
    success_url = reverse_lazy('mahasiswa_list')


class MahasiswaDeleteView(AdminRequiredMixin, DeleteView):
    model = Mahasiswa
    success_url = reverse_lazy('mahasiswa_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('mahasiswa_list')
        return context


class DosenListView(AdminRequiredMixin, ListView):
    model = Dosen
    template_name = 'master_data/dosen_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama__icontains=search) | Q(nidn__icontains=search)
            )
        return qs


class DosenCreateView(AdminRequiredMixin, CreateView):
    model = Dosen
    form_class = DosenForm
    template_name = 'master_data/dosen_form.html'
    success_url = reverse_lazy('dosen_list')


class DosenUpdateView(AdminRequiredMixin, UpdateView):
    model = Dosen
    form_class = DosenForm
    template_name = 'master_data/dosen_form.html'
    success_url = reverse_lazy('dosen_list')


class DosenDeleteView(AdminRequiredMixin, DeleteView):
    model = Dosen
    success_url = reverse_lazy('dosen_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('dosen_list')
        return context


class LaboratoriumListView(AdminRequiredMixin, ListView):
    model = Laboratorium
    template_name = 'master_data/laboratorium_list.html'
    context_object_name = 'data'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(nama_lab__icontains=search) | Q(kode_lab__icontains=search)
            )
        return qs


class LaboratoriumCreateView(AdminRequiredMixin, CreateView):
    model = Laboratorium
    form_class = LaboratoriumForm
    template_name = 'master_data/laboratorium_form.html'
    success_url = reverse_lazy('laboratorium_list')

    def form_valid(self, form):
        form.instance.kode_lab = _next_kode_ruangan()
        messages.success(self.request, 'Ruangan berhasil ditambahkan.')
        return super().form_valid(form)


class LaboratoriumUpdateView(AdminRequiredMixin, UpdateView):
    model = Laboratorium
    form_class = LaboratoriumForm
    template_name = 'master_data/laboratorium_form.html'
    success_url = reverse_lazy('laboratorium_list')


class LaboratoriumDeleteView(AdminRequiredMixin, DeleteView):
    model = Laboratorium
    success_url = reverse_lazy('laboratorium_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('laboratorium_list')
        return context


class KunciListView(AdminRequiredMixin, ListView):
    model = Kunci
    template_name = 'master_data/kunci_list.html'
    context_object_name = 'data'

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


class KunciCreateView(AdminRequiredMixin, CreateView):
    model = Kunci
    form_class = KunciForm
    template_name = 'master_data/kunci_form.html'
    success_url = reverse_lazy('kunci_list')

    def form_valid(self, form):
        form.instance.nomor_kunci = _next_nomor_kunci(
            form.instance.laboratorium
        )
        messages.success(self.request, 'Kunci berhasil ditambahkan.')
        return super().form_valid(form)


class KunciUpdateView(AdminRequiredMixin, UpdateView):
    model = Kunci
    form_class = KunciForm
    template_name = 'master_data/kunci_form.html'
    success_url = reverse_lazy('kunci_list')


class KunciDeleteView(AdminRequiredMixin, DeleteView):
    model = Kunci
    success_url = reverse_lazy('kunci_list')
    template_name = 'master_data/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('kunci_list')
        return context

    def _cegah_hapus(self, request):
        obj = self.get_object()
        if obj.status == 'Dipinjam':
            messages.error(
                request,
                f"Kunci {obj.nomor_kunci} sedang dipinjam, tidak dapat dihapus."
            )
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self._cegah_hapus(request):
            return redirect('kunci_list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self._cegah_hapus(self.request):
            return redirect('kunci_list')
        self.object = self.get_object()
        ruangan = self.object.laboratorium
        success_url = self.get_success_url()
        self.object.delete()
        _renumber_kunci(ruangan)
        messages.success(
            self.request, 'Kunci berhasil dihapus dan penomoran diperbarui.'
        )
        return redirect(success_url)
