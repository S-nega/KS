# Generated by Django 3.2.18 on 2023-04-15 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_alter_books_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
