from django.conf.urls import url

from . import views

urlpatterns = [
	url(r"^$", views.index, name="index"),
	url(r"^blamelist", views.blamelist, name="blamelist"),
	url(r"^execute/(?P<id>[0-9]?)$", views.execute_command, name="execute"),
	url(r"^temp", views.measure_temp, name="measure_temp"),
]
