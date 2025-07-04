from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from libros.models import Libro, Genero, Autor, Calificacion
from django.db.models import Count, Avg
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from django.db.models import Avg


class Command(BaseCommand):
    help = 'Genera 10 reportes diferentes con pandas, seaborn y matplotlib'

    def handle(self, *args, **kwargs):
        output_dir = "graficos"
        os.makedirs(output_dir, exist_ok=True)

        def save_plot(fig, filename):
            path = os.path.join(output_dir, filename)
            fig.savefig(path, bbox_inches='tight')
            plt.close(fig)

        sns.set(style="whitegrid")

        # 1. Total de libros por género
        df1 = pd.DataFrame(Genero.objects.annotate(total=Count('libros')).values('nombre', 'total'))
        if not df1.empty:
            fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño más amplio
            barplot = sns.barplot(data=df1, x='nombre', y='total', ax=ax)

            ax.set_title("Cantidad de libros por género", fontsize=14)
            ax.set_xlabel("Género", fontsize=12)
            ax.set_ylabel("Total de libros", fontsize=12)

            # Rotar etiquetas del eje X para evitar superposición
            plt.xticks(rotation=35, ha='right', fontsize=10)

            # Etiquetas encima de cada barra
            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{int(height)}', 
                            (p.get_x() + p.get_width() / 2., height + 0.1),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "1_libros_por_genero.png")


        # 2. Top 10 autores con más libros
        df2 = pd.DataFrame(Autor.objects.annotate(total=Count('libros')).values('nombre', 'total'))
        df2 = df2.sort_values('total', ascending=False).head(10)
        if not df2.empty:
            fig = sns.barplot(data=df2, y='nombre', x='total').get_figure()
            fig.suptitle("Top 10 autores con más libros")
            save_plot(fig, "2_autores_mas_libros.png")

        # 3. Libros con más calificaciones
        df3 = pd.DataFrame(Libro.objects.annotate(total=Count('calificaciones')).values('titulo', 'total'))
        df3 = df3.sort_values('total', ascending=False).head(10)
        if not df3.empty:
            fig = sns.barplot(data=df3, y='titulo', x='total').get_figure()
            fig.suptitle("Top 10 libros más calificados")
            save_plot(fig, "3_libros_mas_calificados.png")

        # 4. Promedio de calificación por género
        df4 = pd.DataFrame(
            Genero.objects
            .annotate(prom=Avg('libros__calificaciones__puntuacion'))
            .values('nombre', 'prom')
        )
        df4 = df4.dropna()

        if not df4.empty:
            fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño amplio
            barplot = sns.barplot(data=df4, x='nombre', y='prom', ax=ax, color='cornflowerblue')

            ax.set_title("Promedio de calificaciones por género", fontsize=14)
            ax.set_xlabel("Género", fontsize=12)
            ax.set_ylabel("Promedio", fontsize=12)

            plt.xticks(rotation=35, ha='right', fontsize=10)

            # Etiquetas encima de las barras
            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', 
                            (p.get_x() + p.get_width() / 2., height + 0.05),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "4_promedio_genero.png")


        # 5. Promedio de calificación por libro
        df5 = pd.DataFrame(Libro.objects.annotate(prom=Avg('calificaciones__puntuacion')).values('titulo', 'prom'))
        df5 = df5.dropna().sort_values(by='prom', ascending=False).head(10)
        if not df5.empty:
            fig = sns.barplot(data=df5, y='titulo', x='prom').get_figure()
            fig.suptitle("Top 10 libros con mejor promedio")
            save_plot(fig, "5_promedio_libro.png")

        # 6. Promedio de calificación por usuario
        df6 = pd.DataFrame(
            User.objects.annotate(prom=Avg('calificaciones__puntuacion'))
            .values('username', 'prom')
        )
        df6 = df6.dropna()

        if not df6.empty:
            fig, ax = plt.subplots(figsize=(14, 6))  # Ancho extendido
            barplot = sns.barplot(data=df6, x='username', y='prom', ax=ax, color='steelblue')

            ax.set_title("Promedio de calificaciones por usuario", fontsize=14)
            ax.set_xlabel("Usuario", fontsize=12)
            ax.set_ylabel("Promedio", fontsize=12)

            plt.xticks(rotation=35, ha='right', fontsize=9)

            # Mostrar valores encima de las barras
            for p in barplot.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}',
                            (p.get_x() + p.get_width() / 2., height + 0.05),
                            ha='center', va='bottom', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "6_promedio_usuario.png")

        # 7. Usuarios con más calificaciones (formato horizontal para nombres largos)
        df7 = pd.DataFrame(
            User.objects.annotate(total=Count('calificaciones'))
            .values('username', 'total')
        )
        df7 = df7.sort_values(by='total', ascending=False).head(10)

        if not df7.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            barplot = sns.barplot(
                                    data=df7,
                                    y='username',
                                    x='total',
                                    hue='username',         # ← Añadido
                                    dodge=False,            # ← Para que no separe las barras
                                    palette='Blues_d',
                                    legend=False,           # ← Elimina leyenda redundante
                                    ax=ax
                                )


            ax.set_title("Top 10 usuarios con más calificaciones", fontsize=14)
            ax.set_xlabel("Cantidad de calificaciones", fontsize=12)
            ax.set_ylabel("Usuario", fontsize=12)

            # Etiquetas al final de las barras
            for p in barplot.patches:
                width = p.get_width()
                ax.annotate(f'{int(width)}',
                            (width + 0.5, p.get_y() + p.get_height() / 2),
                            va='center', fontsize=9)

            fig.tight_layout()
            save_plot(fig, "7_usuarios_mas_calificaron.png")

        # 8. Mapa de calor: promedio de calificación por usuario y género

        cal_data = Calificacion.objects.select_related('usuario', 'libro__genero')
        df8 = pd.DataFrame([
            {
                'usuario': c.usuario.username,
                'genero': c.libro.genero.nombre,
                'puntuacion': float(c.puntuacion)
            }
            for c in cal_data
        ])

        if not df8.empty:
            pivot = df8.pivot_table(index='usuario', columns='genero', values='puntuacion', aggfunc='mean')
            pivot = pivot.apply(pd.to_numeric, errors='coerce')  # ← cambio clave aquí

            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(pivot, annot=True, cmap="YlGnBu", ax=ax)
            ax.set_title('Promedio de Calificación por Usuario y Género')
            save_plot(fig, "8_mapa_calor_usuario_genero.png")


        # 9. Mapa de calor (libro vs usuario)
        df9 = pd.DataFrame(
            Calificacion.objects.values('libro__titulo', 'usuario__username', 'puntuacion')
        )

        if not df9.empty:
            pivot = df9.pivot(index='libro__titulo', columns='usuario__username', values='puntuacion')
            pivot = pivot.apply(pd.to_numeric, errors='coerce')

            fig, ax = plt.subplots(figsize=(20, 15))
            sns.heatmap(
                pivot,
                annot=True,
                fmt=".1f",
                cmap="YlGnBu",
                ax=ax,
                annot_kws={"size": 8}
            )

            ax.set_title("Mapa de calor de puntuaciones por usuario y libro", fontsize=14, pad=20)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)

            fig.tight_layout()
            save_plot(fig, "9_heatmap_puntuaciones.png")


       # 10. Comparación libros vs promedio y cantidad (Top 10 libros con más calificaciones)
        df10 = pd.DataFrame(
            Libro.objects.annotate(
                prom=Avg('calificaciones__puntuacion'),
                total=Count('calificaciones')
            ).values('titulo', 'prom', 'total')
        )

        df10 = df10.dropna()
        df10 = df10.sort_values(by='total', ascending=False).head(10)  # ← solo los 10 con más calificaciones

        if not df10.empty:
            fig, ax = plt.subplots(figsize=(12, 7))
            sns.scatterplot(data=df10, x='total', y='prom', ax=ax, color='royalblue')

            # Agregar etiquetas de texto a cada punto
            for _, row in df10.iterrows():
                ax.text(row['total'] + 0.1, row['prom'], row['titulo'], fontsize=9)

            ax.set_title("Top 10 libros: cantidad vs. promedio de calificación", fontsize=14)
            ax.set_xlabel("Cantidad de calificaciones")
            ax.set_ylabel("Promedio de calificación")
            fig.tight_layout()

            save_plot(fig, "10_cantidad_vs_promedio.png")



        self.stdout.write(self.style.SUCCESS("✅ ¡Los 10 gráficos fueron generados correctamente!"))
