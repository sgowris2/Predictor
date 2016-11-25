from django.core.management.base import BaseCommand
from predictor.models import Match, Gameweek, User, UserProfile, Prediction
from django.utils import timezone
import datetime
import sendgrid
from sendgrid.helpers.mail import *


class Command(BaseCommand):

    help = 'Sends reminder emails for all users who have subscribed to them'

    def handle(self, *args, **options):
        # send_test_reminder(User.objects.get(email='sgowris2@gmail.com'))

        now = timezone.now()
        current_gameweek = Gameweek.objects.filter(start_time__lte=now, end_time__gte=now)[0]
        if now + datetime.timedelta(hours=20) >= current_gameweek.end_time:
            send_reminders()
        else:
            print(now, now + datetime.timedelta(hours=20), current_gameweek.end_time)


def send_test_reminder(user):

    sg = sendgrid.SendGridAPIClient(apikey='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')
    from_email = Email("sgowris2@gmail.com")
    subject = "[Testing Reminder Feature] Your predictions are due!"
    to_email = Email(user.email)
    content = Content("text/html",
                        "Hi " + user.first_name + "!<br/><br/>"
                            "This is to remind you that your predictions are due very soon at "
                            "<a href=\"predictr.pythonanywhere.com\">Predictr</a>!"
                            "<br/>If you would like to opt out of receiving these reminders in the future, "
                            "please change your "
                            "<a href=\"predictr.pythonanywhere.com/predictor/settings\">e-mail preferences</a>.")
    email = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=email.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


def send_reminder(user):

    try:
        sg = sendgrid.SendGridAPIClient(apikey='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')
        from_email = Email("sgowris2@gmail.com")
        subject = "Your predictions are due!"
        to_email = Email(user.email)
        content = Content("text/html",
                            "Hi " + user.first_name + "!<br/><br/>"
                            "This is to remind you that your predictions are due very soon at "
                            "<a href=\"predictr.pythonanywhere.com\">Predictr</a>!"
                            "<br/>If you would like to opt out of receiving these reminders in the future, "
                            "please change your "
                            "<a href=\"predictr.pythonanywhere.com/predictor/settings\">e-mail preferences</a>.")
        email = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=email.get())
        print("1 email sent")
    except:
        print("1 email not sent.")


def send_reminders():

    now = timezone.now()
    current_gameweek = Gameweek.objects.filter(start_time__lte=now, end_time__gte=now)[0]
    current_week_matches = Match.objects.filter(gameweek=current_gameweek)
    current_week_default_predictions = Prediction.objects.filter(is_default=True, match__in=current_week_matches)
    reminder_users = set(i.user for i in current_week_default_predictions)
    reminder_user_profiles = UserProfile.objects.filter(user__in=reminder_users, reminders=True)

    for user_profile in reminder_user_profiles:
        send_reminder(user_profile.user)
        # print(user_profile)
