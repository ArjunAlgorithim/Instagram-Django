# Generated by Django 5.0 on 2024-01-04 13:31

import django.db.models.deletion
import userauths.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('bio', models.TextField(blank=True, max_length=150, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='default-user.png', null=True, upload_to=userauths.models.user_directory_path, verbose_name='Picture')),
                ('favourite', models.ManyToManyField(to='post.post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
