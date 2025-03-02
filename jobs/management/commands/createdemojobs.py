from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Job

class Command(BaseCommand):
    help = 'Creates demo jobs for testing'

    def handle(self, *args, **kwargs):
        # Get or create a user to post the jobs
        user, _ = User.objects.get_or_create(username='demo_user', email='demo@example.com')
        if _:
            user.set_password('password123')
            user.save()

        # List of demo jobs
        demo_jobs = [
            {
                'title': 'Software Engineer',
                'description': 'Develop scalable web applications using Python and Django.',
                'location': 'New York, USA',
            },
            {
                'title': 'Frontend Developer',
                'description': 'Build responsive and interactive user interfaces using HTML, CSS, and JavaScript.',
                'location': 'San Francisco, USA',
            },
            {
                'title': 'Data Analyst',
                'description': 'Analyze large datasets and provide actionable insights.',
                'location': 'Chicago, USA',
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Manage CI/CD pipelines and cloud infrastructure.',
                'location': 'Austin, USA',
            },
            {
                'title': 'Product Manager',
                'description': 'Define product strategy and work with cross-functional teams.',
                'location': 'Seattle, USA',
            },
        ]

        # Create jobs
        for job_data in demo_jobs:
            Job.objects.create(
                title=job_data['title'],
                description=job_data['description'],
                location=job_data['location'],
                posted_by=user,
            )

        self.stdout.write(self.style.SUCCESS('Successfully created demo jobs!'))