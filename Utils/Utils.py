from Database.FollowersDAO import FollowersDAO
from Database.FollowingsDAO import FollowingsDAO
from Database.GenericDAO import GenericDAO as UserDAO
from Database.Models import Follower, Following, User


def get_user(user_name):
    result = UserDAO().select_by_username(User, user_name.lower())
    return result[0]


def exist_user(username):
    result = UserDAO().select_by_username(User, username.lower())
    if len(result) == 1:
        return True
    else:
        return False


def format_comments(data, number_of_comments):
    num_ant = number_of_comments
    lst_format = []
    i = 0
    while i < (len(data) // number_of_comments):
        if i == 0:
            lst_format.append(data[:number_of_comments])
        else:
            lst_format.append(data[num_ant:num_ant + number_of_comments])
            num_ant = num_ant + number_of_comments
        i += 1

    return lst_format


def create_list_comment(number_of_comments, option, user_id):
    lst_of_comment = []
    lst_of_username = []
    if option == 1:
        result = FollowingsDAO().select_filter_comment(Following, user_id)
    else:
        result = FollowersDAO().select_filter_comment(Follower, user_id)

    for user_orm in result:
        lst_of_username.append(user_orm.username)

    lst_format = format_comments(lst_of_username, number_of_comments)

    for lst_of_username in lst_format:
        comment = ""
        for username in lst_of_username:
            comment += "@"+username + " "
        lst_of_comment.append(comment)

    return lst_of_comment


def load_file(path):
    lst_date = []
    try:
        arq = open(path, 'rt')
        content = arq.readline().strip("\n")
        lst_date = [content.strip("\n")]

        while content != "":
            content = arq.readline()
            if content != '':
                lst_date.append(content.strip("\n"))
        arq.close()
    except IOError:
        pass

    return lst_date


def save_comment_did(path, comment):
    arq = open(path, 'a')
    arq.write(comment + "\n")
    arq.close()
