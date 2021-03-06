# Generated by Django 3.1.7 on 2021-05-10 19:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20210507_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_initialized', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('completed', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='date_initialized',
        ),
        migrations.RemoveField(
            model_name='order',
            name='date_ordered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='order',
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='district',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='full_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.cart'),
        ),
    ]
