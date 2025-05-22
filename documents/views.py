from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DocumentCategory, FarmDocument
from .forms import FarmDocumentForm


@login_required
def document_list(request):
    documents = FarmDocument.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})


@login_required
def document_detail(request, pk):
    document = get_object_or_404(FarmDocument, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})


@login_required
def upload_document(request):
    if request.method == 'POST':
        form = FarmDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('document_list')
    else:
        form = FarmDocumentForm()
    return render(request, 'documents/upload_document.html', {'form': form})
