from django import forms


class QuestionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuestionsForm, self).__init__(*args, **kwargs)

        choices = [(True, 'True'), (False, 'False')]

        for i, question in enumerate(questions):
            self.fields['question_%s' % question.id] = forms.ChoiceField(
                label=question.question,
                choices=choices,
                widget=forms.RadioSelect,
                required=True
            )

    def clean(self):
        cleaned_data = super(QuestionsForm, self).clean()
        return cleaned_data

    def answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('question_'):
                yield (int(name.split('_')[1]), value)
