# Generated by Django 3.1.5 on 2021-01-19 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_URL',
            field=models.CharField(blank=True, default='https://redzonekickboxing.com/wp-content/uploads/2017/04/default-image-620x600.jpg', max_length=200),
        ),
    ]
