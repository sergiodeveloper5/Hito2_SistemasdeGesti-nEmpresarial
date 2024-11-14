from database.bdd import conectar_bd
from modelos.encuesta import Encuesta

# Crear una nueva encuesta
def crear_encuesta(encuesta):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        sql = '''
            INSERT INTO ENCUESTA (idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana,
                                  BebidasFinSemana, BebidasDestiladasSemana, VinosSemana,
                                  PerdidasControl, DiversionDependenciaAlcohol,
                                  ProblemasDigestivos, TensionAlta, DolorCabeza)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        valores = (encuesta.idEncuesta, encuesta.edad, encuesta.Sexo, encuesta.BebidasSemana,
                   encuesta.CervezasSemana, encuesta.BebidasFinSemana, encuesta.BebidasDestiladasSemana,
                   encuesta.VinosSemana, encuesta.PerdidasControl, encuesta.DiversionDependenciaAlcohol,
                   encuesta.ProblemasDigestivos, encuesta.TensionAlta, encuesta.DolorCabeza)
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

# Leer todas las encuestas
def leer_encuestas():
    conexion = conectar_bd()
    encuestas = []
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM ENCUESTA")
        resultados = cursor.fetchall()
        for fila in resultados:
            encuestas.append(Encuesta(*fila))
        cursor.close()
        conexion.close()
    return encuestas

# Actualizar una encuesta
def actualizar_encuesta(encuesta):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        sql = '''
            UPDATE ENCUESTA
            SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s,
                BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s,
                DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s
            WHERE idEncuesta=%s
        '''
        valores = (encuesta.edad, encuesta.Sexo, encuesta.BebidasSemana, encuesta.CervezasSemana,
                   encuesta.BebidasFinSemana, encuesta.BebidasDestiladasSemana, encuesta.VinosSemana,
                   encuesta.PerdidasControl, encuesta.DiversionDependenciaAlcohol, encuesta.ProblemasDigestivos,
                   encuesta.TensionAlta, encuesta.DolorCabeza, encuesta.idEncuesta)
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

# Eliminar una encuesta
def eliminar_encuesta(id_encuesta):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        sql = "DELETE FROM ENCUESTA WHERE idEncuesta=%s"
        cursor.execute(sql, (id_encuesta,))
        conexion.commit()
        cursor.close()
        conexion.close()
