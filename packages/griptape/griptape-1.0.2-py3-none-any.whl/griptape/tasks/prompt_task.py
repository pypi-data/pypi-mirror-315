from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Optional, Union

from attrs import Factory, define, field

from griptape.artifacts import BaseArtifact, ListArtifact, TextArtifact
from griptape.common import PromptStack
from griptape.configs import Defaults
from griptape.mixins.rule_mixin import RuleMixin
from griptape.rules import Ruleset
from griptape.tasks import BaseTask
from griptape.utils import J2

if TYPE_CHECKING:
    from griptape.drivers import BasePromptDriver

logger = logging.getLogger(Defaults.logging_config.logger_name)


@define
class PromptTask(RuleMixin, BaseTask):
    prompt_driver: BasePromptDriver = field(
        default=Factory(lambda: Defaults.drivers_config.prompt_driver), kw_only=True
    )
    generate_system_template: Callable[[PromptTask], str] = field(
        default=Factory(lambda self: self.default_generate_system_template, takes_self=True),
        kw_only=True,
    )
    _input: Union[str, list, tuple, BaseArtifact, Callable[[BaseTask], BaseArtifact]] = field(
        default=lambda task: task.full_context["args"][0] if task.full_context["args"] else TextArtifact(value=""),
        alias="input",
    )

    @property
    def rulesets(self) -> list:
        default_rules = self.rules
        rulesets = self._rulesets.copy()

        if self.structure is not None:
            if self.structure._rulesets:
                rulesets = self.structure._rulesets + self._rulesets
            if self.structure.rules:
                default_rules = self.structure.rules + self.rules

        if default_rules:
            rulesets.append(Ruleset(name=self.DEFAULT_RULESET_NAME, rules=default_rules))

        return rulesets

    @property
    def input(self) -> BaseArtifact:
        return self._process_task_input(self._input)

    @input.setter
    def input(self, value: str | list | tuple | BaseArtifact | Callable[[BaseTask], BaseArtifact]) -> None:
        self._input = value

    output: Optional[BaseArtifact] = field(default=None, init=False)

    @property
    def prompt_stack(self) -> PromptStack:
        stack = PromptStack()
        memory = self.structure.conversation_memory if self.structure is not None else None

        system_template = self.generate_system_template(self)
        if system_template:
            stack.add_system_message(system_template)

        stack.add_user_message(self.input)

        if self.output:
            stack.add_assistant_message(self.output)

        if memory is not None:
            # insert memory into the stack right before the user messages
            memory.add_to_prompt_stack(self.prompt_driver, stack, 1 if system_template else 0)

        return stack

    def default_generate_system_template(self, _: PromptTask) -> str:
        return J2("tasks/prompt_task/system.j2").render(
            rulesets=J2("rulesets/rulesets.j2").render(rulesets=self.rulesets),
        )

    def before_run(self) -> None:
        super().before_run()

        logger.info("%s %s\nInput: %s", self.__class__.__name__, self.id, self.input.to_text())

    def after_run(self) -> None:
        super().after_run()

        logger.info(
            "%s %s\nOutput: %s",
            self.__class__.__name__,
            self.id,
            self.output.to_text() if self.output is not None else "",
        )

    def try_run(self) -> BaseArtifact:
        message = self.prompt_driver.run(self.prompt_stack)

        return message.to_artifact()

    def _process_task_input(
        self,
        task_input: str | tuple | list | BaseArtifact | Callable[[BaseTask], BaseArtifact],
    ) -> BaseArtifact:
        if isinstance(task_input, TextArtifact):
            task_input.value = J2().render_from_string(task_input.value, **self.full_context)

            return task_input
        elif isinstance(task_input, Callable):
            return self._process_task_input(task_input(self))
        elif isinstance(task_input, ListArtifact):
            return ListArtifact([self._process_task_input(elem) for elem in task_input.value])
        elif isinstance(task_input, BaseArtifact):
            return task_input
        elif isinstance(task_input, (list, tuple)):
            return ListArtifact([self._process_task_input(elem) for elem in task_input])
        else:
            return self._process_task_input(TextArtifact(task_input))
