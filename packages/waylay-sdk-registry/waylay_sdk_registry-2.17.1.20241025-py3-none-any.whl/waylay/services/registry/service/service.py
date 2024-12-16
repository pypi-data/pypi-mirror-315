"""Registry Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.about_api import AboutApi
from ..api.jobs_api import JobsApi
from ..api.model_tags_api import ModelTagsApi
from ..api.models_api import ModelsApi
from ..api.plug_tags_api import PlugTagsApi
from ..api.plugs_api import PlugsApi
from ..api.runtimes_api import RuntimesApi
from ..api.schemas_api import SchemasApi
from ..api.tags_api import TagsApi
from ..api.webscript_tags_api import WebscriptTagsApi
from ..api.webscripts_api import WebscriptsApi


class RegistryService(WaylayService):
    """Registry Service Class."""

    name = "registry"
    title = "Registry Service"

    about: AboutApi
    jobs: JobsApi
    model_tags: ModelTagsApi
    models: ModelsApi
    plug_tags: PlugTagsApi
    plugs: PlugsApi
    runtimes: RuntimesApi
    schemas: SchemasApi
    tags: TagsApi
    webscript_tags: WebscriptTagsApi
    webscripts: WebscriptsApi

    def __init__(self, api_client: ApiClient):
        """Create the registry service."""

        super().__init__(api_client)
        self.about = AboutApi(api_client)
        self.jobs = JobsApi(api_client)
        self.model_tags = ModelTagsApi(api_client)
        self.models = ModelsApi(api_client)
        self.plug_tags = PlugTagsApi(api_client)
        self.plugs = PlugsApi(api_client)
        self.runtimes = RuntimesApi(api_client)
        self.schemas = SchemasApi(api_client)
        self.tags = TagsApi(api_client)
        self.webscript_tags = WebscriptTagsApi(api_client)
        self.webscripts = WebscriptsApi(api_client)
