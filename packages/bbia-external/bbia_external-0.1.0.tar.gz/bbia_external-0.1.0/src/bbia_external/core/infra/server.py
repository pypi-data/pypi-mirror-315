from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from ...modules.lang_process.chains import rag_chain
from ..conf import settings
from ..middlewares.rate_limit import RateLimitMiddleware

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

add_routes(app, rag_chain, path="/bbia")

app.add_middleware(RateLimitMiddleware)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")
