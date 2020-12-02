from django.contrib import admin
from video_encoding.admin import FormatInline
from django.db.models.signals import pre_save, post_save, pre_delete
from .models import User, BoardModel
from .signals import convert_video

admin.site.register(User)
admin.site.register(BoardModel)


class BoardModelAdmin(admin.ModelAdmin):
    inlines = (FormatInline,)

    list_dispaly = ('get_filename', 'width', 'height', 'duration')
    fields = ('file', 'width', 'height', 'duration')
    readonly_fields = fields

    def ready(self):
        post_save.connect(convert_video, sender=BoardModel)
        pre_delete.connect(auto_delete_file_on_delete, sender=BoardModel)
        pre_save.connect(auto_delete_file_on_change, sender=BoardModel)
# Register your models here.
