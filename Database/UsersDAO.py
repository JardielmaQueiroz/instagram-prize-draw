from .GenericDAO import GenericDAO
from .Models import User


class UsersDAO(GenericDAO):
    def __init__(self):
        super(UsersDAO, self).__init__()

    def select_by_pk(self, pk):
        result = self.session.query(User).filter(User.pk == pk,
                                                 User.delete == '').all()
        self.session.close()
        return result
