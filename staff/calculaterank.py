from profiles.models import UserProfile


def calculaterank():
    for i in UserProfile.objects.all():
        i.calculate_rank()
