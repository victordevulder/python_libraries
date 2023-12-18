import requests
import json

class MicrosoftGraph:

    root = "https://graph.microsoft.com/v1.0"

    def __init__(self,tenant_id,client_id,client_secret) -> None:
        # URL de l'authentification et de l'obtention du jeton d'accès
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        # Paramètres de la demande d'autorisation client credentials
        auth_payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }
        # Obtention du jeton d'accès
        auth_response = requests.post(auth_url, data=auth_payload)
        auth_response_data = auth_response.json()
        # Extraction du jeton d'accès
        self.access_token = auth_response_data["access_token"]
        #print(self.access_token)

    def sendGetRequest(self,uri):
        headers = {
            "Accept": "application/json;odata.metadata=minimal",
            "Authorization": f"Bearer {self.access_token }"
        }
        url = self.root + uri
        response = requests.get(url, headers=headers)
        return response.json()
    
    def saveToJson(filename,data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def searchSites(self,research):
        uri = f"/sites?search={research}"
        body = self.sendGetRequest(uri)
        return body["value"]

    def getAllSites(self):
        uri = "/getAllSites"
        body = self.sendGetRequest(uri)
        return body["value"]
    
    def getItemsHeaders(self,siteId,listId):
        uri = f"/sites/{siteId}/lists/{listId}/items"
        body = self.sendGetRequest(uri)
        return body["value"]
    
    def getItemFields(self,siteId,listId,itemId):
        uri = f"/sites/{siteId}/lists/{listId}/items/{itemId}"
        item = self.sendGetRequest(uri)
        return item["fields"]

    def getItemsFields(self,siteId,listId):
        items = self.getItemsHeaders(siteId,listId)
        itemsWithFields = []
        for item in items:
            itemsWithFields.append(self.getItemFields(siteId,listId,item["id"]))
        return itemsWithFields