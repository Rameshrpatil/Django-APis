# Generated by Django 5.0.5 on 2024-05-13 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_adminuser_foriegn_id_adminuser_is_admin_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminuser',
            old_name='Is_FundManager',
            new_name='Is_FM',
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='Associated_company',
            field=models.CharField(choices=[('grow', 'grow'), ('upstocks', 'upstocks'), ('zerodha', 'zerodha')]),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='Location',
            field=models.CharField(choices=[('HYD', 'Hyderabad'), ('BAN', 'Bangalore'), ('DEL', 'Delhi'), ('PUN', 'Pune'), ('MUM', 'Mumbai'), ('NYC', 'NEW_YORK')]),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='Role',
            field=models.CharField(choices=[('CUST', 'Customer'), ('Admin', 'Admin'), ('FM', 'FundManager')]),
        ),
        migrations.AlterField(
            model_name='holdings',
            name='stock_name',
            field=models.CharField(choices=[('GOOGL', 'Google'), ('TES', 'TESLA'), ('AAPL', 'Apple'), ('TATH', 'TATA_Tech'), ('AMZ', 'AMAZON'), ('MSFT', 'Microsoft')], max_length=50),
        ),
    ]
