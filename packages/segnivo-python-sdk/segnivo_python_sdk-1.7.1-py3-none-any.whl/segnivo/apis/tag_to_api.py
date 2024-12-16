import typing_extensions

from segnivo.apis.tags import TagValues
from segnivo.apis.tags.relay_transactional_emails_api import RelayTransactionalEmailsApi
from segnivo.apis.tags.email_address_verification_api import EmailAddressVerificationApi
from segnivo.apis.tags.email_campaigns_api import EmailCampaignsApi
from segnivo.apis.tags.subscribers_contacts_api import SubscribersContactsApi
from segnivo.apis.tags.mailing_lists_api import MailingListsApi
from segnivo.apis.tags.relay_api import RelayApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.RELAY_TRANSACTIONAL_EMAILS: RelayTransactionalEmailsApi,
        TagValues.EMAIL_ADDRESS_VERIFICATION: EmailAddressVerificationApi,
        TagValues.EMAIL_CAMPAIGNS: EmailCampaignsApi,
        TagValues.SUBSCRIBERS_CONTACTS: SubscribersContactsApi,
        TagValues.MAILING_LISTS: MailingListsApi,
        TagValues.RELAY: RelayApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.RELAY_TRANSACTIONAL_EMAILS: RelayTransactionalEmailsApi,
        TagValues.EMAIL_ADDRESS_VERIFICATION: EmailAddressVerificationApi,
        TagValues.EMAIL_CAMPAIGNS: EmailCampaignsApi,
        TagValues.SUBSCRIBERS_CONTACTS: SubscribersContactsApi,
        TagValues.MAILING_LISTS: MailingListsApi,
        TagValues.RELAY: RelayApi,
    }
)
