# -*- coding:utf-8 -*-


from django import forms
import mapmomes.models as mo


class RechercheBasique(forms.Form):
    type_lieu = forms.ModelChoiceField(
        queryset=mo.TypeLieu.objects.all(),
        label="Type de lieu",
    )
    équipement = forms.ModelMultipleChoiceField(
        queryset=mo.Équipement.objects.all(),
        label="Équipements souhaités",
        widget=forms.CheckboxSelectMultiple
    )
