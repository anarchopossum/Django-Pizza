from django.shortcuts import render
from .forms import PizzaForm, MultiPizzaForm
from django.forms import formset_factory
from .models import Pizza


def home(request):
    return render(request, 'pizza/home.html')


def order(request):
    multiple_form = MultiPizzaForm()
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        # If the Form is Valid pass and give a number value.
        # Else don't give a number value and 
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thanks for your order! your %s %s and %s pizza is on its way!' % (filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'], filled_form.cleaned_data['topping2'],)
            #  ^^^ The filled form values above will clean the data and add them to the string note. ^^^
            filled_form = PizzaForm()
        else:
            created_pizza_pk = None
            note = "Something went wrong: Your Pizza was not created. Please try again."
        return render(request, 'pizza/order.html', {'created_pizza_pk':created_pizza_pk, 'pizzaform': filled_form, 'note': note, 'multiple_form':
                multiple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form':multiple_form})

# For multiple Pizzas
def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiPizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
            note = "Pizzas have been ordered!"
        else:
            note = 'Order was not created, Please try again'
        return render(request, 'pizza/pizzas.html', {'note': note, 'formset': formset})
    else:
        # if fails at least return one order
        return render(request, 'pizza/pizzas.html', {'formset': formset})

# Allows the user to edit their order.
def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Order has been updated! Thank you!'
            # this will make sure to pass on the note above
            return render(request, 'pizza/edit_order.html', {'note':note,'pizzaform':form,'pizza':pizza})
    return render(request, 'pizza/edit_order.html', {'pizzaform': form,'pizza':pizza})

