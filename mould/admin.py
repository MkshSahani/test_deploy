from django.contrib import admin
from .models import Mould, MouldStatus, MouldComment

admin.site.register(Mould) # register Mould Model. 
admin.site.register(MouldStatus)
admin.site.register(MouldComment)