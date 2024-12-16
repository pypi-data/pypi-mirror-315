import typing_extensions

from segnivo.paths import PathValues
from segnivo.apis.paths.relay_send import RelaySend
from segnivo.apis.paths.relay_raw import RelayRaw
from segnivo.apis.paths.relay_emails_id import RelayEmailsId
from segnivo.apis.paths.validate_email import ValidateEmail
from segnivo.apis.paths.messages import Messages
from segnivo.apis.paths.messages_uid import MessagesUid
from segnivo.apis.paths.messages_uid_pause import MessagesUidPause
from segnivo.apis.paths.messages_uid_resume import MessagesUidResume
from segnivo.apis.paths.messages_uid_delete import MessagesUidDelete
from segnivo.apis.paths.contacts import Contacts
from segnivo.apis.paths.contacts_uid import ContactsUid
from segnivo.apis.paths.contacts_uid_add_tag import ContactsUidAddTag
from segnivo.apis.paths.contacts_uid_subscribe import ContactsUidSubscribe
from segnivo.apis.paths.contacts_uid_unsubscribe import ContactsUidUnsubscribe
from segnivo.apis.paths.contacts_uid_delete import ContactsUidDelete
from segnivo.apis.paths.lists import Lists
from segnivo.apis.paths.lists_uid import ListsUid
from segnivo.apis.paths.lists_uid_add_field import ListsUidAddField
from segnivo.apis.paths.lists_uid_delete import ListsUidDelete

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.RELAY_SEND: RelaySend,
        PathValues.RELAY_RAW: RelayRaw,
        PathValues.RELAY_EMAILS_ID: RelayEmailsId,
        PathValues.VALIDATEEMAIL: ValidateEmail,
        PathValues.MESSAGES: Messages,
        PathValues.MESSAGES_UID: MessagesUid,
        PathValues.MESSAGES_UID_PAUSE: MessagesUidPause,
        PathValues.MESSAGES_UID_RESUME: MessagesUidResume,
        PathValues.MESSAGES_UID_DELETE: MessagesUidDelete,
        PathValues.CONTACTS: Contacts,
        PathValues.CONTACTS_UID: ContactsUid,
        PathValues.CONTACTS_UID_ADDTAG: ContactsUidAddTag,
        PathValues.CONTACTS_UID_SUBSCRIBE: ContactsUidSubscribe,
        PathValues.CONTACTS_UID_UNSUBSCRIBE: ContactsUidUnsubscribe,
        PathValues.CONTACTS_UID_DELETE: ContactsUidDelete,
        PathValues.LISTS: Lists,
        PathValues.LISTS_UID: ListsUid,
        PathValues.LISTS_UID_ADDFIELD: ListsUidAddField,
        PathValues.LISTS_UID_DELETE: ListsUidDelete,
    }
)

path_to_api = PathToApi(
    {
        PathValues.RELAY_SEND: RelaySend,
        PathValues.RELAY_RAW: RelayRaw,
        PathValues.RELAY_EMAILS_ID: RelayEmailsId,
        PathValues.VALIDATEEMAIL: ValidateEmail,
        PathValues.MESSAGES: Messages,
        PathValues.MESSAGES_UID: MessagesUid,
        PathValues.MESSAGES_UID_PAUSE: MessagesUidPause,
        PathValues.MESSAGES_UID_RESUME: MessagesUidResume,
        PathValues.MESSAGES_UID_DELETE: MessagesUidDelete,
        PathValues.CONTACTS: Contacts,
        PathValues.CONTACTS_UID: ContactsUid,
        PathValues.CONTACTS_UID_ADDTAG: ContactsUidAddTag,
        PathValues.CONTACTS_UID_SUBSCRIBE: ContactsUidSubscribe,
        PathValues.CONTACTS_UID_UNSUBSCRIBE: ContactsUidUnsubscribe,
        PathValues.CONTACTS_UID_DELETE: ContactsUidDelete,
        PathValues.LISTS: Lists,
        PathValues.LISTS_UID: ListsUid,
        PathValues.LISTS_UID_ADDFIELD: ListsUidAddField,
        PathValues.LISTS_UID_DELETE: ListsUidDelete,
    }
)
