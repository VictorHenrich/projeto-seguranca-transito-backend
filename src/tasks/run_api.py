from server import App
from server.cli import Task


@App.cli.add_task("api", "run", "r", "Inicializa a aplicação HTTP")
class RunApi(Task):
    def run(self, props) -> None:
        import controllers.http

        App.http.run()
