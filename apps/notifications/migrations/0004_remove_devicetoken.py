from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notifikasi_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeviceToken',
        ),
    ]
