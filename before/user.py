class User:

    def is_authenticated(self):

        # Return True if the user is authenticated, i.e. they have provided valid credentials.

        return True

    def is_active(self):

        # Return True if the user is activate, i.e. in addition to being authenticated, they have activated their
        # account, and not been suspended

        return True

    def is_anonymous(self):

        # Return True if this is an anonymous user

        return False

    def get_id(self):

        # Return a unicode that uniquely identifies the user. Used to load from the user_loader callback.

        return u"1"

