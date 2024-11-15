from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError

from lavanderia.models import Washer, AvaibleSlot, ReservedSlot, LavanderiaUser


class WasherForm(forms.ModelForm):
    class Meta:
        model = Washer
        fields = ['name']


# Validador para garantir que a duração seja positiva
def validate_positive_duration(value):
    if value < timedelta(seconds=0):
        raise ValidationError("A duração não pode ser negativa.")

class AvaibleSlotForm(forms.ModelForm):
    class Meta:
        model = AvaibleSlot
        fields = ['washer', 'start', 'duration']

        # Personalizando widgets para os campos
        widgets = {
            'start': forms.DateTimeInput(
                attrs={
                    'placeholder': 'YYYY-MM-DD HH:MM',  # Orienta o usuário sobre o formato
                    'class': 'form-control',
                    'type': 'datetime-local',  # Usando input datetime-local para navegadores modernos
                }
            ),
            'washer': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'duration': forms.TextInput(
                attrs={
                    'placeholder': 'HH:MM:SS',  # Exemplo: 01:30:00 para 1h30min
                    'class': 'form-control'
                }
            )
        }

    # Adicionando validação personalizada para garantir que a duração seja positiva
    duration = forms.DurationField(
        widget=forms.TextInput(attrs={'placeholder': 'HH:MM:SS', 'class': 'form-control'}),
        validators=[validate_positive_duration],
        label='Duração'
    )


    def clean(self):
        # Primeiro, chamamos o super para garantir que o cleaned_data seja preenchido
        cleaned_data = super().clean()

        # Acessamos os dados limpos que foram passados para o formulário de validação
        washer = cleaned_data.get('washer')
        start = cleaned_data.get('start')
        duration = cleaned_data.get('duration')

        if washer and start and duration:
            # Calcula o horário de término
            end_time = start + duration

            # Verifica se há algum slot existente que sobrepõe o novo slot
            overlapping_slots = AvaibleSlot.objects.filter(
                washer=washer,
                start__lt=end_time,  # Início de um slot já registrado antes do fim do novo slot
                start__gte=start - timedelta(seconds=1)
                # O início do slot já registrado ocorre após o início do novo slot
            )

            if overlapping_slots.exists():
                raise ValidationError(
                    "Já existe um slot para essa lavadora no período selecionado."
                )

        # Retorna os dados limpos após a validação
        return cleaned_data



class ReservedSlotForm(forms.ModelForm):
    # Cria um campo de seleção (drop-down) para os slots disponíveis
    slot = forms.ModelChoiceField(
        queryset=AvaibleSlot.objects.all(),  # Obtém todos os slots disponíveis
        widget=forms.Select(attrs={'class': 'form-control'}),  # Personaliza o widget, se necessário
        label="Available Slot"  # Rotulo para o campo
    )

    class Meta:
        model = ReservedSlot
        fields = ['slot', 'presence']  # Exibe os campos 'slot' e 'presence'

    presence = forms.BooleanField(
        required=False,
        label='Presence',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})  # Personaliza o widget de checkbox
    )


# Formulário para escolher uma data
class DateFilterForm(forms.Form):
    data = forms.DateField(
        label='Filtrar por data',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

class LavanderiaUserForm(forms.ModelForm):
    class Meta:
        model = LavanderiaUser
        fields = ['username', 'email', 'password', 'bolsista', 'matricula', 'apartamento', 'telefone']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bolsista': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'apartamento': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'password': 'Senha',
            'bolsista': 'Bolsista?',
            'matricula': 'Matrícula',
            'apartamento': 'Apartamento',
            'telefone': 'Telefone',
        }
