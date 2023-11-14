# Generated by Django 4.2.5 on 2023-10-05 03:55

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': '2. Attributes',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('color_code', models.CharField(blank=True, max_length=255, null=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.attribute')),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': '3. Attribute Values',
            },
        ),
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='brand_images')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='ecommerce.categories')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': '1. Categories',
            },
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='default_logo.png', null=True, upload_to='logo_images')),
                ('alt_text', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Logo',
                'verbose_name_plural': '1. Logo',
            },
        ),
        migrations.CreateModel(
            name='MainBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('content_id', models.UUIDField(default=uuid.uuid4)),
                ('text1', models.TextField(blank=True, null=True)),
                ('text2', models.TextField(blank=True, null=True)),
                ('text3', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='main_banners/')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'MainBanner',
                'verbose_name_plural': '1. MainBanners',
            },
        ),
        migrations.CreateModel(
            name='MiniBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('content_id', models.UUIDField(default=uuid.uuid4)),
                ('text1', models.TextField(blank=True, null=True)),
                ('text2', models.TextField(blank=True, null=True)),
                ('text3', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='main_banners/')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'MiniBanner',
                'verbose_name_plural': '1. MiniBanners',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('short_description', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('in_stock', models.BooleanField(default=True)),
                ('featured', models.BooleanField(blank=True, default=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('attributes', models.ManyToManyField(through='ecommerce.ProductAttribute', to='ecommerce.attribute')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecommerce.brands')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.categories')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': '4. Products',
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Sku', models.CharField(blank=True, default=uuid.uuid4, max_length=255, unique=True)),
                ('stock', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='variation_Images/')),
            ],
            options={
                'verbose_name': 'Variation',
                'verbose_name_plural': '5. Product Variations',
            },
        ),
        migrations.CreateModel(
            name='VariationAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.attribute')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.attributevalue')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.variation')),
            ],
        ),
        migrations.AddField(
            model_name='variation',
            name='attributes',
            field=models.ManyToManyField(through='ecommerce.VariationAttribute', to='ecommerce.attribute'),
        ),
        migrations.AddField(
            model_name='variation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.products'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.products'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.attributevalue'),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='default.jpg', upload_to='prod_images')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ecommerce.products')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
    ]