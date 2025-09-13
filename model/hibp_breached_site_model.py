from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class HibpBreachedSiteModel(BaseModel):
    name: str
    title: str
    domain: str
    breach_date: str
    added_date: datetime
    modified_date: datetime
    pwn_count: int
    description: str
    logo_path: HttpUrl
    attribution: Optional[str] = None
    disclosure_url: Optional[HttpUrl] = None
    data_classes: List[str]
    is_verified: bool
    is_fabricated: bool
    is_sensitive: bool
    is_retired: bool
    is_spam_list: bool
    is_malware: bool
    is_subscription_free: bool
    is_stealer_log: bool

    model_config = {
        "populate_by_name": True,
        "alias_generator": lambda s: "".join(
            word.capitalize() for word in s.split("_")
        ),
    }
