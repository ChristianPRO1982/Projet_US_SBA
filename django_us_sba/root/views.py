from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import SignupForm
from django.contrib.auth.password_validation import password_validators_help_texts
from django.contrib.auth.models import User
from django.contrib import messages


def get_all_users_data():
    all_users_data = User.objects.all()
    return all_users_data

def error_404(request, exception):
    return render(request, 'root/404.html', status=404)

def root_homepage(request):
    return render(request, 'root/root_homepage.html')

def about(request):
    return render(request, 'root/about.html')

def users(request):
    user_id = request.GET.get('user')
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
        except:
            pass

    all_users_data = get_all_users_data()
    context = {
        "all_users_data": all_users_data,
    }
    return render(request, 'root/users.html', context=context)

def history(request):
    return render(request, 'root/history.html')

# class UserCreationFromCustom(UserCreationForm):
#     class Meta(UserCreationForm.Meta) :
#         model = User

class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False  # Ne pas activer le compte immédiatement
        user.save()
        # self.send_confirmation_email(user)
        return response
    
    def form_invalid(self, form):
        # Récupérer les erreurs du formulaire
        errors = form.errors.get('__all__') or form.errors
        # Ajouter les erreurs dans les messages de la requête
        for field, error in errors.items():
            messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    # def send_confirmation_email(self, user):
    #     mailjet.send.create(data=data)

    # def get_success_url(self):
    #     # Rediriger vers une page informant l'utilisateur de vérifier son email
    #     return reverse_lazy('home')
