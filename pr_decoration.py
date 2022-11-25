import os
from functools import reduce
from urllib.parse import urljoin

import requests


class PullRequestDecorator:

    def __init__(self):
        self._pr_comment_api_url = reduce(
            urljoin,
            (
                os.environ["SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"],
                os.environ["SYSTEM_TEAMPROJECTID"],
                "_apis/git/repositories/",
                os.environ["BUILD_REPOSITORY_NAME"],
                "pullRequests",
                os.environ["SYSTEM_PULLREQUEST_PULLREQUESTID"],
                "/threads?api-version=5.1"
            )
        )
        token = os.environ["SYSTEM_ACCESSTOKEN"]
        self._http_session = requests.Session()
        self._http_session.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

    def add_comment(self, content: str):
        payload = {
            "content": f"Warning occurred during unit tests:\n\n{content}",
            "parentCommentId": 1,
            "commentType": 1
        }
        resp = self._http_session.post(
            self._pr_comment_api_url,
            json=payload,
        )
        if not resp.ok:
            raise RuntimeError(f"Could not add comment to pull request. API returned {resp.text}")
