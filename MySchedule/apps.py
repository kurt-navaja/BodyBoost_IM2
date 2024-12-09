from django.apps import AppConfig # type: ignore

class MyScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MySchedule'
    def ready(self):
        import MySchedule.signals