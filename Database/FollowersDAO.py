from .GenericDAO import GenericDAO
from .Models import Follower


class FollowersDAO(GenericDAO):
    def __init__(self):
        super(FollowersDAO, self).__init__()

    def select_by_userid(self, user_id):
        result = self.session.query(Follower).filter(Follower.users_id == user_id,
                                                     Follower.delete == '').all()

        self.session.close()
        return result
