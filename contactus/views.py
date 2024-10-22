from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile, Enquiry
from .forms import EnquiryForm, EditEnquiryForm


def enquiries(request):
    """ A view to show all enquiries, including sorting and search queries """
    
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        is_anonymous = False
    else:
        profile = None
        is_anonymous = True

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            if profile:
                enquiry.user_profile = profile
            enquiry.save()
            messages.success(request, 'Enquiry submitted successfully')
            
            return redirect('enquiries_success', pk=enquiry.id)
    
    else:
        form = EnquiryForm()

    if is_anonymous:
        enquiries = Enquiry.objects.filter(enquiry_number__icontains=request.GET.get('enquiry_number', '')).order_by('-date')
    else:
        enquiries = profile.enquiries.all().order_by('-date')

    template = 'contactus/enquiries.html'
    context = {
        'enquiry_form': form,
        'profile': profile,
        'on_profile_page': is_anonymous,
        'enquiries': enquiries,
        'is_anonymous': is_anonymous,
    }

    return render(request, template, context)


def enquiry_detail(request, enquiry_id):
    """ View for individual enquiry details """
    enquiry = get_object_or_404(Enquiry, pk=enquiry_id)
    
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST.get('action')
            if action == 'resolve':
                enquiry.resolved = True
                enquiry.save()
                messages.success(request, "Enquiry marked as resolved")
            else:
                form = EditEnquiryForm(request.POST, instance=enquiry)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Enquiry updated successfully")
        else:
            pass
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        if profile.enquiries.filter(id=enquiry.id).exists():
            return render(request, 'contactus/enquiry_detail.html', {'enquiry': enquiry, 'form': EditEnquiryForm(instance=enquiry)})
        else:
            messages.error(request, "You don't have permission to view this enquiry.")
            return redirect('enquiries')  
    else:
        if request.GET.get('enquiry_number'):
            return render(request, 'contactus/enquiry_detail.html', {'enquiry': enquiry, 'form': EditEnquiryForm(instance=enquiry)})
        else:
            messages.error(request, "You must be logged in to view enquiry details.")
            return redirect('login')

    template = 'contactus/enquiry_detail.html'
    context = {
        'enquiry_form': form,
        'profile': profile,
        'enquiries': enquiries,
    }
    return render(request, template, context)


def enquiries_success(request, pk):
    """ View for displaying successful submission """
    enquiry = get_object_or_404(Enquiry, id=pk)
    return render(request, 'contactus/enquiries_success.html', {'enquiry': enquiry})