from slacker import Slacker


def get_slacker():
    return Slacker("xoxb-2293861735-1238450237589-5fHFpkRHGFtY8T5iX0OduJtr")


slack = Slacker("xoxb-2293861735-1238450237589-5fHFpkRHGFtY8T5iX0OduJtr")
response = slack.users.list()
users = response.body["members"]
print(users)
