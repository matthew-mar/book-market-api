# Generated by Django 4.1.5 on 2023-01-05 12:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders_service', '0002_deliverymethod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(unique=True)),
                ('set_id', models.UUIDField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bookset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('set_id', models.UUIDField()),
                ('user_id', models.UUIDField()),
                ('book_id', models.UUIDField()),
            ],
            options={
                'unique_together': {('set_id', 'user_id', 'book_id')},
            },
        ),
    ]
