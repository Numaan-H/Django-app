# itreporting/migrations/0005_backfill_student_profiles.py
from django.db import migrations, models

def backfill_student_profiles(apps, schema_editor):
    Student = apps.get_model('itreporting', 'Student')
    Profile = apps.get_model('users', 'Profile')

    for profile in Profile.objects.all():
        Student.objects.get_or_create(profile=profile)

class Migration(migrations.Migration):

    dependencies = [
        ('itreporting', '0004_remove_user_add_profile'),
        ('users', '0001_initial'),
    ]

    operations = [
        # Backfill profile for existing students
        migrations.RunPython(backfill_student_profiles),
        # Make profile non-nullable after backfill
        migrations.AlterField(
            model_name='student',
            name='profile',
            field=models.OneToOneField(
                to='users.Profile',
                null=False,
                on_delete=models.CASCADE,
                related_name='student',
            ),
        ),
    ]
