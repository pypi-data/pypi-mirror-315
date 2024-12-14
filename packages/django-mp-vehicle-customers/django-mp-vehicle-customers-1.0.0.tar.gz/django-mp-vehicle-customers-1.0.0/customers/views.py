import csv
from datetime import datetime

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from customers import forms
from customers.models import Customer
from invoices.models import ArrivalItem, SaleItem


@staff_member_required
def get_customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    form = forms.ReportForm(request.GET)

    sale_items = (
        SaleItem.objects.filter(
            invoice__customer=customer,
            invoice__created__date__range=[
                form.cleaned_data["date_from"],
                form.cleaned_data["date_to"],
            ],
        )
        .select_related("invoice")
        .order_by("-invoice__created")
    )

    arrival_items = (
        ArrivalItem.objects.filter(
            invoice__customer=customer,
            invoice__created__date__range=[
                form.cleaned_data["date_from"],
                form.cleaned_data["date_to"],
            ],
        )
        .select_related("invoice")
        .order_by("-invoice__created")
    )

    return render(
        request,
        "customers/detail.html",
        {
            "object": customer,
            "sale_items": sale_items,
            "sale_totals": {
                "total": sum([s.subtotal_with_discount for s in sale_items]),
                "qty": sum([s.qty for s in sale_items]),
            },
            "arrival_items": arrival_items,
            "arrival_totals": {
                "total": sum(
                    [s.subtotal_with_discount for s in arrival_items]
                ),
                "qty": sum([s.qty for s in arrival_items]),
            },
            "form": form,
            **admin.site.each_context(request),
        },
    )


@staff_member_required
def export_customers(request):
    file_name = datetime.now().strftime("%d.%m.%Y")

    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = 'attachment; filename="customers_{}.csv"'.format(file_name)

    writer = csv.writer(response)

    writer.writerow(["Name", "Phone", "Vin", "Discount"])

    for customer in Customer.objects.all():
        writer.writerow(
            [
                customer.name,
                customer.phone,
                customer.vin,
                "{}%".format(customer.discount) if customer.discount else "",
            ]
        )

    return response
