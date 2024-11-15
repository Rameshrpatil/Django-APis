# Generated by Django 5.0.5 on 2024-05-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0009_alter_adminuser_associated_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='Associated_company',
            field=models.CharField(choices=[('grow', 'grow'), ('upstocks', 'upstocks'), ('zerodha', 'zerodha')]),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='Foriegn_id',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='Location',
            field=models.CharField(choices=[('HYD', 'Hyderabad'), ('BAN', 'Bangalore'), ('MUM', 'Mumbai'), ('PUN', 'Pune'), ('DEL', 'Delhi'), ('NYC', 'NEW_YORK')]),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='Role',
            field=models.CharField(choices=[('FM', 'FundManager'), ('CUST', 'Customer'), ('Admin', 'Admin')]),
        ),
        migrations.AlterField(
            model_name='holdings',
            name='stock_name',
            field=models.CharField(choices=[('TATH', 'TATA_Tech'), ('AMZ', 'AMAZON'), ('MSFT', 'Microsoft'), ('GOOGL', 'Google'), ('AAPL', 'Apple'), ('TES', 'TESLA')], max_length=50),
        ),
    ]
