from django.apps import AppConfig


class ShopflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopflow'
    def ready(self):
        import shopflow.signals