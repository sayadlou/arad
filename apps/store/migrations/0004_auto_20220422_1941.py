# Generated by Django 3.2.12 on 2022-04-22 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220422_1213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'verbose_name': 'Event ', 'verbose_name_plural': 'Event Categories'},
        ),
        migrations.AlterModelOptions(
            name='learningcategory',
            options={'verbose_name': 'Learning Category', 'verbose_name_plural': 'Learning Categories'},
        ),
        migrations.AlterModelOptions(
            name='learningpost',
            options={'verbose_name': 'Learning Post', 'verbose_name_plural': 'Learning Posts'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('id',), 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('created_at',), 'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
        migrations.AlterModelOptions(
            name='productbasemodel',
            options={'verbose_name': 'Product Base Model', 'verbose_name_plural': 'Product Base Models'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('pub_date',), 'verbose_name': 'Service', 'verbose_name_plural': 'Services'},
        ),
    ]