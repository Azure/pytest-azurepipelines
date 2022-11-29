"""Handles interactions with the Azure DevOps pull request threads API"""

import os

import requests


class PullRequestDecorator:
    """Takes care of managing comment threads under pull requests that are generated from warnings during pytest runs"""

    def __init__(self, max_comments: int):
        self._pr_comment_thread_api_url = "/".join(
            (
                os.environ["SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"].strip("/"),
                os.environ["SYSTEM_TEAMPROJECTID"].strip("/"),
                "_apis/git/repositories",
                os.environ["BUILD_REPOSITORY_NAME"].strip("/"),
                "pullRequests",
                os.environ["SYSTEM_PULLREQUEST_PULLREQUESTID"].strip("/"),
                "threads"
            )
        )

        self._query_params = {
            "api-version": 5.1
        }
        self._n_comments_added = 0
        token = os.environ["SYSTEM_ACCESSTOKEN"]
        self._http_session = requests.Session()
        self._http_session.headers.update(
            {"Authorization": f"Bearer {token}"}
        )
        self._build_number = os.environ["BUILD_BUILDNUMBER"]
        self._max_comments = max_comments

    def add_comment(self, warning_message):
        """Adds a new comment thread under a PR"""
        if self._n_comments_added < self._max_comments:
            try:
                category = warning_message.category.__name__
            except AttributeError:
                category = str(warning_message.category)

            content = (
                f"message : {warning_message.message}\n"
                f"category : {category}\n"
                f"filename : {warning_message.filename}\n"
                f"lineno : {warning_message.lineno}"
            )
            msg = f"pytest_azurepipelines: Warning occurred during build {self._build_number}:\n\n{content}"
        elif self._n_comments_added == self._max_comments:
            msg = (
                f"pytest_azurepipelines: More warnings occurred during build {self._build_number}. "
                f"Please check the logs."
            )
        else:
            return

        payload = {
            "comments": [
                {
                    "content": msg,
                    "parentCommentId": 1,
                    "commentType": "text"
                },
            ],
            # we are using these properties to identify which comments we need to remove before a new pytest run
            # in a new build
            "properties": {
                "createdBy": "pytest_azurepipelines",
                "buildNumber": self._build_number
            },
            "status": "active"
        }
        resp = self._http_session.post(
            self._pr_comment_thread_api_url,
            json=payload,
            params=self._query_params
        )
        if not resp.ok:
            raise RuntimeError(f"Could not add comment to pull request. API returned {resp.text}")

        self._n_comments_added += 1

    def _delete_thread(self, thread):
        """Deletes a thread of comments under a PR"""

        thread_id = thread["id"]
        for comment in thread["comments"]:
            comment_id = comment["id"]
            resp = self._http_session.delete(
                f"{self._pr_comment_thread_api_url}/{thread_id}/comments/{comment_id}",
                params=self._query_params
            )
            if not resp.ok:
                raise RuntimeError(
                    f"Purging comments about warnings in previous runs failed. API returned {resp.text}"
                )

    def purge(self):
        """Scans for all threads under the given PR generated by this tool and removes those with different build
        number"""

        resp = self._http_session.get(
            self._pr_comment_thread_api_url,
            params=self._query_params
        )
        if not resp.ok:
            raise RuntimeError(
                f"Purging comments about warnings in previous runs failed. API returned {resp.text}"
            )
        current_threads = resp.json()

        for thread in current_threads["value"]:
            try:
                already_deleted = thread["isDeleted"]
                build_number = thread["properties"]["buildNumber"]["$value"]
                created_by = thread["properties"]["createdBy"]["$value"]
                if not already_deleted and created_by == "pytest_azurepipelines" and build_number != self._build_number:
                    self._delete_thread(thread)
            except KeyError:
                # if the fields that we are trying to access are not present, this means that the comment has not been
                # created by this tool, so we can ignore it
                pass
