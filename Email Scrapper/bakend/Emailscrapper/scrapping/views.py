from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Scrapping,History
from .serializer import ScrappingSerializers,HistorySerializers
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import JsonResponse

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
    queryset = Scrapping.objects.all()
    serializer_class = ScrappingSerializers

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)
        return queryset
    
    @action(detail=False, methods=['post'])
    def emailsearch(self, request):
        def scrape_info(url, keywords):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                emails = set()
                names = set()
                titles = set()
                website_urls = set()

                # Extracting email addresses
                for keyword in keywords:
                    matches = soup.find_all(string=re.compile(keyword, flags=re.IGNORECASE))
                    for match in matches:
                        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', match)
                        if email:
                            emails.update(email)

                # Extracting possible names from h1, h2, h3 tags
                name_tags = soup.find_all(['h1', 'h2', 'h3', 'meta'])
                for tag in name_tags:
                    if tag.string:
                        name = tag.string.strip()
                        if name:
                            names.add(name)
                
                # Extracting title from the meta tags or title tag
                title_tag = soup.find('title')
                if title_tag and title_tag.string:
                    titles.add(title_tag.string.strip())

                # Getting the URL of the page
                website_urls.add(url)

                return {
                    'emails': emails,
                    'names': names,
                    'titles': titles,
                    'website_urls': website_urls
                }

            except requests.exceptions.SSLError as e:
                print('Error fetching the data:', str(e))
                return None

        # Keywords to look for emails
        keywords = ['contact', 'info', 'email','btfa.gov', 'gmail','btfa','gov', 'support', 'help', 'admin', 'sales', 'customer', 'service', 'inquiry', 'enquiries', 'team', 'hello', 'reach', 'mail', 'newsletter', 'feedback', 'complaint', 'request', 'submit', 'manager', 'career', 'hr', 'billing', 'account', 'legal', 'media', 'press', 'about']
        
        # Data from the request
        urls = request.data.get('url')
        userid = request.data.get('user')
        user_instance = User.objects.get(id=userid)
        scrapping_instance = Scrapping.objects.filter(user=user_instance).first()
        
        if not scrapping_instance:
            scrapping_instance = Scrapping.objects.create(user=user_instance)

        # Check scraping limit
       
        else:
            # Scraping the email, name, title, and website URL
            scraped_data = scrape_info(urls, keywords)
            
            if scraped_data:
                scrapping_instance.scrapping_limit += 1
                scrapping_instance.save()

                # Convert sets to lists
                emails_list = list(scraped_data['emails'])
                names_list = list(scraped_data['names'])
                titles_list = list(scraped_data['titles'])
                website_urls_list = list(scraped_data['website_urls'])

                # Saving to history
                user_History, created = History.objects.update_or_create(
                    url_list=urls,
                    email_list=",".join(emails_list),
                    user=user_instance,
                    scrape_time=timezone.now()
                )

                return JsonResponse({
                    'emails': emails_list,
                    'names': names_list,
                    'titles': titles_list,
                    'website_urls': website_urls_list,
                    'email_count': len(emails_list),
                    'name_count': len(names_list),
                    'title_count': len(titles_list)
                })

            return Response({'error': 'Failed to scrape information from the provided URL.'}, status=500)



class HistoryViewSet(viewsets.ModelViewSet):
    queryset=History.objects.all()
    serializer_class=HistorySerializers

    def get_queryset(self):
        queryset= super().get_queryset()
        user=self.request.query_params.get('user')
        if user:
            queryset=queryset.filter(user=user)
        
        return queryset
