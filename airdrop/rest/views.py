"""
объеденить в одну функции chech_pyment и check_token
"""
from rest import models as rm
from airdrop import libs
from django.http import HttpResponse
import json
import re


ADDRESS = re.compile("([0-9a-fA-F]{40})")


def chech_pyment(request):
    if libs.is_signin(request):
        if request.method == "POST" and request.is_ajax():
            address = request.POST.get("address")
            order_id = request.POST.get("order_id")
            try:
                order_id = int(order_id)
            except TypeError:
                return HttpResponse(json.dumps(
                    {
                        "result": "error",
                        "description": "Order not found"
                    }
                ))
            if address and order_id:
                if re.match(ADDRESS, address):
                    order = rm.SenderOrder.objects.filter(address=address, id=order_id)
                    if order and len(order) == 1:
                        data = {"reload": False}
                        data["result"] = libs.get_data(
                            {
                                "command": "balance",
                                "address": address,
                            },
                            "balance"
                        )
                        if not order[0].payment and data["result"] \
                                and data["result"] >= int(order[0].cost):
                            order.update(payment=True)
                            data["reload"] = True
                        return HttpResponse(json.dumps(data))
                    else:
                        return HttpResponse(json.dumps(
                            {
                                "result": "error",
                                "description": "Address not found"
                            }
                        ))
                        data = {"reload": False}
                        data["result"] = libs.get_data(
                            {
                                "command": "balance",
                                "address": address
                            },
                            "balance"
                        )
                        if data["result"] >= int(order[0].cost):
                            order.update(payment=True)
                            data["reload"] = True
                        return HttpResponse(json.dumps(data))
                else:
                    return HttpResponse(json.dumps(
                        {
                            "result": "error",
                            "description": "Invalid address format"
                        }
                    ))
            else:
                return HttpResponse(json.dumps(
                    {
                        "result": "error",
                        "description": "Not found field 'address'"
                    }
                ))
        else:
            return HttpResponse(json.dumps(
                {
                    "result": "error",
                    "description": "Only POST request"
                }
            ))
    else:
        return HttpResponse(json.dumps(
            {
                "result": "error",
                "description": "Only for authorized users"
            }
        ))


def check_token(request):
    if libs.is_signin(request):
        if request.method == "POST" and request.is_ajax():
            address = request.POST.get("address")
            contract = request.POST.get("contract")
            order_id = request.POST.get("order_id")
            try:
                order_id = int(order_id)
            except TypeError:
                return HttpResponse(json.dumps(
                    {
                        "result": "error",
                        "description": "Order not found"
                    }
                ))
            if address and contract and order_id:
                if re.match(ADDRESS, address) and re.match(ADDRESS, contract):
                    order = rm.SenderOrder.objects.filter(address=address, id=order_id)
                    if order and len(order) == 1:
                        data = {"reload": False}
                        data["result"] = libs.get_data(
                            {
                                "command": "token",
                                "address": address,
                                "contract": contract
                            },
                            "balance"
                        )
                        if not order[0].tokens and data["result"] \
                                and data["result"] >= int(order[0].amount):
                            order.update(tokens=True)
                            data["reload"] = True
                        return HttpResponse(json.dumps(data))
                    else:
                        return HttpResponse(json.dumps(
                            {
                                "result": "error",
                                "description": "Address not found"
                            }
                        ))
                else:
                    return HttpResponse(json.dumps(
                        {
                            "result": "error",
                            "description": "Invalid address format"
                        }
                    ))
            else:
                return HttpResponse(json.dumps(
                    {"result": "error",
                     "description": "Not found field 'address'"}
                ))
        else:
            return HttpResponse(json.dumps(
                {
                    "result": "error",
                    "description": "Only POST request"
                }
            ))
    else:
        return HttpResponse(json.dumps(
            {
                "result": "error",
                "description": "Only for authorized users"
            }
        ))
