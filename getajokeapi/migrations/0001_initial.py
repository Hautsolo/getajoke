# Generated by Django 4.1.3 on 2024-08-20 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Joke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('uid', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getajokeapi.joke')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getajokeapi.tag')),
            ],
        ),
        migrations.AddField(
            model_name='joke',
            name='tags',
            field=models.ManyToManyField(related_name='posts', through='getajokeapi.PostTag', to='getajokeapi.tag'),
        ),
        migrations.AddField(
            model_name='joke',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='upvoted_jokes', to='getajokeapi.user'),
        ),
        migrations.AddField(
            model_name='joke',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getajokeapi.user'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('joke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='getajokeapi.joke')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getajokeapi.user')),
            ],
        ),
    ]
