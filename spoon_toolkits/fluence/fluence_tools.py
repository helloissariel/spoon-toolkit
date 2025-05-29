import asyncio
import os

import requests
import traceback

from spoon_ai.tools import BaseTool


class FluenceListSSHKeysTool(BaseTool):
    name: str = "list_fluence_ssh_keys"
    description: str = "List SSH keys associated with the account"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    async def execute(self, api_key):
        try:
            url = "https://api.fluence.dev/ssh_keys"
            headers = {"Authorization": f"Bearer {api_key}"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return f"✅ SSH keys fetched.\n{res.json()}"
        except Exception as e:
            return f"❌ Error: {e}"


class FluenceCreateSSHKeyTool(BaseTool):
    name: str = "create_fluence_ssh_key"
    description: str = "Create a new SSH key"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"},
            "name": {"type": "string"},
            "public_key": {"type": "string"}
        },
        "required": ["api_key", "name", "public_key"]
    }

    async def execute(self, api_key, name, public_key):
        # 注意name： 只能使用 小写字母、数字、中划线 -，最长 25 个字符
        try:
            url = "https://api.fluence.dev/ssh_keys"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            body = {"name": name, "publicKey": public_key}
            res = requests.post(url, headers=headers, json=body, timeout=1000)
            print(f"create ssh key: {res.text}")
            res.raise_for_status()
            # return f"✅ SSH key created.\n{res.json()}"
            return res.json()
        except Exception as e:
            return f"❌ Error: {traceback.format_exc()}"


class FluenceDeleteSSHKeyTool(BaseTool):
    name: str = "delete_fluence_ssh_key"
    description: str = "Delete an SSH key"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"},
            "fingerprint": {"type": "string"}
        },
        "required": ["api_key", "key_id"]
    }

    async def execute(self, api_key, fingerprint):
        try:
            url = f"https://api.fluence.dev/ssh_keys"
            headers = {"Authorization": f"Bearer {api_key}"}
            body = {"fingerprint": fingerprint}
            res = requests.delete(url, headers=headers, json=body, timeout=10)
            res.raise_for_status()
            return "✅ SSH key deleted."
        except Exception as e:
            return f"❌ Error: {e}"


class FluenceListVMsTool(BaseTool):
    name: str = "list_fluence_vms"
    description: str = "List all active VMs"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    async def execute(self, api_key):
        try:
            url = "https://api.fluence.dev/vms/v3"
            headers = {"Authorization": f"Bearer {api_key}"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return f"✅ VMs fetched.\n{res.json()}"
        except Exception as e:
            return f"❌ Error: {e}"


class FluenceCreateVMTool(BaseTool):
    name: str = "create_fluence_vm"
    description: str = "Create one or more virtual machines on the Fluence marketplace"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {
                "type": "string",
                "description": "Your Fluence API key"
            },
            "vm_config": {
                "type": "object",
                "description": "VM creation configuration",
                "properties": {
                    "constraints": {
                        "type": "object",
                        "description": "Offer constraints for VM",
                        "properties": {
                            "additionalResources": {
                                "type": "object",
                                "properties": {
                                    "storage": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "supply": {"type": "integer"},
                                                "type": {"type": "string"},
                                                "units": {"type": "string"}
                                            },
                                            "required": ["supply", "type", "units"]
                                        }
                                    }
                                }
                            },
                            "basicConfiguration": {"type": "string"},
                            "datacenter": {
                                "type": "object",
                                "properties": {
                                    "countries": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            },
                            "hardware": {
                                "type": "object",
                                "properties": {
                                    "cpu": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "architecture": {"type": "string"},
                                                "manufacturer": {"type": "string"}
                                            },
                                            "required": ["architecture", "manufacturer"]
                                        }
                                    },
                                    "memory": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "generation": {"type": "string"},
                                                "type": {"type": "string"}
                                            },
                                            "required": ["generation", "type"]
                                        }
                                    },
                                    "storage": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "type": {"type": "string"}
                                            },
                                            "required": ["type"]
                                        }
                                    }
                                }
                            },
                            "maxTotalPricePerEpochUsd": {"type": "string"}
                        }
                    },
                    "instances": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "description": "Number of VM instances to create"
                    },
                    "vmConfiguration": {
                        "type": "object",
                        "properties": {
                            "hostname": {
                                "type": ["string", "null"],
                                "description": "Hostname or null"
                            },
                            "name": {
                                "type": "string",
                                "description": "Name of the VM"
                            },
                            "openPorts": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "port": {
                                            "type": "integer",
                                            "minimum": 1,
                                            "maximum": 65535
                                        },
                                        "protocol": {
                                            "type": "string",
                                            "enum": ["tcp", "udp", "sctp"]
                                        }
                                    },
                                    "required": ["port", "protocol"]
                                }
                            },
                            "osImage": {
                                "type": "string",
                                "description": "OS image URL or identifier"
                            },
                            "sshKeys": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of SSH keys"
                            }
                        },
                        "required": ["name", "openPorts", "osImage", "sshKeys"]
                    }
                },
                "required": ["instances", "vmConfiguration"]
            }
        },
        "required": ["api_key", "vm_config"]
    }

    async def execute(self, api_key, vm_config):
        try:
            url = "https://api.fluence.dev/vms/v3"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            res = requests.post(url, headers=headers, json=vm_config, timeout=15)
            print(f"create VM: {res.text}")
            res.raise_for_status()
            return f"✅ VM created successfully.\n{res.json()}"
        except Exception as e:
            return f"❌ Error creating VM: {e}"


