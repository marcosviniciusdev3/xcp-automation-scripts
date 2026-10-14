import json
import os
import ssl

import XenAPI

# Connect to XCP-ng pool master or host
ssl._create_default_https_context = ssl._create_unverified_context

XCP_HOST = os.getenv("XCP_HOST")
XCP_USERNAME = os.getenv("XCP_USERNAME")
XCP_PASSWORD = os.getenv("XCP_PASSWORD")
VM_UUID = os.getenv("VM_UUID")


def main():
    session = None
    logged_in = False

    result = {
        "success": False,
        "vm": None,
        "vifs": [],
        "guest_networks": None,
        "guest_tools_available": False,
    }

    try:
        # 1. Validate required environment variables
        if not all([XCP_HOST, XCP_USERNAME, XCP_PASSWORD, VM_UUID]):
            raise ValueError(
                "XCP_HOST, XCP_USERNAME, XCP_PASSWORD, "
                "and VM_UUID environment variables are required."
            )

        # 2. Connect and authenticate
        session = XenAPI.Session(XCP_HOST)
        session.xenapi.login_with_password(
            XCP_USERNAME,
            XCP_PASSWORD,
            "1.0",
            "vif-query-script",
        )
        logged_in = True

        # 3. Retrieve VM by UUID
        vm_ref = session.xenapi.VM.get_by_uuid(VM_UUID)
        vm_rec = session.xenapi.VM.get_record(vm_ref)

        result["vm"] = {
            "name": vm_rec["name_label"],
            "uuid": vm_rec["uuid"],
        }

        # 4. Retrieve VIF information
        for vif_ref in vm_rec["VIFs"]:
            vif = session.xenapi.VIF.get_record(vif_ref)
            network = session.xenapi.network.get_record(vif["network"])

            result["vifs"].append({
                "device": f"eth{vif['device']}",
                "device_number": int(vif["device"]),
                "uuid": vif["uuid"],
                "mac_address": vif["MAC"],
                "network": {
                    "name": network["name_label"],
                    "uuid": network["uuid"],
                },
                "currently_attached": vif["currently_attached"],
                "mtu": int(vif["MTU"]),
            })

        # 5. Retrieve guest network information
        guest_metrics_ref = vm_rec["guest_metrics"]

        if guest_metrics_ref != "OpaqueRef:NULL":
            guest_metrics = (
                session.xenapi.VM_guest_metrics.get_record(
                    guest_metrics_ref
                )
            )

            result["guest_networks"] = guest_metrics.get("networks", {})
            result["guest_tools_available"] = True

        result["success"] = True

    except Exception as exc:
        result["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }

    finally:
        if session is not None and logged_in:
            try:
                session.xenapi.logout()
            except Exception as exc:
                result.setdefault("warnings", []).append({
                    "type": type(exc).__name__,
                    "message": f"Logout failed: {exc}",
                })

    # Emit exactly one JSON document to stdout
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
