import 'package:flutter/material.dart';

import '../api/api_service.dart';
import 'notifikasi_detail_screen.dart';

class NotifikasiScreen extends StatefulWidget {
  const NotifikasiScreen({super.key});

  @override
  State<NotifikasiScreen> createState() => _NotifikasiScreenState();
}

class _NotifikasiScreenState extends State<NotifikasiScreen> {
  late Future<List<dynamic>> _future;
  final _api = ApiService.instance;

  @override
  void initState() {
    super.initState();
    _future = _load();
  }

  Future<List<dynamic>> _load() => _api.getList('notifikasi/');

  Future<void> _refresh() async {
    setState(() => _future = _load());
  }

  Future<void> _markBaca(dynamic item) async {
    await _api.markBaca(item['id']);
    _refresh();
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _refresh,
      child: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return _Message(
              icon: Icons.error_outline,
              text: 'Gagal memuat notifikasi',
              detail: snapshot.error.toString(),
              onRetry: _refresh,
            );
          }
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final items = snapshot.data!;
          if (items.isEmpty) {
            return const _Message(
              icon: Icons.notifications_off,
              text: 'Belum ada notifikasi',
            );
          }
          return ListView.separated(
            physics: const AlwaysScrollableScrollPhysics(),
            itemCount: items.length,
            separatorBuilder: (_, _) => const Divider(height: 1),
            itemBuilder: (context, index) {
              final item = items[index];
              final dibaca = item['dibaca'] == true;
              final isi = (item['pesan'] ?? '').toString();
              return Dismissible(
                key: ValueKey(item['id']),
                direction: DismissDirection.endToStart,
                background: Container(
                  color: Colors.blue.shade700,
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 20),
                  child: const Icon(Icons.done, color: Colors.white),
                ),
                onDismissed: (_) => _markBaca(item),
                child: ListTile(
                  onTap: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => NotifikasiDetailScreen(
                          notifikasiId: item['id'],
                        ),
                      ),
                    );
                  },
                  leading: Icon(
                    item['tipe'] == 'Dikembalikan'
                        ? Icons.key
                        : Icons.warning_amber,
                    color: item['tipe'] == 'Dikembalikan'
                        ? Colors.green
                        : Colors.orange,
                  ),
                  title: Text(isi),
                  subtitle: Text(
                    _formatTanggal(item['tanggal']?.toString() ?? ''),
                  ),
                  trailing: dibaca
                      ? null
                      : IconButton(
                          tooltip: 'Tandai dibaca',
                          icon: const Icon(Icons.mark_as_unread,
                              color: Colors.blue),
                          onPressed: () => _markBaca(item),
                        ),
                  tileColor: dibaca ? null : const Color(0xFFEFF6FF),
                ),
              );
            },
          );
        },
      ),
    );
  }

  String _formatTanggal(String iso) {
    if (iso.isEmpty) return '';
    final p = DateTime.tryParse(iso);
    if (p == null) return iso;
    return '${p.day.toString().padLeft(2, '0')}-'
        '${p.month.toString().padLeft(2, '0')}-'
        '${p.year} ${p.hour.toString().padLeft(2, '0')}:'
        '${p.minute.toString().padLeft(2, '0')}';
  }
}

class _Message extends StatelessWidget {
  final IconData icon;
  final String text;
  final String? detail;
  final VoidCallback? onRetry;

  const _Message({required this.icon, required this.text, this.detail, this.onRetry});

  @override
  Widget build(BuildContext context) {
    return ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      children: [
        const SizedBox(height: 120),
        Icon(icon, size: 56, color: Colors.grey),
        const SizedBox(height: 12),
        Text(text, textAlign: TextAlign.center),
        if (detail != null) ...[
          const SizedBox(height: 8),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Text(detail!,
                textAlign: TextAlign.center, style: const TextStyle(fontSize: 12)),
          ),
        ],
        if (onRetry != null) ...[
          const SizedBox(height: 16),
          Center(
            child: FilledButton.tonal(onPressed: onRetry, child: const Text('COBA LAGI')),
          ),
        ],
      ],
    );
  }
}