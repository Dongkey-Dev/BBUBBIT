# Generated by Django 3.1.3 on 2021-02-01 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GetStockMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockInfo', models.CharField(max_length=400)),
            ],
            options={
                'verbose_name': 'GetStockMsg',
                'verbose_name_plural': 'GetStockMsges',
            },
        ),
    ]
