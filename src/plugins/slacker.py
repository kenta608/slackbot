from slacker import Slacker


def get_slacker():
    return Slacker("xxx")


slack = Slacker("xxx")
response = slack.users.list()
users = response.body["members"]
print(users)