class FluenceDeleteVMTool(BaseTool):
    name: str = "delete_fluence_vm"
    description: str = "Delete VM by vm_ids"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"},
            "vm_ids": {"type": "array"}
        },
        "required": ["api_key", "vm_ids"]
    }

    async def execute(self, api_key, vm_ids):
        try:
            url = f"https://api.fluence.dev/vms/v3"
            headers = {"Authorization": f"Bearer {api_key}"}
            body = {"vmIds": vm_ids}
            res = requests.delete(url, headers=headers, json=body, timeout=10)
            print(f"delete VM: {res.text}")
            res.raise_for_status()
            return "✅ VM deleted."
        except Exception as e:
            return f"❌ Error: {e}"


class FluencePatchVMTool(BaseTool):
    name: str = "patch_fluence_vm"
    description: str = "Update specific attributes of one or more VMs by sending an updates array, each with id, openPorts, and vmName."

    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string", "description": "Your Fluence API key"},
            "patch_data": {
                "type": "object",
                "description": "Patch data containing updates array",
                "properties": {
                    "updates": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "description": "ID of the VM to update"},
                                "openPorts": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "port": {
                                                "type": "integer",
                                                "minimum": 1,
                                                "maximum": 65535
                                            },
                                            "protocol": {
                                                "type": "string",
                                                "enum": ["tcp", "udp", "sctp"]
                                            }
                                        },
                                        "required": ["port", "protocol"]
                                    }
                                },
                                "vmName": {"type": "string", "description": "New name for the VM"}
                            },
                            "required": ["id"]
                        }
                    }
                },
                "required": ["updates"]
            }
        },
        "required": ["api_key", "patch_data"]
    }

    async def execute(self, api_key, patch_data):
        try:
            url = "https://api.fluence.dev/vms/v3"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            res = requests.patch(url, headers=headers, json=patch_data, timeout=1000)
            print(f"patch VM: {res.text}")
            res.raise_for_status()
            return f"✅ VM(s) patched."
        except Exception as e:
            return f"❌ Error patching VM(s): {e}"


