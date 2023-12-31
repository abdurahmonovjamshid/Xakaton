from django import forms
from django.contrib import admin
from users.models import User

from .models import Category, Post, PostImage

# Register your models here.


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = Category.objects.filter(
            parent__isnull=False)


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    inlines = [PostImageInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'seller'] 
    list_filter = ['seller']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['seller'].initial = request.user.id
        form.base_fields['seller'].widget = forms.HiddenInput()
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Create PostImage instances for the newly created Post object
        for image_file in request.FILES.getlist('photos'):
            PostImage.objects.create(post=obj, image=image_file)
