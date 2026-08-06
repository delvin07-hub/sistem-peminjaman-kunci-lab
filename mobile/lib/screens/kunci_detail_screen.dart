import 'package:flutter/material.dart';

import '../api/api_service.dart';

class KunciDetailScreen extends StatefulWidget {
  final int kunciId;
  const KunciDetailScreen({super.key, required this.kunciId});

  @override
  State<KunciDetailScreen> createState() => _KunciDetailScreenState();
}

class _KunciDetailScreenState extends State<KunciDetailScreen> {
  late Future<dynamic> _future;

  @override
  void initState() {
    super.initState();
    _future = ApiService.instance.getDetail('status-kunci/${widget.kunciId}/');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detail Kunci')),
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
          final aktif = data['peminjaman_aktif'];
          final riwayat = (data['riwayat'] as List<dynamic>?) ?? const [];

          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _card('Info Kunci', [
                _row('Kunci', data['nomor_kunci']),
                _row('Laboratorium', data['nama_lab']),
                _row('Kode Lab', data['kode_lab']),
                _row('Gedung', data['gedung']),
                _row('Lantai', data['lantai']),
                _row('Status', data['status']),
              ]),
              const SizedBox(height: 12),
              if (aktif is Map<String, dynamic>)
                _card('Dipinjam Oleh', [
                  _row('Nama', aktif['mahasiswa']['nama']),
                  _row('NIM', aktif['mahasiswa']['nim']),
                  _row(
                    'Program Studi',
                    aktif['mahasiswa']['program_studi'],
                  ),
                  _row('Dosen', aktif['dosen']['nama']),
                  _row('NIDN', aktif['dosen']['nidn']),
                  _row('Tanggal Pinjam', aktif['tanggal_pinjam']),
                  _row('Jam Pinjam', aktif['jam_pinjam']),
                  _row('Keperluan', aktif['keperluan']),
                ])
              else
                Card(
                  color: Colors.green.shade50,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.green.shade700),
                        const SizedBox(width: 8),
                        const Text(
                          'Kunci tersedia, tidak sedang dipinjam',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 12),
              if (riwayat.isNotEmpty)
                _card('Riwayat Peminjaman', [
                  for (final r in riwayat) _riwayatItem(r),
                ]),
            ],
          );
        },
      ),
    );
  }

  Widget _riwayatItem(dynamic r) {
    final kembali = r['status'] == 'Dikembalikan';
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Divider(),
        Row(
          children: [
            Expanded(
              child: Text(
                '${r['mahasiswa']['nama']} (${r['mahasiswa']['nim']})',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
            Chip(
              label: Text(
                r['status'].toString().toUpperCase(),
                style: const TextStyle(fontSize: 10),
              ),
              backgroundColor: kembali
                  ? Colors.green.withValues(alpha: 0.15)
                  : Colors.red.withValues(alpha: 0.15),
              visualDensity: VisualDensity.compact,
            ),
          ],
        ),
        Text('Dosen: ${r['dosen']['nama']}'),
        Text(
          'Pinjam: ${r['tanggal_pinjam']} ${r['jam_pinjam']}'
          '\nKembali: ${r['tanggal_kembali'] ?? '-'} ${r['jam_kembali'] ?? '-'}',
        ),
        Text('Keperluan: ${r['keperluan']}'),
      ],
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