class FluenceListDefaultImagesTool(BaseTool):
    name: str = "list_fluence_default_vm_images"
    description: str = "List available default images for VMs"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    async def execute(self, api_key):
        try:
            url = "https://api.fluence.dev/vms/v3/default_images"
            headers = {"Authorization": f"Bearer {api_key}"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return f"✅ Default images fetched.\n{res.json()}"
        except Exception as e:
            return f"❌ Error: {e}"


class FluenceEstimateVMTool(BaseTool):
    name: str = "estimate_fluence_vm"
    description: str = "Estimate cost for deploying one or more VMs with specified constraints and instance count."

    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {
                "type": "string",
                "description": "Your Fluence API key for authentication"
            },
            "constraints_spec": {
                "type": "object",
                "description": "Specification of constraints and instance count for VM cost estimation",
                "properties": {
                    "constraints": {
                        "type": "object",
                        "description": "Constraints defining VM hardware requirements, datacenter preferences, resource limits, and pricing caps",
                        "properties": {
                            "additionalResources": {
                                "type": "object",
                                "description": "Additional resource requirements beyond basic hardware",
                                "properties": {
                                    "storage": {
                                        "type": "array",
                                        "description": "List of additional storage requirements",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "supply": {
                                                    "type": "integer",
                                                    "description": "Amount of storage requested",
                                                    "example": 20
                                                },
                                                "type": {
                                                    "type": "string",
                                                    "description": "Type of storage device (e.g. NVMe)",
                                                    "example": "NVMe"
                                                },
                                                "units": {
                                                    "type": "string",
                                                    "description": "Units of storage supply (e.g. GiB)",
                                                    "example": "GiB"
                                                }
                                            },
                                            "required": ["supply", "type", "units"]
                                        }
                                    }
                                },
                                "required": ["storage"]
                            },
                            "basicConfiguration": {
                                "type": "string",
                                "description": "Predefined basic VM configuration string indicating CPU, RAM, and storage size",
                                "example": "cpu-4-ram-8gb-storage-25gb"
                            },
                            "datacenter": {
                                "type": "object",
                                "description": "Preferred datacenter locations by country codes",
                                "properties": {
                                    "countries": {
                                        "type": "array",
                                        "description": "List of ISO country codes for preferred datacenters",
                                        "items": {"type": "string"},
                                        "example": ["FR", "DE", "LT"]
                                    }
                                },
                                "required": ["countries"]
                            },
                            "hardware": {
                                "type": "object",
                                "description": "Detailed hardware preferences",
                                "properties": {
                                    "cpu": {
                                        "type": "array",
                                        "description": "CPU requirements",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "architecture": {
                                                    "type": "string",
                                                    "description": "CPU architecture (e.g. Zen)",
                                                    "example": "Zen"
                                                },
                                                "manufacturer": {
                                                    "type": "string",
                                                    "description": "CPU manufacturer (e.g. AMD)",
                                                    "example": "AMD"
                                                }
                                            },
                                            "required": ["architecture", "manufacturer"]
                                        }
                                    },
                                    "memory": {
                                        "type": "array",
                                        "description": "Memory module specifications",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "generation": {
                                                    "type": "string",
                                                    "description": "Memory generation (e.g. 4)",
                                                    "example": "4"
                                                },
                                                "type": {
                                                    "type": "string",
                                                    "description": "Type of RAM (e.g. DDR)",
                                                    "example": "DDR"
                                                }
                                            },
                                            "required": ["generation", "type"]
                                        }
                                    },
                                    "storage": {
                                        "type": "array",
                                        "description": "Storage device types",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "type": {
                                                    "type": "string",
                                                    "description": "Storage type (e.g. NVMe)",
                                                    "example": "NVMe"
                                                }
                                            },
                                            "required": ["type"]
                                        }
                                    }
                                },
                                "required": ["cpu", "memory", "storage"]
                            },
                            "maxTotalPricePerEpochUsd": {
                                "type": "string",
                                "description": "Maximum total price allowed per epoch in USD",
                                "example": "12.57426"
                            }
                        },
                        "required": ["additionalResources", "basicConfiguration", "datacenter", "hardware",
                                     "maxTotalPricePerEpochUsd"]
                    },
                    "instances": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10,
                        "description": "Number of VM instances to estimate cost for",
                        "example": 1
                    }
                },
                "required": ["constraints", "instances"]
            }
        },
        "required": ["api_key", "constraints_spec"]
    }

    async def execute(self, api_key, constraints_spec):
        try:
            url = "https://api.fluence.dev/vms/v3/estimate"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=constraints_spec, timeout=10)
            response.raise_for_status()
            data = response.json()
            return f"✅ Estimate completed successfully.\n{data}"
        except Exception as e:
            return f"❌ Error during estimate: {e}"


