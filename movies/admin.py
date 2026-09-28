from django.contrib import admin
from .models import Genre, Movie, Person, Rating


class RatingInline(admin.TabularInline):
    """Edit ratings inside the parent movie form."""
    model = Rating
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date')
    search_fields = ('first_name', 'last_name')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year', 'average_score')
    list_filter = ('genres', 'release_year')
    search_fields = ('title', 'director__first_name', 'director__last_name')
    filter_horizontal = ('genres',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]

    def average_score(self, obj):
        """Mean of related ratings."""
        ratings = obj.ratings.all()
        if not ratings:
            return '-'
        return round(sum(r.score for r in ratings) / len(ratings), 1)
    average_score.short_description = 'Avg. score'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'score', 'created_at')
    list_filter = ('score', 'movie__genres')
    search_fields = ('movie__title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
