# Generated by Django 3.2.4 on 2021-10-09 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eva', '0003_alter_parametrosgeneral_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='startDate',
            field=models.DateTimeField(db_column='fecha_inicio'),
        ),
    ]
