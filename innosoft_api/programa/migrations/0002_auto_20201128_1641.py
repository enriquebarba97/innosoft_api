# Generated by Django 3.1.3 on 2020-11-28 16:41

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('programa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ponente',
            name='age',
        ),
        migrations.AddField(
            model_name='ponente',
            name='email',
            field=models.EmailField(default='patata', max_length=254),
        ),
        migrations.AddField(
            model_name='ponente',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
        migrations.AddField(
            model_name='ponente',
            name='surname',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.CreateModel(
            name='Ponencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.CharField(max_length=2000)),
                ('time', models.DateTimeField()),
                ('place', models.CharField(max_length=20)),
                ('ponente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programa.ponente')),
            ],
        ),
    ]