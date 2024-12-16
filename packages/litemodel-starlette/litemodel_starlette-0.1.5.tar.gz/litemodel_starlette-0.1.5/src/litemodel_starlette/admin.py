import functools
from typing import Type

from starlette.routing import Route
from litemodel_starlette.views import BaseAdminView

ROUTES = []


def register_admin_class(admin_view_class: Type[BaseAdminView]) -> list[Route]:
    table = admin_view_class.model.get_table_name()
    return [
        Route(
            f"/admin/{table}",
            endpoint=admin_view_class,
            name=f"admin_{table}",
            methods=["GET", "POST", "HEAD"],
        ),
        Route(
            f"/admin/{table}/new",
            endpoint=admin_view_class,
            name=f"admin_{table}_new",
            methods=["GET", "POST", "HEAD"],
        ),
        Route(
            f"/admin/{table}/{{id:int}}",
            endpoint=admin_view_class,
            name=f"admin_{table}_detail",
            methods=["GET", "POST", "HEAD"],
        ),
        Route(
            f"/admin/{table}/{{id:int}}/edit",
            endpoint=admin_view_class,
            name=f"admin_{table}_edit",
            methods=["GET", "POST", "HEAD"],
        ),
        Route(
            f"/admin/{table}/{{id:int}}/delete",
            endpoint=admin_view_class,
            name=f"admin_{table}_delete",
            methods=["GET", "POST", "HEAD"],
        ),
    ]


def register_admin(admin_view_class: Type[BaseAdminView]):
    """Wraps a class that inherits from the BaseAdminView to add the CRUD
    routes to the server's routes.
    """

    @functools.wraps(admin_view_class)
    def decorate(admin_view_class: Type[BaseAdminView]):
        ROUTES.extend(register_admin_class(admin_view_class))
        return admin_view_class

    return decorate(admin_view_class)
