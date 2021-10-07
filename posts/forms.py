from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column, Submit
from crispy_forms.bootstrap import FormActions
from .models import Post


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["query"].label = ""
        self.fields["query"].widget.attrs.update(
            {"placeholder": "Search for user or post"}
        )
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Row("query"),
                Row(
                    FormActions(
                        Submit(
                            "search_btn",
                            "Search",
                            css_class="w-100",
                        ),
                    ),
                ),
            )
        )

    query = forms.CharField()


class PostForm(forms.ModelForm):
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


class ReplyForm(PostForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].widget.attrs.update({"placeholder": "Reply..."})
        # TODO this is the only way i can get into 'Submit' btn in Layout
        # self.helper["submit_post"] and self.helper.filter(Submit) wont work
        self.helper.layout[0][1][0][0][1][0][0].value = "Reply"

    class Meta:
        model = Post
        fields = ["parent", "body", "picture"]
        exclude = ["author", "liked", "created", "updated"]
        labels = {"body": "", "picture": ""}