class FluenceListBasicConfigurationsTool(BaseTool):
    name: str = "list_fluence_basic_configurations"
    description: str = "List available basic configurations for compute offers"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    async def execute(self, api_key):
        try:
            url = "https://api.fluence.dev/marketplace/basic_configurations"
            headers = {"Authorization": f"Bearer {api_key}"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return f"✅ Basic configurations fetched.\n{res.json()}"
        except Exception as e:
            return f"❌ Error: {e}"


class FluenceListCountriesTool(BaseTool):
    name: str = "list_fluence_marketplace_countries"
    description: str = "List countries supported by Fluence marketplace"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    async def execute(self, api_key):
        try:
            url = "https://api.fluence.dev/marketplace/countries"
            headers = {"Authorization": f"Bearer {api_key}"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return f"✅ Countries listed.\n{res.json()}"
        except Exception as e:
            return f"❌ Error: {e}"


class FluenceListHardwareTool(BaseTool):
    name: str = "list_fluence_marketplace_hardware"
    description: str = "List hardware supported by Fluence marketplace"
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    async def execute(self, api_key):
        try:
            url = "https://api.fluence.dev/marketplace/hardware"
            headers = {"Authorization": f"Bearer {api_key}"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return f"✅ Hardware listed.\n{res.json()}"
        except Exception as e:
            return f"❌ Error: {e}"


class SearchFluenceMarketplaceOffers(BaseTool):
    name: str = "search_fluence_marketplace_offers"
    description: str = (
        "Search for compute resources on Fluence Marketplace using detailed constraints "
        "including storage, datacenter locations, hardware specs, and price limits."
    )
    parameters: dict = {
        "type": "object",
        "properties": {
            "api_key": {"type": "string", "description": "Your Fluence API key"},
            "constraints": {
                "type": "object",
                "description": "VM constraints and preferences",
                "properties": {
                    "additionalResources": {
                        "type": "object",
                        "properties": {
                            "storage": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "supply": {"type": "integer", "description": "Storage amount"},
                                        "type": {"type": "string", "description": "Storage type"},
                                        "units": {"type": "string", "description": "Storage units"}
                                    },
                                    "required": ["supply", "type", "units"]
                                }
                            }
                        }
                    },
                    "basicConfiguration": {"type": "string", "description": "Basic config string"},
                    "datacenter": {
                        "type": "object",
                        "properties": {
                            "countries": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Preferred datacenter countries"
                            }
                        }
                    },
                    "hardware": {
                        "type": "object",
                        "properties": {
                            "cpu": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "architecture": {"type": "string"},
                                        "manufacturer": {"type": "string"}
                                    }
                                }
                            },
                            "memory": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "generation": {"type": "string"},
                                        "type": {"type": "string"}
                                    }
                                }
                            },
                            "storage": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "maxTotalPricePerEpochUsd": {"type": "string", "description": "Price limit in USD"}
                },
                "required": [
                    "additionalResources",
                    "basicConfiguration",
                    "datacenter",
                    "hardware",
                    "maxTotalPricePerEpochUsd"
                ]
            }
        },
        "required": ["api_key", "constraints"]
    }

    async def execute(self, api_key, constraints):
        try:
            url = "https://api.fluence.dev/marketplace/offers"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            body = constraints
            res = requests.post(url, headers=headers, json=body, timeout=10)
            res.raise_for_status()
            data = res.json()
            offers_count = len(data)
            return f"✅ Found {offers_count} offers matching constraints.\n{data}"
        except Exception as e:
            return f"❌ Error: {e}"


"""
    Fluence API Integration Tests
"""


async def test_list_ssh_keys():
    api_key = os.getenv("FLUENCE_API_KEY")
    tool = FluenceListSSHKeysTool()
    print(f"api_key: {api_key}")
    result = await tool.execute(api_key)
    print("🧪 SSH Keys:", result)


