# Generated by Django 2.2.5 on 2019-10-10 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0006_auto_20191009_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='shadow_hand_rank',
            field=models.BooleanField(default=False, null=True, verbose_name='Наличие звания Руки Тени'),
        ),
    ]
