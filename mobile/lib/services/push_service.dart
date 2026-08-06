import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

import '../api/api_service.dart';

@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
  await PushService.showLocalNotification(message);
}

class PushService {
  static final FlutterLocalNotificationsPlugin _local =
      FlutterLocalNotificationsPlugin();
  static String? _fcmToken;
  static final ValueNotifier<RemoteMessage?> onOpenMessage =
      ValueNotifier<RemoteMessage?>(null);

  static Future<void> init() async {
    await Firebase.initializeApp();
    FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

    const settings = AndroidInitializationSettings('@mipmap/ic_launcher');
    await _local.initialize(
      settings: const InitializationSettings(android: settings),
    );
    await _local
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.requestNotificationsPermission();

    await FirebaseMessaging.instance
        .requestPermission(alert: true, badge: true, sound: true);

    FirebaseMessaging.onMessage.listen((message) {
      if (!kIsWeb) PushService.showLocalNotification(message);
    });
    FirebaseMessaging.onMessageOpenedApp.listen((message) {
      onOpenMessage.value = message;
    });
    final initial = await FirebaseMessaging.instance.getInitialMessage();
    if (initial != null) {
      onOpenMessage.value = initial;
    }
  }

  static Future<void> showLocalNotification(RemoteMessage message) async {
    const android = AndroidNotificationDetails(
      'notifikasi_kunci',
      'Notifikasi Kunci',
      channelDescription: 'Pemberitahuan peminjaman/pengembalian kunci lab',
      importance: Importance.high,
      priority: Priority.high,
    );
    await _local.show(
      id: message.messageId?.hashCode ?? DateTime.now().millisecondsSinceEpoch,
      title: message.notification?.title ?? 'Kunci Lab',
      body: message.notification?.body ?? message.data['pesan'] ?? '',
      notificationDetails: const NotificationDetails(android: android),
      payload: message.data['notifikasi_id'],
    );
  }

  static Future<String?> refreshToken() async {
    try {
      _fcmToken = await FirebaseMessaging.instance.getToken();
    } catch (e) {
      debugPrint('FCM getToken gagal: $e');
      _fcmToken = null;
    }
    return _fcmToken;
  }

  static Future<bool> registerDeviceToken() async {
    final token = await refreshToken();
    if (token == null) return false;
    try {
      await ApiService.instance.registerDeviceToken(token);
      return true;
    } catch (e) {
      debugPrint('Registrasi device token gagal: $e');
      return false;
    }
  }

  static Future<void> unregisterDeviceToken() async {
    if (_fcmToken == null) return;
    try {
      await ApiService.instance.unregisterDeviceToken(_fcmToken!);
    } catch (_) {
      // Abaikan; token kadaluarsa akan dibersihkan server
    }
    _fcmToken = null;
  }
}
