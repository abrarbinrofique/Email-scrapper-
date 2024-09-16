from django.urls import path,include
from.import views


from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('loademail',views.ScrappingViewset)

router.register('pasthistory',views.HistoryViewSet)


urlpatterns = [
 
    path("",include(router.urls)),
    
]