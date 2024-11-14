import tkinter as tk
from tkinter import messagebox, ttk, Menu
from controladores.funciones import crear_encuesta, leer_encuestas, actualizar_encuesta, eliminar_encuesta
from modelos.encuesta import Encuesta
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def iniciar_interfaz():
    root = tk.Tk()
    root.title("Gestión de Clientes, Dr. Fernando")
    root.geometry("1000x700")

    # Barra de estado
    status_var = tk.StringVar()
    status_var.set("Listo - Haga clic en los encabezados de columna para ordenar.")
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w")
    status_bar.pack(side="bottom", fill="x")

    def actualizar_estado(mensaje):
        status_var.set(mensaje)

    # Barra de menú
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Menú de Archivo
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exportar a Excel", command=lambda: exportar_a_excel(status_var))
    file_menu.add_separator()
    file_menu.add_command(label="Salir", command=root.quit)
    menu_bar.add_cascade(label="Archivo", menu=file_menu)

    # Menú de Gráficos
    graph_menu = Menu(menu_bar, tearoff=0)
    graph_menu.add_command(label="Consumo Promedio por Edad", command=lambda: mostrar_grafico("Consumo Promedio por Edad"))
    graph_menu.add_command(label="Distribución de Problemas de Salud", command=lambda: mostrar_grafico("Distribución de Problemas de Salud"))
    graph_menu.add_command(label="Consumo de Bebidas por Sexo", command=lambda: mostrar_grafico("Consumo de Bebidas por Sexo"))
    graph_menu.add_command(label="Consumo por Semana (Líneas)", command=lambda: mostrar_grafico("Consumo por Semana (Líneas)"))
    graph_menu.add_command(label="Consumo por Semana (Área)", command=lambda: mostrar_grafico("Consumo por Semana (Área)"))
    menu_bar.add_cascade(label="Gráficos", menu=graph_menu)

    # Menú de Ayuda
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Sistema de gestión de encuestas\nVersión 1.0"))
    menu_bar.add_cascade(label="Ayuda", menu=help_menu)

    # Crear Frame para secciones principales
    frame_entrada = tk.Frame(root, bd=2, relief="groove")
    frame_entrada.pack(side="top", fill="x", padx=10, pady=5)

    frame_botones = tk.Frame(root)
    frame_botones.pack(side="top", fill="x", padx=10, pady=5)

    frame_tree = tk.Frame(root)
    frame_tree.pack(side="top", fill="both", expand=True, padx=10, pady=5)

    # Definir campos de entrada con etiquetas organizadas
    labels_text = [
        "Edad:", "Sexo:", "Bebidas Semana:", "Cervezas Semana:", 
        "Bebidas Fin de Semana:", "Bebidas Destiladas Semana:", 
        "Vinos Semana:", "Pérdidas de Control:", 
        "Diversión Dependencia Alcohol:", "Problemas Digestivos:", 
        "Tensión Alta:", "Dolor de Cabeza:"
    ]
    entries = []
    opciones_si_no = ["Sí", "No"]
    opciones_frecuencia = ["Nunca", "Alguna vez", "A menudo", "Muy a menudo"]

    for i, text in enumerate(labels_text):
        tk.Label(frame_entrada, text=text).grid(row=i, column=0, sticky="w", padx=5)
        if i == 1:  # Campo Sexo
            entry = tk.StringVar()
            tk.OptionMenu(frame_entrada, entry, "Hombre", "Mujer").grid(row=i, column=1, padx=5)
        elif i in [8, 9, 10]:  # Campos Sí/No
            entry = tk.StringVar()
            tk.OptionMenu(frame_entrada, entry, *opciones_si_no).grid(row=i, column=1, padx=5)
        elif i == 11:  # Campo de frecuencia
            entry = tk.StringVar()
            tk.OptionMenu(frame_entrada, entry, *opciones_frecuencia).grid(row=i, column=1, padx=5)
        else:  # Campos numéricos
            entry = tk.Entry(frame_entrada)
            entry.grid(row=i, column=1, padx=5)
        entries.append(entry)

    # Campo para Eliminar por ID
    tk.Label(frame_entrada, text="ID para Eliminar:").grid(row=12, column=0, sticky="w", padx=5)
    entry_id_eliminar = tk.Entry(frame_entrada)
    entry_id_eliminar.grid(row=12, column=1, padx=5)

    # Configuración del Treeview para mostrar encuestas
    columns = [
        "ID", "Edad", "Sexo", "Bebidas Semana", "Cervezas Semana",
        "Bebidas Fin de Semana", "Bebidas Destiladas Semana", "Vinos Semana",
        "Pérdidas de Control", "Diversión Dependencia Alcohol", 
        "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"
    ]
    tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)
    
    # Scrollbars for the Treeview
    scrollbar_vertical = tk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scrollbar_vertical.pack(side="right", fill="y")
    scrollbar_horizontal = tk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
    scrollbar_horizontal.pack(side="bottom", fill="x")
    tree.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    # Función para ordenar las columnas en el Treeview
    def sort_column(tree, col, reverse):
        # Obtener los datos de la columna seleccionada
        data = [(tree.set(k, col), k) for k in tree.get_children("")]
        # Ordenar los datos en función de la columna seleccionada
        data.sort(reverse=reverse)

        # Reordenar los elementos en el Treeview según el orden
        for index, (val, k) in enumerate(data):
            tree.move(k, "", index)

        # Actualizar el estado con información de la ordenación
        orden = "ascendente" if not reverse else "descendente"
        status_var.set(f"Ordenando por {col} en orden {orden}")

        # Cambiar la dirección de ordenación para el próximo clic
        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

    # Configurar encabezados de columnas para que al hacer clic, ordene los datos
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_column(tree, _col, False))


    # Función para refrescar el Treeview
    def actualizar_treeview(encuestas=None):
        for i in tree.get_children():
            tree.delete(i)
        encuestas = encuestas or leer_encuestas()
        for encuesta in encuestas:
            tree.insert("", "end", values=(
                encuesta.idEncuesta, encuesta.edad, encuesta.Sexo, encuesta.BebidasSemana,
                encuesta.CervezasSemana, encuesta.BebidasFinSemana, encuesta.BebidasDestiladasSemana,
                encuesta.VinosSemana, encuesta.PerdidasControl, encuesta.DiversionDependenciaAlcohol,
                encuesta.ProblemasDigestivos, encuesta.TensionAlta, encuesta.DolorCabeza
            ))

    # Función para exportar los datos visibles en el Treeview a un archivo Excel
    def exportar_a_excel(status):
        encuestas = [tree.item(item)["values"] for item in tree.get_children()]
        df = pd.DataFrame(encuestas, columns=columns)
        
        # Crear la ruta de la carpeta de exportación
        carpeta_exportacion = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'exportaciones')
        
        # Imprimir la ruta para verificar si es correcta
        print(f"Ruta de exportación: {carpeta_exportacion}")
        
        # Verificar si la carpeta existe, si no, crearla
        try:
            if not os.path.exists(carpeta_exportacion):
                os.makedirs(carpeta_exportacion)
                print("Carpeta de exportación creada.")
        except Exception as e:
            print(f"Error al crear la carpeta de exportación: {e}")
            status.set("Error al crear la carpeta de exportación")
            messagebox.showerror("Error", f"No se pudo crear la carpeta de exportación: {str(e)}")
            return
        
        # Especificar la ruta completa del archivo
        archivo = os.path.join(carpeta_exportacion, f"consultas_exportadas_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
        
        try:
            df.to_excel(archivo, index=False)
            status.set(f"Datos exportados exitosamente a {archivo}")
            messagebox.showinfo("Éxito", f"Datos exportados exitosamente a {archivo}")
        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            status.set("Error al exportar a Excel")
            messagebox.showerror("Error", f"No se pudo exportar a Excel: {str(e)}")

    # Función para mostrar gráficos basados en los datos del Treeview
    def mostrar_grafico(tipo_grafico):
        encuestas = [tree.item(item)["values"] for item in tree.get_children()]
        if not encuestas:
            messagebox.showwarning("Advertencia", "No hay datos para mostrar en el gráfico.")
            return

        df = pd.DataFrame(encuestas, columns=columns)
    
        # Generar el gráfico según el tipo seleccionado
        if tipo_grafico == "Consumo Promedio por Edad":
            df['Edad'] = df['Edad'].astype(int)  
            df.groupby('Edad')['Bebidas Semana'].mean().plot(kind='bar')
            plt.title("Consumo Promedio de Bebidas por Grupo de Edad")
            plt.xlabel("Edad")
            plt.ylabel("Consumo Promedio de Bebidas")
    
        elif tipo_grafico == "Distribución de Problemas de Salud":
            problemas_salud = ['Problemas Digestivos', 'Tensión Alta', 'Dolor de Cabeza']
            problemas = df[problemas_salud].apply(lambda x: (x == "Sí").sum())
            problemas.plot(kind='pie', autopct='%1.1f%%')
            plt.title("Distribución de Problemas de Salud")
            plt.ylabel("")
    
        elif tipo_grafico == "Consumo de Bebidas por Sexo":
            df.groupby('Sexo')['Bebidas Semana'].mean().plot(kind='bar', color=['blue', 'orange'])
            plt.title("Consumo Promedio de Bebidas por Sexo")
            plt.xlabel("Sexo")
            plt.ylabel("Consumo Promedio de Bebidas")

        elif tipo_grafico == "Consumo por Semana (Líneas)":
            df['Bebidas Semana'] = df['Bebidas Semana'].astype(int)
            df['Cervezas Semana'] = df['Cervezas Semana'].astype(int)
            df[['Bebidas Semana', 'Cervezas Semana']].plot(kind='line')
            plt.title("Consumo por Semana (Líneas)")
            plt.xlabel("Encuestas")
            plt.ylabel("Consumo")

        elif tipo_grafico == "Consumo por Semana (Área)":
            df['Bebidas Semana'] = df['Bebidas Semana'].astype(int)
            df['Cervezas Semana'] = df['Cervezas Semana'].astype(int)
            df[['Bebidas Semana', 'Cervezas Semana']].plot(kind='area', alpha=0.4)
            plt.title("Consumo por Semana (Área)")
            plt.xlabel("Encuestas")
            plt.ylabel("Consumo")

        plt.show()

    # Función para validar los campos obligatorios
    def validar_campos():
        for i, entry in enumerate(entries):
            if isinstance(entry, tk.StringVar):
                if not entry.get():
                    messagebox.showerror("Error", f"El campo '{labels_text[i][:-1]}' es obligatorio.")
                    return False
            elif isinstance(entry, tk.Entry) and not entry.get().strip():
                messagebox.showerror("Error", f"El campo '{labels_text[i][:-1]}' es obligatorio.")
                return False
        return True

    # Función para agregar una nueva encuesta
    def agregar_encuesta():
        if not validar_campos():
            return

        nueva_encuesta = Encuesta(
            edad=int(entries[0].get().strip()),
            Sexo=entries[1].get(),
            BebidasSemana=int(entries[2].get().strip()),
            CervezasSemana=int(entries[3].get().strip()),
            BebidasFinSemana=int(entries[4].get().strip()),
            BebidasDestiladasSemana=int(entries[5].get().strip()),
            VinosSemana=int(entries[6].get().strip()),
            PerdidasControl=int(entries[7].get().strip()),
            DiversionDependenciaAlcohol=entries[8].get(),
            ProblemasDigestivos=entries[9].get(),
            TensionAlta=entries[10].get(),
            DolorCabeza=entries[11].get()
        )
        crear_encuesta(nueva_encuesta)
        actualizar_treeview()
        messagebox.showinfo("Éxito", "Encuesta añadida exitosamente")

    # Función para eliminar encuesta por ID
    def borrar_encuesta_por_id():
        id_encuesta = entry_id_eliminar.get().strip()
        if not id_encuesta:
            messagebox.showerror("Error", "El ID es obligatorio para eliminar")
            return
        try:
            id_encuesta = int(id_encuesta)
        
            # Solicitar confirmación antes de eliminar
            confirmar = messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar la encuesta con ID {id_encuesta}?")
            if not confirmar:
                return  # Si el usuario cancela, no se procede con la eliminación

            # Realizar la eliminación si el usuario confirmó
            eliminar_encuesta(id_encuesta)
            actualizar_treeview()
            messagebox.showinfo("Éxito", f"Encuesta con ID {id_encuesta} eliminada exitosamente")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")


    # Función para actualizar una encuesta seleccionada directamente
    def actualizar_encuesta_interfaz():
        # Seleccionar el elemento activo en el Treeview
        item = tree.focus()
        if not item:
            messagebox.showwarning("Advertencia", "Seleccione una encuesta para actualizar.")
            return

        # Obtener el ID de la encuesta seleccionada
        valores = tree.item(item, 'values')
        id_encuesta = int(valores[0])  # El primer valor es el ID

        # Crear un objeto Encuesta con los valores del formulario actualizados
        try:
            encuesta_modificada = Encuesta(
                idEncuesta=id_encuesta,
                edad=int(entries[0].get().strip()),
                Sexo=entries[1].get(),
                BebidasSemana=int(entries[2].get().strip()),
                CervezasSemana=int(entries[3].get().strip()),
                BebidasFinSemana=int(entries[4].get().strip()),
                BebidasDestiladasSemana=int(entries[5].get().strip()),
                VinosSemana=int(entries[6].get().strip()),
                PerdidasControl=int(entries[7].get().strip()),
                DiversionDependenciaAlcohol=entries[8].get(),
                ProblemasDigestivos=entries[9].get(),
                TensionAlta=entries[10].get(),
                DolorCabeza=entries[11].get()
            )
        except ValueError:
            messagebox.showerror("Error", "Por favor, asegúrese de que todos los campos tienen valores válidos.")
            return

        # Guardar los datos actualizados en la base de datos
        try:
            actualizar_encuesta(encuesta_modificada)
            actualizar_treeview()  # Refrescar el Treeview con los datos actualizados
            messagebox.showinfo("Éxito", "Encuesta actualizada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la encuesta: {str(e)}")



    # Configuración del filtro
    filtro_var = tk.StringVar()
    opciones_filtro = ["Sin filtro", "Alta frecuencia de consumo", "Perdió control +3 veces", "Problema de salud específico"]
    filtro_menu = tk.OptionMenu(frame_entrada, filtro_var, *opciones_filtro)
    filtro_menu.grid(row=13, column=1, padx=5)

    # Función para aplicar el filtro
    def aplicar_filtro():
        filtro = filtro_var.get()
        encuestas = leer_encuestas()

        # Filtrar según la opción seleccionada
        if filtro == "Sin filtro":
            pass
        elif filtro == "Alta frecuencia de consumo":
            encuestas = [e for e in encuestas if e.BebidasSemana > 10]
        elif filtro == "Perdió control +3 veces":
            encuestas = [e for e in encuestas if e.PerdidasControl > 3]
        elif filtro == "Problema de salud específico":
            encuestas = [e for e in encuestas if e.DolorCabeza == "Sí" or e.TensionAlta == "Sí"]

        # Actualizar visualización con datos filtrados
        actualizar_treeview(encuestas)

    # Botón para aplicar el filtro
    boton_filtro = tk.Button(frame_entrada, text="Aplicar Filtro", command=aplicar_filtro)
    boton_filtro.grid(row=13, column=2, padx=5)

    # Botones de acción
    tk.Button(frame_botones, text="Crear", command=agregar_encuesta).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Actualizar", command=actualizar_encuesta_interfaz).pack(side="left", padx=5)
    tk.Button(frame_botones, text="Eliminar por ID", command=borrar_encuesta_por_id).pack(side="left", padx=5)
    
    actualizar_treeview()  # Cargar datos iniciales
    root.mainloop()
