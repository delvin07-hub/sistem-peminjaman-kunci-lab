import 'package:flutter/material.dart';

import '../api/api_service.dart';

class KunciScreen extends StatefulWidget {
  const KunciScreen({super.key});

  @override
  State<KunciScreen> createState() => _KunciScreenState();
}

class _KunciScreenState extends State<KunciScreen> {
  final _api = ApiService.instance;
  late Future<List<dynamic>> _future;

  @override
  void initState() {
    super.initState();
    _future = _api.getList('status-kunci/');
  }

  Future<void> _refresh() async {
    setState(() => _future = _api.getList('status-kunci/'));
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _refresh,
      child: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(
              child: Text('Gagal memuat: ${snapshot.error}',
                  textAlign: TextAlign.center),
            );
          }
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final items = snapshot.data!;
          if (items.isEmpty) {
            return const Center(child: Text('Belum ada kunci'));
          }
          return ListView.separated(
            physics: const AlwaysScrollableScrollPhysics(),
            itemCount: items.length,
            separatorBuilder: (_, _) => const Divider(height: 1),
            itemBuilder: (context, index) {
              final item = items[index];
              final tersedia = item['status'] == 'Tersedia';
              return ListTile(
                leading: Icon(
                  tersedia ? Icons.key : Icons.key_off,
                  color: tersedia ? Colors.green : Colors.red,
                ),
                title: Text('${item['nomor_kunci']}'),
                subtitle: Text('${item['nama_lab']} (${item['kode_lab']})'),
                trailing: Chip(
                  label: Text(item['status'].toString().toUpperCase()),
backgroundColor: tersedia
                    ? Colors.green.withValues(alpha: 0.15)
                    : Colors.red.withValues(alpha: 0.15),
                  labelStyle: TextStyle(
                    color: tersedia ? Colors.green.shade800 : Colors.red.shade800,
                    fontWeight: FontWeight.bold,
                    fontSize: 11,
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}