from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
import json
from django.http import HttpResponseBadRequest, HttpResponse
import csv
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa





import pdfkit
from django.template.loader import render_to_string


# Create your views here.


@login_required
def home(request):
    return render(request, "base.html")

def list_items(request):
    title = "List of list_items"
    items = Stock.objects.all()
    
    context = {
        'title': title,
        'items': items,
        
    }
    
    return render(request, 'screens/product.html', context)

def add_items(request):
    form = StockCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    else:
        print(form.errors)
        
    context = {
        'form': form,
        'title': 'Add item',
    }
    return render (request, "screens/add_items.html", context)

def add_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_items')
    else:
        print(form.errors)
        
    context = {
        'form': form,
        'title': 'Add Category',
    }
    return render (request, "screens/add_category.html", context)

def update_items(request, pk):
    items = get_object_or_404(Stock, id=pk)
    form = StockUpdateForm(instance=items)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST or None, request.FILES or None, instance=items)
        
        if form.is_valid():
            form.save()
            return redirect('list_items')
        
    context = {
        'form': form,
    }
    return render(request, "screens/add_items.html", context)


def view_items(request, pk):
    items = get_object_or_404(Stock, id=pk)
    context = {
        'items': items,
    }
    return render(request, 'screens/view_items.html', context)


def delete_items(request, pk):
    items = get_object_or_404(Stock, id=pk)
    if request.method == 'POST':
        items.delete()
        messages.success(request, 'Item deleted successfully')
        if request.is_ajax():
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        return redirect('list_items')

    else:
        return HttpResponseBadRequest()
    
def export_to_csv(request):
    items = Stock.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=items_export.csv'
    writer = csv.writer(response)
    writer.writerow(
        ['Category', 'Item_name', 'Quantity', 'Price', 'Last_update'])
    items_fields = items.values_list(
        'category', 'item_name', 'quantity', 'price', 'last_update')
    for item in items_fields:
        writer.writerow(item)
    return response

  

def pdf_report_create(request):
    items = Stock.objects.all()
    template_path = 'screens/pdf_product_view.html'
    context = {'items': items}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="items_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def pdf_report_item(request, pk):
    items = Stock.objects.get(id=pk)
    template_path = 'screens/pdf_item_view.html'
    context = {'items': items}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="item_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def issue_items(request, pk):
    items = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=items)
    if form.is_valid():
        instance = form.save(commit=False)

        # Ensure both data.quantity and data.issue_quantity are numeric types
        quantity = int(instance.quantity)
        issue_quantity = int(instance.issue_quantity)

        instance.quantity = quantity - issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/view_items/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(items.item_name),
        "items": items,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "screens/issue_item.html", context)


def receive_items(request, pk):
    items = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=items)

    if form.is_valid():
        instance = form.save(commit=False)

        # Ensure both data.quantity and data.issue_quantity are numeric types
        quantity = int(instance.quantity)
        receive_quantity = int(instance.receive_quantity)

        instance.quantity = quantity + receive_quantity
        instance.receive_by = str(request.user)
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/view_items/'+str(instance.id))

    context = {
        "title": 'Receive ' + str(items.item_name),
        "instance": items,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "screens/receive_items.html", context)
