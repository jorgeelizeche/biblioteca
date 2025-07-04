from django.core.management.base import BaseCommand
from libros.models import Libro, Genero
from django.db.models import Avg, Count
import pandas as pd

class Command(BaseCommand):
    help = 'Recomienda libros por género basados en promedio de puntuaciones'

    def add_arguments(self, parser):
        parser.add_argument('--genero', type=int, help='ID del género para recomendar libros')

    def handle(self, *args, **options):
        genero_id = options['genero']
        if not genero_id:
            self.stdout.write(self.style.ERROR("⚠️  Debes proporcionar un ID de género con --genero=N"))
            return

        try:
            genero = Genero.objects.get(id=genero_id)
        except Genero.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Género con ID {genero_id} no encontrado."))
            return

        libros = (
            Libro.objects.filter(genero=genero)
            .annotate(prom=Avg('calificaciones__puntuacion'), votos=Count('calificaciones'))
            .filter(votos__gt=0)
            .order_by('-prom')[:10]
        )

        if not libros:
            self.stdout.write(self.style.WARNING(f"⚠️  No hay libros con calificaciones en el género '{genero.nombre}'."))
            return

        df = pd.DataFrame(libros.values('titulo', 'prom', 'votos'))
        df.rename(columns={'prom': 'promedio', 'votos': 'cantidad_calificaciones'}, inplace=True)
        df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce').round(1)


        self.stdout.write(self.style.SUCCESS(f"\n📚 Recomendaciones para el género '{genero.nombre}':\n"))

        try:
            from tabulate import tabulate
            tabla = tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)
            self.stdout.write(tabla)
        except ImportError:
            self.stdout.write(self.style.WARNING("ℹ️ Instala 'tabulate' con pip para una mejor visualización"))
            self.stdout.write(df.to_string(index=False))
