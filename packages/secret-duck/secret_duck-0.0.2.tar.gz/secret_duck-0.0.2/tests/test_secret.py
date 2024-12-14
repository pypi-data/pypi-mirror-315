from secret_duck.secret import Secret

import sqlfluff


def test_secret():
    secret = Secret("my_secret", secret_type="s3")

    sql = str(secret)
