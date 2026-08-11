import 'package:flutter/material.dart';

import '../api/api_service.dart';
import 'kunci_screen.dart';
import 'notifikasi_screen.dart';

class HomeScreen extends StatefulWidget {
  final VoidCallback onLogout;
  const HomeScreen({super.key, required this.onLogout});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      const NotifikasiScreen(),
      const KunciScreen(),
      _LogoutPage(onLogout: widget.onLogout),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Kunci Lab'),
        backgroundColor: const Color(0xFF0D3B66),
        foregroundColor: Colors.white,
      ),
      body: pages[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(
              icon: Icon(Icons.notifications), label: 'Notifikasi'),
          NavigationDestination(
              icon: Icon(Icons.key), label: 'Kunci'),
          NavigationDestination(
              icon: Icon(Icons.logout), label: 'Keluar'),
        ],
      ),
    );
  }
}

class _LogoutPage extends StatelessWidget {
  final VoidCallback onLogout;
  const _LogoutPage({required this.onLogout});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('Anda login sebagai penanggung jawab.'),
          const SizedBox(height: 16),
          FilledButton.tonalIcon(
            onPressed: () async {
              await ApiService.instance.logout();
              onLogout();
            },
            icon: const Icon(Icons.logout),
            label: const Text('KELUAR'),
          ),
        ],
      ),
    );
  }
}
