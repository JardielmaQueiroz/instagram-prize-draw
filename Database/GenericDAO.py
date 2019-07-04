from .MyDatabase import MyDatabase


class GenericDAO:
    def __init__(self):
        self.session = MyDatabase().getSession()

    def insert_or_update_all(self, date):
        self.session.add_all(date)
        self.session.commit()
        self.session.close()

    def insert_or_update(self, date):
        self.session.add(date)
        self.session.commit()
        self.session.close()

    def get_all(self, table):
        result = self.session.query(table).all()
        self.session.close()
        return result

    def select_by_pk(self, table, pk, user_id):
        result = self.session.query(table).filter(table.pk == pk,
                                                  table.users_id == user_id,
                                                  table.delete == '').all()
        self.session.close()
        return result

    def select_by_username(self, table, user_name):
        result = self.session.query(table).filter(table.username == user_name,
                                                  table.delete == '').all()
        self.session.close()
        return result

    def select_filter_comment(self, table, user_id):
        result = self.session.query(table).filter(table.users_id == user_id,
                                                  table.delete == '',
                                                  table.following_count > 500,
                                                  table.following_count < 3000,
                                                  table.follower_count > 500,
                                                  table.follower_count < 4000).all()
        self.session.close()
        return result
