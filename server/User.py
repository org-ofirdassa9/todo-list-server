class User():

    def __init__(self, id, email, has_password, first_name, last_name, created_at):
        self.id = id
        self.email = email
        self.has_password = has_password
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = created_at
    
    @classmethod
    def from_string(cls, user_string):
        id, email, hashed_password, first_name, last_name = user_string.split('-')
        return cls(id, email, hashed_password, first_name, last_name)
    
    @staticmethod
    def check_password(hashed_password):
        if 'b' in hashed_password:
            return True
        return False

    def format_user(self): 
        return {
            'id': self.id,
            'email': self.email,
            'has_password': self.has_password,
            'fist_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at
        }