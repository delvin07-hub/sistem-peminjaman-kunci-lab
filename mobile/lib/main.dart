import 'package:flutter/material.dart';

import 'api/api_service.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/notifikasi_detail_screen.dart';
import 'services/push_service.dart';

final GlobalKey<NavigatorState> appNavigatorKey = GlobalKey<NavigatorState>();

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await PushService.init();
  PushService.onOpenMessage.addListener(_handleOpenMessage);
  runApp(const KunciLabApp());
}

void _handleOpenMessage() {
  final message = PushService.onOpenMessage.value;
  final notifId = message?.data['notifikasi_id'];
  if (notifId == null) return;
  final nav = appNavigatorKey.currentState;
  if (nav == null) return;
  nav.pushAndRemoveUntil(
    MaterialPageRoute(
      builder: (_) => NotifikasiDetailScreen(
        notifikasiId: int.tryParse(notifId) ?? 0,
      ),
    ),
    (route) => false,
  );
}

class KunciLabApp extends StatelessWidget {
  const KunciLabApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: appNavigatorKey,
      title: 'Kunci Lab',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0D3B66)),
        useMaterial3: true,
      ),
      home: const AuthGate(),
    );
  }
}

class AuthGate extends StatelessWidget {
  const AuthGate({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: ApiService.instance.isLoggedIn(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }
        final loggedIn = snapshot.data == true;
        if (loggedIn) {
          return HomeScreen(onLogout: () => _reset(context));
        }
        return LoginScreen(onLogin: () => _reset(context));
      },
    );
  }

  void _reset(BuildContext context) {
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const AuthGate()),
      (route) => false,
    );
  }
}
