from django.contrib import admin
from .models import University, SubjectArea

# Register your models here.

#tutaj będą modele które admin może edytować
# Username: Admin
# email: admin@mail.com
# Pass: 123

#drugi admin dla leniwych
# Username: admin
# Pass: admin

admin.site.register(University)
admin.site.register(SubjectArea)