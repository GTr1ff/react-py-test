"""Cloudflare Workers entry point.

Bridges incoming requests into the FastAPI app via the Workers ASGI
adapter. ``workers`` and ``asgi`` are provided by the Workers Python
runtime; this module is only imported there, never by the test suite.
"""

from workers import WorkerEntrypoint # type: ignore[import-not-found]

_app = None


def _get_app():
    global _app
    if _app is None:
        from main import app

        _app = app
    return _app


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi # type: ignore[import-not-found]

        return await asgi.fetch(_get_app(), request, self.env)
