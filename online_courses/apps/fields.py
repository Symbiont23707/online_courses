from rest_framework.fields import CurrentUserDefault


class CurrentStudentDefault(CurrentUserDefault):
    def __call__(self, serializer_field):
        return super().__call__(serializer_field).student