async def test_create_and_delete_ssh_key():
    create_tool = FluenceCreateSSHKeyTool()
    api_key = os.getenv("FLUENCE_API_KEY")
    print(f"api_key: {api_key}")
    key_name: str = "test-key"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC9QHHp9UvEzoVAlxlgiaBuSvzHunok4fxiBgVGYZBfMKcOuiVsGLsDt+zYRfs0magpxglrlyQxw31+Dssr85G3VYQ5KOlcOrseSGLrUQxGRC1faV2UG5fcV5j9HmyWWWxqXb49xBtzcVHCgnV0kjsCirbyjNxGa/AX+aQR53pmGdej27WGsa+qb8ITCLNKRqo/0A9je79juEgGnYsSL7H40ZT/z/sCwhz0fpJU3Hin7/pD/OWq/Ep0u5RaVeEF9FC219NNjSDLkEyulXjkwM+SChvw3096P67Np2GeEZw3AbtZfASE95UYlNf67dazPcZAjkXIvMr52ZlihrzI5ut5dQDOua1MH8l3bMdBdHF9/xYILf8lVrlCt3c5PocLFfy0iSvAUlHY9Ve6QvXbNkXQE3+70e4sN+CO/PwK6AesB6eUxMl2I3B6IR3cAmvygXZffNdbIGu1//2B2vmG+INA53eu4ItOYjsVYIa9+lQvoRuQCSWm7CMDF54j7JZIOpxV6B1CNRqLgsOT9wp0FLH/R17SNyKZvbuOO21E0rcoLJGaPANTeYzd2TKobbS1ZZyeGKAN2fx/I6JLBb6WEnAh7OilU4hk2E3o+1VRRxZlVo2R0ViCoxhtLHiiupRTRCYMqqFqm0zC9+kRX3tB9Nd7d+gv06qVHGDdqsJEAL0haw== 1534632920@163.com"
    create_result = await create_tool.execute(api_key=api_key, name=key_name, public_key=public_key)
    print("🧪 Create SSH Key:", create_result)
    # if isinstance(create_result, dict):
    #     # fingerprint = "SHA256:sINcLA/hlKG0nDpE9n233xEnXAgSISxq0/nVWbbx5A4"
    #     fingerprint = create_result.get("fingerprint", "")
    #     delete_tool = FluenceDeleteSSHKeyTool()
    #     delete_result = await delete_tool.execute(api_key=api_key, fingerprint=fingerprint)
    #     print("🧪 Delete SSH Key:", delete_result)


async def test_list_vms():
    tool = FluenceListVMsTool()
    api_key = os.getenv("FLUENCE_API_KEY")
    result = await tool.execute(api_key)
    print("🧪 List VMs:", result)


async def test_create_and_patch_and_delete_vm():
    api_key = os.getenv("FLUENCE_API_KEY")
    vm_config = {
        "constraints": {
            "additionalResources": {
                "storage": [
                    {
                        "supply": 20,
                        "type": "NVMe",
                        "units": "GiB"
                    }
                ]
            },
            "basicConfiguration": "cpu-4-ram-8gb-storage-25gb",
            # "datacenter": {
            #     "countries": [
            #         "DE",
            #         "LT",
            #         "FR"
            #     ]
            # },
            # "hardware": {
            #     "cpu": [
            #         {
            #             "architecture": "Zen",
            #             "manufacturer": "AMD"
            #         }
            #     ],
            #     "memory": [
            #         {
            #             "generation": "4",
            #             "type": "DDR"
            #         }
            #     ],
            #     "storage": [
            #         {
            #             "type": "NVMe"
            #         }
            #     ]
            # },
            "maxTotalPricePerEpochUsd": "12.57426"
        },
        "instances": 1,
        "vmConfiguration": {
            "hostname": "custom-hostname-or-null",
            "name": "my-vm",
            "openPorts": [
                {
                    "port": 5050,
                    "protocol": "udp"
                },
                {
                    "port": 5050,
                    "protocol": "tcp"
                },
                {
                    "port": 80,
                    "protocol": "tcp"
                }
            ],
            "osImage": "https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img",
            "sshKeys": [
                "test-key"
            ]
        }
    }
    # create_tool = FluenceCreateVMTool()
    # result = await create_tool.execute(
    #     api_key=api_key,
    #     vm_config=vm_config
    # )
    # print("🧪 Create VM:", result)

    patch_tool = FluencePatchVMTool()
    vm_patch_data = {
        "updates": [
            {
                "id": "0xab8904e72a5134035ff744727530443eb6534652",
                "openPorts": [
                    {
                        "port": 1,
                        "protocol": "tcp"
                    }
                ],
                "vmName": "my-vm"
            }
        ]
    }
    patch_result = await patch_tool.execute(api_key=api_key, patch_data=vm_patch_data)
    print("🧪 Patch VM:", patch_result)
    delete_vm_ids = [
        "0xab8904e72a5134035ff744727530443eb6534652"
    ]
    delete_tool = FluenceDeleteVMTool()
    delete_result = await delete_tool.execute(api_key=api_key, vm_ids=delete_vm_ids)
    print("🧪 Delete VM:", delete_result)


