import requests


class RestUtility:
    def __init__(self, auth_server_url, authorization_header_constant, *, logger):
        self.auth_server_url = auth_server_url
        self.request_headers = {
            "Authorization": authorization_header_constant,
            "content-type": "application/json",
        }
        self.logger = logger

    def get_request(self, path_params=None, headers={}, data=None, cookies=None):
        server_url = self.auth_server_url
        if path_params:
            server_url += path_params
        self.logger.info(
            "Got <GET> Request for URL and Path Params: {}".format(server_url)
        )
        return requests.get(
            server_url,
            headers=headers,
            data=data,
            cookies=cookies,
        )

    def post_request(
        self, path_params=None, additional_headers={}, data=None, cookies=None
    ):
        # is it required to add validation for data is not None?

        server_url = self.auth_server_url
        if path_params:
            if not server_url.endswith("/"):
                server_url += "/"
            server_url += path_params

        if additional_headers:
            self.request_headers.update(additional_headers)

        self.logger.info("Got <POST> Request for URL: {}".format(self.auth_server_url))
        self.logger.debug(f"Final request route = {server_url}")
        self.logger.debug(f"Request Headers = {self.request_headers}")
        return requests.post(
            server_url,
            headers=self.request_headers,
            data=data,
            cookies=cookies,
        )
