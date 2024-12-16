from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sign a JWT token for a given app"

    def add_arguments(self, parser):
        parser.add_argument("app", nargs="?", type=int)
        parser.add_argument("user", nargs="?", type=int)

    def handle(self, *args, **options):
        from linked_services.django.actions import get_jwt

        from ...models import App

        if not options["app"]:
            raise Exception("Missing app id")

        try:
            app = App.objects.get(id=options["app"])

        except App.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'App {options["app"]} not found'))
            return

        token = get_jwt(app, user_id=options["user"], reverse=True)

        self.stdout.write(f"Authorization: Link App={app.slug},Token={token}")
