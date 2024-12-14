"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Dict, Any
from datetime import datetime, UTC
from aws_lambda_powertools import Logger
from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
    IntegrationTestFactory,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_configurations import (
    TestConfiguration,
)

logger = Logger(service="IntegrationTestSuite")


class IntegrationTestSuite:
    """Runs Tests against an active instance"""

    def __init__(self):
        self.test_results: List[Dict[str, Any]] = []
        self.verbose: bool = False
        self.raise_on_failure: bool = False
        self.fail_fast: bool = False

    def test(self, test_config: TestConfiguration) -> bool:
        """Run a full suite of integration tests"""

        # reset the test results
        self.test_results = []

        start_time: datetime = datetime.now(UTC)
        factory: IntegrationTestFactory = IntegrationTestFactory()
        test: IntegrationTestBase | None = None
        for test in factory.test_instances:
            test.config = test_config
            test_result: Dict[str, Any] = {
                "test_name": test.name,
                "success": True,
                "error": None,
                "skipped": False,
                "start_time_utc": None,
                "end_time_utc": None,
            }

            logger.info(f"Running test class {test.name}")
            try:
                test_result["start_time_utc"] = datetime.now(UTC)
                success = test.test()
                test_result["success"] = success
                test_result["results"] = test.results

            except Exception as e:  # pylint: disable=broad-except
                test_result["success"] = False
                test_result["error"] = str(e)
                if self.fail_fast:
                    # just break and let the failure routine handle it
                    break

            test_result["end_time_utc"] = datetime.now(UTC)
            self.test_results.append(test_result)

            if test_result["success"]:
                logger.info(f"Test {test.name} succeeded")
                logger.debug(test_result)
            else:
                logger.error(test_result)
        # find the failures
        failures = [test for test in self.test_results if not test["success"]]
        self.__print_results(start_time, failures)

        # print the results

        if self.raise_on_failure and len(failures) > 0:
            count = len(failures)
            logger.error(f"{count} tests failed. Raising exception.")
            raise RuntimeError(f"{count} tests failed")

        return len(failures) == 0

    def __print_results(self, start_time: datetime, failures: List[Dict[str, Any]]):
        print("Test Results:")
        for test_result in self.test_results:
            duration = test_result["end_time_utc"] - test_result["start_time_utc"]
            print(
                f"  {test_result['test_name']} {'succeeded' if test_result['success'] else 'failed'} duration: {duration}"
            )
            if not test_result["success"]:
                print(f"    Error: {test_result['error']}")

        print(f"Test Suite completed in {datetime.now(UTC) - start_time}")

        print(f"Total Tests: {len(self.test_results)}")
        print(f"Successful Tests: {len(self.test_results) - len(failures)}")
        print(f"Failed Tests: {len(failures)}")
        print(
            f"Skipped Tests: {len([test for test in self.test_results if test['skipped']])}"
        )
