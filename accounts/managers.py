from django.db.models import Manager


class UserManager(Manager):
    def students(self):
        return self.filter(is_student=True)

    def teachers(self):
        return self.filter(is_student=False)
