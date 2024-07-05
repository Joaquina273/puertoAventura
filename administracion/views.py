from django.shortcuts import render
from django.db.models import Q
from db.models import User, Report, Post, Offer
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

def ver_reportes(request):
     reports = Report.objects.all();
     return render(request, 'administracion/reportes.html', { "reportes": reports})

def bloqueo(request):
     reports = Report.objects.all();
     action = request.POST.get('action')
     reporteId = request.POST.get('reporte')
     reporte = Report.objects.get(id=reporteId)
     usuario = reporte.user
     if action == 'rechazar':
          reporte.is_resolved = True;
          reporte.save()
     elif action == 'bloquear':
          reporte.is_resolved = True;
          reporte.save()
          usuario.is_blocked = True;
          usuario.save()
     return render(request,'administracion/reportes.html', {"reportes": reports})

     
def ver_estadisticas(request):
    return render(request, 'administracion/estadisticas/listado_estadisticas.html')

def ver_estadisticas_publicaciones(request):
    posts = Post.objects.all()

    if posts.exists():
        ship_type_counts = Counter(post.ship_type for post in posts)

        # TODO: Grafico de torta para la cantidad de publicaciones según su tipo
        fig_pie = px.pie(
            names=ship_type_counts.keys(), 
            values=ship_type_counts.values(), 
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.4
        )
        fig_pie.update_traces(
            textposition='inside',
            hovertemplate='<b>Embarcacion:</b> %{label}<br><b>Cantidad:</b> %{value}',
            textinfo='percent+label'
        )

        fig_pie.update_layout(
            title={
                'text': "Distribución de publicaciones por tipo de embarcacion",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        )

        # TODO: Grafico de barra para la cantidad de publicaciones según su estado

        state_map = {0: 'Disponible', 1: 'Pendiente', 2: 'Finalizada'}
        state_counts = Counter(state_map[post.state] for post in posts)
        colors = ['indianred', 'lightblue', 'lightgreen']

        fig_bar = go.Figure([go.Bar(x=list(state_counts.keys()), y=list(state_counts.values()), marker_color=colors[:len(state_counts)], hovertemplate='Estado: %{x}, Cantidad: %{y}<extra></extra>')])

        fig_bar.update_layout(
            xaxis_title="Estado", 
            yaxis_title="Cantidad",
            title={
                'text': "Cantidad de publicaciones según el estado",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            yaxis=dict(
                tickmode='linear',
                dtick=5,  # Intervalo de 5 en 5
                tick0=0,  # Valor inicial del tick
                range=[0, max(state_counts.values()) + 5]
            ),
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(len(state_counts.keys()))),
                ticktext=list(state_counts.keys())
            ),
        )

        # Gráfico de burbujas para la cantidad de publicaciones según su puerto
        port_counts = Counter(post.port.name for post in posts)
        colors=['indianred', 'lightblue', 'lightgreen'], # Puedes personalizar los colores aquí
        # Crear la figura de barras con Plotly Graph Objects
        fig_ports = go.Figure([go.Bar(x=list(port_counts.keys()), y=list(port_counts.values()), marker_color=colors[:len(state_counts)], hovertemplate='Puerto: %{x}, Cantidad: %{y}<extra></extra>')])

        # Configurar las etiquetas emergentes (hoverlabels)
        fig_ports.update_layout(
            xaxis_title="Puerto", 
            yaxis_title="Cantidad",
            title={
                'text': "Cantidad de publicaciones según el puerto",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        # Configurar graficos
        configure_plot(fig_pie)
        configure_plot(fig_bar)
        configure_plot(fig_ports)


        # Convertir gráficos a JSON para renderizarlos en el template
        pie_chart = fig_pie.to_html(full_html=False)
        bar_chart = fig_bar.to_html(full_html=False)
        fig_ports = fig_ports.to_html(full_html=False)

        context = {
            'pie_chart': pie_chart,
            'bar_chart': bar_chart,
            'fig_ports': fig_ports,
            'has_data': posts.exists(),
        }
    else:
        context = {
            'has_data': posts.exists(),
        }

    return render(request, 'administracion/estadisticas/estadisticas_publicaciones.html', context)



def ver_estadisticas_usuarios(request):

    users = User.objects.all()

    types_users = {
        0 : "Usuario normal",
        1 : "Usuario con permisos para publicar",   # Creo que es mejor implementarlo de esta manera
        2 : "Personal del Puerto",
        3 : "Administrador"
    }

    user_type_counts = Counter()

    if users.exists():
        for user in users:
            tipo = types_users.get(user.type_user, user.type_user)
            user_type_counts[tipo] += 1

        # TODO: Grafico de torta para la cantidad de publicaciones según su tipo
        fig_pie = px.pie(
            names=user_type_counts.keys(), 
            values= user_type_counts.values(), 
            color_discrete_sequence=px.colors.sequential.RdBu,
            hole=0.4
        )
        fig_pie.update_traces(
            textposition='inside',
            hovertemplate='<b>Tipo de usuario:</b> %{label}<br><b>Cantidad:</b> %{value}',
            textinfo='percent+label'
        )

        fig_pie.update_layout(
            title={
                'text': "Distribución de usuarios por tipo",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        )

        usuarios_bloqueados = User.objects.filter(is_blocked=True).count()
        usuarios_no_bloqueados = User.objects.filter(is_blocked=False).count()

        # Crear los datos para el gráfico
        data = {
            "Estado": ["Bloqueados", "No Bloqueados"],
            "Cantidad": [usuarios_bloqueados, usuarios_no_bloqueados]
        }

        # Crear el gráfico de barras
        fig = go.Figure(data=[go.Bar(
            x=data["Estado"],
            y=data["Cantidad"],
            text=data["Cantidad"],
            textposition='auto'
        )])

        # Actualizar el diseño del gráfico
        fig.update_layout(
            title={
                'text': "Cantidad de Usuarios Bloqueados y No Bloqueados",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'y': 0.9
            },
            xaxis=dict(title="Estado"),
            yaxis=dict(title="Cantidad de Usuarios"),
            bargap=0.2,
            bargroupgap=0.1
        )

        configure_plot(fig_pie)
        configure_plot(fig)

        fig_pie = fig_pie.to_html(full_html=False)
        fig = fig.to_html(full_html=False)

        context = {
            'fig_pie': fig_pie,
            'fig': fig,
            'has_data': users.exists(),
        }
    else:
        context = {
            'has_data': users.exists(),
        }

    return render(request, 'administracion/estadisticas/estadisticas_usuarios.html', context)

def ver_estadisticas_intercambios(request):

    # Grafico de barra para las ofertas segun el estado

    ofertas = Offer.objects.filter(Q(answer=1) | Q(answer=2))

    if ofertas.exists():
        state_map = {1: 'Aceptado', 2: 'Rechazado'}
        state_counts = Counter(state_map[oferta.answer] for oferta in ofertas)
        colors = ['indianred', 'lightblue', 'lightgreen']

        fig_bar_answers = go.Figure([go.Bar(x=list(state_counts.keys()), y=list(state_counts.values()), marker_color=colors[:len(state_counts)], hovertemplate='Respuesta: %{x}, Cantidad: %{y}<extra></extra>')])


        fig_bar_answers.update_layout(
        xaxis_title="Estado", 
        yaxis_title="Cantidad",
        title={
            'text': "Cantidad de intercambios aceptados y rechazados",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        yaxis=dict(
            tickmode='linear',
            dtick=5,  # Intervalo de 5 en 5
            tick0=0,  # Valor inicial del tick
            range=[0, max(state_counts.values()) + 5]
            ),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(state_counts.keys()))),
            ticktext=list(state_counts.keys())
            ),
        )


        # TODO: Grafico de barra para la cantidad de intercambios aceptados por mes
        ofertas_aceptadas = Offer.objects.filter(answer = 2)

        # Contador para contar ofertas por mes
        ofertas_por_mes = Counter()

        # Diccionario para traducir nombres de meses de inglés a español
        meses_ingles_a_espanol = {
            'January': 'Enero',
            'February': 'Febrero',
            'March': 'Marzo',
            'April': 'Abril',
            'May': 'Mayo',
            'June': 'Junio',
            'July': 'Julio',
            'August': 'Agosto',
            'September': 'Septiembre',
            'October': 'Octubre',
            'November': 'Noviembre',
            'December': 'Diciembre'
        }

        # Llenar el contador con las ofertas por mes
        for oferta in ofertas_aceptadas:
            mes_ingles = oferta.date.strftime('%B')
            mes_espanol = meses_ingles_a_espanol.get(mes_ingles, mes_ingles)
            ofertas_por_mes[mes_espanol] += 1

        # Lista de meses en orden
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        # Asignar un color a cada mes basado en su posición en la lista
        colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
                '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78']

        color_meses = [colores[i % len(colores)] for i in range(len(meses))]

        # Crear el gráfico inicial
        fig_bar_answers_mes = go.Figure()

        # Añadir las barras al gráfico
        for mes, color in zip(meses, colores):
            if mes in ofertas_por_mes.keys():
                fig_bar_answers_mes.add_trace(go.Bar(x=[mes], y=[ofertas_por_mes[mes]], name=mes, marker_color=color, visible=False, hovertemplate=f'Mes: {mes}, Cantidad: {ofertas_por_mes[mes]}<extra></extra>'))
            else:
                fig_bar_answers_mes.add_trace(go.Bar(x=[mes], y=[0], name=mes, marker_color=color, visible=False, hovertemplate=f'Mes: {mes}, Cantidad: {ofertas_por_mes[mes]}<extra></extra>'))

        # Hacer visible solo la primera barra (mes de Enero)
        fig_bar_answers_mes.data[0].visible = True

        # Crear botones para cada mes
        buttons = []
        for i, (mes, color) in enumerate(zip(meses, colores)):
            visibility = [False] * len(meses)
            visibility[i] = True  # Hacer visible solo la barra correspondiente al mes
            annotation_text = ""
            if ofertas_por_mes[mes] == 0:
                annotation_text = f"No hay intercambios aceptados en {mes}."
            buttons.append(dict(
                label=mes,
                method="update",
                args=[{"visible": visibility},
                    {"title": {'text': f"Cantidad de Intercambios Aceptados en {mes}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top',  'y': 1},
                    "annotations": [dict(text=annotation_text, x=0.5, y=0.6, xref="paper", yref="paper", showarrow=False)] if annotation_text else []}]
            ))
        
        # Agregar botones al diseño del gráfico
        fig_bar_answers_mes.update_layout(
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x= 1.05,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                ),
            ]
        )

        # Verificar si el mes inicial (enero) no tiene ofertas y agregar anotación
        initial_annotation = ""
        if ofertas_por_mes["Enero"] == 0:
            initial_annotation = "No hay intercambios aceptados en enero."

        fig_bar_answers_mes.update_layout(
            title={
                'text': "Cantidad de Intercambios Aceptados por mes", 
                'x': 0.5, 
                'xanchor': 'center', 
                'yanchor': 'top',
                'y': 1
                },
            annotations=[dict(text=initial_annotation, x=0.5, y=0.6, xref="paper", yref="paper", showarrow=False)] if initial_annotation else [],
            xaxis=dict(title="Mes", tickangle= 0),
            yaxis=dict(
                title="Cantidad de Intercambios Aceptados",
                tickmode='linear',
                dtick=5,  # Establece el intervalo de los ticks del eje y en 5
                range=[0, max(ofertas_por_mes.values(), default=0) + 5]  # Ajusta el rango del eje y según tus datos
            ),
            bargap=0.1,
            bargroupgap=0.1,
        ),


        configure_plot(fig_bar_answers)
        configure_plot(fig_bar_answers_mes)

        fig_bar_answers = fig_bar_answers.to_html(full_html=False)
        fig_bar_answers_mes = fig_bar_answers_mes.to_html(full_html=False)

        context = {
            'fig_bar_answers': fig_bar_answers,
            'fig_bar_answers_mes': fig_bar_answers_mes,
            'has_data': ofertas.exists(),
            }
    else:
        context = {
            'has_data': ofertas.exists(),
            }

    return render(request, 'administracion/estadisticas/estadisticas_intercambios.html', context)

