# Generated by Django 3.2.5 on 2021-07-20 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=256)),
                ('phone_number', models.CharField(max_length=45)),
                ('kakao_id', models.CharField(max_length=45, null=True)),
                ('card_company', models.CharField(max_length=45, null=True)),
                ('card_numnber', models.CharField(max_length=45, null=True)),
                ('address', models.CharField(max_length=128, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]