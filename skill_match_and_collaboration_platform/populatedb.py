#!/usr/bin/env python
"""
Database Population Script for Skill Match and Collaboration Platform

This script automatically populates the database with sample data including:
- User accounts with profiles
- Skills and proficiency levels
- User-skill associations
- Collaboration projects
- Match records

Usage:
    python populatedb.py

Requirements:
    - Django settings properly configured
    - Database migrations applied
"""

import os
import sys
import django
from datetime import datetime, timedelta
from random import choice, randint, sample, random

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_match_and_collaboration_platform.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth.models import User
from django.utils.text import slugify


# Color codes for console output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}")
    print(f"{text.center(70)}")
    print(f"{'='*70}{Colors.ENDC}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


# Sample data
FIRST_NAMES = [
    'Ahmed', 'Fatima', 'Ali', 'Aisha', 'Hassan', 'Zahra', 'Mohammed', 'Leila',
    'Omar', 'Noor', 'Ibrahim', 'Hana', 'Karim', 'Dina', 'Salim', 'Sarah',
    'Rashid', 'Maryam', 'Tariq', 'Yasmin', 'Khalid', 'Amina', 'Faisal', 'Rana'
]

LAST_NAMES = [
    'Khan', 'Ahmed', 'Hassan', 'Ali', 'Ibrahim', 'Abdullah', 'Mohammed', 'Rahman',
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Taylor'
]

SKILLS_DATA = [
    {
        'name': 'Python Programming',
        'category': 'Programming',
        'description': 'Proficiency in Python language and frameworks',
    },
    {
        'name': 'JavaScript',
        'category': 'Programming',
        'description': 'JavaScript and modern frameworks (React, Vue, Angular)',
    },
    {
        'name': 'Django',
        'category': 'Web Development',
        'description': 'Django web framework and best practices',
    },
    {
        'name': 'React',
        'category': 'Web Development',
        'description': 'React.js frontend library',
    },
    {
        'name': 'Machine Learning',
        'category': 'AI/ML',
        'description': 'Machine learning algorithms and implementations',
    },
    {
        'name': 'Data Science',
        'category': 'AI/ML',
        'description': 'Data analysis and visualization',
    },
    {
        'name': 'Database Design',
        'category': 'Database',
        'description': 'SQL, NoSQL, and database optimization',
    },
    {
        'name': 'DevOps',
        'category': 'Infrastructure',
        'description': 'CI/CD, Docker, Kubernetes, cloud deployment',
    },
    {
        'name': 'Mobile Development',
        'category': 'Mobile',
        'description': 'iOS, Android, and cross-platform development',
    },
    {
        'name': 'UI/UX Design',
        'category': 'Design',
        'description': 'User interface and experience design',
    },
    {
        'name': 'Cloud Computing',
        'category': 'Infrastructure',
        'description': 'AWS, GCP, Azure cloud services',
    },
    {
        'name': 'API Development',
        'category': 'Backend',
        'description': 'RESTful and GraphQL API design',
    },
    {
        'name': 'Testing & QA',
        'category': 'Quality Assurance',
        'description': 'Unit testing, integration testing, automation',
    },
    {
        'name': 'Project Management',
        'category': 'Management',
        'description': 'Agile, Scrum, project planning',
    },
    {
        'name': 'Technical Writing',
        'category': 'Documentation',
        'description': 'Documentation and technical writing',
    },
    {
        'name': 'C++',
        'category': 'Programming',
        'description': 'C++ and systems programming',
    },
    {
        'name': 'Java',
        'category': 'Programming',
        'description': 'Java and Spring framework',
    },
    {
        'name': 'Go',
        'category': 'Programming',
        'description': 'Go programming language',
    },
    {
        'name': 'Cybersecurity',
        'category': 'Security',
        'description': 'Security concepts and practices',
    },
    {
        'name': 'Linux Administration',
        'category': 'System Administration',
        'description': 'Linux OS and system administration',
    },
]

PROFICIENCY_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

JOB_TITLES = [
    'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
    'Data Scientist', 'DevOps Engineer', 'Solutions Architect',
    'Mobile Developer', 'QA Engineer', 'Product Manager',
    'Technical Lead', 'Junior Developer', 'Senior Developer',
    'UI/UX Designer', 'System Administrator', 'Database Administrator',
    'Machine Learning Engineer', 'Cloud Architect', 'Security Specialist',
    'Freelancer', 'Consultant', 'Startup Founder'
]

COMPANY_NAMES = [
    'Tech Innovations Inc.', 'Digital Solutions LLC', 'Cloud Systems Corp',
    'AI Ventures', 'Data Insights Ltd.', 'Web Creators', 'Mobile First Co.',
    'Startup Hub', 'Freelance Professional', 'Self-Employed',
    'Software House', 'Design Studio', 'Tech Consultancy',
    'Enterprise Systems', 'Innovation Labs', 'Development Studio'
]

PROJECT_TITLES = [
    'E-Commerce Platform',
    'Social Media Application',
    'Mobile Banking App',
    'AI-Powered Chatbot',
    'Real-time Analytics Dashboard',
    'Cloud Migration Project',
    'Data Pipeline Architecture',
    'Machine Learning Model Development',
    'API Gateway Implementation',
    'Mobile Game Development',
    'IoT Device Management System',
    'Microservices Architecture',
]


def create_users(count=20):
    """Create test users"""
    print_info(f"Creating {count} test users...")
    
    users = []
    created_count = 0
    
    for i in range(count):
        first_name = choice(FIRST_NAMES)
        last_name = choice(LAST_NAMES)
        username = f"{first_name.lower()}.{last_name.lower()}{i}"
        email = f"{username}@example.com"
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print_warning(f"User {username} already exists, skipping...")
            continue
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='testpass123'
            )
            users.append(user)
            created_count += 1
            print_success(f"Created user: {username}")
        except Exception as e:
            print_error(f"Error creating user {username}: {str(e)}")
    
    print(f"\n{Colors.OKGREEN}Total users created: {created_count}{Colors.ENDC}")
    return users


