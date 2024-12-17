import httpx
from connector.generated import OAuthCredential
from connector.oai.capability import CapabilityName
from connector.oai.errors import HTTPHandler
from connector.oai.integration import DescriptionData, Integration

from {name}.__about__ import __version__
from {name}.enums import entitlement_types, resource_types
from {name}.settings import {pascal}Settings
from {name} import capabilities_read, capabilities_write


integration = Integration(
    app_id="{hyphenated_name}",
    version=__version__,
    auth=OAuthCredential,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
    description_data=DescriptionData(
        logo_url="", user_friendly_name="{pascal}", description="", categories=[]
    ),
    settings_model={pascal}Settings,
    resource_types=resource_types,
    entitlement_types=entitlement_types,
)

integration.register_capabilities(
    {{
        # Read capabilities
        CapabilityName.VALIDATE_CREDENTIALS: capabilities_read.validate_credentials,
        # CapabilityName.LIST_ACCOUNTS: capabilities_read.list_accounts,
        # CapabilityName.LIST_RESOURCES: capabilities_read.list_resources,
        # CapabilityName.LIST_ENTITLEMENTS: capabilities_read.list_entitlements,
        # CapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: capabilities_read.find_entitlement_associations,
        # CapabilityName.GET_LAST_ACTIVITY: capabilities_read.get_last_activity,
        # Write capabilities
        # CapabilityName.ASSIGN_ENTITLEMENT: capabilities_write.assign_entitlement,
        # CapabilityName.UNASSIGN_ENTITLEMENT: capabilities_write.unassign_entitlement,
        # CapabilityName.CREATE_ACCOUNT: capabilities_write.create_account,
        # CapabilityName.ACTIVATE_ACCOUNT: capabilities_write.activate_account,
        # CapabilityName.DEACTIVATE_ACCOUNT: capabilities_write.deactivate_account,
        # CapabilityName.DELETE_ACCOUNT: capabilities_write.delete_account,
    }}
)
