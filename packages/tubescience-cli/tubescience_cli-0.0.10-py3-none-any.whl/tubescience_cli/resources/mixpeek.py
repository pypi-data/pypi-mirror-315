from typing import Any
from pydantic import BaseModel, SecretStr


class MixpeekResource(BaseModel):
    base_url: str = "https://api.mixpeek.com"
    api_key: SecretStr = SecretStr("")
    namespace: str = "features-default"

    @property
    def headers(self):
        headers = {
            "Authorization": f"Bearer {self.api_key.get_secret_value()}",
        }
        if self.namespace and self.namespace != "features-default":
            headers["X-Namespace"] = self.namespace
        return headers

    def Client(self, **kwargs):
        import httpx

        kwargs.setdefault("headers", self.headers)
        return httpx.Client(base_url=self.base_url, **kwargs)

    def AsyncClient(self, **kwargs):
        import httpx

        kwargs.setdefault("headers", self.headers)
        return httpx.AsyncClient(base_url=self.base_url, **kwargs)

    def with_namespace(self, namespace: str):
        return self.copy(update={"namespace": namespace})

    # Organization endpoints
    def get_organization(self):
        with self.Client() as client:
            r = client.get("/organizations")
            r.raise_for_status()
        return r.json()

    async def aget_organization(self):
        async with self.AsyncClient() as client:
            r = await client.get("/organizations")
            r.raise_for_status()
        return r.json()

    def get_usage(self):
        with self.Client() as client:
            r = client.get("/organizations/usage")
            r.raise_for_status()
        return r.json()

    async def aget_usage(self):
        async with self.AsyncClient() as client:
            r = await client.get("/organizations/usage")
            r.raise_for_status()
        return r.json()

    def get_user(self, user_email: str):
        with self.Client() as client:
            r = client.get(f"/organizations/users/{user_email}")
            r.raise_for_status()
        return r.json()

    async def aget_user(self, user_email: str):
        async with self.AsyncClient() as client:
            r = await client.get(f"/organizations/users/{user_email}")
            r.raise_for_status()
        return r.json()

    def delete_user(self, user_email: str):
        with self.Client() as client:
            r = client.delete(f"/organizations/users/{user_email}")
            r.raise_for_status()
        return r.json()

    async def adelete_user(self, user_email: str):
        async with self.AsyncClient() as client:
            r = await client.delete(f"/organizations/users/{user_email}")
            r.raise_for_status()
        return r.json()

    def add_user(self, user_data: dict):
        with self.Client() as client:
            r = client.post("/organizations/users", json=user_data)
            r.raise_for_status()
        return r.json()

    async def aadd_user(self, user_data: dict):
        async with self.AsyncClient() as client:
            r = await client.post("/organizations/users", json=user_data)
            r.raise_for_status()
        return r.json()

    def create_api_key(self, user_email: str, key_name: str = "default"):
        with self.Client() as client:
            r = client.post(
                f"/organizations/users/{user_email}/api-keys",
                params={"key_name": key_name},
            )
            r.raise_for_status()
        return r.json()

    async def acreate_api_key(self, user_email: str, key_name: str = "default"):
        async with self.AsyncClient() as client:
            r = await client.post(
                f"/organizations/users/{user_email}/api-keys",
                params={"key_name": key_name},
            )
            r.raise_for_status()
        return r.json()

    def delete_api_key(self, user_email: str, api_key: str):
        with self.Client() as client:
            r = client.delete(f"/organizations/users/{user_email}/api-keys/{api_key}")
            r.raise_for_status()
        return r.json()

    async def adelete_api_key(self, user_email: str, api_key: str):
        async with self.AsyncClient() as client:
            r = await client.delete(
                f"/organizations/users/{user_email}/api-keys/{api_key}"
            )
            r.raise_for_status()
        return r.json()

    def update_api_key(self, user_email: str, key_name: str, update_data: dict):
        with self.Client() as client:
            r = client.patch(
                f"/organizations/users/{user_email}/api-keys/{key_name}",
                json=update_data,
            )
            r.raise_for_status()
        return r.json()

    async def aupdate_api_key(self, user_email: str, key_name: str, update_data: dict):
        async with self.AsyncClient() as client:
            r = await client.patch(
                f"/organizations/users/{user_email}/api-keys/{key_name}",
                json=update_data,
            )
            r.raise_for_status()
        return r.json()

    # Namespace endpoints
    def list_namespaces(self):
        with self.Client() as client:
            r = client.get("/namespaces")
            r.raise_for_status()
        return r.json()

    async def alist_namespaces(self):
        async with self.AsyncClient() as client:
            r = await client.get("/namespaces")
            r.raise_for_status()
        return r.json()

    def create_namespace(self, namespace_data: dict):
        with self.Client() as client:
            r = client.post("/namespaces", json=namespace_data)
            r.raise_for_status()
        return r.json()

    async def acreate_namespace(self, namespace_data: dict):
        async with self.AsyncClient() as client:
            r = await client.post("/namespaces", json=namespace_data)
            r.raise_for_status()
        return r.json()

    def update_namespace(self, namespace: str, update_data: dict):
        with self.Client() as client:
            r = client.put(f"/namespaces/{namespace}", json=update_data)
            r.raise_for_status()
        return r.json()

    async def aupdate_namespace(self, namespace: str, update_data: dict):
        async with self.AsyncClient() as client:
            r = await client.put(f"/namespaces/{namespace}", json=update_data)
            r.raise_for_status()
        return r.json()

    def delete_namespace(self, namespace: str):
        with self.Client() as client:
            r = client.delete(f"/namespaces/{namespace}")
            r.raise_for_status()
        return r.json()

    async def adelete_namespace(self, namespace: str):
        async with self.AsyncClient() as client:
            r = await client.delete(f"/namespaces/{namespace}")
            r.raise_for_status()
        return r.json()

    # collection endpoints
    def list_collections(self):
        with self.Client() as client:
            r = client.get("/collections")
            r.raise_for_status()
        return r.json()

    def get_collection(self, collection_id: str):
        with self.Client() as client:
            r = client.get(f"/collections/{collection_id}")
            r.raise_for_status()
        return r.json()

    def create_collection(self, name: str, metadata=None):
        if metadata is None:
            metadata = {}
        data = {"collection_name": name, "metadata": metadata}
        with self.Client() as client:
            r = client.post("/collections", json=data)
            r.raise_for_status()
        return r.json()

    def delete_collection(self, collection_id: str):
        with self.Client() as client:
            r = client.delete(f"/collections/{collection_id}")
            r.raise_for_status()
        return r.json()

    def update_collection(self, collection_id: str, update_data: dict):
        with self.Client() as client:
            r = client.put(f"/collections/{collection_id}", json=update_data)
            r.raise_for_status()
        return r.json()

    # Feature endpoints
    def get_feature(self, feature_id: str):
        with self.Client() as client:
            r = client.get(f"/features/{feature_id}")
            r.raise_for_status()
        return r.json()

    async def aget_feature(self, feature_id: str):
        async with self.AsyncClient() as client:
            r = await client.get(f"/features/{feature_id}")
            r.raise_for_status()
        return r.json()

    def delete_feature(self, feature_id: str):
        with self.Client() as client:
            r = client.delete(f"/features/{feature_id}")
            r.raise_for_status()
        return r.json()

    async def adelete_feature(self, feature_id: str):
        async with self.AsyncClient() as client:
            r = await client.delete(f"/features/{feature_id}")
            r.raise_for_status()
        return r.json()

    def update_feature(self, feature_id: str, update_data: dict):
        with self.Client() as client:
            r = client.put(f"/features/{feature_id}", json=update_data)
            r.raise_for_status()
        return r.json()

    async def aupdate_feature(self, feature_id: str, update_data: dict):
        async with self.AsyncClient() as client:
            r = await client.put(f"/features/{feature_id}", json=update_data)
            r.raise_for_status()
        return r.json()

    def list_features(
            self,
            collections: list[str] | str,
            filters: dict | None = None,
            sort: dict | None = None,
            select: list | None = None,
            offset_feature_id: str | None = None,
            page_size: int | None = None,
        ) -> dict:
        """List features based on provided criteria

        Args:
            collections: List of collection IDs or names
            filters: Optional filter conditions
            sort: Optional sort criteria
            select: Optional fields to return
            offset_feature_id: Optional feature ID to start from
            page_size: Optional number of results per page
        """
        if isinstance(collections, str):
            collections = [collections]
        search_params: dict[str, Any] = {
            "collections": collections
        }
        if filters:
            search_params["filters"] = filters
        if sort:
            search_params["sort"] = sort
        if select:
            search_params["select"] = select

        params = {}
        if offset_feature_id:
            params["offset_feature_id"] = offset_feature_id
        if page_size:
            params["page_size"] = page_size

        with self.Client() as client:
            r = client.post("/features", params=params, json=search_params)
            r.raise_for_status()
        return r.json()

    async def alist_features(
        self,
        collections: list[str],
        filters: dict | None = None,
        sort: dict | None = None,
        select: list | None = None,
        offset_feature_id: str | None = None,
        page_size: int | None = None,
    ) -> dict:
        if isinstance(collections, str):
            collections = [collections]
        search_params: dict[str, Any] = {
            "collections": collections
        }
        if filters:
            search_params["filters"] = filters
        if sort:
            search_params["sort"] = sort
        if select:
            search_params["select"] = select

        params = {}
        if offset_feature_id:
            params["offset_feature_id"] = offset_feature_id
        if page_size:
            params["page_size"] = page_size

        async with self.AsyncClient() as client:
            r = await client.post("/features", params=params, json=search_params)
            r.raise_for_status()
        return r.json()

    def search_features(
        self,
        queries: list[dict],
        collections: list[str],
        filters: dict | None = None,
        group_by: dict | None = None,
        sort: dict | None = None,
        select: list[str] | None = None,
        reranking_options: dict | None = None,
        session_id: str | None = None,
        return_url: bool = False,
        offset_position: int | None = None,
        page_size: int | None = None,
    ) -> dict:
        """Search features with complex criteria

        Args:
            queries: List of search queries
            collections: List of collections to search in
            filters: Optional filter conditions
            group_by: Optional grouping configuration
            sort: Optional sort criteria
            select: Optional fields to include
            reranking_options: Optional reranking settings
            session_id: Optional session identifier
            return_url: Whether to return presigned URLs
            offset_position: Optional starting position
            page_size: Optional results per page
        """
        if isinstance(collections, str):
            collections = [collections]
        search_params: dict[str, Any] = {
            "queries": queries,
            "collections": collections,
            "return_url": return_url
        }

        if filters:
            search_params["filters"] = filters
        if group_by:
            search_params["group_by"] = group_by
        if sort:
            search_params["sort"] = sort
        if select:
            search_params["select"] = select
        if reranking_options:
            search_params["reranking_options"] = reranking_options
        if session_id:
            search_params["session_id"] = session_id

        params = {}
        if offset_position is not None:
            params["offset_position"] = offset_position
        if page_size is not None:
            params["page_size"] = page_size

        with self.Client() as client:
            r = client.post("/features/search", params=params, json=search_params)
            r.raise_for_status()
        return r.json()

    # Interaction endpoints
    def create_interaction(self, interaction_data: dict):
        with self.Client() as client:
            r = client.post("/features/search/interactions", json=interaction_data)
            r.raise_for_status()
        return r.json()

    async def acreate_interaction(self, interaction_data: dict):
        async with self.AsyncClient() as client:
            r = await client.post(
                "/features/search/interactions", json=interaction_data
            )
            r.raise_for_status()
        return r.json()

    def list_interactions(
        self,
        feature_id: str | None = None,
        interaction_type: str | None = None,
        session_id: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if feature_id:
            params["feature_id"] = feature_id
        if interaction_type:
            params["interaction_type"] = interaction_type
        if session_id:
            params["session_id"] = session_id

        with self.Client() as client:
            r = client.get("/features/search/interactions", params=params)
            r.raise_for_status()
        return r.json()

    async def alist_interactions(
        self,
        feature_id: str | None = None,
        interaction_type: str | None = None,
        session_id: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if feature_id:
            params["feature_id"] = feature_id
        if interaction_type:
            params["interaction_type"] = interaction_type
        if session_id:
            params["session_id"] = session_id

        async with self.AsyncClient() as client:
            r = await client.get("/features/search/interactions", params=params)
            r.raise_for_status()
        return r.json()

    def get_interaction(self, interaction_id: str):
        with self.Client() as client:
            r = client.get(f"/features/search/interactions/{interaction_id}")
            r.raise_for_status()
        return r.json()

    async def aget_interaction(self, interaction_id: str):
        async with self.AsyncClient() as client:
            r = await client.get(f"/features/search/interactions/{interaction_id}")
            r.raise_for_status()
        return r.json()

    def delete_interaction(self, interaction_id: str):
        with self.Client() as client:
            r = client.delete(f"/features/search/interactions/{interaction_id}")
            r.raise_for_status()
        return r.json()

    async def adelete_interaction(self, interaction_id: str):
        async with self.AsyncClient() as client:
            r = await client.delete(f"/features/search/interactions/{interaction_id}")
            r.raise_for_status()
        return r.json()

    def ingest_text(
            self,
            collection: str,
            feature_extractors: dict | None = None,
            asset_update: dict | None = None,
            metadata: dict | None = None,
            percolate: dict | None = None,
            skip_duplicate: bool = True
        ) -> dict:
            """Ingest text content

            Args:
                collection: Collection ID or name
                feature_extractors: Optional text processing settings
                asset_update: Optional asset update information
                metadata: Optional metadata
                percolate: Optional percolator settings
                skip_duplicate: Whether to skip duplicates
            """
            ingest_data = {
                "collection": collection,
                "skip_duplicate": skip_duplicate
            }
            if feature_extractors:
                ingest_data["feature_extractors"] = feature_extractors
            if asset_update:
                ingest_data["asset_update"] = asset_update
            if metadata:
                ingest_data["metadata"] = metadata
            if percolate:
                ingest_data["percolate"] = percolate

            with self.Client() as client:
                r = client.post("/ingest/text", json=ingest_data)
                r.raise_for_status()
            return r.json()

    def ingest_video_url(
        self,
        url: str,
        collection: str,
        feature_extractors: list[dict] | None = None,
        asset_update: dict | None = None,
        metadata: dict | None = None,
        percolate: dict | None = None,
        skip_duplicate: bool = True
    ) -> dict:
        """Ingest video from URL

        Args:
            url: Video URL to process
            collection: Collection ID or name
            feature_extractors: Optional video processing settings
            asset_update: Optional asset update information
            metadata: Optional metadata
            percolate: Optional percolator settings
            skip_duplicate: Whether to skip duplicates
        """
        ingest_data = {
            "url": url,
            "collection": collection,
            "skip_duplicate": skip_duplicate
        }
        if feature_extractors:
            ingest_data["feature_extractors"] = feature_extractors
        if asset_update:
            ingest_data["asset_update"] = asset_update
        if metadata:
            ingest_data["metadata"] = metadata
        if percolate:
            ingest_data["percolate"] = percolate

        with self.Client() as client:
            r = client.post("/ingest/videos/url", json=ingest_data)
            r.raise_for_status()
        return r.json()

    def ingest_image_url(
        self,
        url: str,
        collection: str,
        feature_extractors: dict | None = None,
        asset_update: dict | None = None,
        metadata: dict | None = None,
        percolate: dict | None = None,
        skip_duplicate: bool = True
    ) -> dict:
        """Ingest image from URL

        Args:
            url: Image URL to process
            collection: Collection ID or name
            feature_extractors: Optional image processing settings
            asset_update: Optional asset update information
            metadata: Optional metadata
            percolate: Optional percolator settings
            skip_duplicate: Whether to skip duplicates
        """
        ingest_data = {
            "url": url,
            "collection": collection,
            "skip_duplicate": skip_duplicate
        }
        if feature_extractors:
            ingest_data["feature_extractors"] = feature_extractors
        if asset_update:
            ingest_data["asset_update"] = asset_update
        if metadata:
            ingest_data["metadata"] = metadata
        if percolate:
            ingest_data["percolate"] = percolate

        with self.Client() as client:
            r = client.post("/ingest/images/url", json=ingest_data)
            r.raise_for_status()
        return r.json()

    def list_assets(
        self,
        collections: list[str],
        filters: dict | None = None,
        group_by: dict | None = None,
        sort: dict | None = None,
        select: list[str] | None = None,
        return_url: bool = False,
        page: int = 1,
        page_size: int = 10
    ) -> dict:
        """List assets with filtering and pagination

        Args:
            collections: List of collection IDs or names
            filters: Optional filter conditions
            group_by: Optional grouping configuration
            sort: Optional sort criteria
            select: Optional fields to include
            return_url: Whether to return presigned URLs
            page: Page number
            page_size: Results per page
        """
        list_params = {
            "collections": collections,
            "return_url": return_url
        }
        if filters:
            list_params["filters"] = filters
        if group_by:
            list_params["group_by"] = group_by
        if sort:
            list_params["sort"] = sort
        if select:
            list_params["select"] = select

        params = {
            "page": page,
            "page_size": page_size
        }

        with self.Client() as client:
            r = client.post("/assets", params=params, json=list_params)
            r.raise_for_status()
        return r.json()

    def search_assets(
        self,
        collections: list[str],
        query: dict | None = None,
        filters: dict | None = None,
        sort: dict | None = None,
        select: list[str] | None = None,
        return_url: bool = False
    ) -> dict:
        """Search assets with complex criteria

        Args:
            collections: List of collection IDs or names
            query: Optional structured query object
            filters: Optional filter conditions
            sort: Optional sort criteria
            select: Optional fields to include
            return_url: Whether to return presigned URLs
        """
        search_params = {
            "collections": collections,
            "return_url": return_url
        }
        if query:
            search_params["query"] = query
        if filters:
            search_params["filters"] = filters
        if sort:
            search_params["sort"] = sort
        if select:
            search_params["select"] = select

        with self.Client() as client:
            r = client.post("/assets/search", json=search_params)
            r.raise_for_status()
        return r.json()

    # Async versions of the last three methods
    async def aingest_video_url(
        self,
        url: str,
        collection: str,
        feature_extractors: list[dict] | None = None,
        asset_update: dict | None = None,
        metadata: dict | None = None,
        percolate: dict | None = None,
        skip_duplicate: bool = True
    ) -> dict:
        ingest_data = {
            "url": url,
            "collection": collection,
            "skip_duplicate": skip_duplicate
        }
        if feature_extractors:
            ingest_data["feature_extractors"] = feature_extractors
        if asset_update:
            ingest_data["asset_update"] = asset_update
        if metadata:
            ingest_data["metadata"] = metadata
        if percolate:
            ingest_data["percolate"] = percolate

        async with self.AsyncClient() as client:
            r = await client.post("/ingest/videos/url", json=ingest_data)
            r.raise_for_status()
        return r.json()

    async def aingest_image_url(
        self,
        url: str,
        collection: str,
        feature_extractors: dict | None = None,
        asset_update: dict | None = None,
        metadata: dict | None = None,
        percolate: dict | None = None,
        skip_duplicate: bool = True
    ) -> dict:
        ingest_data = {
            "url": url,
            "collection": collection,
            "skip_duplicate": skip_duplicate
        }
        if feature_extractors:
            ingest_data["feature_extractors"] = feature_extractors
        if asset_update:
            ingest_data["asset_update"] = asset_update
        if metadata:
            ingest_data["metadata"] = metadata
        if percolate:
            ingest_data["percolate"] = percolate

        async with self.AsyncClient() as client:
            r = await client.post("/ingest/images/url", json=ingest_data)
            r.raise_for_status()
        return r.json()

    async def alist_assets(
        self,
        collections: list[str],
        filters: dict | None = None,
        group_by: dict | None = None,
        sort: dict | None = None,
        select: list[str] | None = None,
        return_url: bool = False,
        page: int = 1,
        page_size: int = 10
    ) -> dict:
        list_params = {
            "collections": collections,
            "return_url": return_url
        }
        if filters:
            list_params["filters"] = filters
        if group_by:
            list_params["group_by"] = group_by
        if sort:
            list_params["sort"] = sort
        if select:
            list_params["select"] = select

        params = {
            "page": page,
            "page_size": page_size
        }

        async with self.AsyncClient() as client:
            r = await client.post("/assets", params=params, json=list_params)
            r.raise_for_status()
        return r.json()

    async def asearch_assets(
        self,
        collections: list[str],
        query: dict | None = None,
        filters: dict | None = None,
        sort: dict | None = None,
        select: list[str] | None = None,
        return_url: bool = False
    ) -> dict:
        search_params = {
            "collections": collections,
            "return_url": return_url
        }
        if query:
            search_params["query"] = query
        if filters:
            search_params["filters"] = filters
        if sort:
            search_params["sort"] = sort
        if select:
            search_params["select"] = select

        async with self.AsyncClient() as client:
            r = await client.post("/assets/search", json=search_params)
            r.raise_for_status()
        return r.json()

    # Task endpoints
    def get_task(self, task_id: str):
        with self.Client() as client:
            r = client.get(f"/tasks/{task_id}")
            r.raise_for_status()
        return r.json()

    async def aget_task(self, task_id: str):
        async with self.AsyncClient() as client:
            r = await client.get(f"/tasks/{task_id}")
            r.raise_for_status()
        return r.json()

    def kill_task(self, task_id: str):
        with self.Client() as client:
            r = client.delete(f"/tasks/{task_id}")
            r.raise_for_status()
        return r.json()

    async def akill_task(self, task_id: str):
        async with self.AsyncClient() as client:
            r = await client.delete(f"/tasks/{task_id}")
            r.raise_for_status()
        return r.json()

    # Health endpoint
    def healthcheck(self):
        with self.Client() as client:
            r = client.get("/healthcheck")
            r.raise_for_status()
        return r.json()

    async def ahealthcheck(self):
        async with self.AsyncClient() as client:
            r = await client.get("/healthcheck")
            r.raise_for_status()
        return r.json()