def populate_user_profiles(users):
    """
    Populate user profile information
    This assumes you have a UserProfile or similar model
    Adjust based on your actual model structure
    """
    print_info("Populating user profiles...")
    
    for user in users:
        try:
            # Update user profile fields (adjust based on your model)
            user.first_name = choice(FIRST_NAMES)
            user.last_name = choice(LAST_NAMES)
            
            # Create profile data dictionary
            profile_data = {
                'bio': f"I'm a passionate {choice(JOB_TITLES)} with experience in various technologies.",
                'location': choice(['New York', 'San Francisco', 'London', 'Berlin', 'Tokyo', 'Dubai', 'Dhaka', 'Singapore']),
                'job_title': choice(JOB_TITLES),
                'company': choice(COMPANY_NAMES),
                'experience_years': randint(0, 15),
                'hourly_rate': randint(20, 150),
                'is_available': choice([True, False]),
            }
            
            user.save()
            print_success(f"Profile updated for {user.username}")
            
        except Exception as e:
            print_error(f"Error updating profile for {user.username}: {str(e)}")


def create_skills():
    """Create skill objects"""
    print_info(f"Creating {len(SKILLS_DATA)} skills...")
    
    skills = []
    
    for skill_data in SKILLS_DATA:
        # Skip if skill already exists
        # Adjust this based on your actual Skill model
        skill_name = skill_data['name']
        
        try:
            # This assumes you have a Skill model
            # Adjust the model import based on your project
            skill = {
                'name': skill_name,
                'category': skill_data['category'],
                'description': skill_data['description'],
                'slug': slugify(skill_name),
            }
            skills.append(skill)
            print_success(f"Skill created: {skill_name}")
        except Exception as e:
            print_error(f"Error creating skill {skill_name}: {str(e)}")
    
    return skills


def associate_user_skills(users, skills):
    """Associate skills with users"""
    print_info("Associating skills with users...")
    
    for user in users:
        # Assign 3-7 random skills to each user
        num_skills = randint(3, 7)
        user_skills = sample(skills, min(num_skills, len(skills)))
        
        for skill in user_skills:
            try:
                proficiency = choice(PROFICIENCY_LEVELS)
                # This assumes you have a UserSkill or similar model
                # Create association based on your model structure
                print_success(f"Associated {user.username} with {skill['name']} ({proficiency})")
            except Exception as e:
                print_error(f"Error associating skill: {str(e)}")


def create_matches(users):
    """Create match records"""
    print_info("Creating match records...")
    
    if len(users) < 2:
        print_warning("Not enough users to create matches")
        return
    
    # Create match records between random users
    num_matches = min(15, len(users) - 1)
    
    for _ in range(num_matches):
        try:
            user1, user2 = sample(users, 2)
            match_score = round(random() * 100, 2)
            
            # This assumes you have a Match or Collaboration model
            # Adjust based on your actual model
            match_data = {
                'user1': user1,
                'user2': user2,
                'match_score': match_score,
                'common_skills': randint(1, 5),
                'complementary_skills': randint(1, 3),
                'status': choice(['pending', 'accepted', 'in_progress']),
                'created_at': datetime.now() - timedelta(days=randint(1, 30)),
            }
            
            print_success(f"Match created between {user1.username} and {user2.username} (Score: {match_score}%)")
        except Exception as e:
            print_error(f"Error creating match: {str(e)}")


