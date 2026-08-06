from rest_framework import generics

from apps.master_data.models import Kunci

from .models import Notifikasi
from .permissions import IsPenanggungJawab
from .serializers import KunciStatusSerializer, NotifikasiSerializer


class NotifikasiListView(generics.ListAPIView):
    permission_classes = [IsPenanggungJawab]
    serializer_class = NotifikasiSerializer

    def get_queryset(self):
        queryset = Notifikasi.objects.filter(
            penanggung_jawab__user=self.request.user
        )
        dibaca = self.request.query_params.get('dibaca')
        if dibaca is not None:
            queryset = queryset.filter(
                dibaca=dibaca.lower() in ('1', 'true', 'yes')
            )
        return queryset


class NotifikasiBacaView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsPenanggungJawab]
    serializer_class = NotifikasiSerializer

    def get_queryset(self):
        return Notifikasi.objects.filter(
            penanggung_jawab__user=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(dibaca=True)


class KunciStatusListView(generics.ListAPIView):
    permission_classes = [IsPenanggungJawab]
    serializer_class = KunciStatusSerializer
    queryset = Kunci.objects.select_related('laboratorium')