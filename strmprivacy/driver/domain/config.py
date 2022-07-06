import logging

from pbr.version import SemanticVersion

from .. import __version__


class ClientConfig(object):
    def __init__(self, log_level=logging.INFO, **kwargs):
        self._log_level = log_level
        self._gateway_protocol = kwargs.get("gateway_protocol", "https")
        self._gateway_host = kwargs.get("gateway_host", "events.strmprivacy.io")
        self._gateway_endpoint = kwargs.get("gateway_endpoint", "/event")
        self._egress_protocol = kwargs.get("egress_protocol", "https")
        self._egress_host = kwargs.get("egress_host", "websocket.strmprivacy.io")
        self._egress_endpoint = kwargs.get("egress_endpoint", "/ws")
        self._egress_health_endpoint = kwargs.get("egress_health_endpoint", "/is-alive")
        self._keycloak_protocol = kwargs.get("keycloak_protocol", "https")
        self._keycloak_host = kwargs.get("keycloak_host", "accounts.strmprivacy.io")
        self._keycloak_endpoint = kwargs.get("keycloak_endpoint", "/auth/realms/streams/protocol/openid-connect/token")
        self._keycloak_refresh_interval = kwargs.get("sts_refresh_interval", 300)
        self._version = SemanticVersion.from_pip_string(__version__)

    def get_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(self._log_level)
        return logger

    @property
    def gateway_uri(self):
        return f"{self._gateway_protocol}://{self._gateway_host}{self._gateway_endpoint}"

    @property
    def egress_uri(self):
        return f"{self._egress_protocol}://{self._egress_host}{self._egress_endpoint}"

    @property
    def egress_health_uri(self):
        return f"{self._egress_protocol}://{self._egress_host}{self._egress_health_endpoint}"

    @property
    def keycloak_auth_uri(self):
        return f"{self._keycloak_protocol}://{self._keycloak_host}{self._keycloak_endpoint}"

    @property
    def keycloak_refresh_interval(self):
        return self._keycloak_refresh_interval

    @property
    def version(self) -> SemanticVersion:
        return self._version
