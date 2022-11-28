import unittest
from unittest.mock import patch
import pr_decoration
import os
from copy import deepcopy
from warnings import WarningMessage

INITIAL_THREADS = {
    "value": [
        {
            "comments": [
                {"id": 1},
                {"id": 2},
                {"id": 3},
            ],
            "isDeleted": False,
            "id": 2,
            "properties": {
                "buildNumber": {"$value": "1"},
                "createdBy": {"$value": "not_pytest_azurepipelines"}
            },
            "status": "active"
        },
        {
            "comments": [
                {"id": 1},
                {"id": 2},
                {"id": 3},
            ],
            "isDeleted": False,
            "id": 3,
            "properties": {},
            "status": "active"
        }
    ]
}


class MockResponse:
    def __init__(self, data=None):
        self.ok = True
        self.data = data

    def json(self):
        return self.data


class MockSession:
    def __init__(self):
        self.max_comment_id = 0
        self.headers = {}
        self.threads = deepcopy(INITIAL_THREADS)

    def get(self, *args, **kwargs):
        return MockResponse(self.threads)

    def post(self, url, json, *args, **kwargs):
        self.max_comment_id += 1
        for i in range(len(json["comments"])):
            json["comments"][i]["id"] = i + 1
            json["comments"][i]["isDeleted"] = False

        self.threads["value"].append(
            {
                "comments": json["comments"],
                "isDeleted": False,
                "id": self.max_comment_id,
                "properties": {
                    "buildNumber": {"$value": json["properties"]["buildNumber"]},
                    "createdBy": {"$value": json["properties"]["createdBy"]}
                },
                "status": json["status"]
            }
        )
        return MockResponse()

    def delete(self, url, *args, **kwargs):
        elements = url.split("/")
        comment_id = int(elements[-1])
        thread_id = int(elements[-3])

        for thread_idx, thread in enumerate(self.threads["value"]):
            if thread["id"] == thread_id:
                print(f'thread: {thread["id"]} vs {thread_id}')
                deleted = []
                for comment_idx, comment in enumerate(thread["comments"]):
                    print(f'comment: {comment["id"]} vs {comment_id}')
                    if comment["id"] == comment_id:
                        self.threads["value"][thread_idx]["comments"][comment_idx]["isDeleted"] = True
                    deleted.append(comment["isDeleted"])
                self.threads["value"][thread_idx]["isDeleted"] = all(deleted)

        return MockResponse()


class PullRequestAnnotationTestCase(unittest.TestCase):
    env_patcher = None
    pr_decorator = None
    mock_session = None
    build_number = None
    pull_request_id = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.build_number = "42"
        cls.pull_request_id = "13"
        env_vars = {
            "SYSTEM_TEAMFOUNDATIONCOLLECTIONURI": "https://tfc.com",
            "SYSTEM_TEAMPROJECTID": "pid",
            "BUILD_REPOSITORY_NAME": "repo",
            "SYSTEM_PULLREQUEST_PULLREQUESTID": str(cls.pull_request_id),
            "SYSTEM_ACCESSTOKEN": "top_secret",
            "BUILD_BUILDNUMBER": cls.build_number
        }
        cls.mock_session = MockSession()
        cls.env_patcher = unittest.mock.patch.dict(os.environ, env_vars)
        cls.env_patcher.start()
        cls.pr_decorator = pr_decoration.PullRequestDecorator(10)
        cls.pr_decorator._http_session = cls.mock_session

    @classmethod
    def tearDownClass(cls) -> None:
        cls.env_patcher.stop()

    def test_lifecycle(self):
        with self.subTest("initial purge should not change anything"):
            self.pr_decorator.purge()
            self.assertEqual(INITIAL_THREADS, self.mock_session.threads)

        with self.subTest("test post a comment"):
            warning_message = WarningMessage(
                message="This is a test",
                category=RuntimeWarning,
                filename="testfilename",
                lineno=42
            )
            self.pr_decorator.add_comment(warning_message)

            content = (
                f"message : {warning_message.message}\n"
                f"category : {warning_message.category}\n"
                f"filename : {warning_message.filename}\n"
                f"lineno : {warning_message.lineno}\n"
                f"line : {warning_message.line}"
            )
            expected_message = f"pytest_azurepipelines: Warning occurred during build {self.build_number}:\n\n{content}"
            expected_threads = deepcopy(INITIAL_THREADS)
            expected_threads["value"].append(
                {
                    "comments": [
                        {
                            "content": expected_message,
                            "parentCommentId": 1,
                            "commentType": "text",
                            "id": 1,
                            "isDeleted": False,
                        }
                    ],
                    "isDeleted": False,
                    "id": self.mock_session.max_comment_id,
                    "properties": {
                        "createdBy": {"$value": "pytest_azurepipelines"},
                        "buildNumber": {"$value": self.build_number}
                    },
                    "status": "active"
                }
            )
            self.assertEqual(expected_threads, self.mock_session.threads)

        with self.subTest("should not purge created comments of this run"):
            self.pr_decorator.purge()
            expected_threads = deepcopy(INITIAL_THREADS)
            expected_threads["value"].append(
                {
                    "comments": [
                        {
                            "content": expected_message,
                            "parentCommentId": 1,
                            "commentType": "text",
                            "id": 1,
                            "isDeleted": False,
                        }
                    ],
                    "isDeleted": False,
                    "id": self.mock_session.max_comment_id,
                    "properties": {
                        "createdBy": {"$value": "pytest_azurepipelines"},
                        "buildNumber": {"$value": self.build_number}
                    },
                    "status": "active"
                }
            )
            self.assertEqual(expected_threads, self.mock_session.threads)

        with self.subTest("should purge created comments of different run"):
            self.pr_decorator._build_number = "43"
            self.pr_decorator.purge()
            expected_threads = deepcopy(INITIAL_THREADS)
            expected_threads["value"].append(
                {
                    "comments": [
                        {
                            "content": expected_message,
                            "parentCommentId": 1,
                            "commentType": "text",
                            "id": 1,
                            "isDeleted": True,
                        }
                    ],
                    "isDeleted": True,
                    "id": self.mock_session.max_comment_id,
                    "properties": {
                        "createdBy": {"$value": "pytest_azurepipelines"},
                        "buildNumber": {"$value": self.build_number}
                    },
                    "status": "active"
                }
            )
            self.assertEqual(expected_threads, self.mock_session.threads)
