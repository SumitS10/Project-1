# Generated migration to update models and add WebullTrade and TradeLog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        # Update FidelityTrade model
        migrations.AddField(
            model_name='fidelitytrade',
            name='trade_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fidelitytrade',
            name='strategy',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='fidelitytrade',
            name='action',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='fidelitytrade',
            name='strike',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fidelitytrade',
            name='expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fidelitytrade',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.RemoveField(
            model_name='fidelitytrade',
            name='option_type',
        ),
        migrations.RemoveField(
            model_name='fidelitytrade',
            name='pnl',
        ),
        
        # Update TradierTrade model
        migrations.AddField(
            model_name='tradiertrade',
            name='trade_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tradiertrade',
            name='strategy',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='tradiertrade',
            name='action',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='tradiertrade',
            name='strike',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tradiertrade',
            name='expiry',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tradiertrade',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.RemoveField(
            model_name='tradiertrade',
            name='option_type',
        ),
        migrations.RemoveField(
            model_name='tradiertrade',
            name='pnl',
        ),
        
        # Create WebullTrade model
        migrations.CreateModel(
            name='WebullTrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_id', models.CharField(blank=True, max_length=100, null=True)),
                ('trade_date', models.DateField()),
                ('symbol', models.CharField(max_length=20)),
                ('strategy', models.CharField(blank=True, max_length=50)),
                ('strike', models.FloatField(blank=True, null=True)),
                ('action', models.CharField(blank=True, max_length=10)),
                ('quantity', models.FloatField()),
                ('premium', models.FloatField()),
                ('expiry', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-trade_date', 'symbol'],
            },
        ),
        
        # Create TradeLog model
        migrations.CreateModel(
            name='TradeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_id', models.CharField(max_length=200, unique=True)),
                ('source', models.CharField(max_length=20)),
                ('trade_date', models.DateField()),
                ('close_date', models.DateField(blank=True, null=True)),
                ('symbol', models.CharField(max_length=20)),
                ('strategy', models.CharField(blank=True, max_length=50)),
                ('expiration', models.DateField(blank=True, null=True)),
                ('strikes', models.CharField(blank=True, max_length=200)),
                ('net_premium', models.FloatField(default=0)),
                ('total_cost', models.FloatField(default=0)),
                ('pl', models.FloatField(default=0)),
                ('pl_percent', models.FloatField(default=0)),
                ('status', models.CharField(default='Open', max_length=10)),
                ('win_loss', models.CharField(blank=True, max_length=20)),
                ('dte', models.IntegerField(blank=True, null=True)),
                ('legs', models.IntegerField(default=0)),
                ('closed_legs', models.IntegerField(default=0)),
                ('open_net', models.FloatField(default=0)),
                ('close_net', models.FloatField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-trade_date', 'symbol'],
            },
        ),
    ]

