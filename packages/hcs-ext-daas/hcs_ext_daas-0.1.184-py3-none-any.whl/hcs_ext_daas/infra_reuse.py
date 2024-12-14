"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import ipaddress
import hashlib
import logging
from hcs_cli.service import admin
from hcs_ext_azure.provider import _az_facade as az
from hcs_core.plan import PlanException, context

log = logging.getLogger(__name__)


def process(data: dict, state: dict) -> dict:
    org_id = data["orgId"]
    provider = data["provider"]
    provider_id = provider["id"]
    if provider_id:
        log.info("Reusing provider: %s", provider_id)
        providerInstance = admin.provider.get("azure", provider_id, org_id)
        if providerInstance:
            providerData = providerInstance["providerDetails"]["data"]
            region = providerData["region"]
        else:
            raise PlanException("Provider not found: " + provider_id)
    else:
        region = data["provider"]["region"]
        provider_id = state["output"]["myProvider"]["id"]

    # identify subnets
    subnet_map = _prepare_subnet_map(data["network"]["vNetId"])

    edge = {"managementNetwork": subnet_map[data["network"]["managementNetworkName"]]}
    uag = {
        "managementNetwork": subnet_map[data["network"]["managementNetworkName"]],
        "dmzNetwork": subnet_map[data["network"]["dmzNetworkName"]],
        "desktopNetwork": subnet_map[data["network"]["desktopNetworkName"]],
    }
    image = {
        "desktopSubnetId": uag["desktopNetwork"]["id"],
        "desktopPassword": [c for c in data["desktop"]["adminPassword"]],
        "multiSessionImageName": _generate_image_name("m"),
        "desktopImageName": _generate_image_name("d"),
    }

    return {
        "location": region,
        "providerInstanceId": provider_id,
        "edge": edge,
        "uag": uag,
        "image": image,
    }


def _prepare_subnet_map(vnet_id):
    # /subscriptions/a2ef2de8-f2b5-43da-bf68-2b182dd5f928/resourceGroups/horizonv2-sg-dev/providers/Microsoft.Network/virtualNetworks/westus2-vnet-1
    pattern = r"/subscriptions/.+?/resourceGroups/(.+?)/providers/Microsoft.Network/virtualNetworks/(.+)"
    matcher = re.search(pattern, vnet_id)
    if not matcher:
        raise PlanException("Fail parsing vNet ID: " + vnet_id)
    rg = matcher.group(1)
    vnet_name = matcher.group(2)
    subnets = az.network.subnet.list(rg, vnet_name)

    ret = {}
    for subnet in subnets:
        subnet_name = subnet["name"]
        cidr = subnet["addressPrefix"]
        addrs = ipaddress.ip_network(cidr).num_addresses - 4
        ret[subnet_name] = _to_network(vnet_id, subnet_name, addrs, cidr)
    return ret


def _to_network(vnet_id, subnet_name, available_ip_addresses, cidr):
    return {
        "kind": "subnets",
        "id": f"{vnet_id}/subnets/{subnet_name}",
        "data": {"parent": vnet_id, "name": subnet_name, "availableIpAddresses": available_ip_addresses, "cidr": cidr},
    }


def _generate_image_name(prefix: str) -> str:
    ret = prefix + "-" + context.get("deploymentId")
    # 11 chars max
    return _to_limited_string(ret, 11)


def _to_limited_string(text: str, limit: int) -> str:
    l = len(text)
    if l <= limit:
        return text
    first_part = text[: limit - 4]
    second_part = text[limit - 4 :]

    sha256_hash = hashlib.sha256(second_part.encode()).hexdigest()
    truncated_hash = sha256_hash[:3]
    return first_part + "-" + truncated_hash


def destroy(data: dict, state: dict, force: bool):
    return


def eta(action: str, data: dict, state: dict):
    return "1m"
