from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from .models import User, Book, Chat, DeleteRequest, Feedback
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import ChatForm, BookForm, UserForm
from . import models
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def profile(request):
    return render(request, 'bookstore/profile.html',{'object': request.user})

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserForm(instance=user)

    return render(request, 'bookstore/update_profile.html', {'form': form})


# Shared Views
def custom_404_view(request, exception):
    """Custom 404 Error View."""
    context = {
        'error_message': 'The page you are looking for does not exist.',
        'suggestion': 'Return to the homepage or try a different URL.',
    }
    return render(request, '404.html', context, status=404)

def login_form(request):
	return render(request, 'bookstore/login.html')


def logoutView(request):
	logout(request)
	return redirect('home')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('publisher')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('login')  
    return render(request, 'bookstore/login.html')


def register_form(request):
	return render(request, 'bookstore/register.html')


def registerView(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=make_password(password))
            user.save()

            messages.success(request, 'Account was created successfully')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('regform')
    else:
        messages.error(request, 'Invalid request method')
        return redirect('regform')
    
# Publisher views
@login_required
def publisher(request):
	return render(request, 'publisher/home.html')

def books_by_category(request):
    category = request.GET.get('category')  # Fetch selected category from request
    books = Book.objects.filter(category=category) if category else Book.objects.all()
    return render(request, 'publisher/books.html', {'books': books, 'selected_category': category})

@login_required
def uabook_form(request):
	return render(request, 'publisher/add_book.html')


@login_required
def request_form(request):
	return render(request, 'publisher/delete_request.html')


@login_required
def feedback_form(request):
	return render(request, 'publisher/send_feedback.html')

@login_required
def about(request):
	return render(request, 'publisher/about.html')	


@login_required
def usearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('publisher')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()

                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)

                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res

                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)
   


                if files:
                    return render(request,'publisher/result.html',{'files':files,'word':word})
                return render(request,'publisher/result.html',{'files':files,'word':word})



@login_required
def delete_request(request):
	if request.method == 'POST':
		book_id = request.POST['delete_request']
		current_user = request.user
		user_id = current_user.id
		username = current_user.username
		user_request = username + "  want book with id  " + book_id + " to be deleted"

		a = DeleteRequest(delete_request=user_request)
		a.save()
		messages.success(request, 'Request was sent')
		return redirect('request_form')
	else:
	    messages.error(request, 'Request was not sent')
	    return redirect('request_form')



@login_required
def send_feedback(request):
	if request.method == 'POST':
		feedback = request.POST['feedback']
		current_user = request.user
		user_id = current_user.id
		username = current_user.username
		feedback = username + " " + " says " + feedback

		a = Feedback(feedback=feedback)
		a.save()
		messages.success(request, 'Feedback was sent')
		return redirect('feedback_form')
	else:
	    messages.error(request, 'Feedback was not sent')
	    return redirect('feedback_form')

class UBookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'publisher/book_list.html'
	context_object_name = 'books'
	paginate_by = 2

	def get_queryset(self):
		return Book.objects.order_by('-id')

@login_required
def uabook(request):
	if request.method == 'POST':
		title = request.POST['title']
		author = request.POST['author']
		year = request.POST['year']
		category = request.POST['category']
		desc = request.POST['desc']
		cover = request.FILES['cover']
		pdf = request.FILES['pdf']
		current_user = request.user
		user_id = current_user.id
		username = current_user.username

		a = Book(title=title, author=author, year=year, category=category, 
			desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
		a.save()
		messages.success(request, 'Book was uploaded successfully')
		return redirect('publisher')
	else:
	    messages.error(request, 'Book was not uploaded successfully')
	    return redirect('uabook_form')	



class UCreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'publisher/chat_form.html'
	success_url = reverse_lazy('ulchat')


	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)


class UListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'publisher/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')

# Admin views
@user_passes_test(lambda u: u.is_superuser)
@login_required() 
def dashboard(request):
	book = Book.objects.all().count()
	user = User.objects.all().count()

	context = {'book':book, 'user':user}

	return render(request, 'dashboard/home.html', context)

@login_required() 
def create_user_form(request):
    choices = {'choice': ['user', 'admin']}
    return render(request, 'dashboard/add_user.html', choices)


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"


class AEditUser(SuccessMessageMixin, UpdateView): 
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"

class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')

def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        userType = request.POST['userType']
        email = request.POST['email']
        password = request.POST['password']

        password = make_password(password)

        if userType == "user":
            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.save()
            messages.success(request, 'User account was created successfully!')
        elif userType == "admin":
            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True
            )
            user.is_admin = True
            user.save()
            messages.success(request, 'Admin account was created successfully!')
        else:
            messages.error(request, 'Invalid user role selected.')
            return redirect('create_user_form')

        return redirect('aluser')

    return redirect('create_user_form')

class ALViewUser(DetailView):
    model = User
    template_name='dashboard/user_detail.html'

class ACreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'dashboard/chat_form.html'
	success_url = reverse_lazy('alchat')

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class AListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'dashboard/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


@login_required
def aabook_form(request):
	return render(request, 'dashboard/add_book.html')


@login_required
def aabook(request):
	if request.method == 'POST':
		title = request.POST['title']
		author = request.POST['author']
		year = request.POST['year']
		category = request.POST['category']
		desc = request.POST['desc']
		cover = request.FILES['cover']
		pdf = request.FILES['pdf']
		current_user = request.user
		user_id = current_user.id
		username = current_user.username

		a = Book(title=title, author=author, year=year, category=category, 
			desc=desc, cover=cover, pdf=pdf, uploaded_by=username, user_id=user_id)
		a.save()
		messages.success(request, 'Book was uploaded successfully')
		return redirect('albook')
	else:
	    messages.error(request, 'Book was not uploaded successfully')
	    return redirect('aabook_form')


class ABookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/book_list.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')

class AManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')

class ADeleteBook(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete2.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was dele successfully'


class ADeleteBookk(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete.html'
	success_url = reverse_lazy('dashboard')
	success_message = 'Data was dele successfully'


class AViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/book_detail.html'

class AEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'dashboard/edit_book.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was updated successfully'

class ADeleteRequest(LoginRequiredMixin,ListView):
	model = DeleteRequest
	template_name = 'dashboard/delete_request.html'
	context_object_name = 'feedbacks'
	paginate_by = 3

	def get_queryset(self):
		return DeleteRequest.objects.order_by('-id')

class AFeedback(LoginRequiredMixin,ListView):
	model = Feedback
	template_name = 'dashboard/feedback.html'
	context_object_name = 'feedbacks'
	paginate_by = 3

	def get_queryset(self):
		return Feedback.objects.order_by('-id')

@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))


    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashborad')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()

                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res

                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)

                if files:
                    return render(request,'dashboard/result.html',{'files':files,'word':word})
                return render(request,'dashboard/result.html',{'files':files,'word':word})
