from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.sites.models import Site
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from knox.models import AuthToken


def basic_perm_translation(text):
    text = text.replace('Can view', 'Puede ver')
    text = text.replace('Can add', 'Puede agregar')
    text = text.replace('Can change', 'Puede modificar')
    text = text.replace('Can delete', 'Puede eliminar')
    text = text.replace('group', 'grupos')
    text = text.replace('log entry', 'entradas de registro')
    text = text.replace('permission', 'permisos')
    text = text.replace('session', 'sesiones')
    return text


Permission.__str__ = lambda self: '%s | %s' %  (self.content_type, basic_perm_translation(self.name))

admin.site.site_header = 'Repuestos Toretto'
admin.site.site_title = 'Repuestos Toretto'
admin.site.index_title = 'Panel de Administración'

admin.site.index_template = 'admin/customIndex.html'
admin.site.site_url = settings.SITE_URL
# Cancelar registro de los modelos DjangoJob and DjangoJobExecution
admin.site.unregister(DjangoJob)
admin.site.unregister(DjangoJobExecution)
admin.site.unregister(AuthToken)

admin.site.unregister(Site)
