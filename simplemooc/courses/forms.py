from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from simplemooc.core.mail import send_mail_template
from .models import Comments

class ContactCourse(forms.Form):

    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

    def send_mail(self, course):
        subject = 'Contato Sobre o curso'+ course.name
        message = 'nome: %(name)s;E-mail: %(email)s;%(message)s'
        context = {'name': self.cleaned_data['name'],
                   'email': self.cleaned_data['email'],
                   'message': self.cleaned_data['message'], }
        message = message % context
        template_name = 'courses/contact_email.html'
        send_mail_template(subject,template_name,  context, [settings.EMAIL_CONTACT])

class CommentForm(forms.ModelForm):


    class Meta:
        model = Comments
        fields = ['comment']