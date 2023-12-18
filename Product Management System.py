from abc import ABC, abstractmethod

class Composition:
    def __init__(self, produit, quantite):
        self._produit = produit
        self._quantite = quantite

    @property
    def produit(self):
        return self._produit

    @produit.setter
    def produit(self, value):
        self._produit = value

    @property
    def quantite(self):
        return self._quantite

    @quantite.setter
    def quantite(self, value):
        self._quantite = value

    def equals(self, other):
        if isinstance(other, Composition):
            return self.produit.equals(other.produit) and self.quantite == other.quantite
        return False

class Produit(ABC):
    def __init__(self, nom, code):
        self._nom = nom
        self._code = code

    @property
    def nom(self):
        return self._nom

    @property
    def code(self):
        return self._code

    @abstractmethod
    def getPrixHT(self):
        pass

    def equals(self, other):
        if isinstance(other, Produit):
            return self.nom == other.nom and self.code == other.code
        return False

class ProduitElementaire(Produit):
    def __init__(self, nom, code, prixAchat):
        super().__init__(nom, code)
        self._prixAchat = prixAchat

    def __str__(self):
        return f"Produit Elementaire: {self.nom}, Code: {self.code}, Prix Achat: {self._prixAchat}"

    def getPrixHT(self):
        return self._prixAchat

    def equals(self, other):
        return super().equals(other) and self._prixAchat == other._prixAchat

class ProduitCompose(Produit):
    tauxTVA = 0.18

    def __init__(self, nom, code, fraisFabrication):
        super().__init__(nom, code)
        self._fraisFabrication = fraisFabrication
        self._listeConstituants = []

    @property
    def fraisFabrication(self):
        return self._fraisFabrication

    def ajouterConstituant(self, constituant):
        self._listeConstituants.append(constituant)

    def __str__(self):
        return f"Produit Composé: {self.nom}, Code: {self.code}, Frais de Fabrication: {self._fraisFabrication}"

    def getPrixHT(self):
        prixHT = self._fraisFabrication
        for constituant in self._listeConstituants:
            prixHT += constituant.produit.getPrixHT() * constituant.quantite
        return prixHT

    def equals(self, other):
        if not super().equals(other):
            return False
        return self._fraisFabrication == other._fraisFabrication and self.compareConstituants(other._listeConstituants)

    def compareConstituants(self, otherConstituants):
        if len(self._listeConstituants) != len(otherConstituants):
            return False
        for constituant in self._listeConstituants:
            if not any(constituant.equals(c) for c in otherConstituants):
                return False
        return True

# Example usage
p1 = ProduitElementaire("Produit 1", "P1", 100)
p2 = ProduitElementaire("Produit 2", "P2", 150)

p3 = ProduitCompose("Produit 3", "P3", 50)
p3.ajouterConstituant(Composition(p1, 2))
p3.ajouterConstituant(Composition(p2, 4))

# Test and display
print(p3)
print(f"Prix HT de {p3.nom}: {p3.getPrixHT()}")
