from starlette.middleware.cors import CORSMiddleware

from settings import ORIGINS


def allow_cross_domain(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app