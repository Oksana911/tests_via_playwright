from typing import Any

from playwright.sync_api import Playwright, APIRequestContext

from settings import settings


class Client:
    login_url = 'login'

    def __init__(self, request_context: APIRequestContext):
        self.request_context = request_context

    @classmethod
    def get_client(
        cls,
        playwright: Playwright,
        authenticate: bool = False,
        admin: bool = True,
    ) -> 'Client':
        headers = {}
        request_context = playwright.request.new_context(base_url=settings.base_url)
        if authenticate:
            token = cls._get_token(request_context, admin)
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            request_context = playwright.request.new_context(
                base_url=settings.base_url,
                extra_http_headers=headers,
            )
        return cls(request_context)

    @staticmethod
    def _get_token(request_context, admin: bool):
        if admin:
            payload = {
                'username': settings.admin.username,
                'password': settings.admin.password,
            }
        else:
            payload = {
                'username': settings.user.username,
                'password': settings.user.password,
            }
        login_url = '/login'
        response = request_context.post(login_url, data=payload)
        assert response.ok, 'Ошибка получения токена.'
        token = response.json().get('access_token')
        assert token is not None
        return token

    def get(self, url, **kwargs):
        return self.request_context.get(url, **kwargs)

    def post(self, url, json: dict[str, Any] = {}, **kwargs):
        return self.request_context.post(url, data=json, **kwargs)

    def put(self, url, json: dict[str, Any], **kwargs):
        return self.request_context.put(url, data=json, **kwargs)

    def delete(self, url):
        return self.request_context.delete(url)

    def close(self):
        self.request_context.dispose()
