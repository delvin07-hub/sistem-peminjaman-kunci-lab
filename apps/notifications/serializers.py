from rest_framework import serializers

from apps.authentication.models import PenanggungJawab
from apps.master_data.models import Kunci

from .models import Notifikasi


class NotifikasiSerializer(serializers.ModelSerializer):
    tanggal = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Notifikasi
        fields = ['id', 'tipe', 'pesan', 'dibaca', 'peminjaman', 'tanggal']


class KunciStatusSerializer(serializers.ModelSerializer):
    kode_lab = serializers.CharField(
        source='laboratorium.kode_lab', read_only=True
    )
    nama_lab = serializers.CharField(
        source='laboratorium.nama_lab', read_only=True
    )

    class Meta:
        model = Kunci
        fields = ['id', 'kode_lab', 'nama_lab', 'nomor_kunci', 'status']


class PenanggungJawabSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PenanggungJawab
        fields = ['username', 'nama_lengkap', 'telepon', 'aktif']