import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Penyimpanan token akses API.
/// - Android/iOS/Windows: `flutter_secure_storage` (terenkripsi/DPAPI).
/// - Web: `shared_preferences` (secure storage web belum penuh dukungannya).
class TokenStorage {
  static const _key = 'api_token';

  static bool get _isWeb => kIsWeb;

  static Future<String?> read() async {
    if (_isWeb) {
      final prefs = await SharedPreferences.getInstance();
      return prefs.getString(_key);
    }
    const storage = FlutterSecureStorage();
    return storage.read(key: _key);
  }

  static Future<void> write(String token) async {
    if (_isWeb) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(_key, token);
      return;
    }
    const storage = FlutterSecureStorage();
    await storage.write(key: _key, value: token);
  }

  static Future<void> clear() async {
    if (_isWeb) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove(_key);
      return;
    }
    const storage = FlutterSecureStorage();
    await storage.delete(key: _key);
  }
}
