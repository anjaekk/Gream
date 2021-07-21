# Generated by Django 3.2.5 on 2021-07-20 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_seller', models.BooleanField()),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=18)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
            options={
                'db_table': 'biddings',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buying_bid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buying_bid', to='orders.bidding', unique=True)),
                ('selling_bid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='selling_bid', to='orders.bidding', unique=True)),
            ],
            options={
                'db_table': 'contracts',
            },
        ),
        migrations.AddField(
            model_name='bidding',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.status'),
        ),
        migrations.AddField(
            model_name='bidding',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user'),
        ),
    ]