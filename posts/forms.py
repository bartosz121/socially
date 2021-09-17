from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column, Submit
from crispy_forms.bootstrap import FormActions
from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Row(Column("body", css_class="col")),
                Row(
                    Column(
                        Row(
                            Column("picture", css_class="col-lg-9"),
                            Column(
                                FormActions(
                                    Submit(
                                        "submit_post",
                                        "Post",
                                        css_class="w-100",
                                    ),
                                    css_class="ms-lg-3 w-100",
                                ),
                            ),
                        ),
                    ),
                ),
                css_class="mx-md-5",
            ),
        )
        self.fields["body"].widget.attrs.update(
            {
                "rows": 4,
                "placeholder": "What's on your mind?",
            }
        )

    class Meta:
        model = Post
        fields = ["body", "picture"]
        exclude = ["parent", "author", "liked", "created", "updated"]
        labels = {"body": "", "picture": ""}