def ver_estadisticas_ofertas(request):

    # TODO: Grafico de barra para la cantidad de ofertas segun el mes
    ofertas = Offer.objects.all()

    if ofertas.exists():
        # Contador para contar ofertas por mes
        ofertas_por_mes = Counter()

        # Diccionario para traducir nombres de meses de inglés a español
        meses_ingles_a_espanol = {
            'January': 'Enero',
            'February': 'Febrero',
            'March': 'Marzo',
            'April': 'Abril',
            'May': 'Mayo',
            'June': 'Junio',
            'July': 'Julio',
            'August': 'Agosto',
            'September': 'Septiembre',
            'October': 'Octubre',
            'November': 'Noviembre',
            'December': 'Diciembre'
        }

        # Llenar el contador con las ofertas por mes
        for oferta in ofertas:
            mes_ingles = oferta.date.strftime('%B')
            mes_espanol = meses_ingles_a_espanol.get(mes_ingles, mes_ingles)
            ofertas_por_mes[mes_espanol] += 1

        # Lista de meses en orden
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        # Asignar un color a cada mes basado en su posición en la lista
        colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
                '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78']

        color_meses = [colores[i % len(colores)] for i in range(len(meses))]

        # Crear el gráfico inicial
        fig_bar = go.Figure()

        # Añadir las barras al gráfico
        for mes, color in zip(meses, colores):
            if mes in ofertas_por_mes.keys():
                fig_bar.add_trace(go.Bar(x=[mes], y=[ofertas_por_mes[mes]], name=mes, marker_color=color, visible=False, hovertemplate=f'Mes: {mes}, Cantidad: {ofertas_por_mes[mes]}<extra></extra>'))
            else:
                fig_bar.add_trace(go.Bar(x=[mes], y=[0], name=mes, marker_color=color, visible=False))

        # Hacer visible solo la primera barra (mes de Enero)
        fig_bar.data[0].visible = True

        # Crear botones para cada mes
        buttons = []
        for i, (mes, color) in enumerate(zip(meses, colores)):
            visibility = [False] * len(meses)
            visibility[i] = True  # Hacer visible solo la barra correspondiente al mes
            annotation_text = ""
            if ofertas_por_mes[mes] == 0:
                annotation_text = f"No hay ofertas realizadas en {mes}."

            buttons.append(dict(
                label=mes,
                method="update",
                args=[{"visible": visibility},
                    {"title": {'text': f"Cantidad de Ofertas Realizadas en {mes}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top', 'y': 1},
                    "annotations": [dict(text=annotation_text, x=0.5, y=0.6, xref="paper", yref="paper", showarrow=False)] if annotation_text else []}]
            ))

        # Agregar botones al diseño del gráfico
        fig_bar.update_layout(
            updatemenus=[
                dict(
                    buttons=buttons,
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=1.05,
                    xanchor="left",
                    y=1.15,
                    yanchor="top"
                ),
            ]
        )

        # Verificar si el mes inicial (enero) no tiene ofertas y agregar anotación
        initial_annotation = ""
        if ofertas_por_mes["Enero"] == 0:
            initial_annotation = "No hay ofertas realizadas en enero."

        fig_bar.update_layout(
            title={
                'text': "Cantidad de Ofertas Realizadas por mes", 
                'x': 0.5, 
                'xanchor': 'center', 
                'yanchor': 'top',
                'y': 1
                },
            annotations=[dict(text=initial_annotation, x=0.5, y=0.6, xref="paper", yref="paper", showarrow=False)] if initial_annotation else [],
            xaxis=dict(title="Mes", tickangle= 0),
            yaxis=dict(
                title="Cantidad de Ofertas",
                tickmode='linear',
                dtick=5,  # Establece el intervalo de los ticks del eje y en 5
                range=[0, max(ofertas_por_mes.values(), default=0) + 5]  # Ajusta el rango del eje y según tus datos
            ),
            bargap=0.1,
            bargroupgap=0.1,
        ) 

        
        configure_plot(fig_bar)

        fig_bar = fig_bar.to_html(full_html=False)

        context = {
            'fig_bar': fig_bar,
            'has_data': ofertas.exists(),
            }
    else:
        context = {
            'has_data': ofertas.exists(),
            }

    return render(request, 'administracion/estadisticas/estadisticas_ofertas.html', context)


def configure_plot(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="black"
        ),
        uirevision=False,  # Evita que la figura se actualice al hacer zoom o pan
        dragmode=False,    # Desactiva la funcionalidad de zoom y pan
        # Deshabilitar zoom y ajuste de ejes
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        # Configuración para desactivar todas las herramientas de selección
        clickmode='event+select',
        # Configuración para desactivar la barra de herramientas
        modebar={'orientation': 'v', 'bgcolor': 'rgba(0,0,0,0)', 'activecolor': 'rgba(0,0,0,0)'}
    )

