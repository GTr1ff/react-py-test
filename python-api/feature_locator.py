import importlib
import logging
from pathlib import Path
from fastapi import APIRouter

logger = logging.getLogger("app") 

class FeatureLocator:
    """Feature locator class to automatically register and get feature routers in the application"""

    def __init__(self, base_package: str = "features"):
        self._features: dict[str, APIRouter] = {}
        self._discover_and_register(base_package)

    def _discover_and_register(self, base_package: str) -> None:
        base_path = Path(__file__).resolve().parent / base_package
        for router_file in base_path.rglob("router.py"):
            module_path = self._path_to_module(router_file, base_path)
            try:
                module = importlib.import_module(module_path)
                router = getattr(module, "router", None)
                if isinstance(router, APIRouter):
                    self._features[module_path] = router
            except Exception as e:
                logger.exception("Failed to load %s", module_path, extra={"error_type": type(e).__name__})
                raise

    def _path_to_module(self, file_path: Path, base_path: Path) -> str:
        relative_path = file_path.relative_to(base_path.parent)
        return ".".join(relative_path.with_suffix("").parts)

    def register(self, name: str, feature: APIRouter):
        self._features[name] = feature

    def get(self, name: str) -> APIRouter | None:
        return self._features.get(name)

    def get_feature_routers(self) -> dict[str, APIRouter]:
        return self._features