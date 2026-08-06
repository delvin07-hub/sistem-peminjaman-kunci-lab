import 'package:flutter/material.dart';

import '../api/api_service.dart';

class NotifikasiDetailScreen extends StatefulWidget {
  final int notifikasiId;
  const NotifikasiDetailScreen({super.key, required this.notifikasiId});

  @override
  State<NotifikasiDetailScreen> createState() => _NotifikasiDetailScreenState();
}

class _NotifikasiDetailScreenState extends State<NotifikasiDetailScreen> {
  late Future<dynamic> _future;

  @override
  void initState() {
    super.initState();
    _future = ApiService.instance
        .getDetail('notifikasi/${widget.notifikasiId}/baca/');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detail Notifikasi')),
      body: FutureBuilder<dynamic>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(child: Text('Gagal memuat: ${snapshot.error}'));
          }
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snapshot.data as Map<String, dynamic>;
          final detail = data['peminjaman_detail'];
          if (detail is! Map<String, dynamic>) {
            return const Center(child: Text('Detail peminjaman tidak tersedia'));
          }
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _header(data),
              const SizedBox(height: 16),
              _card('Data Peminjam', [
                _row('Nama', detail['mahasiswa']['nama']),
                _row('NIM', detail['mahasiswa']['nim']),
                _row('Program Studi', detail['mahasiswa']['program_studi']),
                _row('Dosen', detail['dosen']['nama']),
                _row('NIDN', detail['dosen']['nidn']),
              ]),
              const SizedBox(height: 12),
              _card('Kunci', [
                _row('Kunci', detail['kunci']['nomor_kunci']),
                _row(
                  'Laboratorium',
                  detail['laboratorium']['nama_lab'],
                ),
                _row('Kode Lab', detail['laboratorium']['kode_lab']),
                _row('Gedung', detail['laboratorium']['gedung']),
                _row('Lantai', detail['laboratorium']['lantai']),
              ]),
              const SizedBox(height: 12),
              _card('Peminjaman', [
                _row('Status', detail['status']),
                _row('Tanggal Pinjam', detail['tanggal_pinjam']),
                _row('Jam Pinjam', detail['jam_pinjam']),
                _row('Tanggal Kembali', detail['tanggal_kembali']?.toString() ?? '-'),
                _row('Jam Kembali', detail['jam_kembali']?.toString() ?? '-'),
                _row('Keperluan', detail['keperluan']),
              ]),
            ],
          );
        },
      ),
    );
  }

  Widget _header(Map<String, dynamic> data) {
    final tipe = data['tipe'] == 'Dikembalikan' ? 'Dikembalikan' : 'Dipinjam';
    final isKembali = tipe == 'Dikembalikan';
    return Card(
      color: isKembali ? Colors.green.shade50 : Colors.orange.shade50,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  isKembali ? Icons.key : Icons.warning_amber,
                  color: isKembali ? Colors.green : Colors.orange.shade800,
                ),
                const SizedBox(width: 8),
                Text(
                  'Kunci $tipe',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: isKembali ? Colors.green.shade800 : Colors.orange.shade900,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(data['pesan'] ?? ''),
          ],
        ),
      ),
    );
  }

  Widget _card(String title, List<Widget> rows) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
            ),
            const SizedBox(height: 12),
            ...rows,
          ],
        ),
      ),
    );
  }

  Widget _row(String label, String? value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 130,
            child: Text(
              label,
              style: const TextStyle(color: Colors.grey),
            ),
          ),
          Expanded(child: Text(value ?? '-')),
        ],
      ),
    );
  }
}
