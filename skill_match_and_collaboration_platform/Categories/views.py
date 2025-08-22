from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Categories
from .forms import CatForm

@method_decorator(login_required, name='dispatch')
class AddCatView(CreateView):
    model = Categories
    form_class = CatForm
    template_name = 'add_cat.html'
    success_url = reverse_lazy('addCat')  # Redirect after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as the author
        return super().form_valid(form)