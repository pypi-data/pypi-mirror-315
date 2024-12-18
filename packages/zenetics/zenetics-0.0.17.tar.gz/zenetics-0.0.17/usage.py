from typing import Union

from zenetics import TestSuiteRunner, GenerationData


def generate(input: str) -> Union[GenerationData, str]:
    return "Generated output from LLM model."


runner = TestSuiteRunner(["smoke"])
runner.run(generate)
