from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from movies import models
from movies.forms import ActorForm, EditReviewForm
from movies.forms import AddReviewForm
from movies.forms import CategoryForm
from movies.forms import DeleteUserForm
from movies.forms import DirectorForm
from movies.forms import GenreForm
from movies.forms import GetActorForm
from movies.forms import GetCategoryForm
from movies.forms import GetDirectorForm
from movies.forms import GetGenreForm
from movies.forms import GetMovieForm
from movies.forms import GetUserForm
from movies.forms import MovieForm
from movies.forms import MovieImageForm
from movies.forms import RaitingForm
from movies.forms import UpdateStatusForm
from movies.models import Actor
from movies.models import Category
from movies.models import Director
from movies.models import Genre
from movies.models import Movie
from movies.models import Raiting
from movies.models import Review


########################################################################################################################
#                                                     CLASSES
########################################################################################################################


class PoiskList:
    def get_genres(self):
        """
        The get_genres function returns a list of all the genres in the database.
        :param self: Represent the instance of the object itself
        :return: All the genres in the database
        """
        return Genre.objects.all()

    def get_category(self):
        """
        The get_category function returns all the categories in the database.
        :param self: Represent the instance of the object itself
        :return: All the categories in the database
        """
        return Category.objects.all()

    def get_years(self):
        """
        The get_years function returns a list of years in which movies were published.
        The function uses the Movie model to filter for all published movies, then it
        uses the values_list method to get only the year field from each movie and
        returns that as a flat list (i.e., not nested). Finally, we use distinct() to
        remove any duplicate years.

        :param self: Access the data of the class
        :return: A list of years that are associated with published movies
        """
        return list(
            sorted(
                Movie.objects.filter(status=Movie.Status.PUBLISHED)
                .values_list("year", flat=True)
                .distinct()
            )
        )


class MovieList(PoiskList, generic.ListView):
    """Class-based view for the movie list on the home page."""

    model = models.Movie
    queryset = model.objects.filter(status=model.Status.PUBLISHED)
    paginate_by = 3
    context_object_name = "movies"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["title"] = "Главная страница"
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")
        return context

    def get_queryset(self):
        return self.queryset


class MovieDetail(PoiskList, generic.DetailView):
    """Class-based view for displaying movie details."""

    model = Movie
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        """
        The get_context_data function is a method that Django calls when rendering the template.
        In this case, we are adding two variables: average_rating and rating_count.

        :param self: Represent the instance of the object
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A dictionary with the context of the template
        """
        context = super().get_context_data(**kwargs)
        movie = self.object
        average_rating = Raiting.objects.filter(movie=movie).aggregate(
            avg_rating=Avg("rating")
        )["avg_rating"]
        rating_count = Raiting.objects.filter(movie=movie).count()
        context["rating_count"] = rating_count
        context["average_rating"] = average_rating
        context["movies"] = self.get_queryset().distinct()
        context["categories"] = Category.objects.all()
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        user = self.request.user
        if not user.is_anonymous:
            rating = Raiting.objects.filter(user=user, movie=movie).first()
            if rating:
                context["rating_form"] = RaitingForm(instance=rating)
                context["can_edit_rating"] = True
                context["rating"] = rating.rating
                context["rating_id"] = rating.id
            else:
                context["rating_form"] = RaitingForm()

        return context

    def post(self, request, *args, **kwargs):

        """
        The post function is used to create a new rating for the movie.
        If the user has already rated this movie, then delete that rating and redirect to the detail page.
        Otherwise, save a new rating instance with form data and redirect to detail page.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A redirect to the movie detail page
        :doc-author: Trelent
        """
        movie = self.get_object()
        user = request.user
        print(user)
        rating = Raiting.objects.filter(user=user, movie=movie).first()

        if rating:
            rating.delete()
            return redirect("movie_detail", slug=movie.slug)
        form = RaitingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = user
            rating.movie = movie
            print(rating)
            rating.save()

        return redirect("movie_detail", slug=movie.slug)


class ActorView(PoiskList, DetailView):
    """Class-based view for displaying actor details."""

    model = Actor
    template_name = "persons/actors.html"
    slug_field = "name"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        return context


class DirectorView(PoiskList, DetailView):
    """Class-based view for displaying director details."""

    model = Director
    template_name = "persons/directors.html"
    slug_field = "name"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["director_name"] = self.object.name
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        return context


