# Generated by Django 3.2.5 on 2021-07-20 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210720_0725'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiredWithin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.IntegerField()),
            ],
            options={
                'db_table': 'expired_within',
            },
        ),
        migrations.AddField(
            model_name='bidding',
            name='expired_within',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.expiredwithin'),
        ),
    ]