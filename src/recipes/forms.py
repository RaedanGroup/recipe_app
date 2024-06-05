from django import forms

CHART_CHOICES = (
    ('pie-chart', 'Pie'),
    ('line-chart', 'Line'),
    ('bar-chart', 'Bar')
)

class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(label='Search', max_length=100, required=False)
    chart_type = forms.ChoiceField(label='Chart', choices=CHART_CHOICES, required=False)