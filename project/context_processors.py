from main.models import Settings


def theme_context(request):
    if request.user.is_authenticated:
        settings_obj, _ = Settings.objects.get_or_create(user=request.user)
        return {'user_theme': settings_obj.theme}
    return {'user_theme': 'light'}
