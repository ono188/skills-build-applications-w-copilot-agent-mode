from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(email='thundergod@mhigh.edu', name='Thor', age=30),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', age=35),
            User(email='zerocool@mhigh.edu', name='Steve Rogers', age=32),
            User(email='crashoverride@mhigh.edu', name='Natasha Romanoff', age=28),
            User(email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40),
        ]
        for user in users:
            user.save()

        # Create teams
        teams = [
            Team(name='Blue Team', members=[user.email for user in users[:3]]),
            Team(name='Gold Team', members=[user.email for user in users[3:]]),
        ]
        Team.objects.bulk_create(teams)

        # Create activities
        activities = [
            Activity(user=users[0], type='Cycling', duration=60, date='2025-04-12'),
            Activity(user=users[1], type='Crossfit', duration=120, date='2025-04-11'),
            Activity(user=users[2], type='Running', duration=90, date='2025-04-10'),
            Activity(user=users[3], type='Strength', duration=30, date='2025-04-09'),
            Activity(user=users[4], type='Swimming', duration=75, date='2025-04-08'),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard = [
            Leaderboard(user=users[0], points=100),
            Leaderboard(user=users[1], points=90),
            Leaderboard(user=users[2], points=95),
            Leaderboard(user=users[3], points=85),
            Leaderboard(user=users[4], points=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))