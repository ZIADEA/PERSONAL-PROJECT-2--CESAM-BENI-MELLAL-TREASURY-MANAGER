from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pickle
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image  # Importez la classe Image
from kivy.graphics import Color, Rectangle
# Classe représentant la communauté
class Communaute:
    montant_cot = 0
    nbr_comm = 0

    def __init__(self, nat, nbr):
        self.nationalite = nat
        self.montant = 0
        self.nombre = nbr
        Communaute.nbr_comm += 1

    def afficher(self):
        return f"Nationalité : {self.nationalite}, Nombre : {self.nombre}, Montant : {self.montant}"

# Classe représentant l'entrée d'argent
class EntrerArgent:
    somme = 0
    nbr_source = 0

    def __init__(self, source):
        self.source = source
        self.apport = 0
        EntrerArgent.nbr_source += 1

# Classe représentant la dépense
class Depense:
    total_retrait = 0

    def __init__(self, motif):
        self.motif = motif
        self.retrait = 0

# Fonction pour calculer le solde total
def totaux_argent():
    solde = Communaute.montant_cot + EntrerArgent.somme - Depense.total_retrait
    return solde

# Fonction pour charger l'historique à partir d'un fichier
def charger_historique(nom_fichier):
    try:
        with open(nom_fichier, 'rb') as fichier:
            historique = pickle.load(fichier)
    except FileNotFoundError:
        historique = []
    return historique

# Fonction pour sauvegarder l'historique dans un fichier
def sauvegarder_historique(nom_fichier, historique):
    with open(nom_fichier, 'wb') as fichier:
        pickle.dump(historique, fichier)

# Classe principale de l'application
class ProjetApp(App):
    historique_cotisations = []
    historique_entree_argent = []
    historique_depenses = []

    def build(self):
        layout = BoxLayout(orientation='vertical') 
       
         
        
        logo = Image(source='R.png', size_hint=(1, None), height=100)
        layout.add_widget(logo)


# Créez un label
        titre_label = Label(text="TRESORERIE DE LA CESAM", font_size=24, size_hint=(1, None), height=50)

# Créez un canvas avec un Rectangle coloré en arrière-plan
        with titre_label.canvas.before:
            Color(1, 1, 0, 1)  # Couleur de l'arrière-plan (dans cet exemple, jaune)
            titre_label.rect = Rectangle(pos=titre_label.pos, size=titre_label.size)

# Lorsque la position ou la taille de l'étiquette change, mettez à jour la position et la taille du Rectangle
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size

        titre_label.bind(pos=update_rect, size=update_rect)

