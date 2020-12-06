from django.contrib import admin
from video_encoding.admin import FormatInline
from django.db.models.signals import pre_save, post_save, pre_delete
from .models import User, BoardModel, SnippetModel
from .signals import convert_video

admin.site.register(User)
admin.site.register(BoardModel)
admin.site.register(SnippetModel)


class BoardModelAdmin(admin.ModelAdmin):
    inlines = (FormatInline,)

    list_dispaly = ('get_filename', 'width', 'height', 'duration')
    fields = ('file', 'width', 'height', 'duration')
    readonly_fields = fields

    def ready(self):
        post_save.connect(convert_video, sender=BoardModel)
        pre_delete.connect(auto_delete_file_on_delete, sender=BoardModel)
        pre_save.connect(auto_delete_file_on_change, sender=BoardModel)
        pre_delete.connect(auto_delete_snippet_file_ondelete,
                           sender=SnippetModel)
        pre_save.connect(auto_delete_snippet_file_onchange,
                         sender=SnippetModel)
# Register your models here.
