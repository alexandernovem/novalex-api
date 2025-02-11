from fastapi import APIRouter
from fastapi.responses import JSONResponse


class GeneralController:
    async def up(self) -> JSONResponse:
        return JSONResponse(status_code=200, content={"Status": "OK"})

    async def info(self) -> JSONResponse:
        return JSONResponse(status_code=200, content={"Info": "OK"})


def provide_general_router(controller: GeneralController) -> APIRouter:
    router = APIRouter()
    router.add_api_route("/up", controller.up, methods=["GET"], include_in_schema=False)
    router.add_api_route("/info", controller.info, methods=["GET"], include_in_schema=False)

    return router
