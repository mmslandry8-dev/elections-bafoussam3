def user_role(request):
    if request.user.is_authenticated:
        group = request.user.groups.first()
        return {'user_role': group.name if group else None}
    return {'user_role': None}