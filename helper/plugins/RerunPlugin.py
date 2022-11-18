from helper.plugins import PluginSpec
import os
import json


def rerun_script():
    print("RERUN EXECUTION")
    # EXECUTION OF RERUN SCRIPT
    # text_command='behave -t "'
    text_command = 'behave -f allure_behave.formatter:AllureFormatter -o reporte -t "'
    counter = os.getenv("COUNT")
    total_repeat = os.getenv("REPEAT")
    if counter < total_repeat and os.getenv("EXECUTE_RERUN") == "true":
        i = 0
        scenarios_to_rerun = os.getenv(
            "FAILED_SCENARIO_ARRAY").replace("'", '"')
        print(scenarios_to_rerun)
        scenarios_to_rerun = json.loads(scenarios_to_rerun)
        print("escenarios to re run ", scenarios_to_rerun)
        for scen in scenarios_to_rerun:
            if i == len(scenarios_to_rerun) - 1:
                text_command = text_command + ' @' + scen + '"'
            else:
                text_command = text_command + ' @' + scen + ','
            i += 1
        print("antes de ejecutar " + text_command)
        os.environ["COUNT"] = str(int(counter) + 1)
        os.system(text_command)
        print("despues de ejecutar")


class RerunPlugin:
    """A hook implementation namespace."""

    @PluginSpec.hookimpl
    def after_all(self):
        if os.getenv("EXECUTE_RERUN") == "true":
            rerun_script()

    @PluginSpec.hookimpl
    def after_scenario(self, scenario):
        scenarios = []
        if os.getenv("EXECUTE_RERUN") == "true":
            if scenario.status == "failed":
                scenarios.append(scenario.tags[0])
            os.environ["FAILED_SCENARIO_ARRAY"] = str(scenarios)
