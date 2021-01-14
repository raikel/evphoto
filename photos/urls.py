from rest_framework.routers import SimpleRouter

from . import views

app_name = 'restapi'

router = SimpleRouter()

router.register(r'photos', views.PhotoView, 'photos')

urlpatterns = router.urls