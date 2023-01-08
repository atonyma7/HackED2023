# Generated by Django 4.1.5 on 2023-01-08 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('score', models.PositiveIntegerField(verbose_name='Score')),
                ('publication', models.CharField(max_length=250, verbose_name='Publication')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
                ('img_src', models.CharField(max_length=250, verbose_name='Img_src')),
            ],
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('name', 'publication'), name='unique'),
        ),
    ]
