from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import EggProduction, Incubation, Product
from .forms import EggProductionForm, IncubationForm # assuming you have these forms created

@login_required
def eggproduction_list(request):
    eggs = EggProduction.objects.filter(collected_by=request.user).order_by('-date_laid')
    return render(request, 'eggproduction/list.html', {'eggs': eggs})

@login_required
def eggproduction_detail(request, pk):
    egg = get_object_or_404(EggProduction, pk=pk)
    if egg.collected_by != request.user:
        return HttpResponseForbidden()
    return render(request, 'eggproduction/detail.html', {'egg': egg})

@login_required
def eggproduction_create(request):
    if request.method == 'POST':
        form = EggProductionForm(request.POST)
        if form.is_valid():
            egg = form.save(commit=False)
            egg.collected_by = request.user
            egg.save()
            form.save_m2m()
            return redirect('eggproduction_list')
    else:
        form = EggProductionForm()
    return render(request, 'eggproduction/form.html', {'form': form})

@login_required
def eggproduction_update(request, pk):
    egg = get_object_or_404(EggProduction, pk=pk)
    if egg.collected_by != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EggProductionForm(request.POST, instance=egg)
        if form.is_valid():
            form.save()
            return redirect('eggproduction_detail', pk=egg.pk)
    else:
        form = EggProductionForm(instance=egg)
    return render(request, 'eggproduction/form.html', {'form': form})

@login_required
def eggproduction_delete(request, pk):
    egg = get_object_or_404(EggProduction, pk=pk)
    if egg.collected_by != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        egg.delete()
        return redirect('eggproduction_list')
    return render(request, 'eggproduction/confirm_delete.html', {'object': egg})


# Incubation Views
@login_required
def incubation_list(request):
    incubations = Incubation.objects.filter(chicken__owner=request.user).order_by('-start_date')
    return render(request, 'incubation/list.html', {'incubations': incubations})

@login_required
def incubation_detail(request, pk):
    incubation = get_object_or_404(Incubation, pk=pk)
    if incubation.chicken.owner != request.user:
        return HttpResponseForbidden()
    return render(request, 'incubation/detail.html', {'incubation': incubation})

@login_required
def incubation_create(request):
    if request.method == 'POST':
        form = IncubationForm(request.POST)
        if form.is_valid():
            incubation = form.save(commit=False)
            # optionally, set user or other defaults here
            incubation.save()
            form.save_m2m()
            return redirect('incubation_list')
    else:
        form = IncubationForm()
    return render(request, 'incubation/form.html', {'form': form})

@login_required
def incubation_update(request, pk):
    incubation = get_object_or_404(Incubation, pk=pk)
    if incubation.chicken.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = IncubationForm(request.POST, instance=incubation)
        if form.is_valid():
            form.save()
            return redirect('incubation_detail', pk=incubation.pk)
    else:
        form = IncubationForm(instance=incubation)
    return render(request, 'incubation/form.html', {'form': form})

@login_required
def incubation_delete(request, pk):
    incubation = get_object_or_404(Incubation, pk=pk)
    if incubation.chicken.owner != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        incubation.delete()
        return redirect('incubation_list')
    return render(request, 'incubation/confirm_delete.html', {'object': incubation})


# Product Views (simple listing and detail)

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product/detail.html', {'product': product})

