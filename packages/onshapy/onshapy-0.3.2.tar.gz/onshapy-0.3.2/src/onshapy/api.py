import json
from typing import Any, cast

import keyring
from requests import Response
from requests_oauthlib import OAuth2Session

from .models import Assembly, Document, Element, Part, PartStudio, Workspace
from .stl import STLExportSettings
from .urlinfo import UrlInfo


class API:
    CLIENT_ID: str = "VQE3LTA2DCJTBVOGTST4N2WX5UBV3SEMKDOT5QY="
    CLIENT_SECRET: str = "75OAMQGO2QNL77FHEG3P7KVAJK73FKPMGVT3DOZEN2YM72OGY22Q===="
    AUTH_URL: str = "https://oauth.onshape.com/oauth/authorize"
    TOKEN_URL: str = "https://oauth.onshape.com/oauth/token"
    BASE_URL: str = "https://cad.onshape.com/api/v10"

    _session: OAuth2Session
    _sessionName: str

    def __init__(self, sessionName: str = "onshapy"):
        self._sessionName = sessionName
        self._session = OAuth2Session(
            client_id=self.CLIENT_ID,
            redirect_uri="",
            auto_refresh_url=self.TOKEN_URL,
            auto_refresh_kwargs={
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
            },
            token_updater=self._storeToken,
            token=self._loadToken(),
        )

    def authorize(self) -> None:
        if self._session.authorized:
            self._refreshToken()
        else:
            self._reauthorize()

    def _reauthorize(self) -> None:
        authUri, _ = self._session.authorization_url(  # type: ignore
            url=self.AUTH_URL,
        )
        print('Go to "{}" to authorize.'.format(authUri))
        code = input("Enter the verification code here: ")
        self._session.fetch_token(  # type: ignore
            token_url=self.TOKEN_URL,
            code=code,
            include_client_id=True,
            client_secret=self.CLIENT_SECRET,
        )
        self._storeToken()

    def _refreshToken(self) -> None:
        token = self._currentToken()
        if token is None:
            return
        self._session.refresh_token(  # type: ignore
            token_url=self.TOKEN_URL,
            refresh_token=token["refresh_token"],
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
        )
        self._storeToken()

    def _currentToken(self) -> dict[str, Any] | None:
        token = self._session.token  # type: ignore
        if token is None:
            return None
        token = cast(dict[str, Any], token)
        return token

    def _storeToken(self) -> None:
        tokenJson = json.dumps(self._currentToken())
        keyring.set_password("onshapy", self._sessionName, tokenJson)

    def _loadToken(self) -> dict[str, Any] | None:
        tokenJson = keyring.get_password("onshapy", self._sessionName)
        if not isinstance(tokenJson, str):
            return None
        return json.loads(tokenJson)

    def _apiUri(self, path: str) -> str:
        path = path if path.startswith("/") else "/{}".format(path)
        return "{}{}".format(self.BASE_URL, path)

    def decodeUrl(self, url: str) -> UrlInfo:
        return UrlInfo(url)

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        urlIsPath: bool = True,
    ) -> Response:
        realUrl = self._apiUri(url) if urlIsPath else url
        print("GET: {}".format(realUrl))
        response = self._session.get(url=realUrl, params=params, allow_redirects=False)

        if response.status_code == 200:
            return response

        print("Status Code: {}".format(response.status_code))
        if response.status_code == 307:
            request = response.next
            if request is None or request.url is None:
                raise Exception()
            print("Redirect to: {}".format(request.url))
            return self.get(request.url, urlIsPath=False)

        raise Exception()

    def getJson(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        urlIsPath: bool = True,
    ) -> dict[str, Any] | list[Any]:
        response = self.get(url, params, urlIsPath)
        return response.json()

    def findDocuments(self, query: str) -> list[Document]:
        data = self.getJson(
            "/documents",
            {"filter": 0, "q": query},
        )
        if not isinstance(data, dict):
            raise Exception()
        return [Document(d) for d in data["items"]]

    def getDocument(self, documentId: str) -> Document:
        data = self.getJson("/documents/{}".format(documentId))
        if not isinstance(data, dict):
            raise Exception()
        return Document(data)

    def getWorkspaces(self, document: str | Document) -> list[Workspace]:
        documentId = document.id if isinstance(document, Document) else document
        data = self.getJson("/documents/d/{}/workspaces".format(documentId))
        if not isinstance(data, list):
            raise Exception()
        return [Workspace(d) for d in data]

    def getElements(
        self,
        document: str | Document,
        workspace: str | Workspace,
        type: str | None = None,
    ) -> list[Element]:
        url = "/documents/d/{d}/w/{w}/elements".format(
            d=document.id if isinstance(document, Document) else document,
            w=workspace.id if isinstance(workspace, Workspace) else workspace,
        )
        params: dict[str, Any] | None = {"type": type} if type else None
        data = self.getJson(url, params)
        if not isinstance(data, list):
            raise Exception()
        return [Element(d) for d in data]

    def getPartStudios(
        self,
        document: str | Document,
        workspace: str | Workspace,
    ) -> list[PartStudio]:
        return [
            PartStudio(e)
            for e in self.getElements(document, workspace, "PARTSTUDIO")
            if e.type == "PARTSTUDIO"
        ]

    def getAssemblies(
        self,
        document: str | Document,
        workspace: str | Workspace,
    ) -> list[Assembly]:
        return [
            Assembly(e)
            for e in self.getElements(document, workspace, "ASSEMBLY")
            if e.type == "ASSEMBLY"
        ]

    def getParts(
        self,
        document: str | Document,
        workspace: str | Workspace,
        element: str | Element,
    ) -> list[Part]:
        url = "/parts/d/{d}/w/{w}/e/{e}".format(
            d=document.id if isinstance(document, Document) else document,
            w=workspace.id if isinstance(workspace, Workspace) else workspace,
            e=element.id if isinstance(element, Element) else element,
        )
        data = self.getJson(url)
        if not isinstance(data, list):
            raise Exception()
        return [Part(d) for d in data]

    def getSTL(
        self,
        document: str | Document,
        workspace: str | Workspace,
        element: str | Element,
        settings: STLExportSettings,
    ) -> str | bytes:
        url = "/documents/d/{d}/w/{w}/e/{e}/export".format(
            d=document.id if isinstance(document, Document) else document,
            w=workspace.id if isinstance(workspace, Workspace) else workspace,
            e=element.id if isinstance(element, Element) else element,
        )
        params = settings.dict()
        response = self.get(url, params)
        return response.content
