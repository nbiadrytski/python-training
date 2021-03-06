class JSONFixture:

    @staticmethod
    def for_create_issue(project_key):
        json = {
            "fields": {
                "project":
                    {
                        "key": project_key
                    },
                "summary": "Test Summary",
                "description": "Creating of an issue",
                "assignee": {"name": "webinar5"},
                "priority": {"name": "High"},
                "issuetype": {"name": "Bug"}
            }
        }
        return json
