from .GenericDAO import GenericDAO
from .Models import Following


class FollowingsDAO(GenericDAO):
    def __init__(self):
        super(FollowingsDAO, self).__init__()

    def select_by_userid(self, user_id):
        result = self.session.query(Following).filter(Following.users_id == user_id,
                                                      Following.delete == '').all()
        self.session.close()
        return result
