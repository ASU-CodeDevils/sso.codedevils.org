from typing import Any, Dict, List, Optional, Tuple, Union

JWT = Tuple[str, str]


# Flameboi dict structuring
class SlackUserProfileDict(Dict):
    title: str
    phone: str
    skype: Optional[str]
    real_name: str
    real_name_normalized: Optional[str]
    display_name: Optional[str]
    display_name_normalized: Optional[str]
    fields: Optional[Union[List[Any], None]]
    status_text: str = ""
    status_emoji: str = ""
    status_expiration: int
    avatar_hash: str
    image_original: str
    is_custom_image: Optional[bool]
    email: str
    first_name: str
    last_name: str
    image_24: str
    image_32: str
    image_48: str
    image_72: str
    image_192: str
    image_512: str
    image_1024: str
    status_text_canonical: Optional[Union[str, None]]
    team: Union[str, None]


class SlackEnterpriseUserDict(Dict):
    id: str
    enterprise_id: str
    enterprise_name: str
    is_admin: bool
    is_owner: bool
    teams: Union[Dict[str, str], None]


class SlackUserDict(Dict):
    id: str
    team_id: str
    name: Optional[str]
    deleted: bool
    color: Optional[str]
    real_name: str
    tz: str
    tz_label: str
    tz_offset: int
    profile: SlackUserProfileDict
    is_admin: bool
    is_owner: bool
    is_primary_owner: bool
    is_restricted: bool
    is_ultra_restricted: bool
    is_bot: bool
    is_stranger: Optional[bool]
    is_invited_user: Optional[bool]
    is_app_user: Optional[bool]
    updated: Optional[int]
    has_2fa: Optional[bool]
    locale: Optional[str]


class SlackUserObject(Dict):
    """
    Defines a Slack user object. This is meant to directly replicate the user object defined by Slack
    and add which fields are optional for this project. You can see more information here:
    https://api.slack.com/types/user
    """

    ok: Optional[bool]
    user: SlackUserDict
    enterprise_user: Optional[SlackEnterpriseUserDict]