class AddReview(FormView):
    """Class-based view for adding a review to a movie."""

    template_name = "movies/movie_detail.html"
    form_class = AddReviewForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        It's responsible for instantiating the view and calling other methods to do the work of responding to a request.
        The dispatch method on View classes is responsible for instantiating an instance of the class,
        calling setup(), then calling either get() or post(). It also takes care of exception handling.

        :param self: Refer to the current instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A httpresponseredirect object to the detail page of the movie that was just edited
        """
        self.movie = Movie.objects.get(id=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Save the review form data.
        :param self: Refer to the instance of the class
        :param form: Access the form data
        :return: A redirect to the movie detail page
        """
        review = form.save(commit=False)
        review.user = self.request.user
        review.movie = self.movie
        review.save()
        return redirect(self.movie.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["movie"] = self.movie
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        return context


class FilterMovies(PoiskList, generic.ListView):
    """Class-based view for filtering movies based on category, genre, and year."""

    def get_queryset(self):
        """
        The get_queryset function is used to filter the queryset of movies based on the
        GET parameters in the URL.

        :param self: Represent the instance of the class
        :return: A queryset of movies that are published
        """
        queryset = Movie.objects.filter(status=Movie.Status.PUBLISHED)
        if "category" in self.request.GET:
            queryset = queryset.filter(
                category__in=self.request.GET.getlist("category")
            )
        if "genre" in self.request.GET and self.request.GET.getlist("genre"):
            queryset = queryset.filter(genre__in=self.request.GET.getlist("genre"))
        if "year" in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist("year"))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["movies"] = self.get_queryset().distinct()
        context["categories"] = Category.objects.all()
        context["year"] = "".join([x for x in self.request.GET.getlist("year")])
        context["genre"] = "".join([x for x in self.request.GET.getlist("genre")])
        context["category"] = "".join([x for x in self.request.GET.getlist("category")])
        context["title"] = "Поиск фильма"
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        return context


