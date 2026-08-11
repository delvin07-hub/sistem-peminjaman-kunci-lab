from rest_framework import serializers

from apps.authentication.models import PenanggungJawab
from apps.master_data.models import Dosen, Kunci, Laboratorium, Mahasiswa
from apps.transaction.models import Peminjaman

from .models import Notifikasi


class MahasiswaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = ['nim', 'nama', 'program_studi']


class DosenDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dosen
        fields = ['nidn', 'nama']


class LaboratoriumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratorium
        fields = ['kode_lab', 'nama_lab', 'gedung', 'lantai']


class KunciDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kunci
        fields = ['id', 'nomor_kunci', 'status']


class PeminjamanDetailSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaDetailSerializer(read_only=True)
    dosen = DosenDetailSerializer(read_only=True)
    laboratorium = LaboratoriumDetailSerializer(read_only=True)
    kunci = KunciDetailSerializer(read_only=True)

    class Meta:
        model = Peminjaman
        fields = [
            'id',
            'status',
            'tanggal_pinjam',
            'jam_pinjam',
            'tanggal_kembali',
            'jam_kembali',
            'keperluan',
            'mahasiswa',
            'dosen',
            'laboratorium',
            'kunci',
        ]


class NotifikasiSerializer(serializers.ModelSerializer):
    tanggal = serializers.DateTimeField(source='created_at', read_only=True)
    peminjaman_detail = PeminjamanDetailSerializer(
        source='peminjaman', read_only=True
    )

    class Meta:
        model = Notifikasi
        fields = [
            'id',
            'tipe',
            'pesan',
            'dibaca',
            'peminjaman',
            'peminjaman_detail',
            'tanggal',
        ]


class KunciStatusSerializer(serializers.ModelSerializer):
    kode_lab = serializers.CharField(
        source='laboratorium.kode_lab', read_only=True
    )
    nama_lab = serializers.CharField(
        source='laboratorium.nama_lab', read_only=True
    )
    gedung = serializers.CharField(
        source='laboratorium.gedung', read_only=True
    )
    lantai = serializers.CharField(
        source='laboratorium.lantai', read_only=True
    )
    peminjaman_aktif = serializers.SerializerMethodField()

    class Meta:
        model = Kunci
        fields = [
            'id',
            'kode_lab',
            'nama_lab',
            'gedung',
            'lantai',
            'nomor_kunci',
            'status',
            'peminjaman_aktif',
        ]

    def get_peminjaman_aktif(self, obj):
        peminjaman = (
            obj.peminjaman.filter(status='Dipinjam')
            .select_related('mahasiswa', 'dosen', 'laboratorium', 'kunci')
            .first()
        )
        if peminjaman is None:
            return None
        return PeminjamanDetailSerializer(peminjaman).data


class KunciRiwayatSerializer(serializers.ModelSerializer):
    mahasiswa = MahasiswaDetailSerializer(read_only=True)
    dosen = DosenDetailSerializer(read_only=True)
    laboratorium = LaboratoriumDetailSerializer(read_only=True)

    class Meta:
        model = Peminjaman
        fields = [
            'id',
            'status',
            'tanggal_pinjam',
            'jam_pinjam',
            'tanggal_kembali',
            'jam_kembali',
            'keperluan',
            'mahasiswa',
            'dosen',
            'laboratorium',
        ]


class KunciDetailEndpointSerializer(KunciStatusSerializer):
    riwayat = serializers.SerializerMethodField()

    class Meta(KunciStatusSerializer.Meta):
        fields = KunciStatusSerializer.Meta.fields + ['riwayat']

    def get_riwayat(self, obj):
        riwayat = (
            obj.peminjaman.select_related('mahasiswa', 'dosen', 'laboratorium')
            .order_by('-created_at')[:10]
        )
        return KunciRiwayatSerializer(riwayat, many=True).data


class PenanggungJawabSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PenanggungJawab
        fields = ['username', 'nama_lengkap', 'telepon', 'aktif']
