class User:
    def __init__(self, user_id, username, password, email, roles):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.roles = roles
        self.is_active = True

    def has_role(self, role):
        return role in self.roles

    def add_role(self, role):
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def change_password(self, new_password):
        self.password = new_password

    def update_email(self, new_email):
        self.email = new_email
