import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

/// Ubah base URL sesuai server backend.
/// Untuk HP Android yang menekan server di satu PC/lab, gunakan
/// IP komputer server, contoh: http://192.168.1.10:8000/api/
class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://localhost:8000/api/',
  );

  static Uri uri(String path) =>
      Uri.parse('$baseUrl${path.startsWith('/') ? path.substring(1) : path}');
}

class ApiException implements Exception {
  final String message;
  ApiException(this.message);

  @override
  String toString() => message;
}

class ApiService {
  String? _token;

  static final ApiService instance = ApiService._();

  ApiService._();

  static Future<String?> get _storedToken async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('api_token');
  }

  static Future<void> saveToken(String? token) async {
    final prefs = await SharedPreferences.getInstance();
    if (token == null) {
      await prefs.remove('api_token');
    } else {
      await prefs.setString('api_token', token);
    }
  }

  Future<bool> isLoggedIn() async {
    _token ??= await _storedToken;
    return _token != null;
  }

  Future<void> login(String username, String password) async {
    final response = await http.post(
      ApiConfig.uri('token/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
    final data = _decode(response);
    if (response.statusCode == 200) {
      _token = data['token'] as String;
      await saveToken(_token);
    } else {
      throw ApiException(data['non_field_errors']?[0] ??
          data['detail'] ??
          'Login gagal (${response.statusCode})');
    }
  }

  Future<void> logout() async {
    _token = null;
    await saveToken(null);
  }

  Future<List<dynamic>> getList(String path) async {
    final data = await _authenticatedGet(path);
    if (data is Map && data.containsKey('results')) {
      return data['results'] as List<dynamic>;
    }
    if (data is List) return data;
    return const [];
  }

  Future<List<dynamic>> getNotifikasi() => getList('notifikasi/');

  Future<dynamic> _authenticatedGet(String path) async {
    _token ??= await _storedToken;
    final response = await http.get(
      ApiConfig.uri(path),
      headers: {'Authorization': 'Token $_token'},
    );
    return _decode(response);
  }

  Future<void> markBaca(int id) async {
    _token ??= await _storedToken;
    final response = await http.patch(
      ApiConfig.uri('notifikasi/$id/baca/'),
      headers: {
        'Authorization': 'Token $_token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'dibaca': true}),
    );
    if (response.statusCode != 200) {
      throw ApiException('Gagal menandai dibaca (${response.statusCode})');
    }
  }

  dynamic _decode(http.Response response) {
    if (response.body.isEmpty) return <String, dynamic>{};
    try {
      return jsonDecode(utf8.decode(response.bodyBytes));
    } catch (_) {
      throw ApiException('Respons tidak valid (${response.statusCode})');
    }
  }
}