from django import forms
from category.models import Category

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name","description")

    name = forms.CharField(max_length=50, label="类别名")
    description = forms.CharField(max_length=300, label="描述")