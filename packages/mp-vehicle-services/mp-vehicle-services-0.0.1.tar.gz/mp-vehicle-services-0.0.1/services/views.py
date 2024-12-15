from cap.decorators import admin_render_view
from cap.views import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from djforms import get_clean_data
from pagination import paginate

from invoices.models import Sale
from services import forms
from services.models import Service, ServiceItem


@admin_render_view(template_name="services/print-service-items.html")
def print_service_items(request):
    return {}


@admin_render_view(template_name="services/print-services.html")
def print_services(request, sale_id):
    sale = request.invoices.get_sale(sale_id)
    return {"sale": sale, "services": sale.services.all()}


@admin_render_view(template_name="services/report.html")
def get_report(request):
    form = forms.ReportForm(request.GET)

    services = Service.objects.filter(
        sale__created__date__range=[
            form.cleaned_data["date_from"],
            form.cleaned_data["date_to"],
        ],
        sale__type=Sale.TYPE_CASH_REGISTER,
    ).order_by("sale__created")

    worker = form.cleaned_data.get("worker")

    if worker:
        services = services.filter(worker=worker)

    return {
        "services": services,
        "form": form,
        "totals": {
            "qty": sum([s.qty for s in services]),
            "grand_total": sum([s.subtotal for s in services]),
        },
        **form.cleaned_data,
    }


@staff_member_required
def add_service_item(request):
    form = forms.AddServiceItemForm(request.POST or None)

    status_code = 200

    if request.method == "POST":
        if form.is_valid():
            service_item = form.save()

            return JsonResponse(
                {
                    "message": _("Service added"),
                    "service_item_id": service_item.pk,
                }
            )
        else:
            status_code = 403

    return render(
        request,
        "services/add-service-item.html",
        {"form": form, "status_code": status_code},
        status=status_code,
    )


@require_GET
@staff_member_required
def get_service_items(request):
    form = forms.SearchServiceForm(request.GET)

    page = paginate(
        request,
        ServiceItem.objects.search(**get_clean_data(form)),
        per_page=30,
    )

    return JsonResponse(
        {
            "items": render_to_string(
                "services/service-items.html",
                {"request": request, "page_obj": page},
            ),
            **page.serialize(),
        }
    )


@require_POST
def add_service(request, sale_id):
    sale = request.invoices.get_sale(sale_id)

    service_item = ServiceItem.objects.get(pk=request.POST["service_item"])

    service = request.services.add_service(sale, service_item)

    return JsonResponse(
        {
            "message": _("Service added"),
            "status": "OK",
            "html": service.render(),
            "item_id": service.id,
            "total": sale.serialize_totals(),
        }
    )


@method_decorator(staff_member_required, "dispatch")
class ServiceAPI(View):
    def post(self, request, service_id):
        service = request.services.get_service(service_id)

        try:
            service.update(request.POST)
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        return JsonResponse(
            {
                "message": _("Service updated"),
                "total": service.sale.serialize_totals(),
            }
        )

    def delete(self, request, service_id):
        if not request.user.is_superuser:
            return HttpResponseForbidden(_("You can`t delete service items"))

        service = request.services.get_service(service_id)

        sale = service.sale

        service.delete()

        return JsonResponse(
            {"message": _("Service removed"), "total": sale.serialize_totals()}
        )
