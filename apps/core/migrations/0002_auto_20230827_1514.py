# Generated by Django 4.2.3 on 2023-08-10 10:01

from django.db import migrations


def run_sql(apps, schema_editor):
    # Read the SQL file
    with open('viloyat.sql','r', encoding="utf8") as sql_file:
        sql = sql_file.read()

    # Execute the SQL statements
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql)

        
class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(run_sql),
    ]