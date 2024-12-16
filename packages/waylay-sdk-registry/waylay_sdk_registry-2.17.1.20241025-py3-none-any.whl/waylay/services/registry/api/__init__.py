"""Waylay Function Registry: apis."""

# import apis into api package
from .about_api import AboutApi
from .jobs_api import JobsApi
from .model_tags_api import ModelTagsApi
from .models_api import ModelsApi
from .plug_tags_api import PlugTagsApi
from .plugs_api import PlugsApi
from .runtimes_api import RuntimesApi
from .schemas_api import SchemasApi
from .tags_api import TagsApi
from .webscript_tags_api import WebscriptTagsApi
from .webscripts_api import WebscriptsApi

__all__ = [
    "AboutApi",
    "JobsApi",
    "ModelTagsApi",
    "ModelsApi",
    "PlugTagsApi",
    "PlugsApi",
    "RuntimesApi",
    "SchemasApi",
    "TagsApi",
    "WebscriptTagsApi",
    "WebscriptsApi",
]
