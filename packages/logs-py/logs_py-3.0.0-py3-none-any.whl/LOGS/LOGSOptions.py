from dataclasses import dataclass


@dataclass
class LOGSOptions:
    showRequestUrl: bool = False
    showRequestBody: bool = False
    showServerInfo: bool = False
