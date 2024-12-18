from zenetics import TestSuiteRunner
from zenetics.model import TestCase


class MockAPIController:
    def get_testcases_by_testsuite(self, suite: str):
        return [
            TestCase(
                id=1,
                name="Test case 1",
                input="Input for test case 1",
                description="Description for test case 1",
                expected_output="Expected output for test case 1",
            ),
            TestCase(
                id=2,
                name="Test case 2",
                input="Input for test case 2",
                description="Description for test case 2",
                expected_output="Expected output for test case 2",
            ),
        ]


def simple_generate(input: str):
    return "Generated output from LLM model."


def test_test_suite_runner():
    suites = ["default"]
    runner = TestSuiteRunner(suites, MockAPIController())
    runner.run(simple_generate)
