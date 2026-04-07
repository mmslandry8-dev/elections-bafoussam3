from elections.models import AuditLog

class AuditService:

    @staticmethod
    def log(action, user, description):
        AuditLog.objects.create(
            action=action,
            user=user,
            description=description
        )

# class AuditService:

#     @staticmethod
#     def log(action, user, message):
#         print(f"[AUDIT] {action} - {user} - {message}")