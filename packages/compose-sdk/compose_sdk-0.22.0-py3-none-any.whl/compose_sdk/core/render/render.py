import inspect
import datetime

from ..generator import display_none
from ..ui import INTERACTION_TYPE, TYPE
from ..file import File

from .validate import validate_static_layout
from .diff import diff_static_layouts


class Render:
    def validate_static_layout(layout):
        return validate_static_layout(layout)

    def diff_static_layouts(old_layout, new_layout):
        return diff_static_layouts(old_layout, new_layout)

    def generate_static_layout(layout, resolver):
        executed = None

        if callable(layout):
            layout_params = inspect.signature(layout).parameters
            kwargs = {}
            if "resolve" in layout_params:
                kwargs["resolve"] = resolver
            executed = layout(**kwargs)
        else:
            executed = layout

        if executed is None:
            return display_none()

        return executed

    def find_component_by_id(static_layout, component_id):
        if static_layout["model"]["id"] == component_id:
            return static_layout

        if static_layout["interactionType"] == INTERACTION_TYPE.LAYOUT:
            children = (
                static_layout["model"]["children"]
                if isinstance(static_layout["model"]["children"], list)
                else [static_layout["model"]["children"]]
            )

            for child in children:
                found = Render.find_component_by_id(child, component_id)
                if found is not None:
                    return found

        return None

    def static_layout_without_ids(static_layout):
        new_layout = static_layout.copy()

        new_layout["model"] = new_layout["model"].copy()
        new_layout["model"]["id"] = None

        if new_layout["interactionType"] == INTERACTION_TYPE.LAYOUT:
            new_layout["model"]["children"] = [
                Render.static_layout_without_ids(child)
                for child in new_layout["model"]["children"]
            ]

        return new_layout

    async def run_hook_function(hook_function, *args):
        """
        Run a hook function with arguments.

        - If the hook function is a coroutine function, it will be awaited.
        - Checks how many arguments the hook function expects and provides the
          correct number of arguments to the hook function.
        """

        async def _run_hook_function(*arguments):
            if inspect.iscoroutinefunction(hook_function):
                return await hook_function(*arguments)
            else:
                return hook_function(*arguments)

        param_count = len(inspect.signature(hook_function).parameters)
        num_args = len(args)

        if param_count > num_args:
            raise Exception(
                f"hook function supplies {num_args} arguments, but {hook_function.__name__} function expects {param_count}."
            )

        return await _run_hook_function(*args[:param_count])

    def hydrate_form_data(form_data, component_tree, temp_files):
        hydrated = {}
        temp_files_to_delete = []

        for key, data in form_data.items():
            try:
                if (
                    isinstance(data, list)
                    and "fileId" in data[0]
                    and isinstance(data[0]["fileId"], str)
                ):
                    hydrated[key] = [
                        File(
                            temp_files[file["fileId"]],
                            file["fileName"],
                            file["fileType"],
                        )
                        for file in data
                    ]
                    temp_files_to_delete.extend([file["fileId"] for file in data])
                elif (
                    isinstance(data, dict)
                    and "value" in data
                    and "type" in data
                    and len(data) == 2
                ):
                    if data["type"] == TYPE.INPUT_DATE:
                        if data["value"] is None:
                            hydrated[key] = None
                        else:
                            hydrated[key] = datetime.date(
                                data["value"]["year"],
                                data["value"]["month"],
                                data["value"]["day"],
                            )
                    elif data["type"] == TYPE.INPUT_TIME:
                        if data["value"] is None:
                            hydrated[key] = None
                        else:
                            hydrated[key] = datetime.time(
                                data["value"]["hour"],
                                data["value"]["minute"],
                            )
                    elif data["type"] == TYPE.INPUT_DATE_TIME:
                        if data["value"] is None:
                            hydrated[key] = None
                        else:
                            hydrated[key] = datetime.datetime(
                                data["value"]["year"],
                                data["value"]["month"],
                                data["value"]["day"],
                                data["value"]["hour"],
                                data["value"]["minute"],
                            )
                    elif data["type"] == TYPE.INPUT_TABLE:
                        component = Render.find_component_by_id(component_tree, key)

                        if (
                            component is not None
                            and component["type"] == TYPE.INPUT_TABLE
                        ):
                            rows = [
                                component["model"]["properties"]["data"][idx]
                                for idx in data["value"]
                            ]
                            hydrated[key] = rows
                        else:
                            raise Exception(
                                "An error occurred while trying to hydrate a table input: could not find the table within the component tree"
                            )
                    else:
                        hydrated[key] = data["value"]
                else:
                    hydrated[key] = data
            except Exception:
                hydrated[key] = data

        return hydrated, temp_files_to_delete

    async def get_form_input_errors(form_data, static_layout):
        input_errors = {}
        has_errors = False

        for component_id, data in form_data.items():
            input_component = Render.find_component_by_id(static_layout, component_id)

            if (
                input_component is None
                or input_component["interactionType"] != INTERACTION_TYPE.INPUT
                or input_component["hooks"]["validate"] is None
            ):
                continue

            validator_func = input_component["hooks"]["validate"]
            validator_response = await Render.run_hook_function(validator_func, data)

            if isinstance(validator_response, str):
                has_errors = True
                input_errors[component_id] = validator_response
            elif validator_response is False:
                has_errors = True
                input_errors[component_id] = "Invalid value"

        if has_errors:
            return input_errors

        return None

    async def get_form_error(component, form_data):
        if component["hooks"]["validate"] is None:
            return None

        validator_func = component["hooks"]["validate"]
        validator_response = await Render.run_hook_function(validator_func, form_data)

        if isinstance(validator_response, str):
            return validator_response
        elif validator_response is False:
            return "Invalid value"

        return None
