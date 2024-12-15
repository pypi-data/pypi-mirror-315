# Copyright 2020-2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Profiler Schedule"""
from enum import Enum

from mindspore import log as logger

__all__ = ["ProfilerAction", "Schedule"]


class ProfilerAction(Enum):
    """
    Enum class representing different actions that can be performed by the profiler.

    Each member of the enum represents a specific profiling action, which can be used
    to control the behavior of the profiler at different stages of execution.

    Attributes:
        NONE (ProfilerAction): No profiling action.
        WARM_UP (ProfilerAction): Warm-up phase of profiling.
        RECORD (ProfilerAction): Record phase of profiling.
        RECORD_AND_SAVE (ProfilerAction): Record and save phase of profiling.
    """
    NONE = 0
    WARM_UP = 1
    RECORD = 2
    RECORD_AND_SAVE = 3

    @staticmethod
    def get_by_value(value):
        """
        Retrieves a ProfilerAction enum member by its value.

        Args:
            value (int): The value of the ProfilerAction enum member to retrieve.

        Returns:
            ProfilerAction: The enum member corresponding to the given value, or None if not found.
        """
        value_map = {action.value: action for action in ProfilerAction}
        return value_map.get(value, None)


class Schedule:
    """
    Schedule class use to get the actions of each step
    The schedule is as follows:
    (NONE)        (NONE)            (NONE)       (WARM_UP)       (RECORD)      (RECORD)        (RECORD_AND_SAVE)    None
    START-------->skip_first-------->wait-------->warm_up-------->active........active.........active-------------->stop
                                    |                                                               |
                                    |                           repeat_1                            |
                                    ----------------------------------------------------------------
    details:
    The profiler will skip the first ``skip_first`` steps, then wait for ``wait`` steps,
    then do the warm_up for the next ``warm_up`` steps, then do the active recording for the next
    ``active`` steps and then repeat the cycle starting with ``wait`` steps. The optional number
    of cycles is specified with the ``repeat`` parameter, the zero value means that
    the cycles will continue until the profiling is finished.
    """

    def __init__(self, *, wait: int, active: int, warm_up: int = 0, repeat: int = 0, skip_first: int = 0) -> None:
        self.wait = wait
        self.active = active
        self.warm_up = warm_up
        self.repeat = repeat
        self.skip_first = skip_first
        self._check_params()

    def __call__(self, step: int) -> ProfilerAction:
        """
        Obtain the action of the specified step from the schedule

        Args:
            step: step num

        Returns:
            ProfilerAction: The action corresponding to a step
        """
        if step < 0:
            raise ValueError("Invalid parameter step, which must be not less than 0.")
        if step < self.skip_first:
            return ProfilerAction.NONE

        step -= self.skip_first

        num_steps = self.wait + self.warm_up + self.active
        if 0 < self.repeat <= step / num_steps:
            return ProfilerAction.NONE

        mod_step = step % num_steps
        if mod_step < self.wait:
            return ProfilerAction.NONE
        if mod_step < self.wait + self.warm_up:
            return ProfilerAction.WARM_UP
        return ProfilerAction.RECORD if mod_step < num_steps - 1 else ProfilerAction.RECORD_AND_SAVE

    def _check_params(self):
        """
        Verify all parameters in the schedule,
        and set them to default values if the parameters are not compliant
        """
        if not isinstance(self.wait, int) or self.wait < 0:
            logger.warning("Invalid parameter wait, reset it to 0.")
            self.wait = 0
        if not isinstance(self.warm_up, int) or self.warm_up < 0:
            logger.warning("Invalid parameter warm_up, reset it to 0.")
            self.warm_up = 0
        if not isinstance(self.active, int) or self.active <= 0:
            logger.warning("Invalid parameter active, reset it to 1.")
            self.active = 1
        if not isinstance(self.repeat, int) or self.repeat < 0:
            logger.warning("Invalid parameter repeat, reset it to 0.")
            self.repeat = 0
        if not isinstance(self.skip_first, int) or self.skip_first < 0:
            logger.warning("Invalid parameter skip_first, reset it to 0.")
            self.skip_first = 0
        if self.warm_up == 0:
            logger.warning("Profiler won't be using warmup, this can skew profiler results")

    def to_dict(self):
        """
        Convert the schedule class to a map

        Returns:
            Map: schedule map.
        """
        return {'wait': self.wait, 'active': self.active, 'warm_up': self.warm_up,
                'repeat': self.repeat, 'skip_first': self.skip_first}


def _default_schedule_fn(_: int) -> ProfilerAction:
    """
    Default profiler behavior - immediately starts recording the events,
    keeps doing it on every profiler step.

    Args:
        _: step num

    Returns:
        ProfilerAction: The RECORD action.
    """
    return ProfilerAction.RECORD
