from django import forms
from .models import Integrated_development_env,Useraccess

from .models import CodeSnippet

class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['code']
        

class IDE_form(forms.ModelForm):
    class Meta:
        model = Integrated_development_env
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'id': 'code'}),    
            
        }
        
                       
    
class UseraccessForm(forms.Form):
    access_code = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Access Code'}))

