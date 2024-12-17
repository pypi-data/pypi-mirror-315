from RVCapture.configManage import ConfigStore

class AuthKeys:
    def __init__(self):
        self.config = ConfigStore()
        self.keys = self.config.getConfig("authKeys") or {}
        self.config.setConfig("authKeys", self.keys)  # Ensure persistence
        
        self.selectedKeyAlias = self.config.getConfig("selectedKeyAlias")
        if not self.selectedKeyAlias:
            self.selectedKeyAlias = next(iter(self.keys), None)
            self.config.setConfig("selectedKeyAlias", self.selectedKeyAlias)

    def addKey(self, alias, accessKey, accessID):
        self.keys[alias] = {"accessKey": accessKey, "accessID": accessID}
        self.config.setConfig("authKeys", self.keys)
        self.config.setConfig("selectedKeyAlias", alias)
    
    def getKey(self, alias):
        return self.keys.get(alias)

    def deleteKey(self, alias):
        if alias in self.keys:
            del self.keys[alias]
            self.config.setConfig("authKeys", self.keys)
            if self.selectedKeyAlias == alias:
                self.selectedKeyAlias = next(iter(self.keys), None)
                self.config.setConfig("selectedKeyAlias", self.selectedKeyAlias)
            return True
        return False

    def getAllAuthKeys(self):
        return self.keys

    def getSelectedKey(self):
        return self.keys.get(self.selectedKeyAlias)

    def setSelectedKey(self, alias):
        if alias in self.keys:
            self.selectedKeyAlias = alias
            self.config.setConfig("selectedKeyAlias", alias)
