"""
    Clase que representa una encuesta realizada a un individuo.
    """
class Encuesta:
    def __init__(self, idEncuesta=None, edad=None, Sexo=None, BebidasSemana=None, 
                 CervezasSemana=None, BebidasFinSemana=None, BebidasDestiladasSemana=None, 
                 VinosSemana=None, PerdidasControl=None, DiversionDependenciaAlcohol=None, 
                 ProblemasDigestivos=None, TensionAlta=None, DolorCabeza=None):
        self.idEncuesta = idEncuesta
        self.edad = edad
        self.Sexo = Sexo
        self.BebidasSemana = BebidasSemana
        self.CervezasSemana = CervezasSemana
        self.BebidasFinSemana = BebidasFinSemana
        self.BebidasDestiladasSemana = BebidasDestiladasSemana
        self.VinosSemana = VinosSemana
        self.PerdidasControl = PerdidasControl
        self.DiversionDependenciaAlcohol = DiversionDependenciaAlcohol
        self.ProblemasDigestivos = ProblemasDigestivos
        self.TensionAlta = TensionAlta
        self.DolorCabeza = DolorCabeza
