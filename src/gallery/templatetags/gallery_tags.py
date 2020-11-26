from django import forms, template
from django.conf import settings
from django.template import Context, loader

from crispy_forms.utils import TEMPLATE_PACK, get_template_pack

register = template.Library()


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)


@register.filter
def is_radioselect(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_checkboxselectmultiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_clearable_file(field):
    return isinstance(field.field.widget, forms.ClearableFileInput)


@register.filter
def is_multivalue(field):
    return isinstance(field.field.widget, forms.MultiWidget)


@register.filter
def classes(field):
    return field.widget.attrs.get("class", None)


@register.filter
def css_class(field):
    return field.field.widget.__class__.__name__.lower()


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


class CrispyFieldNode(template.Node):
    def __init__(self, field, attrs):
        self.field = field
        self.attrs = attrs
        self.html5_required = "html5_required"

    def render(self, context):  # noqa: C901
        # Nodes are not threadsafe so we must store and look up our instance
        # variables in the current rendering context first
        if self not in context.render_context:
            context.render_context[self] = (
                template.Variable(self.field),
                self.attrs,
                template.Variable(self.html5_required),
            )

        field, attrs, html5_required = context.render_context[self]
        field = field.resolve(context)
        try:
            html5_required = html5_required.resolve(context)
        except template.VariableDoesNotExist:
            html5_required = False

        template_pack = context.get("template_pack", TEMPLATE_PACK)

        widgets = getattr(field.field.widget, "widgets", [getattr(field.field.widget, "widget", field.field.widget)])

        if isinstance(attrs, dict):
            attrs = [attrs] * len(widgets)

        converters = {
            "textinput": "textinput textInput",
            "fileinput": "fileinput fileUpload",
            "passwordinput": "textinput textInput",
        }
        converters.update(getattr(settings, "CRISPY_CLASS_CONVERTERS", {}))

        for widget, attr in zip(widgets, attrs):
            class_name = widget.__class__.__name__.lower()
            class_name = converters.get(class_name, class_name)
            css_class = widget.attrs.get("class", "")
            if css_class:
                if css_class.find(class_name) == -1:
                    css_class += " %s" % class_name
            else:
                css_class = class_name

            if (
                    template_pack == "bootstrap3"
                    and not is_checkbox(field)
                    and not is_file(field)
                    and not is_multivalue(field)
            ):
                css_class += " form-control"
                if field.errors:
                    css_class += " form-control-danger"

            if template_pack == "bootstrap4" and not is_multivalue(field):
                if not is_checkbox(field):
                    css_class += " form-control"
                    if is_file(field):
                        css_class += "-file"
                if field.errors:
                    css_class += " is-invalid"
                elif field.form.is_bound:
                    css_class += " is-valid"

            widget.attrs["class"] = css_class

            # HTML5 required attribute
            if html5_required and field.field.required and "required" not in widget.attrs:
                if field.field.widget.__class__.__name__ != "RadioSelect":
                    widget.attrs["required"] = "required"

            for attribute_name, attribute in attr.items():
                attribute_name = template.Variable(attribute_name).resolve(context)

                if attribute_name in widget.attrs:
                    widget.attrs[attribute_name] += " " + template.Variable(attribute).resolve(context)
                else:
                    widget.attrs[attribute_name] = template.Variable(attribute).resolve(context)

        return str(field)


@register.tag(name="crispy_field")
def crispy_field(parser, token):
    token = token.split_contents()
    field = token.pop(1)
    attrs = {}

    token.pop(0)
    for attribute_name, value in pairwise(token):
        attrs[attribute_name] = value

    return CrispyFieldNode(field, attrs)
