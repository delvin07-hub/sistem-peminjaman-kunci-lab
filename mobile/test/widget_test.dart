import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:kunci_lab_mobile/api/api_service.dart';
import 'package:kunci_lab_mobile/screens/login_screen.dart';

void main() {
  testWidgets('Login screen menampilkan judul dan field username/password',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: LoginScreen(onLogin: () {}),
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0D3B66)),
          useMaterial3: true,
        ),
      ),
    );

    expect(find.text('Kunci Lab'), findsOneWidget);
    expect(find.text('Login Penanggung Jawab'), findsOneWidget);
    expect(find.text('Username'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.text('MASUK'), findsOneWidget);
  });

  test('ApiConfig baseUrl default ke localhost', () {
    expect(ApiConfig.baseUrl, contains('localhost'));
  });
}