class Search(PoiskList, generic.ListView):
    """Class-based view for searching movies based on a search query."""

    def get_queryset(self):
        """
        Get the queryset of movies based on the search query.
        :param self: Access the current instance of the class
        :return: The result of the filter function on the movie model
        """
        return Movie.objects.filter(title__iregex=self.request.GET.get("s"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        movies = self.get_queryset().distinct()
        context["s"] = f'q={self.request.GET.get("s")}&'
        context["movies"] = movies
        context["no_results"] = len(movies) == 0
        context["categories"] = Category.objects.all()
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        return context


class TopMoviesView(PoiskList, ListView):
    """Class-based view for displaying the top rated movies."""

    model = Movie
    template_name = "movies/top_movies.html"
    context_object_name = "top_movies"
    paginate_by = 5

    def get_queryset(self):
        """
        Get the queryset of top rated movies.
        :param self: Access the object itself
        :return: A queryset of all published movies that have at least one rating
        """

        return (
            Movie.objects.filter(status=Movie.Status.PUBLISHED)
            .exclude(
                Q(movie_of_rating__isnull=True)
                | Q(movie_of_rating__rating__isnull=True)
            )
            .annotate(average_rating=Avg("movie_of_rating__rating"))
            .order_by("-average_rating")
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["title"] = "Лучшие фильмы"
        context["soon_movies"] = Movie.objects.filter(status=Movie.Status.DRAFT)
        context["reviews"] = Review.objects.order_by("-id")

        return context


########################################################################################################################
#                                                     FUNCTIONS
########################################################################################################################
########################################################################################################################
#                                            Function that delete review
########################################################################################################################


@login_required
def delete_review(request, pk):
    """
    The delete_review function takes a request and primary key (pk) as arguments.
    It gets the review object with the given pk or returns a 404 error if it doesn't exist.
    It then gets the movie associated with that review, so we can redirect to its detail page after deleting it.
    If the user who made this request is also the user who created this review,
    delete it from our database; otherwise do nothing.

    :param request: Get the user who is logged in
    :param pk: Get the primary key of the review object
    :return: The movie's absolute url
    """
    review = get_object_or_404(Review, pk=pk)
    review_movie = review.movie
    if (
        review.user == request.user
        or request.user.is_superuser
        or request.user.is_staff
    ):
        review.delete()
    return redirect(review_movie.get_absolute_url())


########################################################################################################################

########################################################################################################################
#                                   Functions that add something (use on custom admin panel)
########################################################################################################################


def add_movie(request):
    """
    The add_movie function is used to add a new movie to the database.
    It uses the MovieForm class, which is defined in forms.py, and it takes
    a POST request as input (which contains all of the information about
    the movie that we want to add). If this POST request contains valid data, then we save it using form.save(),
    and redirect the user back to our homepage.

    :param request: Get information about the current request
    :return: A redirect to the movie_detail page
    """
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect("movie_detail", slug=movie.slug)

    else:
        form = MovieForm()
    return render(
        request,
        "movies/add_movie.html",
        {"form": form, "categories": Category.objects.all(), "title": "Добавить фильм"},
    )


def add_category(request):
    """
    The add_category function is used to add a new category to the database.
    It takes in a request object and returns an HTML page with the form for adding
    a new category. If the form is valid, it saves it and renders another HTML page
    with buttons for adding other objects.

    :param request: Get the data from the form
    :return: The add_buttons"""
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = CategoryForm()

    return render(
        request,
        "movies/add_category.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить категорию",
        },
    )


def add_genre(request):
    """
    The add_genre function is used to add a new genre to the database.
    It takes in a request object and returns an HTML page with the form for adding genres.
    If the form is valid, it saves it and redirects back to buttons page.

    :param request: Get the request from the user
    :return: The add_buttons
    """
    if request.method == "POST":
        form = GenreForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = GenreForm()

    return render(
        request,
        "movies/add_genre.html",
        {"form": form, "categories": Category.objects.all(), "title": "Добавить жанр"},
    )


def add_director(request):
    """
    The add_director function is used to add a new director to the database.
    It takes in a request object and returns an HTML page with the form for adding
    a new director. If the form is valid, it saves it and redirects back to the main page.

    :param request: Get the data from the form
    :return: The add_buttons
    """
    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = DirectorForm()

    return render(
        request,
        "movies/add_director.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить режиссера",
        },
    )


def add_actor(request):
    """
    The add_actor function is used to add a new actor to the database.
    It takes in a request object and returns an HTML page with the form for adding actors.
    If the method of this request is POST, then it will save the data from that form into our database.

    :param request: Get the data from the form
    :return: A render function
    """
    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "movies/add_buttons.html")
    else:
        form = ActorForm()

    return render(
        request,
        "movies/add_actor.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить актера",
        },
    )


def add_movie_images(request):
    """
    The add_movie_images function is used to add images for a movie.
    The function takes in the request and returns an HTML page with a form that allows users to upload images for movies.
    If the user submits the form, then it saves the image and redirects them back to buttons page.

    :param request: Get the request object that is sent to the view
    :return: The add_buttons
    """
    if request.method == "POST":
        form = MovieImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, "movies/add_buttons.html")

    else:
        form = MovieImageForm()
    return render(
        request,
        "movies/add_movie_images.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Добавить изображение",
        },
    )


########################################################################################################################

########################################################################################################################
#                                   Function all categories that consist of buttons
########################################################################################################################


def category_buttons(request):
    """
    The category_buttons function is a view that returns the category_buttons.html template,
    which contains buttons for each of the categories in our database. The template uses a for loop to iterate over
    the list of categories and create an HTML button element for each one.

    :param request: Pass the request object to the view
    :return: A template with a list of all categories
    """
    categories = Category.objects.all()
    return render(
        request,
        "movies/category_buttons.html",
        {"categories": categories, "title": "Категории"},
    )


########################################################################################################################

########################################################################################################################
#                                   Function that displays all actions on the admin panel
########################################################################################################################


def add_buttons(request):
    """
    The add_buttons function is a view that renders the add_buttons.html template,
    which contains buttons for adding new movies and categories to the database.

    :param request: Get the request object
    :return: The add_buttons
    """
    return render(
        request,
        "movies/add_buttons.html",
        {"categories": Category.objects.all(), "title": "Добавить"},
    )


########################################################################################################################

########################################################################################################################
#                                   Function that displays the description of the site
########################################################################################################################


