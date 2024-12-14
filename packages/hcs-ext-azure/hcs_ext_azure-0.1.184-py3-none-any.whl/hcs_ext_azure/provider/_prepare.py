import logging
from . import _az_facade as az

log = logging.getLogger(__name__)


def prepare(data: dict):
    subscription_id = data["subscriptionId"]
    az.set_subscription(subscription_id)

    applicationId = data.get("applicationId")
    if applicationId:
        log.info("Initializing with configured SP.")
        applicationKey = data.get("applicationKey")
        # print("Login az CLI...")
        ret = az.login(applicationId, applicationKey, data.get("directoryId"))
        # print(ret)
    # _az_facade.login(provider['applicationId'], provider['applicationKey'], directory_id)
    # _az_facade.set_subscription(subscription_id)
    else:
        log.info("No configured SP found. Using Azure CLI stored login.")

    ret = az.test_credential()
    # print(ret)
