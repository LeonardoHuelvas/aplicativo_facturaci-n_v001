from datetime import date, datetime
import os
import pandas as pd
import streamlit as st
from database import *
from factura_pdf import mostrar_factura_pdf

 
#----------------------------------------------------------------------------------
 
from decimal import Decimal
 #...............................................................................................

def calcular_valor_descontado(precio, cantidad, total, descuento_porcentaje):
    precio_decimal = Decimal(precio)
    cantidad_decimal = Decimal(cantidad)
    total_decimal = Decimal(total)
    descuento_decimal = Decimal(descuento_porcentaje) / Decimal(100)

    subtotal = precio_decimal * cantidad_decimal
    return (subtotal * descuento_decimal) if descuento_decimal > 0 else Decimal(0)
#...............................................................................................
def mostrar_facturas(facturas):
    df_facturas = pd.DataFrame(facturas, columns=[
        'Factura ID', 'Cliente ID', 'Nombre Cliente', 'ID Servicio', 'Cantidad', 
        'Precio', 'Total', 'Descuento', 'Fecha Factura'
    ])
    df_facturas['Valor Descontado'] = df_facturas.apply(
        lambda row: calcular_valor_descontado(row['Precio'], row['Cantidad'], row['Total'], row['Descuento']), axis=1)
    df_facturas['Nombre Archivo PDF'] = df_facturas.apply(
        lambda row: f"factura-{row['Cliente ID']}-{row['Factura ID']}.pdf", axis=1)

    st.dataframe(df_facturas[['Factura ID', 'Cliente ID', 'Nombre Cliente', 'ID Servicio', 'Cantidad', 'Precio', 'Descuento', 'Valor Descontado', 'Total', 'Fecha Factura']])
    for _, factura in df_facturas.iterrows():
        descargar_factura_pdf(factura['Factura ID'])
#...............................................................................................
def descargar_factura_pdf(factura_id):
    nombre_archivo_pdf = f"factura-{factura_id}.pdf"
    ruta_archivo_pdf = os.path.join('./facturas_generadas', nombre_archivo_pdf)  # Asegúrate de que esta ruta es correcta

    if os.path.exists(ruta_archivo_pdf):
        with open(ruta_archivo_pdf, "rb") as pdf_file:
            st.download_button(label="Descargar Factura", data=pdf_file, file_name=nombre_archivo_pdf, mime="application/pdf")
    else:
        st.write(f"No se encontró el archivo PDF para la factura {factura_id}.")
#...............................................................................................
def interfaz_descargar_facturas(get_facturas_por_fecha, obtener_detalle_cliente_por_id, obtener_cliente_por_nombre, obtener_total_factura, connection):
    pdf_dir = 'I:/Desarrollo/proyecto/facutracion_internet/aplicativo_facturación/facturas_generadas'
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    st.subheader("Descargar Factura Específica")
    factura_id_para_descargar = st.text_input("Ingrese el ID de la factura para descargar")
    if st.button("Descargar Factura Específica"):
        descargar_factura_pdf(factura_id_para_descargar)

    cliente_input = st.text_input("Ingrese Nombre o ID del cliente para la búsqueda")
    if cliente_input:
        inicio = st.date_input("Fecha de inicio", min_value=datetime(2020, 1, 1))
        fin = st.date_input("Fecha de fin", min_value=datetime(2020, 1, 1))
        if inicio <= fin and st.button("Buscar Facturas"):
            try:
                facturas = get_facturas_por_fecha(connection, inicio, fin, cliente_input)
                mostrar_facturas(facturas) if facturas else st.info("No se encontraron facturas en el rango de fechas seleccionado.")
            except Exception as e:
                st.error(f"Ocurrió un error al buscar las facturas: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Descargar Facturas", layout="wide")
    connection = create_server_connection("localhost", "root", "123", "lucmonet")
    interfaz_descargar_facturas(get_facturas_por_fecha, connection)
