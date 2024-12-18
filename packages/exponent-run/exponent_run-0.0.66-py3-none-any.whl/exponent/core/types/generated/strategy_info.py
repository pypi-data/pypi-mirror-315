# Auto-generated, do not edit directly. Run `make generate_strategy_info` to update.

import enum

from pydantic import BaseModel

from exponent.core.remote_execution.types import ChatMode


class StrategyName(str, enum.Enum):
    NATURAL_EDIT = "NATURAL_EDIT"
    NATURAL_EDIT_EXPERIMENTAL = "NATURAL_EDIT_EXPERIMENTAL"
    FULL_FILE_REWRITE = "FULL_FILE_REWRITE"
    STREAMING_NATURAL_EDIT = "STREAMING_NATURAL_EDIT"
    FUNCTION_CALLING = "FUNCTION_CALLING"
    RAW_GPT = "RAW_GPT"
    STRICT_NATURAL_EDIT = "STRICT_NATURAL_EDIT"
    AGENT = "AGENT"


class StrategyInfo(BaseModel):
    strategy_name: StrategyName
    display_name: str
    description: str
    disabled: bool
    display_order: int


CHAT_MODE_DEFAULTS: dict[ChatMode, StrategyName] = {
    ChatMode.DEFAULT: StrategyName.RAW_GPT,
    ChatMode.CLI: StrategyName.NATURAL_EDIT,
    ChatMode.CLOUD: StrategyName.NATURAL_EDIT,
    ChatMode.PYTHON_INTERPRETER: StrategyName.NATURAL_EDIT,
}

STRATEGY_INFO_LIST: list[StrategyInfo] = [
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT,
        display_name="Natural Edit",
        description="A natural file editing strategy.",
        disabled=False,
        display_order=0,
    ),
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT_EXPERIMENTAL,
        display_name="Natural Edit Experimental",
        description="A natural file editing strategy.",
        disabled=True,
        display_order=0,
    ),
    StrategyInfo(
        strategy_name=StrategyName.STREAMING_NATURAL_EDIT,
        display_name="Streaming Natural Edit",
        description="A natural file editing strategy that streams edits.",
        disabled=True,
        display_order=1,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=False,
        display_order=2,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FUNCTION_CALLING,
        display_name="Function Calling",
        description="No description",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.RAW_GPT,
        display_name="Raw GPT",
        description="No description",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.STRICT_NATURAL_EDIT,
        display_name="Natural Edit No FFR",
        description="A natural file editing strategy that does not use full file rewrites.",
        disabled=True,
        display_order=99,
    ),
    StrategyInfo(
        strategy_name=StrategyName.AGENT,
        display_name="Agent",
        description="No description",
        disabled=True,
        display_order=99,
    ),
]


ENABLED_STRATEGY_INFO_LIST: list[StrategyInfo] = [
    StrategyInfo(
        strategy_name=StrategyName.NATURAL_EDIT,
        display_name="Natural Edit",
        description="A natural file editing strategy.",
        disabled=False,
        display_order=0,
    ),
    StrategyInfo(
        strategy_name=StrategyName.FULL_FILE_REWRITE,
        display_name="Full File Rewrites",
        description="Rewrites the full file every time. Use this if your files are generally less than 300 lines.",
        disabled=False,
        display_order=2,
    ),
]
