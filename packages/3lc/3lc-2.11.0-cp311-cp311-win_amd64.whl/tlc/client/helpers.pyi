from _typeshed import Incomplete
from tlc.client.session import Session as Session
from tlc.core.objects.mutable_objects.run import Run as Run
from tlc.core.url import AliasPrecedence as AliasPrecedence, Url as Url, UrlAliasRegistry as UrlAliasRegistry

logger: Incomplete

def active_run() -> Run | None:
    """Return the active Run, if any."""
def set_active_run(run: Run | Url) -> None:
    """Set the active Run."""
def active_project_name() -> str | None:
    """Return the active project name, if any."""
def register_url_alias(token: str, path: str, force: bool = True) -> None:
    """Register an alias for a URL.

    :param token: The alias token to register. Must be match the regex `[A-Z][A-Z0-9_]*`.
    :param path: The path to alias.
    :param force: If True, force the registration of the alias even if it is already registered.
    :raises ValueError: If the token is already registered and force is False.
    """
def unregister_url_alias(token: str) -> None:
    """Unregister an alias for a URL.

    :param token: The alias token to unregister. Must match the regex `[A-Z][A-Z0-9_]*`.
    :raises KeyError: If the token is not registered.
    """
def get_registered_url_aliases() -> dict[str, str]:
    """Return the registered URL aliases.

    :return: A dictionary mapping alias tokens to paths.
    """
def register_project_url_alias(token: str, path: str, force: bool = True, project: str | None = None, root: str | None = None) -> None:
    """Register and persist a project URL alias.

    A project URL alias is a per-project alias that is persisted in the project's configuration file and will be loaded
    for other users that share the same project but not necessarily the same startup-config. The alias is also
    registered in the current session and is immediately available for use.

    :param token: The alias token to register. Must match the regex `[A-Z][A-Z0-9_]*`.
    :param path: The path to alias.
    :param force: If True, force the registration of the alias even if it is already registered.
    :param project: The project name. If None, the active project is used.
    :param root: The root name. If None, the active root is used.
    :raises ValueError: If the token is already registered and force is False.

    """
