
class User(object):
    def __init__(self, id, username):
        """
        :type username: basestring
        """
        self.id = id
        self.username = username

    def __str__(self):
        return "User(id='%s')" % self.id