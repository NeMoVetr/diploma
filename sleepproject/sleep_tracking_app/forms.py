from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import SleepRecord, UserData, User


class UserDataForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    )
    date_of_birth = forms.DateField(required=True, label='Дата рождения',
                                    widget=forms.DateInput(attrs={'type': 'date'}))
    weight = forms.IntegerField(min_value=10, required=True, label='Вес',
                                widget=forms.TextInput(attrs={'placeholder': 'Введите ваш вес (кг)'}))
    gender = forms.CharField(label='Пол', widget=forms.Select(choices=GENDER_CHOICES))
    height = forms.IntegerField(min_value=10, required=True, label='Рост',
                                widget=forms.TextInput(attrs={'placeholder': 'Введите ваш рост (см)'}))
    active = forms.BooleanField(label='Подписаться на рассылку', required=False)

    class Meta:
        model = UserData
        fields = ['date_of_birth', 'weight', 'gender', 'height', 'active']


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Ваш пароль должен содержать не менее 8 символов.'
        self.fields['password2'].help_text = 'Введите тот же пароль, что и раньше, для подтверждения.'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Никнейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }
        help_texts = {
            'username': 'Требуемый. не более 150 символов. Только буквы, цифры и @/./+/-/_.',
        }


class UserInfoUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Ник', max_length=150)
    first_name = forms.CharField(label='Имя', max_length=150)
    last_name = forms.CharField(label='Фамилия', max_length=150)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Ник',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class SleepRecordForm(forms.ModelForm):
    deep_sleep_duration = forms.FloatField(label='Продолжительность глубокой фазы сна:',
                                           widget=forms.TextInput(attrs={'placeholder': 'Введите число в часах'}))
    fast_sleep_duration = forms.FloatField(label='Продолжительность лёгкой фазы сна:',
                                           widget=forms.TextInput(attrs={'placeholder': 'Введите число в часах'}))
    total_time_bed = forms.FloatField(label='Общее время, проведённое в кровати:',
                                      widget=forms.TextInput(attrs={'placeholder': 'Введите число в часах'}))

    class Meta:
        model = SleepRecord
        fields = ['deep_sleep_duration', 'fast_sleep_duration', 'total_time_bed']
        labels = {
            'deep_sleep_duration': 'Продолжительность глубокой фазы сна:',
            'fast_sleep_duration': 'Продолжительность лёгкой фазы сна:',
            'total_time_bed': 'Общее время, проведённое в кровати:',
        }


class UpdateSleepRecordForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UpdateSleepRecordForm, self).__init__(*args, **kwargs)
        # Filter the queryset based on the user input
        self.fields['data_sleep'].queryset = SleepRecord.objects.filter(user=user).values_list('sleep_time',
                                                                                               flat=True).distinct()

    data_sleep = forms.ModelChoiceField(queryset=SleepRecord.objects.values_list('sleep_time', flat=True).distinct(),
                                        label='Дата:', to_field_name='sleep_time')
    deep_sleep_duration = forms.FloatField(label='Продолжительность глубокой фазы сна:',
                                           widget=forms.TextInput(attrs={'placeholder': 'Введите число в часах'}))
    fast_sleep_duration = forms.FloatField(label='Продолжительность лёгкой фазы сна:',
                                           widget=forms.TextInput(attrs={'placeholder': 'Введите число в часах'}))
    total_time_bed = forms.FloatField(label='Общее время, проведённое в кровати:',
                                      widget=forms.TextInput(attrs={'placeholder': 'Введите число в часах'}))

    class Meta:
        model = SleepRecord
        fields = ['data_sleep', 'deep_sleep_duration', 'fast_sleep_duration', 'total_time_bed']
        labels = {
            'deep_sleep_duration': 'Продолжительность глубокой фазы сна:',
            'fast_sleep_duration': 'Продолжительность лёгкой фазы сна:',
            'total_time_bed': 'Общее время, проведённое в кровати:',
        }
