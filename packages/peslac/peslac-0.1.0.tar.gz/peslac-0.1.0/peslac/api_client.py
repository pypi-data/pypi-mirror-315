import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .config import BASE_URL

class Peslac:
    def __init__(self, api_key, base_url=BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _request(self, method, endpoint, data=None, files=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method, url, headers=self.headers, data=data, files=files
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")

    def retrieve_document(self, document_id):
        return self._request("GET", f"/documents/{document_id}")

    def use_tool(self, file_path, tool_id):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as file:
            multipart_data = MultipartEncoder(
                fields={
                    "file": (os.path.basename(file_path), file),
                    "tool_id": tool_id,
                }
            )
            headers = {**self.headers, "Content-Type": multipart_data.content_type}
            response = requests.post(
                f"{self.base_url}/tools/use",
                headers=headers,
                data=multipart_data,
            )
            response.raise_for_status()
            return response.json()

    def use_tool_with_file_url(self, file_url, tool_id):
        data = {"fileUrl": file_url, "tool_id": tool_id}
        return self._request("POST", "/tools/use-url", data=data)

    def submit_bank_statement(self, file_path, type_of_account, currency):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as file:
            multipart_data = MultipartEncoder(
                fields={
                    "file": (os.path.basename(file_path), file),
                    "type_of_account": type_of_account,
                    "currency": currency,
                }
            )
            headers = {**self.headers, "Content-Type": multipart_data.content_type}
            response = requests.post(
                f"{self.base_url}/bank-statements/pdf",
                headers=headers,
                data=multipart_data,
            )
            response.raise_for_status()
            return response.json()

    def retrieve_bank_statement(self, document_id):
        if not document_id:
            raise ValueError("Document ID is required")
        return self._request("GET", f"/bank-statements/{document_id}")
