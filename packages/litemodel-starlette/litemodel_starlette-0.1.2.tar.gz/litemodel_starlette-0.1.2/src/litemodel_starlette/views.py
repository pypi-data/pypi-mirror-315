from dataclasses import dataclass
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse
from litemodel.async_core import Model
from litemodel_starlette.resources import database, admin_templates
from litemodel_starlette.utils import tables


async def get_sidebar() -> list:
    data = await database.fetch_all(tables())
    return [d for d in data if d.name not in ["sqlite_sequence"]]


@dataclass
class AdminUrlHelper:
    def __init__(self, model: Model):
        self.model = model

    @property
    def create_view(self) -> str:
        return f"/admin/{self.model.get_table_name()}/new"

    @property
    def create_template(self) -> str:
        return "admin_new.html"

    @property
    def detail_view(self) -> str:
        return f"/admin/{self.model.get_table_name()}/{{id}}"

    @property
    def detail_template(self) -> str:
        return "admin_detail.html"

    @property
    def delete_view(self) -> str:
        return f"/admin/{self.model.get_table_name()}/{{id}}/delete"

    @property
    def delete_template(self) -> str:
        return "admin_delete.html"

    @property
    def edit_view(self) -> str:
        return f"/admin/{self.model.get_table_name()}/{{id}}/edit"

    @property
    def edit_template(self) -> str:
        return "admin_edit.html"

    @property
    def list_view(self) -> str:
        return f"/admin/{self.model.get_table_name()}"

    @property
    def list_template(self) -> str:
        return "admin_list.html"


class BaseAdminView(HTTPEndpoint):
    model: Model = None
    fields: tuple[str]

    # @login_required
    async def get(self, request: Request):
        return await self.process_get(request)

    # @login_required
    async def post(self, request: Request):
        return await self.process_post(request)

    async def process_get(self, request: Request):
        request_url_path = request.url.path
        if "new" in request_url_path:
            return await self._get_create_view(request)
        if "edit" in request_url_path:
            return await self._get_edit_view(request)
        if "delete" in request_url_path:
            return await self._get_delete_view(request)
        id = request.path_params.get("id")
        if id:
            return await self._get_detail_view(request)
        return await self._get_list_view(request)

    async def process_post(self, request: Request):
        request_url_path = request.url.path
        if "new" in request_url_path:
            return await self._post_create_view(request)
        if "edit" in request_url_path:
            return await self._post_edit_view(request)
        if "delete" in request_url_path:
            return await self._post_delete_view(request)
        return None

    async def _get_create_view(self, request: Request):
        return admin_templates.TemplateResponse(
            request,
            AdminUrlHelper(self.model).create_template,
            context={
                "model": self.model,
                "tables": await get_sidebar(),
                "table": self.model.get_table_name(),
                "breadcrumb": "new"
            },
        )

    async def _get_edit_view(self, request: Request):
        id = request.path_params["id"]
        row = await self.model.find(id)
        return admin_templates.TemplateResponse(
            request,
            AdminUrlHelper(self.model).edit_template,
            context={
                "row": row,
                "tables": await get_sidebar(),
                "table": self.model.get_table_name(),
                "breadcrumb": "edit"
            },
        )

    async def _get_detail_view(self, request: Request):
        id = request.path_params["id"]
        row = await self.model.find(id)
        return admin_templates.TemplateResponse(
            request,
            AdminUrlHelper(self.model).detail_template,
            context={
                "row": row,
                "tables": await get_sidebar(),
                "table": self.model.get_table_name(),
                "breadcrumb": "detail"
            },
        )

    async def _get_delete_view(self, request: Request):
        id = request.path_params["id"]
        row = await self.model.find(id)
        return admin_templates.TemplateResponse(
            request,
            AdminUrlHelper(self.model).delete_template,
            context={
                "row": row,
                "tables": await get_sidebar(),
                "table": self.model.get_table_name(),
                "breadcrumb": "delete"
            },
        )

    async def _get_list_view(self, request: Request):
        # TODO -- obviously make this pagination more effecient but works fine
        # for now
        items_per_page = 20
        page = int(request.query_params.get("page", 1))
        rows = await self.model.all()
        start = 0 if page == 1 else (page-1)*items_per_page
        end = items_per_page if page == 1 else (page+1)*items_per_page
        rows = rows[start:end]
        if rows:
            headers = list(rows[0].fields.keys())
            self._add_links(rows)
        else:
            headers = []
        return admin_templates.TemplateResponse(
            request,
            AdminUrlHelper(self.model).list_template,
            context={
                "rows": rows,
                "headers": headers,
                "table": self.model.get_table_name(),
                "tables": await get_sidebar(),
                "breadcrumb": "list",
                "next_page": int(page) + 1,
                "current_page": int(page),
                "previous_page": int(page) - 1,
            },
        )

    def _add_links(self, rows: list[Model]) -> None:
        for row in rows:
            row.detail_link = AdminUrlHelper(self.model).detail_view.format(id=row.id)
            row.edit_link = AdminUrlHelper(self.model).edit_view.format(id=row.id)
            row.delete_link = AdminUrlHelper(self.model).delete_view.format(id=row.id)

    async def _post_create_view(self, request: Request):
        form_data = await request.form()
        instance: Model = self.model(**form_data)
        await instance.save()
        return RedirectResponse(f"/admin/{self.model.get_table_name()}/{instance.id}", 303)

    async def _post_edit_view(self, request: Request):
        form_data = await request.form()
        instance: Model = self.model(**form_data)
        await instance.save()
        return RedirectResponse(f"/admin/{self.model.get_table_name()}/{instance.id}", 303)

    async def _post_delete_view(self, request: Request):
        id = request.path_params["id"]
        await self.model.delete(id)
        return RedirectResponse(f"/admin/{self.model.get_table_name()}", 303)
