from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})


def about(request):
    return render(request, "about.html")

def movies_per_year():
    matplotlib.use("Agg")
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}

    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic

def movies_per_genre():
    matplotlib.use("Agg")

    # Obtener los géneros únicos y contar las películas por género
    genres = Movie.objects.values_list('genre', flat=True)
    movie_counts_by_genre = {}

    for genre_list in genres:
        if genre_list:
            first_genre = genre_list.split(',')[0].strip()  # Considerar solo el primer género
            if first_genre in movie_counts_by_genre:
                movie_counts_by_genre[first_genre] += 1
            else:
                movie_counts_by_genre[first_genre] = 1

    # Crear la gráfica de barras solo si hay datos
    if movie_counts_by_genre:
        bar_width = 0.5
        bar_positions = range(len(movie_counts_by_genre))

        plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')

        plt.title('Movies per Genre')
        plt.xlabel('Genre')
        plt.ylabel('Number of Movies')
        plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)

        plt.subplots_adjust(bottom=0.3)

        # Guardar la gráfica en un buffer de memoria
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # Convertir la imagen a base64
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
    else:
        graphic = None

    # Renderizar la gráfica en la plantilla
    return graphic
            

def statics_view(request):
    return render(request, 'statistics.html', {'movies_per_year': movies_per_year(), "movies_per_genre": movies_per_genre()})