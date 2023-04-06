import string
import time
import random
from django.core.mail import send_mail
import datetime
from django.shortcuts import redirect
import os
from datetime import datetime
from django.utils import timezone


def set_false_after_first_false(data):
    first_false = False
    for key in data:
        if data[key] == False:
            first_false = True
        if first_false:
            data[key] = False
    return data


def find_latest_file(image_files):
    image_files = {file_name: datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S') for file_name, timestamp_str in image_files.items()}
    latest_time = max(image_files.values())

    for file_name, timestamp in image_files.items():
        if timestamp == latest_time:
            return file_name

    return None


def send_signup_email(recipient):
    subject = 'CCH23: Hackathon Registeration Signup'
    message = 'Welcome to CCH 2023 Hackathon Competition. Please follow the link to complete the registeration for your team.'
    recipient_list = [recipient]
    send_mail(subject, message, from_email=None, recipient_list=recipient_list, fail_silently=False)

def post_announcement(request,topic,msg, to):
    announcement = Announcement(
                title=topic,
                content=msg,
                created_by=request.user,
                audience=to
            )
    announcement.created_at = timezone.now()
    return announcement.save()
def generate_unique_strings():
    num_strings = 3
    string_length = 9
    chars = string.ascii_lowercase + string.digits
    strings = set()

    # Generate strings until we have enough unique ones
    while len(strings) < num_strings:
        # Use current time as seed for random number generator
        seed = int(time.time() * 1000)
        random.seed(seed)

        # Generate random string of given length
        random_string = ''.join(random.choices(chars, k=string_length)).upper()

        # Add string to set of unique strings
        strings.add(random_string)

    return list(strings)

def getmailinglist(group_name):
    if not group_name:        
        # Return all emails
        members = Members.objects.all()
        mailing_list = [member.email for member in members if validate_email(member.email)]
    else:
        mailing_list = [group_name]
    return mailing_list

def list_files(root_dir):
    # Initialize empty dictionary to store all file names and their last modified time stamps
    all_files = {}

    # Walk through all subdirectories of the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check each file in the current directory
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Check if the file is an image file or a zip file
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.zip')):
                # Add the file name and last modified time stamp to the dictionary
                all_files[filename] = str(datetime.fromtimestamp(os.path.getmtime(file_path))).split('.')[0]

    # Print and return the dictionary of all file names and their last modified time stamps
    # print(all_files)
    return all_files




def has_team(function):
    def wrap(request, *args, **kwargs):
        if not request.session.get('has_team', False):
            return redirect('registeration2')
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
