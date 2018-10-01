from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from sender import forms
from sender import models as sm
from django.conf import settings
from airdrop import libs
# from django.contrib import messages
from django.http import HttpResponse
from multiprocessing import Process


def deploy_contract(data):
    tx_receipt = libs.get_data(data, "tx_receipt")
    work_contract = tx_receipt.contractAddress
    # libs.add_statistic(
    #     order=data["order"],
    #     event="Deploy copntract",
    #     tx_hash=tx_receipt.transactionHash
    # )
    order = sm.SenderOrder.objects.filter(id=data["order"])
    order.update(work_contract=work_contract[2:])
    data["work_contract"] = work_contract[2:]


# def run_task(data):
#     tx_receipt = None
#     return tx_receipt


def run_order(data):
    """
    установить таймаут при деплое или хранить адрес размещенного контракта,
    а потом обращаться за ним
    если ошибка размещения - выслать письмо
    """
    if not data.get("work_contract"):
        deploy_contract(data)
    data["command"] = "task"
    del data["address"]
    del data["contract"]
    del data["amount"]
    addresses = []
    order = sm.SenderOrder.objects.get(id=data["order"])
    all_addresses = order.recipient_odrer.all().values("address")
    for rec in all_addresses:
        addresses.append(rec.address)
    iterations = len(addresses) // settings.COUNT_ADDRESSES
    sizes_arrays = settings.COUNT_ADDRESSES * iterations
    staff = (len(addresses) - (settings.COUNT_ADDRESSES * iterations))
    if staff:
        sizes_arrays.append(staff)
    start = 0
    end = 0
    for size_array in sizes_arrays:
        end += size_array
        data["addresses"] = addresses[start:start+end]
        tx_receipt = libs.get_data(data, "tx_receipt")
        # libs.add_statistic(
        #     order=data["order"],
        #     event="Call method 'transfer'",
        #     tx_hash=tx_receipt.transactionHash
        # )
        start += size_array


def load(request):
    if libs.is_signin(request):
        data = {"title": _("Load Data"), "sender": "active"}
        if request.method == "POST":
            form_airdrop = forms.AirdropForm(request.POST, request.FILES)
            if form_airdrop.is_valid():
                form_airdrop.save(request)
                return redirect("user_page")
        else:
            form_airdrop = forms.AirdropForm()
        data["form_airdrop"] = form_airdrop
        return render(request, "load_data.html", data)
    else:
        return redirect("user_signin")


def start(request, address):
    if libs.is_signin(request):
        order = sm.SenderOrder.objects.filter(address=address)
        if not order:
            raise Http404
        order.update(status=0)
        data = {
            "address": order[0].address,
            "contract": order[0].contract,
            "amount": order[0].recepient_order.all()[0].amount,
            "order": order[0].id
        }
        if order[0].work_contract:
            data["work_contract"] = order[0].work_contract
            data["command"] = "run"
        else:
            data["command"] = "deploy"
        deploy = Process(target=run_order, args=[data])
        deploy.start()
        return redirect("view_order", order[0].address)
    else:
        return redirect("user_signin")


def repeat(request, address):
    pass


def orders(request, num):
    if libs.is_signin(request):
        data = {"title": _("Orders"), "orders": "active"}
        user_id = libs.who_signin(request)[0]
        orders = sm.SenderOrder.objects.filter(user_id=user_id).order_by("-id")
        if orders.count() > 0 and num > orders.count():
            raise Http404
        data["pages"] = range(1, libs.count_pages(orders.count())+1)
        begin, end = libs.pages(num)
        data["all_orders"] = orders[begin:end]
        data["curent_page"] = num
        return render(request, "orders.html", data)
    else:
        return redirect("user_signin")


def order(request, address):
    if libs.is_signin(request):
        data = {"title": _("Order #"), "orders": "active"}
        user_id = libs.who_signin(request)[0]
        try:
            data["order"] = sm.SenderOrder.objects.get(address=address, user_id=user_id)
        except sm.SenderOrder.DoesNotExist:
            raise Http404
        try:
            data["back"] = request.META['HTTP_REFERER']
        except KeyError:
            pass
        data["title"] += str(data["order"].id)
        return render(request, "order.html", data)
    else:
        return redirect("user_signin")


def download(request, order_address):
    try:
        order = sm.SenderOrder.objects.get(address=order_address)
    except sm.SenderOrder.DoesNotExist:
        raise Http404
    addresses = sm.RecipientData.objects.filter(order=order)
    print(addresses)
    file = ""
    for address in addresses:
        file += "{}\n".format(address.address)
    response = HttpResponse(file, content_type="application/csv")
    return response


def start_order(request, address):
    if libs.is_signin(request):
        pass
    else:
        return redirect("user_signin")
