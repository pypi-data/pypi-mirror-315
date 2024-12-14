import textwrap


class Secret:
    """
    Secret
    https://duckdb.org/docs/configuration/secrets_manager.html
    """

    def __init__(
        self,
        name: str,
        secret_type: str,
        persistent: bool = False,
        replace: bool = False,
        if_not_exists: bool = False,
        **keys,
    ):
        self._name = name
        self._type = secret_type
        self._persistent = persistent
        self._replace = replace
        self._if_not_exists = if_not_exists
        self._keys = keys

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', type='{self.secret_type}')"

    def __str__(self):
        return self.to_sql()

    @property
    def persistent(self) -> str:
        """
        https://duckdb.org/docs/sql/statements/create_secret.html#syntax-for-create-secret
        """
        return "PERSISTENT" if self._persistent else "TEMPORARY"

    @property
    def replace(self) -> str:
        return " OR REPLACE" if self._replace else ""

    @property
    def if_not_exists(self) -> str:
        return " IF NOT EXISTS" if self._if_not_exists else ""

    @property
    def keys(self) -> str:
        return ",\n  ".join(
            f"{key.upper()} '{value}'"
            for key, value in self._keys.items()
            if value is not None
        )

    @property
    def type(self) -> str:
        return self._type.upper()

    @property
    def name(self) -> str:
        return self._name

    def to_sql(self) -> str:
        """
        Generate CREATE SECRET syntax in SQL
        https://duckdb.org/docs/sql/statements/create_secret.html
        """
        return textwrap.dedent(
            f"""
CREATE{self.replace} {self.persistent} SECRET{self.if_not_exists} {self.name} (
  TYPE {self.type}
  {self.keys}
);""".strip()
        )
