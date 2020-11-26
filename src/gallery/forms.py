from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
from django.forms import ValidationError
from django.template import Template
from re import sub

from crispy_forms.helper import FormHelper
from crispy_forms.layout import LayoutObject, ButtonHolder, Submit, HTML
from crispy_forms.layout import Layout, Row, Column, Fieldset, Div, Field

from django import forms
from gallery import models


class SucessField(Field):
    template = 'forms/success_field.html'


class JasnyImageField(LayoutObject):

    def __init__(self, name, prefix):
        self.template = 'forms/image_field.html'
        self.name = name
        self.prefix = prefix

    def render(self, form, form_style, context, template_pack):
        extra_context = {
            'field_name': self.name,
            'field_prefix': self.prefix
        }
        return render_to_string(self.template, extra_context)


class SubmitOutline(Submit):
    def __init__(self, *args, **kwargs):
        super(SubmitOutline, self).__init__(*args, **kwargs)
        self.field_classes = 'col col-md-4 btn btn-outline-success ml-md-auto'


class Formset(LayoutObject):

    def __init__(self, formset_name):
        self.template = 'forms/formset.html'
        self.formset_name = formset_name

    def render(self, form, form_style, context, **kwargs):
        extra_context = {
            'formset': context[self.formset_name]
        }
        return render_to_string(self.template, extra_context)


class Control:

    def __init__(self, direction, css_classes):
        control_base = '<span class=\"{}\">\n\t' + \
                       '<i class=\"fas fa-angle-{}\"></i>\n' + \
                       '</span>'
        self.html = control_base.format(css_classes, direction)

    def render(self, form, form_style, context, **kwargs):
        return Template(str(self.html)).render(context)


class PetPhotoForm(forms.ModelForm):

    class Meta:
        model = models.PetPhoto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PetPhotoForm, self).__init__(*args, **kwargs)

        formtag_prefix = sub('-[0-9]+$', '', kwargs.get('prefix', ''))

        self.helper = FormHelper()
        self.helper.disable_csrf = True

        self.helper.layout = Layout(
            Row(
                JasnyImageField('image', kwargs.get('prefix', '')),
                css_class='formset_row-{}'.format(formtag_prefix)
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class PetForm(forms.ModelForm):

    class Meta:
        model = models.Pet
        exclude = ['created_by']

        widgets = {
            'description': forms.Textarea(attrs={'cols': 70, 'rows': 4})
        }
        help_texts = {
            'age': 'Type it in years',
            'description': '150 symbols'
        }

    def __init__(self, *args, **kwargs):
        super(PetForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.disable_csrf = True

        self.helper.layout = Layout(Div(
            Row(
                Column(SucessField('name'), css_class='col-12'),
                Column(SucessField('category'), css_class='col-12 col-sm-6'),
                Column(SucessField('breed'), css_class='col-12 col-sm-6'),
                Column(SucessField('gender'), css_class='col-12 col-sm-6'),
                Column(SucessField('age'), css_class='col-12 col-sm-6'),
                Column(SucessField('description'), css_class='col-12')
            ),
            Fieldset(
                'Add photo',
                Div(
                    Formset('photo'),
                    css_class='formset-photos'
                ),
                Control('left', 'formset-prev d-none d-sm-flex'),
                Control('right', 'formset-next d-none d-sm-flex'),
                css_class='form-row-photos'
            ),
            HTML('<hr>'),
            ButtonHolder(
                SubmitOutline('submit', 'Create', formnovalidate=''),
                css_class='d-flex'
            )
        ))

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')

        if age and (age < 0 or age > 100):
            raise ValidationError(
                {'age': 'Incorrect age. Please, write it again.'}
            )

        return cleaned_data

PetFormset = inlineformset_factory(
    models.Pet,
    models.PetPhoto,
    form=PetPhotoForm,
    fields=['image'],
    extra=0,
    can_delete=True,
    min_num=1,
    max_num=6
)