# Ajoutez l'étiquette à votre mise en page
        layout.add_widget(titre_label)

        
              

       

        # ...

        self.input_nat = TextInput(hint_text="Nationalité")
        self.input_nbr = TextInput(hint_text="Nombre")
        self.input_source = TextInput(hint_text="Source d'argent")
        self.input_motif = TextInput(hint_text="Motif de la dépense")
        self.input_montant_cot = TextInput(hint_text="Montant cotisation")
        self.input_apport = TextInput(hint_text="Montant apport")
        self.input_retrait = TextInput(hint_text="Montant retrait")

        # Bouton pour enregistrer une cotisation
        cotisation_button = Button(text="Enregistrer une cotisation", background_color=(0, 0, 1, 1))
        cotisation_button.bind(on_release=self.enregistrer_cotisation)
        layout.add_widget(self.input_nat)
        layout.add_widget(self.input_nbr)
        layout.add_widget(self.input_montant_cot)
        layout.add_widget(cotisation_button)

        # Bouton pour enregistrer une entrée d'argent
        entree_argent_button = Button(text="Enregistrer une entrée d'argent",background_color=(0, 0, 1, 1))
        entree_argent_button.bind(on_release=self.enregistrer_entree_argent)
        layout.add_widget(self.input_source)
        layout.add_widget(self.input_apport)
        layout.add_widget(entree_argent_button)

        # Bouton pour enregistrer une dépense
        depense_button = Button(text="Enregistrer une dépense", background_color=(0, 0, 1, 1))
        depense_button.bind(on_release=self.enregistrer_depense)
        layout.add_widget(self.input_motif)
        layout.add_widget(self.input_retrait)
        layout.add_widget(depense_button)

        # Bouton pour afficher l'historique des cotisations
        cotisation_history_button = Button(text="Historique des Cotisations" ,background_color=(0.5, 0.5, 1, 1))
        cotisation_history_button.bind(on_release=self.afficher_historique_cotisations)
        layout.add_widget(cotisation_history_button)

        # Bouton pour afficher l'historique des entrées d'argent
        entree_argent_history_button = Button(text="Historique des Entrées d'Argent",background_color=(0.5, 0.5, 1, 1))
        entree_argent_history_button.bind(on_release=self.afficher_historique_entree_argent)
        layout.add_widget(entree_argent_history_button)

        # Bouton pour afficher l'historique des dépenses
        depense_history_button = Button(text="Historique des Dépenses",background_color=(0.5, 0.5, 1, 1))
        depense_history_button.bind(on_release=self.afficher_historique_depenses)
        layout.add_widget(depense_history_button)

        # Bouton pour afficher le solde total
        solde_button = Button(text="Afficher le solde total")
        solde_button.bind(on_release=self.afficher_solde)
        layout.add_widget(solde_button)

        self.popup = None  # Popup pour afficher les résultats

        # Charger les données au démarrage de l'application
        self.charger_donnees()

        return layout

    def enregistrer_cotisation(self, instance):
        nat = self.input_nat.text
        nbr = int(self.input_nbr.text)
        montant_cot = float(self.input_montant_cot.text)
        communaute = Communaute(nat, nbr)

        # Enregistrement de la cotisation
        communaute.montant = montant_cot
        print(f"Vous avez ajouté : {montant_cot} au montant de la cotisation de la communauté {nat}. Le nouveau montant est de {communaute.montant}")

        # Mettre à jour l'historique des cotisations
        ProjetApp.historique_cotisations.append(communaute.afficher())

        # Mettre à jour le montant total des cotisations
        Communaute.montant_cot += montant_cot

        # Mettre à jour le solde total
        self.sauvegarder_donnees()

    def enregistrer_entree_argent(self, instance):
        source = self.input_source.text
        apport = float(self.input_apport.text)
        entree_argent = EntrerArgent(source)

        # Enregistrement de l'entrée d'argent
        entree_argent.apport = apport
        print(f"{source} a apporté : {apport}")

        # Mettre à jour l'historique des entrées d'argent
        ProjetApp.historique_entree_argent.append(f"{source} : {entree_argent.apport}")

        # Mettre à jour le montant total des entrées d'argent
        EntrerArgent.somme += apport

        # Mettre à jour le solde total
        self.sauvegarder_donnees()

    def enregistrer_depense(self, instance):
        motif = self.input_motif.text
        retrait = float(self.input_retrait.text)
        depense = Depense(motif)

        # Enregistrement de la dépense
        depense.retrait = retrait
        print(f"{motif} a nécessité : {retrait}")

        # Mettre à jour l'historique des dépenses
        ProjetApp.historique_depenses.append(f"{motif} : {depense.retrait}")

        # Mettre à jour le montant total des dépenses
        Depense.total_retrait += retrait

        # Mettre à jour le solde total
        self.sauvegarder_donnees()

    def afficher_historique_cotisations(self, instance):
        historique_text = "\n".join(ProjetApp.historique_cotisations)
        self.afficher_resultat("Historique des Cotisations", historique_text)

    def afficher_historique_entree_argent(self, instance):
        historique_text = "\n".join(ProjetApp.historique_entree_argent)
        self.afficher_resultat("Historique des Entrées d'Argent", historique_text)

    def afficher_historique_depenses(self, instance):
        historique_text = "\n".join(ProjetApp.historique_depenses)
        self.afficher_resultat("Historique des Dépenses", historique_text)

    def afficher_solde(self, instance):
        solde = totaux_argent()
        self.afficher_resultat("Solde Total", f"Le solde total est de : {solde}")

    def afficher_resultat(self, title, text):
        content = BoxLayout(orientation="vertical")
        label = Label(text=text)
        scrollview = ScrollView(size_hint=(1, 0.8))
        scrollview.add_widget(label)
        content.add_widget(scrollview)
        close_button = Button(text="Fermer")
        close_button.bind(on_press=self.dismiss_popup)
        content.add_widget(close_button)
        self.popup = Popup(title=title, content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def dismiss_popup(self, instance):
        if self.popup:
            self.popup.dismiss()

    def sauvegarder_donnees(self):
        # Sauvegarde de l'historique dans un fichier
        sauvegarder_historique("historique_cotisations.pkl", ProjetApp.historique_cotisations)
        sauvegarder_historique("historique_entree_argent.pkl", ProjetApp.historique_entree_argent)
        sauvegarder_historique("historique_depenses.pkl", ProjetApp.historique_depenses)

        # Sauvegarde des montants dans un fichier
        with open("montants.pkl", "wb") as fichier:
            pickle.dump({
                "montant_cot": Communaute.montant_cot,
                "somme_entree_argent": EntrerArgent.somme,
                "total_depenses": Depense.total_retrait
            }, fichier)

    def charger_donnees(self):
        # Charger l'historique à partir des fichiers
        ProjetApp.historique_cotisations = charger_historique("historique_cotisations.pkl")
        ProjetApp.historique_entree_argent = charger_historique("historique_entree_argent.pkl")
        ProjetApp.historique_depenses = charger_historique("historique_depenses.pkl")

        # Charger les montants à partir du fichier
        try:
            with open("montants.pkl", "rb") as fichier:
                montants = pickle.load(fichier)
                Communaute.montant_cot = montants["montant_cot"]
                EntrerArgent.somme = montants["somme_entree_argent"]
                Depense.total_retrait = montants["total_depenses"]
        except FileNotFoundError:
            pass
    def afficher_popup_bienvenue(self, instance):
        # Créez un popup avec le message "Bienvenue"
        popup = Popup(title="Bienvenue", content=Label(text="Bienvenue"), size_hint=(None, None), size=(400, 200))

        # Affichez le popup
        popup.open()
if __name__ == '__main__':
    ProjetApp().run()