def about_us(request):
    """
    The about_us function is responsible for rendering the about_us.html template,
    which contains information about the website and its creators.

    :param request: Get the request object
    :return: The about_us
    """
    return render(
        request, "about_us/about_us.html", {"categories": Category.objects.all()}
    )


########################################################################################################################

########################################################################################################################
#                                   Functions that change the status of the user
########################################################################################################################
def get_user(request):
    """
    The get_user function is a view that allows the user to select a username
    from the database. The selected username is then stored in session data, and
    the user is redirected to update_status.

    :param request: Get the current request
    :return: The get_user
    """
    if request.method == "POST":
        form = GetUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            request.session["selected_username"] = username
            return redirect("update_status")
    else:
        form = GetUserForm()

    return render(
        request,
        "movies/get_user.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Выбрать пользователя",
        },
    )


def update_status(request):
    """
    The update_status function is used to update the status of a user.
    The function takes in a request and returns an HTML page with the form for updating
    the status of a user. The function also checks if the form is valid, and if it is,
    updates the status of that particular user.

    :param request: Pass the request object to the view
    :return: A page with a form to update the status of the user
    """
    username = request.session.get("selected_username")
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == "POST":
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data["status"]
            if new_status == "администратор":
                user.is_superuser = True
                user.is_staff = True
            if new_status == "менеджер":
                user.is_superuser = False
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = False

            user.status = new_status
            user.save(update_fields=["status", "is_superuser", "is_staff"])
            return redirect("add_buttons")
    else:
        initial_data = {"username": user}
        form = UpdateStatusForm(initial=initial_data)

    return render(
        request,
        "movies/update_status.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Обновить статус",
        },
    )


########################################################################################################################

########################################################################################################################
#                       Functions that allow you to change or delete something(use on admin panel)
########################################################################################################################
def category_list(request):
    """
    The category_list function is responsible for displaying a list of all categories.
    It accepts the request object as an argument and returns an HttpResponse object that contains the rendered HTML template.
    The function uses Django's ORM to query the database for all Category objects, then passes them to a template called category_list.html.

    :param request: Get the request object
    :return: A rendered template with a list of all the categories in the database
    """
    categories = Category.objects.all()
    form = GetCategoryForm(request.GET)
    search_query = request.GET.get("search", "")

    if search_query:
        categories = categories.filter(name__icontains=search_query)
        # if not categories:

    return render(
        request, "movies/category_list.html", {"categories": categories, "form": form}
    )


def edit_category(request, category_id):
    """
    The edit_category function is used to edit a category.
    It takes in the request and the id of the category to be edited as parameters.
    The function first gets the category object from its id, then checks if it's a POST request or not. If it is,
    we create an instance of CategoryForm with that specific movie object and save it if valid.
    Otherwise, we just create an empty form for editing purposes.

    :param request: Get the data from the form
    :param category_id: Get the category object from the database
    :return: A rendered template, which is a string
    """
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        return redirect("category_list")
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "movies/edit_category.html",
        {"form": form, "categories": Category.objects.all()},
    )


def delete_category(request, category_id):
    """
    The delete_category function is a view that allows the user to delete a category.
    It takes in two arguments, request and category_id. It first gets the Category object with
    the primary key of category_id, then checks if it's a POST request (meaning that the user has submitted
    a form). If so, it deletes the Category object and redirects to category_list. Otherwise, it renders
    delete_category, passing in all categories as context.

    :param request: Get the request that is sent to the server
    :param category_id: Get the category that we want to delete
    :return: The delete_category
    """
    category = Category.objects.get(pk=category_id)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(
        request, "movies/delete_category.html", {"categories": Category.objects.all()}
    )


def genre_list(request):
    """
    The genre_list function is a view that displays all the genres in the database.
    It also has a search bar to filter through them by name.

    :param request: Pass the request object to the view
    :return: A list of all genres
    """
    genres = Genre.objects.all()
    form = GetGenreForm()
    search_query = request.GET.get("search", "")

    if search_query:
        genres = genres.filter(name__icontains=search_query)

    return render(
        request,
        "movies/genre_list.html",
        {"genres": genres, "categories": Category.objects.all(), "form": form},
    )


