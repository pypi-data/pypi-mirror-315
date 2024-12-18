from dataclasses import dataclass
from typing import Callable, List, Union

from zenetics.api_client import APIController


@dataclass
class GenerationData:
    output: str
    prompt: Union[str, None] = None
    retrieval_context: Union[List[str], None] = None


class TestSuiteRunnerException(Exception):
    pass


class TestSuiteRunner:

    def __init__(
        self, suites: List[str], api_controller: Union[APIController, None] = None
    ):
        self.suites = suites
        self.api_controller = api_controller or APIController()

    def run(self, generate: Callable) -> None:
        """
        @param generate: A Callable implementing the interface:

            def generate(input: str) -> Union[GenerationData, str]:
                pass
        """

        # TODO:
        # 1. Display nicely formatted report output
        # 2. Handle parallelism

        self._run_suites(generate)

    def _run_suites(self, generate: Callable):
        for suite in self.suites:
            self._run_suite(generate, suite)

    def _run_suite(self, generate, suite: str):
        tcs = self.api_controller.get_testcases_by_testsuite(suite)

        for tc in tcs:
            self._run_test_case(generate, tc)

    def _run_test_case(self, generate, tc):
        output = generate(tc.input)

        if not (isinstance(output, GenerationData) or isinstance(output, str)):
            raise TestSuiteRunnerException(
                "generate must return a GenerationData or str"
            )

        # TODO
        # Run evaluators assigns to this test suite
