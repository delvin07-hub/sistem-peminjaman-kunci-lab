import json
import logging
import threading
from urllib import error, request

from django.conf import settings
from django.db import transaction

from apps.authentication.models import PenanggungJawab

from .models import Notifikasi

logger = logging.getLogger(__name__)


def _telegram_config():
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    if not token or not chat_id:
        logger.warning('Telegram belum dikonfigurasi; notifikasi dilewati')
        return None
    return token, str(chat_id)


def _kirim_telegram(token, chat_id, pesan):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = json.dumps({
        'chat_id': chat_id,
        'text': pesan,
        'disable_web_page_preview': True,
    }).encode('utf-8')
    req = request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with request.urlopen(req, timeout=10) as resp:
        body = json.loads(resp.read().decode('utf-8') or '{}')
    if not body.get('ok'):
        raise RuntimeError(body.get('description', 'Telegram error'))


class PushNotifikasiService:
    @staticmethod
    def kirim(notifikasi):
        config = _telegram_config()
        if not config:
            Notifikasi.objects.filter(pk=notifikasi.pk).update(status='Gagal')
            return
        token, chat_id = config
        try:
            _kirim_telegram(token, chat_id, notifikasi.pesan)
        except (error.URLError, TimeoutError, ValueError, RuntimeError) as exc:
            logger.warning('Gagal kirim Telegram: %s', exc)
            Notifikasi.objects.filter(pk=notifikasi.pk).update(status='Gagal')
            return
        Notifikasi.objects.filter(pk=notifikasi.pk).update(status='Terkirim')

    @staticmethod
    def kirim_untuk_peminjaman(peminjaman_id, tipe):
        try:
            for notifikasi in Notifikasi.objects.filter(
                peminjaman_id=peminjaman_id, tipe=tipe
            ):
                PushNotifikasiService.kirim(notifikasi)
        except Exception:
            logger.exception(
                'Gagal mengirim notifikasi Telegram untuk peminjaman %s (%s)',
                peminjaman_id,
                tipe,
            )


def _kirim_push_bg(peminjaman_id, tipe):
    """Mulai pengiriman Telegram di thread latar belakang (daemon)."""
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
        mhs_nama = mhs.nama if mhs else '-'
        lab_nama = lab.nama_lab if lab else '-'
        if tipe == 'Dipinjam':
            return (
                f'[PENANGGUNG JAWAB KUNCI]\n'
                f'{mhs_nama} meminjam kunci {nome} ({lab_nama})\n'
                f'Jam: {peminjaman.jam_pinjam}'
            )
        return (
            f'[PENANGGUNG JAWAB KUNCI]\n'
            f'{mhs_nama} mengembalikan kunci {nome} ({lab_nama})'
        )
