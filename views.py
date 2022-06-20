from django.shortcuts import render

import mapmomes.models as mo
import mapmomes.forms as forms

from dijk.progs_python.mon_folium import couleur_of_int



def recherche(requête):
    form = forms.RechercheBasique(requête.GET or None)
    if form.is_valid():
        # formulaire rempli
        return résultat_recherche(requête, form)
    else:
        return render(requête, "mapmomes/recherche.html", {"form":form})



def résultat_recherche(requête, form):
    """
    Entrée : requête, contenant un GET rempli.
    """
    tl = form.cleaned_data["type_lieu"]
    éqs = form.cleaned_data["équipement"]


    def score(lieu):
        return sum(1 for é in lieu.équipement.all() if é in éqs )

    res = sorted(
        (
            {"score": score(l), "lieu":l}
            for l in mo.Lieu.objects.filter(typeLieu=tl)
        ),
        key = lambda d: -d["score"]
    )
    res = [d for d in res if d["score"]>0]
    if res:
        for r in res:
            r["couleur"] = couleur_of_int(r["score"], 1, len(éqs))

        lons = [r["lieu"].lon for r in res]
        lats = [r["lieu"].lat for r in res]
        centre = (sum(lons)/len(lons), sum(lats)/len(lats))
    else:
        print("Aucun résultat")
        res=[]

    données = {"type_lieu": tl, "res":res, "centre":centre}
    return render(requête, "mapmomes/résultat.html", données)
