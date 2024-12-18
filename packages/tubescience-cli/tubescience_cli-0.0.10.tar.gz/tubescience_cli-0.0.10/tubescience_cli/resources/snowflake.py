from pydantic import BaseModel, SecretStr


class SnowflakeResource(BaseModel):
    account: str = "ov02505.us-east-2.aws"
    warehouse: str = "ANALYTICS_WH"
    database: str = "RETOOL_DEV_DB"
    db_schema: str = "DAPPER"
    user: str = "RETOOL_USER"
    password: SecretStr = SecretStr("")

    def get_connection(self):
        import snowflake.connector

        return snowflake.connector.connect(
            user=self.user,
            password=self.password.get_secret_value(),
            account=self.account,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.db_schema,
        )

    def get_cursor(self):

        return self.get_connection().cursor()

    def get_dict_cursor(self):
        from snowflake.connector import DictCursor

        return self.get_connection().cursor(DictCursor)
