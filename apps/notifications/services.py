import logging
import threading

from django.conf import settings
from django.db import transaction

from apps.authentication.models import PenanggungJawab

from .models import DeviceToken, Notifikasi

logger = logging.getLogger(__name__)

_firebase_app = None


def _get_firebase_app():
    """Inisialisasi firebase_admin satu kali; None jika key tidak tersedia."""
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app
    path = settings.FCM_SERVICE_ACCOUNT_JSON
    if not path or not __import__('pathlib').Path(path).exists():
        logger.warning(
            'FCM_SERVICE_ACCOUNT_JSON tidak ditemukan (%s); push dinonaktifkan',
            path,
        )
        _firebase_app = False
        return None
    import firebase_admin
    from firebase_admin import credentials

    try:
        _firebase_app = firebase_admin.initialize_app(
            credentials.Certificate(str(path))
        )
    except Exception:
        logger.exception('Gagal inisialisasi firebase_admin')
        _firebase_app = False
    return _firebase_app if _firebase_app else None


class PushNotifikasiService:
    @staticmethod
    def kirim(notifikasi):
        app = _get_firebase_app()
        if not app:
            return
        try:
            from firebase_admin import messaging
        except ImportError:
            logger.warning('firebase-admin belum terinstall; push dilewati')
            return
        peminjaman = notifikasi.peminjaman
        data = {
            'notifikasi_id': str(notifikasi.id),
            'tipe': notifikasi.tipe,
            'peminjaman_id': str(peminjaman.id) if peminjaman else '',
            'pesan': notifikasi.pesan,
        }
        token_ids = notifikasi.penanggung_jawab.device_tokens.values_list(
            'token', flat=True
        )
        for token in token_ids:
            try:
                messaging.send(
                    messaging.Message(
                        notification=messaging.Notification(
                            title='Kunci Dipinjam'
                            if notifikasi.tipe == 'Dipinjam'
                            else 'Kunci Dikembalikan',
                            body=notifikasi.pesan,
                        ),
                        data=data,
                        token=token,
                    )
                )
            except Exception as exc:
                logger.warning(
                    'Gagal kirim FCM ke token %s...: %s', token[:20], exc
                )
                from firebase_admin import exceptions as fb_exc
                from firebase_admin import messaging as fcm

                if isinstance(
                    exc, (fcm.UnregisteredError, fb_exc.InvalidArgumentError)
                ):
                    DeviceToken.objects.filter(token=token).delete()
                    logger.info('Device token kadaluarsa dihapus: %s...', token[:20])

    @staticmethod
    def kirim_untuk_peminjaman(peminjaman_id, tipe):
        try:
            for notifikasi in Notifikasi.objects.filter(
                peminjaman_id=peminjaman_id, tipe=tipe
            ):
                PushNotifikasiService.kirim(notifikasi)
        except Exception:
            logger.exception(
                'Gagal mengirim push untuk peminjaman %s (%s)',
                peminjaman_id, tipe,
            )


def _kirim_push_bg(peminjaman_id, tipe):
    """Mulai pengiriman push FCM di thread latar belakang (daemon)."""
    threading.Thread(
        target=PushNotifikasiService.kirim_untuk_peminjaman,
        args=(peminjaman_id, tipe),
        daemon=True,
    ).start()


class NotifikasiService:
    @staticmethod
    def buat(peminjaman, tipe):
        pesan = NotifikasiService._bentuk_pesan(peminjaman, tipe)
        for pj in PenanggungJawab.objects.filter(aktif=True):
            Notifikasi.objects.create(
                penanggung_jawab=pj,
                peminjaman=peminjaman,
                tipe=tipe,
                pesan=pesan,
            )
        transaction.on_commit(
            lambda: _kirim_push_bg(peminjaman.id, tipe)
        )

    @staticmethod
    def _bentuk_pesan(peminjaman, tipe):
        kunci = peminjaman.kunci
        nome = kunci.nomor_kunci if kunci else '-'
        lab = peminjaman.laboratorium
        mhs = peminjaman.mahasiswa
        if tipe == 'Dipinjam':
            return (
                f'{mhs.nama} meminjam kunci {nome}'
                f' ({lab.nama_lab}) jam {peminjaman.jam_pinjam}'
            )
        return (
            f'{mhs.nama} mengembalikan kunci {nome}'
            f' ({lab.nama_lab})'
        )
