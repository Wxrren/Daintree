from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserProfile, Enquiry
from .forms import EnquiryForm

def enquiries(request):
    """ A view to show all enquiries, including sorting and search queries """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.user_profile = profile
            enquiry.save()
            messages.success(request, 'Enquiry submitted successfully')
            return redirect('enquiries')  
    else:
        form = EnquiryForm()

    enquiries = profile.enquiries.all().order_by('-date')

    template = 'contactus/enquiries.html'
    context = {
        'enquiry_form': form,
        'profile': profile,
        'on_profile_page': True,
        'enquiries': enquiries,
    }

    return render(request, template, context)