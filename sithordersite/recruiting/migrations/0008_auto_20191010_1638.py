# Generated by Django 2.2.5 on 2019-10-10 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0007_auto_20191010_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='recruiting.Sith'),
        ),
    ]
