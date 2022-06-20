

function latLng_of_texte(texte){
    const t = texte.split(";").map(parseFloat);
    return L.latLng(t[1], t[0]);
}

function markerHtmlStyles(coul){
    return `
  background-color: ${coul};
  width: 3rem;
  height: 3rem;
  display: block;
  left: -1.5rem;
  top: -1.5rem;
  position: relative;
  border-radius: 3rem 3rem 0;
  transform: rotate(45deg);
  border: 1px solid gray`;
}


function mon_icone(coul){
    return L.divIcon({
	className: "my-custom-pin",
	iconAnchor: [0, 24],
	labelAnchor: [-6, 0],
	popupAnchor: [0, -36],
	html: `<span style="${markerHtmlStyles(coul)}" />`
    });
}



function ajoute_marqueur(carte, coords, nom, lien, couleur){
    const marqueur = new L.marker(coords, {icon: mon_icone(couleur)});
    marqueur.addTo(carte)
	.bindPopup(contenu_popup(nom, lien));
}

function contenu_popup(nom, lien){
    return nom + "</br>" + "<a href='"+lien+"'> site officiel </a>";
}
