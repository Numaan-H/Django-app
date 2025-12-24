# itreporting/migrations/0004_remove_user_add_profile.py
from django.db import migrations, models, connection

def remove_user_field_if_exists(apps, schema_editor):
    """
    Safely drop 'user' column if it exists.
    """
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM itreporting_student LIKE 'user';")
        if cursor.fetchone():
            cursor.execute("ALTER TABLE itreporting_student DROP COLUMN user;")

class Migration(migrations.Migration):

    dependencies = [
        ('itreporting', '0003_course_student_module'),
        ('users', '0001_initial'),
    ]

    operations = [
        # Safely remove old user field
        migrations.RunPython(remove_user_field_if_exists),
        # Add profile field (nullable for backfill)
        migrations.AddField(
            model_name='student',
            name='profile',
            field=models.OneToOneField(
                to='users.Profile',
                null=True,
                on_delete=models.CASCADE,
                related_name='student',
            ),
        ),
        # Module adjustments
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='credit',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='module',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='modules', to='itreporting.student'),
        ),
    ]
