# Generated by Django 3.2.2 on 2021-05-12 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_phone', models.CharField(max_length=200, null=True)),
                ('to_phone', models.CharField(max_length=200, null=True)),
                ('money_amt', models.FloatField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='money',
            field=models.FloatField(null=True),
        ),
    ]
