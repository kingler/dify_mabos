# mabos/user_management/authorization_manager.py
class AuthorizationManager:
    def __init__(self, role_repository, permission_repository):
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        # Initialize other attributes and components

    def assign_role_to_user(self, user, role):
        # Assign a role to a user
        pass

    def revoke_role_from_user(self, user, role):
        # Revoke a role from a user
        pass

    def check_user_permission(self, user, permission):
        # Check if a user has a specific permission
        pass