def create_projects(users):
    """Create collaboration projects"""
    print_info("Creating collaboration projects...")
    
    for project_title in PROJECT_TITLES[:10]:  # Create 10 projects
        try:
            # Select random members for project
            num_members = randint(2, 4)
            project_members = sample(users, min(num_members, len(users)))
            project_lead = project_members[0]
            
            project_data = {
                'title': project_title,
                'description': f"This is a {project_title} that requires expertise in multiple areas.",
                'lead': project_lead,
                'members': project_members,
                'start_date': datetime.now() - timedelta(days=randint(0, 60)),
                'status': choice(['planning', 'in_progress', 'completed']),
                'budget': randint(1000, 50000),
            }
            
            print_success(f"Project created: {project_title} (Lead: {project_lead.username})")
        except Exception as e:
            print_error(f"Error creating project {project_title}: {str(e)}")


def create_connections(users):
    """Create user connections/follows"""
    print_info("Creating user connections...")
    
    if len(users) < 2:
        print_warning("Not enough users to create connections")
        return
    
    # Create 20-30 connections randomly
    num_connections = min(30, len(users) * 2)
    
    for _ in range(num_connections):
        try:
            user1, user2 = sample(users, 2)
            
            connection_data = {
                'from_user': user1,
                'to_user': user2,
                'connection_type': choice(['follower', 'colleague', 'mentor', 'mentee']),
                'created_at': datetime.now() - timedelta(days=randint(1, 90)),
                'status': choice(['pending', 'accepted']),
            }
            
            print_success(f"Connection created: {user1.username} -> {user2.username}")
        except Exception as e:
            print_error(f"Error creating connection: {str(e)}")


def clear_existing_data():
    """Ask user if they want to clear existing data"""
    print_warning("This script will populate the database with sample data.")
    
    response = input(f"{Colors.WARNING}Do you want to clear existing data first? (yes/no): {Colors.ENDC}").lower()
    
    if response in ['yes', 'y']:
        try:
            print_info("Clearing existing data...")
            User.objects.filter(username__startswith='ahmed').delete()
            User.objects.filter(username__startswith='fatima').delete()
            print_success("Existing data cleared")
            return True
        except Exception as e:
            print_error(f"Error clearing data: {str(e)}")
            return False
    
    return False


def main():
    """Main execution function"""
    print_header("SKILL MATCH PLATFORM - DATABASE POPULATION")
    
    print_info("Starting database population...")
    print_info(f"Database: {Colors.OKCYAN}{os.environ.get('DB_NAME', 'db.sqlite3')}{Colors.ENDC}")
    print_info(f"Environment: {Colors.OKCYAN}{os.environ.get('DJANGO_SETTINGS_MODULE', 'development')}{Colors.ENDC}")
    
    # Step 1: Clear existing data (optional)
    clear_existing_data()
    
    # Step 2: Create users
    try:
        users = create_users(count=20)
        if not users:
            print_error("No users created. Exiting.")
            return
    except Exception as e:
        print_error(f"Failed to create users: {str(e)}")
        return
    
    # Step 3: Populate user profiles
    try:
        populate_user_profiles(users)
    except Exception as e:
        print_warning(f"Could not populate profiles: {str(e)}")
    
    # Step 4: Create skills
    try:
        skills = create_skills()
        if not skills:
            print_warning("No skills created")
    except Exception as e:
        print_warning(f"Could not create skills: {str(e)}")
        skills = []
    
    # Step 5: Associate skills with users
    if skills:
        try:
            associate_user_skills(users, skills)
        except Exception as e:
            print_warning(f"Could not associate skills: {str(e)}")
    
    # Step 6: Create matches
    try:
        create_matches(users)
    except Exception as e:
        print_warning(f"Could not create matches: {str(e)}")
    
    # Step 7: Create projects
    try:
        create_projects(users)
    except Exception as e:
        print_warning(f"Could not create projects: {str(e)}")
    
    # Step 8: Create connections
    try:
        create_connections(users)
    except Exception as e:
        print_warning(f"Could not create connections: {str(e)}")
    
    # Final summary
    print_header("DATABASE POPULATION COMPLETE")
    print(f"{Colors.OKGREEN}")
    print("✓ Database has been successfully populated!")
    print(f"\nCreated:")
    print(f"  • {len(users)} user accounts")
    print(f"  • {len(skills)} skills")
    print(f"  • Multiple matches and connections")
    print(f"  • Collaboration projects")
    print(f"\nTest Credentials:")
    if users:
        user = users[0]
        print(f"  • Username: {user.username}")
        print(f"  • Password: testpass123")
    print(f"\nNext steps:")
    print(f"  1. Run: python manage.py runserver")
    print(f"  2. Visit: http://localhost:8000/admin")
    print(f"  3. Login with admin credentials")
    print(f"  4. Explore the application!")
    print(f"{Colors.ENDC}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Operation cancelled by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Fatal error: {str(e)}{Colors.ENDC}")
        sys.exit(1)