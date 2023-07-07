class UserMixin:
    @property
    def is_annotator(self):
        return False

    def has_permission(self, user):
        return user.active_organization in self.organizations.all()
