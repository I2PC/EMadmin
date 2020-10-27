from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from getpass import getpass
from time import sleep
  
class Command(BaseCommand):
    help = "reset user password, provide email"

    def handle(self, *args, **options):
     try:
        userEmail = input("Please enter email: ")
        pswd = getpass()
        User = get_user_model()
        l = User.objects.get(email=userEmail) 
        l.set_password(pswd)
        l.save()
        print("changed password for user", userEmail)
     except:
        print("password change failed. In 5 seconds you will get a list of users")
        sleep(5)
        for u in User.objects.all():
            if u.is_superuser:
                print("---->",u.get_username())
            else:
                print(u.get_username())

        CommandError("password change failed")
 