def edit_genre(request, genre_id):
    """
    The edit_genre function takes a request and genre_id as parameters.
    It gets the Genre object with the given id, then checks if it's a POST request.
    If so, it creates an instance of GenreForm using the POST data and saves it to database.
    Otherwise, it creates an empty form instance for editing purposes.

    :param request: Get the data from the form
    :param genre_id: Find the genre that is being edited
    :return: A render function
    """
    genre = Genre.objects.get(id=genre_id)

    if request.method == "POST":
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect("genre_list")
    else:
        form = GenreForm(instance=genre)

    return render(
        request,
        "movies/edit_genre.html",
        {"form": form, "genre": genre, "categories": Category.objects.all()},
    )


def delete_genre(request, genre_id):
    """
    The delete_genre function is a view that allows the user to delete a genre.
    It takes in two parameters: request and genre_id. The function first gets the
    genre object from the database using its primary key, which is passed as an argument.
    If it's a POST request, then we delete the genre and redirect to our list of genres; otherwise,
    we render our template with all categories.

    :param request: Get information about the request that was made
    :param genre_id: Get the genre object from the database
    :return: The delete_genre
    """
    genre = Genre.objects.get(pk=genre_id)
    if request.method == "POST":
        genre.delete()
        return redirect("genre_list")
    return render(
        request,
        "movies/delete_genre.html",
        {"genre": genre, "categories": Category.objects.all()},
    )


def actor_list(request):
    """
    The actor_list function is responsible for displaying a list of actors.
    It accepts an HTTP GET request and returns an HTTP response with the rendered actor_list.html template,
     which displays all actors in the database.

    :param request: Get the request object from the view
    :return: A list of all the actors in the database
    """
    actors = Actor.objects.all()
    form = GetActorForm(request.GET)
    search_query = request.GET.get("search", "")

    if search_query:
        actors = actors.filter(name__icontains=search_query)

    return render(
        request,
        "movies/actor_list.html",
        {"actors": actors, "categories": Category.objects.all(), "form": form},
    )


def edit_actor(request, actor_id):
    """
    The edit_actor function takes in a request and an actor_id. It then gets the
    actor with that id from the database, and if it's a POST request, it creates
    a form using ActorForm with the data from that POST request. If this form is valid,
    it saves it to the database and redirects to actor_list. Otherwise, if there was no
    POST request or if there were errors in validation of said POST request (i.e., not valid),
    then we create an empty ActorForm instance for editing.

    :param request: Get the request object, which is used to get information about the current web request
    :param actor_id: Get the actor object from the database
    :return: A render function
    """
    actor = Actor.objects.get(id=actor_id)

    if request.method == "POST":
        form = ActorForm(request.POST, request.FILES, instance=actor)
        if form.is_valid():
            form.save()
            return redirect("actor_list")
    else:
        form = ActorForm(instance=actor)

    return render(
        request,
        "movies/edit_actor.html",
        {"form": form, "actor": actor, "categories": Category.objects.all()},
    )


def delete_actor(request, actor_id):
    """
    The delete_actor function is a view that allows the user to delete an actor from the database.
    It takes in a request and an actor_id, which is used to find the specific Actor object in question.
    If it's a POST request, then we delete that Actor object and redirect back to our list of actors.
    Otherwise, we render out our template with all of our categories.

    :param request: Get the request from the user
    :param actor_id: Get the actor object from the database
    :return: A redirect to the actor_list view
    """
    actor = Actor.objects.get(pk=actor_id)
    if request.method == "POST":
        actor.delete()
        return redirect("actor_list")
    return render(
        request,
        "movies/delete_actor.html",
        {"actor": actor, "categories": Category.objects.all()},
    )


def director_list(request):
    """
    The director_list function is responsible for displaying a list of directors.
    It takes in the request object and returns an HTML page with all the directors listed.

    :param request: Get the request from the user
    :return: A list of all directors in the database
    """
    directors = Director.objects.all()
    form = GetDirectorForm()
    search_query = request.GET.get("search", "")

    if search_query:
        directors = directors.filter(name__icontains=search_query)

    return render(
        request,
        "movies/director_list.html",
        {"directors": directors, "categories": Category.objects.all(), "form": form},
    )


