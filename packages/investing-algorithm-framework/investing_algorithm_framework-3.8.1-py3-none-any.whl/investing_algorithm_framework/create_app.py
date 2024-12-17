import logging

from .app import App
from .dependency_container import setup_dependency_container

logger = logging.getLogger("investing_algorithm_framework")


def create_app(config=None, stateless=False, web=False) -> App:
    app = App(web=web, stateless=stateless)
    app = setup_dependency_container(
        app,
        ["investing_algorithm_framework"],
        ["investing_algorithm_framework"]
    )
    # After the container is setup, initialize the services
    app.initialize_services()
    app.set_config(config)
    logger.info("Investing algoritm framework app created")
    return app
