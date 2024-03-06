from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ModelApi
from .forms import ModelApiForm
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.http import HttpResponse


@login_required
def predict_homepage(request):
    data = ModelApi.objects.all()
    return render(request, 'predict/predict_homepage.html', {'data': data})

@method_decorator(login_required, name='dispatch')
class SelectProcess(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = ModelApi.objects.get(pk=pk)
        context = {'data': data}
        request.session['process_pk'] = pk
        return render(request, 'predict/select_process.html', context=context)

@login_required
def new_process(request):
    if request.method == 'POST':
        form = ModelApiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predict_homepage')

    else:
        form = ModelApiForm()
    return render(request, 'predict/new_process.html', {'form': form})

@login_required
def process_location(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data
            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(City=form_data['City'],
                                                           State=form_data['State'],
                                                           Zip=form_data['Zip'])
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_bank')
        else:
            print(form.errors)
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_location.html', {'Name': data.Name, 'form': form})

@login_required
def process_bank(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data
            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(Bank=form_data['Bank'],
                                                           BankState=form_data['BankState'],
                                                           NAICS=form_data['NAICS'])
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_activity')
        else:
            print(form.errors)
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_bank.html', {'Name': data.Name, 'form': form})

@login_required
def process_activity(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data

            # variables booléennes
            FranchiseCode = 2
            if request.POST.get('r_FranchiseCode') == 'yes':
                FranchiseCode = 0
            RevLineCr = 'N'
            if request.POST.get('r_RevLineCr') == 'yes':
                RevLineCr = 'Y'
            LowDoc = 'N'
            if request.POST.get('r_LowDoc') == 'yes':
                LowDoc = 'Y'
            # variable Urban Rural
            UrbanRural = 0
            if request.POST.get('r_UrbanRural') == 'Urban':
                UrbanRural = 1
            elif request.POST.get('r_UrbanRural') == 'Rural':
                UrbanRural = 2
            
            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(NewExist=form_data['NewExist'],
                                                           NoEmp=form_data['NoEmp'],
                                                           CreateJob=form_data['CreateJob'],
                                                           RetainedJob=form_data['RetainedJob'],
                                                           DiffJobs=form_data['RetainedJob'] - form_data['CreateJob'],
                                                           FranchiseCode=FranchiseCode,
                                                           UrbanRural=UrbanRural,
                                                           RevLineCr=RevLineCr,
                                                           LowDoc=LowDoc)
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_bankloan')
        else:
            print(form.errors)
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_activity.html', {'Name': data.Name, 'form': form})

@login_required
def process_bankloan(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data

            # ApprovalFY
            ApprovalFY = request.POST.get('date_ApprovalFY') + '-01-01'

            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(ApprovalDate=form_data['ApprovalDate'],
                                                           ApprovalFY=ApprovalFY,
                                                           Term=form_data['Term'])
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_guaranteedamountrequested')
        else:
            print(form.errors)
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_bankloan.html', {'Name': data.Name, 'form': form})

@login_required
def process_guaranteedamountrequested(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data

            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(GrAppv=form_data['GrAppv'])
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_sbaapprouval')
        else:
            print(form.errors)
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_guaranteedamountrequested.html', {'Name': data.Name, 'form': form})

@login_required
def process_sbaapprouval(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data
            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(Bank=form_data['Bank'], BankState=form_data['BankState'], NAICS=form_data['NAICS'])
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
        else:
            print(form.errors)
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_sbaapprouval.html', {'Name': data.Name, 'form': form})