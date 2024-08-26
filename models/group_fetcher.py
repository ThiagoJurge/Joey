import json

class GroupFetcher:
    def __init__(self, json_path):
        self.json_path = json_path
        self.groups = self.load_groups()

    def load_groups(self):
        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def find_group_by_name(self, name):
        for group in self.groups:
            if name in group["group_name"]:
                return group
        return None
