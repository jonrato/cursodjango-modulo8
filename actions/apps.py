from django.apps import AppConfig
import pylogalert as log
import os

class ActionsConfig(AppConfig):
    name = 'actions'

    def ready(self):
        log_file_path = os.path.join(os.path.dirname(__file__), "../logs/activity.log")
        log.configure(
            service=os.getenv("SERVICE_NAME"),
            env=os.getenv("APP_ENV"),
            level=os.getenv("LOG_LEVEL"),
            stream=open(log_file_path, "a"),
            color=False,
            redact_keys=["token", "email"],
            sample={"debug": 0.0, "info": 1.0}
        )

        log.info('PylogAlert iniciado com sucesso!!!')