def edit_director(request, director_id):
    """
    The edit_director function takes in a request and director_id,
    gets the director with that id, then checks if the request is POST.
    If it is POST, it creates a DirectorForm instance with the data from
    that post and saves it to the database. If not POST, then we create an empty form.

    :param request: Get the request from the user
    :param director_id: Get the director object from the database
    :return: A rendered template with a form
    """
    director = Director.objects.get(id=director_id)

    if request.method == "POST":
        form = DirectorForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            form.save()
            return redirect("all_directors_list")
    else:
        form = DirectorForm(instance=director)

    return render(
        request,
        "movies/edit_director.html",
        {"form": form, "director": director, "categories": Category.objects.all()},
    )


def delete_director(request, director_id):
    """
    The delete_director function is a view that allows the user to delete a director from the database.
    It takes in two arguments: request and director_id. The function first gets the Director object with
    the primary key of director_id, then checks if it's a POST request (i.e., if someone has clicked on
    the Delete button). If so, it deletes that Director object and redirects to all_directors_list; otherwise,
    it renders delete_director.html with context data containing both the categories and directors.

    :param request: Get the request from the user
    :param director_id: Get the director object from the database
    :return: The delete_director
    """
    director = Director.objects.get(pk=director_id)
    if request.method == "POST":
        director.delete()
        return redirect("all_directors_list")
    return render(
        request,
        "movies/delete_director.html",
        {"director": director, "categories": Category.objects.all()},
    )


def movie_list_admin(request):
    """
    The movie_list_admin function is a view that displays all movies in the database.
    It also allows for searching of movies by title, and filtering by category.

    :param request: Get the data from the form
    :return: The movie_list_admin
    """
    movies = Movie.objects.all()
    form = GetMovieForm()
    search_query = request.GET.get("search", "")

    if search_query:
        movies = movies.filter(title__icontains=search_query)
    return render(
        request,
        "movies/movie_list_admin.html",
        {"movies": movies, "categories": Category.objects.all(), "form": form},
    )


def edit_movie(request, movie_id):
    """
    The edit_movie function is used to edit a movie.
      It takes in the request and the movie_id as parameters.
      The function gets the movie object from Movie model using its id, then checks if it's a POST request or not.
      If it's a POST request, we create an instance of MovieForm with data from the form and files
      (if any) and save it to database after checking if it's valid or not.
      If it's not a POST request, we just create an instance of
      MovieForm with data from that specific movie object without saving anything yet.

    :param request: Get the data from the form
    :param movie_id: Get the movie object from the database
    :return: The edit_movie
    """
    movie = Movie.objects.get(id=movie_id)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("movie_list_admin")
    else:
        form = MovieForm(instance=movie)

    return render(
        request,
        "movies/edit_movie.html",
        {"form": form, "movie": movie, "categories": Category.objects.all()},
    )


def delete_movie(request, movie_id):
    """
    The delete_movie function is a view that allows an admin to delete a movie from the database.
    It takes in two parameters: request and movie_id. The request parameter is used to determine if the user has submitted
    the form, and if so, it deletes the movie with id equal to movie_id from the database. If not, it renders a template
    that displays all of the information about that particular Movie object.

    :param request: Get the request object
    :param movie_id: Get the movie object from the database
    :return: A render, which is a request to display the delete_movie
    """
    movie = Movie.objects.get(pk=movie_id)
    if request.method == "POST":
        movie.delete()
        return redirect("movie_list_admin")
    return render(
        request,
        "movies/delete_movie.html",
        {"movie": movie, "categories": Category.objects.all()},
    )


########################################################################################################################

########################################################################################################################
#                                              Delete user function
########################################################################################################################
def delete_user(request):
    """
    The delete_user function is used to delete a user from the database.
    It takes in a request object and returns an HTML page with the form for deleting users.
    If the form is valid, it deletes the user from the database and redirects to add_buttons page.

    :param request: Get the current request
    :return: The rendered template
    """
    if request.method == "POST":
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user = get_user_model().objects.get(username=username)
                user.delete()
                messages.success(request, f"Пользователь {username} успешно удален.")
                return redirect("add_buttons")
            except get_user_model().DoesNotExist:
                messages.error(request, f"Пользователь {username} не найден.")
    else:
        form = DeleteUserForm()

    return render(
        request,
        "movies/delete_user.html",
        {
            "form": form,
            "categories": Category.objects.all(),
            "title": "Удалить пользователя",
        },
    )


########################################################################################################################


def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', slug=review.movie.slug)
    else:
        form = EditReviewForm(instance=review)

    return render(request, 'movies/edit_review.html', {'form': form, 'review': review})