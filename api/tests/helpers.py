def authenticate_as(client, username, password):
    token = client.post(
        "/auth/authenticate/", {"username": username, "password": password}
    ).data["token"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
