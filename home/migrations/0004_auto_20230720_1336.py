# Generated by Django 3.2.16 on 2023-07-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20230720_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.CharField(blank=True, choices=[('Accessories', 'Accessories'), ('IT Equipment', 'IT Equipment'), ('Electronics', 'Electronics')], max_length=100, null=True),
        ),
    ]