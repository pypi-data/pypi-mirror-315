from dataclasses import dataclass


@dataclass
class AdFeatures:
    creative_url: str
    script: str
    transcript: str
    thumbnail_url: str
    creative_title: str
    creative_body: str
    call_to_action: str
