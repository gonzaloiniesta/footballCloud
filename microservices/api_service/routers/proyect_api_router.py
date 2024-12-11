from fastapi import APIRouter, Depends
from integrations import MongoDBFootballCloud

class ProyectAPIRouter(APIRouter):
    """
    Custom APIRouter that automatically injects the database dependency
    in all routes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = self._get_db()

    @staticmethod
    def _get_db():
        db = MongoDBFootballCloud().get_db()
        return next(db)

    def add_api_route(self, path, endpoint, **kwargs):
        """
        Overrides the method to inject the `db` dependency automatically.
        """
        # Ensure the database dependency is included
        kwargs.setdefault("dependencies", [])
        kwargs["dependencies"].append(Depends(self._get_db))
        super().add_api_route(path, endpoint, **kwargs)
