# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from segnivo.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    RELAY_SEND = "/relay/send"
    RELAY_RAW = "/relay/raw"
    RELAY_EMAILS_ID = "/relay/emails/{id}"
    VALIDATEEMAIL = "/validate-email"
    MESSAGES = "/messages"
    MESSAGES_UID = "/messages/{uid}"
    MESSAGES_UID_PAUSE = "/messages/{uid}/pause"
    MESSAGES_UID_RESUME = "/messages/{uid}/resume"
    MESSAGES_UID_DELETE = "/messages/{uid}/delete"
    CONTACTS = "/contacts"
    CONTACTS_UID = "/contacts/{uid}"
    CONTACTS_UID_ADDTAG = "/contacts/{uid}/add-tag"
    CONTACTS_UID_SUBSCRIBE = "/contacts/{uid}/subscribe"
    CONTACTS_UID_UNSUBSCRIBE = "/contacts/{uid}/unsubscribe"
    CONTACTS_UID_DELETE = "/contacts/{uid}/delete"
    LISTS = "/lists"
    LISTS_UID = "/lists/{uid}"
    LISTS_UID_ADDFIELD = "/lists/{uid}/add-field"
    LISTS_UID_DELETE = "/lists/{uid}/delete"
