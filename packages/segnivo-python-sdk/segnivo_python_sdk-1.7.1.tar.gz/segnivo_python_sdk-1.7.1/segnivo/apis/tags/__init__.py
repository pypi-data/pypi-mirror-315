# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from segnivo.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    RELAY_TRANSACTIONAL_EMAILS = "Relay Transactional Emails"
    EMAIL_ADDRESS_VERIFICATION = "Email Address Verification"
    EMAIL_CAMPAIGNS = "Email Campaigns"
    SUBSCRIBERS_CONTACTS = "Subscribers Contacts"
    MAILING_LISTS = "Mailing Lists"
    RELAY = "Relay"
