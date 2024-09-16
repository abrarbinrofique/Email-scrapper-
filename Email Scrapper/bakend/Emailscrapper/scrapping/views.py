from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Scrapping,History
from .serializer import ScrappingSerializers,HistorySerializers
from django.utils import timezone
from django.contrib.auth.models import User

#deorators
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

#scrapping package
import requests
from bs4 import BeautifulSoup
import re
import time



# Create your views here.

class ScrappingViewset(viewsets.ModelViewSet):
    queryset=Scrapping.objects.all()
    serializer_class=ScrappingSerializers

    
    @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    def emailsearch(self,request):

      
        def scrape_emails(url, keywords):
           headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
           try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
 
                emails = set()
 
                for keyword in keywords:
                    matches = soup.find_all(string=re.compile(keyword, flags=re.IGNORECASE))
                    for match in matches:
                        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', match)
                        if email:
                          emails.update(email)
                return emails
        
           except requests.exceptions.SSLError as e:
             

            return Response('There is no email available')

      
        keywords = ['contact', 'info', 'email', 'gmail', 'support', 'help', 'admin', 'sales', 'customer', 'service', 'inquiry', 'enquiries', 'team', 'hello', 'reach', 'mail', 'newsletter', 'feedback', 'complaint', 'request', 'submit', 'manager', 'career', 'hr', 'billing', 'account', 'legal', 'media', 'press', 'about']
        urls=request.data.get('url')
        userid=request.data.get('user')
        user_instance=User.objects.get(id=userid)
        scrapping_instance = Scrapping.objects.filter(user=user_instance).first()
        if not scrapping_instance:
            scrapping_instance = Scrapping.objects.create(user=user_instance)

        if scrapping_instance.scrapping_limit>=3:
             return Response('you have cross the limit of scrap email')
        else:
             emails = scrape_emails(urls, keywords)
             if emails is not None:
                    scrapping_instance.scrapping_limit+=1
                    scrapping_instance.save()
                    print(emails)
                    print(f"Found {len(emails)} email addresses.")
       
                    user_History,created=History.objects.update_or_create(       
                      url_list=urls,
                      email_list=",".join(emails),
                      user=user_instance,
                      scrape_time=timezone.now()
                    )
                    return Response(f'congratulations you get your email,your emails are{emails}')

             return Response({'error': 'Failed to scrape emails from the provided URL.'}, status=500)



class HistoryViewSet(viewsets.ModelViewSet):
    queryset=History.objects.all()
    serializer_class=HistorySerializers

    def get_queryset(self):
        queryset= super().get_queryset()
        user=self.request.query_params.get('user')
        if user:
            queryset=queryset.filter(user=user)
        
        return queryset
