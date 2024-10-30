from django.shortcuts import render, get_object_or_404, redirect
from restaurant.models import Category, Menu, Comment, Reservation, Chef
from restaurant.forms import CommentForm, ReservationForm
from rest_framework import viewsets
from restaurant.serializers import ReservationSerializer, MenuSerializer, CommentSerializer, CategorySerializer, ChefSerializer


def home(request):
    comments = Comment.objects.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'comments': comments,
        'form': form,
    }

    return render(request, 'Menu/home.html', context)

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()

    return redirect('home')

def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.dislikes += 1
    comment.save()

    return redirect('home')

def menu(request):
    # Récupérer les catégories
    premiere_selection = get_object_or_404(Category, name='Première Sélection')
    deuxieme_selection = get_object_or_404(Category, name='Deuxième Sélection')
    troisieme_selection = get_object_or_404(Category, name='Troisième Sélection')

    # Récupérer les plats par catégorie
    plats_premiere_selection = Menu.objects.filter(category=premiere_selection)
    plats_deuxieme_selection = Menu.objects.filter(category=deuxieme_selection)
    plats_troisieme_selection = Menu.objects.filter(category=troisieme_selection)

    # Passer les plats et les prix des sous-catégories au template
    context = {
        'plats_premiere_selection': plats_premiere_selection,
        'plats_deuxieme_selection': plats_deuxieme_selection,
        'plats_troisieme_selection': plats_troisieme_selection,
    }

    return render(request, 'Menu/menu.html', context)

def reservations(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        date = request.POST.get('date')
        people = request.POST.get('people')
        time = request.POST.get('time')
        content = request.POST.get('content')

        print(f"Name: {name}, Mail: {mail}, Date: {date}, People: {people}, Time: {time}, Content: {content}")

        # Sauvegarder les données dans la base de données
        if name and mail and date and people and time:
            Reservation.objects.create(
                name=name,
                mail=mail,
                date=date,
                people=people,
                time=time,
                content=content
            )
            return redirect('reservations')

    form = ReservationForm()  # Assurez-vous que le formulaire est initialisé pour être utilisé dans le template
    return render(request, 'Menu/reservations.html', {'form': form})

def contact(request):
    return render(request, 'Menu/contact.html')

def send_contact(request):
    return render(request, 'Menu/send_contact.html')

def history(request):
    return render(request, 'Menu/history.html')

#Views for l'API REST

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

