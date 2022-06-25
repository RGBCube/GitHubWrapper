__all__ = ("SecurtiyAndAnalysis",)

from typing import Literal, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import NotRequired


class AdvancedSecurity(TypedDict):
    status: Literal["enabled", "disabled"]


class SecretScanning(TypedDict):
    status: Literal["enabled", "disabled"]


class SecretScanningPushProtection(TypedDict):
    status: Literal["enabled", "disabled"]


class SecurtiyAndAnalysis(TypedDict):
    advanced_security: NotRequired[AdvancedSecurity]
    secret_scanning: NotRequired[SecretScanning]
    secret_scanning_push_protection: NotRequired[SecretScanningPushProtection]