async def test_list_default_images():
    api_key = os.getenv("FLUENCE_API_KEY")
    tool = FluenceListDefaultImagesTool()
    result = await tool.execute(api_key=api_key)
    print("🧪 Default Images:", result)


async def test_vm_cost_estimation():
    tool = FluenceEstimateVMTool()
    api_key = os.getenv("FLUENCE_API_KEY")
    estimation = {
        "constraints": {
            "additionalResources": {
                "storage": [
                    {
                        "supply": 20,
                        "type": "NVMe",
                        "units": "GiB"
                    }
                ]
            },
            "basicConfiguration": "cpu-4-ram-8gb-storage-25gb",
            "datacenter": {
                "countries": [
                    "FR",
                    "DE",
                    "LT"
                ]
            },
            "hardware": {
                "cpu": [
                    {
                        "architecture": "Zen",
                        "manufacturer": "AMD"
                    }
                ],
                "memory": [
                    {
                        "generation": "4",
                        "type": "DDR"
                    }
                ],
                "storage": [
                    {
                        "type": "NVMe"
                    }
                ]
            },
            "maxTotalPricePerEpochUsd": "12.57426"
        },
        "instances": 1
    }
    result = await tool.execute(api_key=api_key, constraints_spec=estimation)
    print("🧪 Estimate VM Cost:", result)


async def test_marketplace_configs():
    api_key = os.getenv("FLUENCE_API_KEY")
    tool = FluenceListBasicConfigurationsTool()
    result = await tool.execute(api_key=api_key)
    print("🧪 Basic Configurations:", result)


async def test_marketplace_countries():
    api_key = os.getenv("FLUENCE_API_KEY")
    tool = FluenceListCountriesTool()
    result = await tool.execute(api_key=api_key)
    print("🧪 Countries:", result)


async def test_marketplace_hardware():
    api_key = os.getenv("FLUENCE_API_KEY")
    tool = FluenceListHardwareTool()
    result = await tool.execute(api_key=api_key)
    print("🧪 Hardware:", result)


async def test_marketplace_post_offers():
    api_key = os.getenv("FLUENCE_API_KEY")
    tool = SearchFluenceMarketplaceOffers()
    constraints = {
        "additionalResources": {
            "storage": [
                {
                    "supply": 20,
                    "type": "NVMe",
                    "units": "GiB"
                }
            ]
        },
        "basicConfiguration": "cpu-4-ram-8gb-storage-25gb",
        "datacenter": {
            "countries": [
                "FR",
                "DE",
                "LT"
            ]
        },
        "hardware": {
            "cpu": [
                {
                    "architecture": "Zen",
                    "manufacturer": "AMD"
                }
            ],
            "memory": [
                {
                    "generation": "4",
                    "type": "DDR"
                }
            ],
            "storage": [
                {
                    "type": "NVMe"
                }
            ]
        },
        "maxTotalPricePerEpochUsd": "12.57426"
    }
    result = await tool.execute(api_key=api_key, constraints=constraints)
    print("🧪 Offers:", result)


if __name__ == '__main__':
    async def run_all_tests():
        # ssh key test
        await test_list_ssh_keys()
        # await test_create_and_delete_ssh_key()
        #
        # vm test
        # await test_list_vms()
        # await test_create_and_patch_and_delete_vm()
        # await test_list_default_images()
        # await test_vm_cost_estimation()
        #
        # # marketplace test
        # await test_marketplace_configs()
        # await test_marketplace_countries()
        # await test_marketplace_hardware()
        await test_marketplace_post_offers()


    asyncio.run(run_all_tests())
