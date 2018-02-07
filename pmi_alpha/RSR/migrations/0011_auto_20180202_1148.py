# Generated by Django 2.0.1 on 2018-02-02 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RSR', '0010_auto_20180129_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(default='None', max_length=70, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='TitleToCert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TitleToTrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TitleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RSR.Title')),
            ],
        ),
        migrations.AddField(
            model_name='certifications',
            name='Interest',
            field=models.CharField(choices=[('Interested', 'Interested'), ('In Progess', 'In Progess'), ('Completed', 'Completed')], default='Interested', max_length=50, verbose_name='Interest'),
        ),
        migrations.AddField(
            model_name='trainings',
            name='Interest',
            field=models.CharField(choices=[('Interested', 'Interested'), ('In Progess', 'In Progess'), ('Completed', 'Completed')], default='Interested', max_length=50, verbose_name='Interest'),
        ),
        migrations.AddField(
            model_name='titletotrain',
            name='TrainID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RSR.Trainings'),
        ),
        migrations.AddField(
            model_name='titletocert',
            name='CertID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RSR.Certifications'),
        ),
        migrations.AddField(
            model_name='titletocert',
            name='TitleID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RSR.Title'),
        ),
        migrations.AddField(
            model_name='person',
            name='Title',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='RSR.Title'),
            preserve_default=False,
        ),
    ]
