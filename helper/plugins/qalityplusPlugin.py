import os
import json
import html
import base64
import requests
import tempfile
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from helper.plugins import PluginSpec


class QAlityPlusApiV1:

    def __init__(self, cycle_id):
        self.jira_base_url = os.getenv("SERVER_JIRA")
        self.qality_base_url = os.getenv("URL_QALITYPLUS")
        self.username = os.getenv("USER_EMAIL_JIRA")
        self.password = os.getenv("TOKEN_JIRA")
        self.cycle_id = cycle_id
        self.auth_header = self._generate_auth_header()
        self.context_jwt = self.get_context_jwt()
        self.test_cases = self.get_test_cases()

    def _generate_auth_header(self):
        auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return {
            "Authorization": f"Basic {auth}",
            "Accept": "application/json"
        }

    def get_context_jwt(self):
        url = f"{self.jira_base_url}/plugins/servlet/ac/com.soldevelo.apps.test_management_premium/test-cycles?classifier=json"
        response = requests.get(url, headers=self.auth_header)
        response.raise_for_status()
        return response.json().get("contextJwt")

    def get_test_cases(self):
        url = f"{self.qality_base_url}/testCycles/{self.cycle_id}?jwt={self.context_jwt}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("testCases", [])
    
    def get_test_execution_details(self, test_execution_id):
        url = f"{self.qality_base_url}/testExecutions/{test_execution_id}?jwt={self.context_jwt}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "testSteps": data.get("testSteps", []),
            "version_testSteps": data.get("version", {}).get("testSteps", [])
        }

    def capture_screenshot(self, context):
        screenshot_bytes = context.browser.get_screenshot_as_png()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_file.write(screenshot_bytes)
        temp_file.close()
        context.qality_screenshot_path = temp_file.name

    def upload_attachment(self, test_case_id, image_path):
        headers = self.auth_header.copy()
        headers["X-Atlassian-Token"] = "no-check"
        url = f"{self.jira_base_url}/rest/api/3/issue/{test_case_id}/attachments"
        with open(image_path, "rb") as file:
            files = [('file', ('test-file.png', file, 'image/png'))]
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
            return response.json()[0]["id"]

    def clean_html_text(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        raw_text = soup.get_text()
        return html.unescape(raw_text)

    def update_test_step_status(self, scenario_name, step_name, step_status, attachment_id):
        status_id_map = {"Passed": 61878, "Failed": 61879}

        for test_case in self.test_cases:
            test_execution = test_case.get("testExecution", {})
            if scenario_name in test_execution.get("name", ""):
                test_execution_id = test_execution["id"]
                test_steps = self.get_test_execution_details(test_execution_id)
                test_steps_name = test_steps["version_testSteps"]
                test_steps_id = test_steps["testSteps"]
                for test_step_name in test_steps_name:
                    result_text = self.clean_html_text(test_step_name.get("result", ""))
                    if step_name in result_text:
                        version_steps_id = test_step_name["id"]
                        for test_step_id in test_steps_id:
                            if test_step_id["testCaseStepId"] == version_steps_id:
                                attachments_string = json.dumps([{"id": str(attachment_id)}], separators=(",", ":"))
                                url = f"{self.qality_base_url}/testExecutionSteps/bulk?jwt={self.context_jwt}"
                                payload = [
                                    {
                                        "fields": {
                                            "comment": f"Resultado de la ejecución del test step: {step_status}",
                                            "statusId": status_id_map[step_status],
                                            "attachments": attachments_string
                                        },
                                        "id": test_step_id["id"]
                                    }
                                ]
                                headers = {"Content-Type": "application/json"}
                                response = requests.patch(url, headers=headers, json=payload)
                                response.raise_for_status()

    def update_test_case_status(self, scenario_name, status_name):
        status_id_map = {"Passed": 61878, "Failed": 61879}

        for test_case in self.test_cases:
            test_execution = test_case.get("testExecution", {})
            if scenario_name in test_execution.get("name", ""):
                test_execution_id = test_execution["id"]
                url = f"{self.qality_base_url}/testExecutions/{test_execution_id}?jwt={self.context_jwt}"
                payload = {
                    "fields": {
                        "comment": f"Resultado de la ejecución del test case: {status_name}",
                        "statusId": status_id_map[status_name]
                    }
                }
                headers = {"Content-Type": "application/json"}
                response = requests.patch(url, headers=headers, data=json.dumps(payload))
                response.raise_for_status()


class QAlityPlusPlugin:


    @PluginSpec.hookimpl
    def before_all(self, context):
        load_dotenv(dotenv_path='.env')
        cycle_id = os.getenv("QALITYPLUS_CYCLE_ID")
        if cycle_id:
            context.qality = QAlityPlusApiV1(cycle_id)

    @PluginSpec.hookimpl
    def before_feature(self, context, feature):
        context.feature_title = feature.name
        context.scenario_results = []

    @PluginSpec.hookimpl
    def after_step(self, context, step):
        is_qality_flag = os.getenv("USE_QALITYPLUS", "false").lower() == "true"
        if is_qality_flag:
            context.qality.capture_screenshot(context)
            status = "Passed" if step.status == "passed" else "Failed"
            try:
                for test_case in context.qality.test_cases:
                    if context.scenario.name in test_case.get("testExecution", {}).get("name", ""):
                        test_case_id = test_case["testCaseId"]
                        attachment_id = context.qality.upload_attachment(test_case_id, context.qality_screenshot_path)
                        context.qality.update_test_step_status(context.scenario.name, step.name, status, attachment_id)
                        break
            except Exception as e:
                print(f"[ERROR] Falló la actualización en QAlity Plus: {e}")
            finally:
                os.remove(context.qality_screenshot_path)
                del context.qality_screenshot_path

    @PluginSpec.hookimpl
    def after_scenario(self, context, scenario):
        is_qality_flag = os.getenv("USE_QALITYPLUS", "false").lower() == "true"
        if is_qality_flag:
            status = "Passed" if scenario.status == "passed" else "Failed"
            context.scenario_results.append((scenario.name, status))
            cycle_id = os.getenv("QALITYPLUS_CYCLE_ID")
            qality = QAlityPlusApiV1(cycle_id)
            try:
                qality.update_test_case_status(scenario.name, status)
            except Exception as e:
                print(f"[ERROR] Falló la actualización en QAlity Plus: {e}")
