from django.shortcuts import render
from home.models import (Page, 
            SEO_Optimiser, 
            FAQ, Feedback, RentalsAndServices,
            PAGE_TEMPLATE_CHOICES)
from tours.models import Tour
from blog.models import Post
from django.core.mail import send_mail 
from django.shortcuts import redirect 
from django.http import HttpResponseRedirect
from tours.models import Destination
# Create your views here.

def homePage(request):
    tours = Tour.objects.all().order_by('-id')[:4]
    posts = Post.objects.all().order_by('-id')[:4]
    SEO = SEO_Optimiser.objects.get(seoid=2)
    feedbacks = Feedback.objects.all()
    destinations = Destination.objects.filter()[:6] 
    args = {
            'SEO': SEO,
            'tours': tours,
            'posts': posts,
            'feedbacks': feedbacks,
            'destinations': destinations, 
        }
    return render(request, 'home/index.html', args)

def requestPage(request):
    
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        message = request.POST.get('message','')
        # if result['success']:
        fromDTP = 'info@pakoltravel.com' #'sales@pakoltravel.com'
        reciever_list= ('info@pakoltravel.com',) #info@pakoltravel.com
        # toDTP = 'info@pakoltravel.com'
        
        # Send a notofocation to client also

        
        message = "A new request from "+str(name)+". \n\n" \
        + "\n\nCUSTOMER DETAILS and INFORMATION:\n" \
        +"\nName: "+str(name)  \
        + "\nEmail: " + str(email)  \
        + "\nMessage: "+str(message) \
        + " \n\nPlease reply to this message  during 24 hours. \n\n" \
        + "Best regards,\n\n Pakol Travel team"
        
        subject = 'New request from '+str(name) 

        send_mail(subject, message, fromDTP, reciever_list, fail_silently=False, )
        return HttpResponseRedirect('/send-request/success')

    SEO = SEO_Optimiser.objects.get(seoid=1) 

    args = {
        'SEO': SEO,
    }
    return render(request, 'home/request.html',args)

def aboutUs(request):
    page = Page.objects.get(pageid=1) #Look in admin for the page id
    template = 'home/about-us.html'
    SEO = page.SEO
    args = {
        'page': page,
        'SEO': SEO,
    }
    return render(request, template, args) #



def contacts(request):

    if request.method == 'POST':
        name = request.POST.get('name') if request.POST.get('name') != None else ''
        phone = request.POST.get('phone') if request.POST.get('phone') != None else ''
        email = request.POST.get('email') if request.POST.get('email') != None else ''
        message = request.POST.get('message') if request.POST.get('message') != None else ''

        fromEmail = 'info@pakoltravel.com'
        toEmail = 'info@pakoltravel.com'

        finalMessage = 'Hello!!\n\nOne of our visitors - '\
            'has sent an email using Contact form of our website. \n\
            Please read his/her requirements below:\n\n\
            MESSAGE AND SENDER DETAILS:\n\
            Name: '+ str(name) + '\n\
            Email: '+ str(email) + '\n\
            Phone: ' + str(phone) + '\n\
            Message:' +str(message)+ '\n\n\
            Please reply to his/her email during next 24 hours.\n\n\
            Best regards,\n\nPakol Travel team'

        subject = "A new message via 'Contact' form from " + str(name) 
        send_mail(subject, finalMessage, fromEmail, (toEmail,), fail_silently=False,)
        # return redirect('home:contacts')
        # args = {
        #         'tours': Tour.objects.order_by('-Created')[:3],
        #     }
        # return render(request, 'home/mail-sent-success.html', args)
        return HttpResponseRedirect('/send-request/success')


        
    # page = Page.objects.get(pageid=1) 
    template = 'home/contacts.html'
    SEO = SEO_Optimiser.objects.get(seoid=4)
    args = {
        # 'page': page,
        'SEO': SEO,
    }
    return render(request, template, args) #

def FAQs(request):
    # SEO = SEO_Optimiser.objects.get(seoid=1)
    page = Page.objects.get(pageid=7)
    SEO = page.SEO
    FAQs = FAQ.objects.all()

    args = {
            'SEO': SEO,
            'page': page,
            'FAQs': FAQs,
            }
    return render(request, 'home/faq.html', args) 


def ourServices(request):
    page = Page.objects.get(pageid=2) 
    objs=RentalsAndServices.objects.all()

    template = 'home/our-services.html'
    SEO = page.SEO
    args = {
        'page': page,
        'SEO': SEO,
        'objs': objs,
    }
    return render(request, template, args) #


def serviceRentalDetails(request, Slug):
    service=RentalsAndServices.objects.get(Slug=Slug)
    objs=RentalsAndServices.objects.all()

    # title = ' '.join(Slug.split('-')).capitalize() 
    context = {
        'obj' : service,
        'objs': objs, 
        # 'title': title,
    }
    return render(request, 'home/our-service-details.html',context)



