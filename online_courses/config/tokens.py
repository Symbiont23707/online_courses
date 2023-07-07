from rest_framework_simplejwt.tokens import Token


class CustomToken(Token):
    @classmethod
    def for_user(cls, user):
        token = cls()
        token['user_id'] = str(user.uuid)  # Replace 'uuid' with the actual UUID field name
        token['username'] = user.get_username()
        # Add any additional claims you want to include in the token
        # token['claim_name'] = 'claim_value'
        return token
