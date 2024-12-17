import django33.contrib.sites.models
from django33.contrib.sites.models import _simple_domain_name_validator
from django33.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "domain",
                    models.CharField(
                        max_length=100,
                        verbose_name="domain name",
                        validators=[_simple_domain_name_validator],
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="display name")),
            ],
            options={
                "ordering": ["domain"],
                "db_table": "django_site",
                "verbose_name": "site",
                "verbose_name_plural": "sites",
            },
            bases=(models.Model,),
            managers=[
                ("objects", django33.contrib.sites.models.SiteManager()),
            ],
        ),
    ]
