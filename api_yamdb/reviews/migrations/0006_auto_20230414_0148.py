# Generated by Django 3.2 on 2023-04-13 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230413_0122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': 'comments', 'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': 'reviews', 'ordering': ('-pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='жанр'),
        ),
        migrations.AlterUniqueTogether(
            name='title',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.UniqueConstraint(fields=('name', 'year'), name='unique_name_year_title'),
        ),
    ]
