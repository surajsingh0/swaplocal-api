from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),  # Ensure this matches your existing migration
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='exchange',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='exchanges.Exchange'),
        ),
    ]
