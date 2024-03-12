from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
import requests
import re
import json
from .models import ModelApi
from .forms import ModelApiForm
from .utils import process_validation


@login_required
def predict_homepage(request):
    request.session['process_pk'] = 0
    data = ModelApi.objects.all()
    return render(request, 'predict/predict_homepage.html', {'data': data})

@method_decorator(login_required, name='dispatch')
class SelectProcess(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        request.session['process_pk'] = pk
        # data = ModelApi.objects.get(pk=pk)
        # context = {'data': data}
        instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
        form = ModelApiForm(instance=instance)
        return render(request, 'predict/select_process.html', {'form': form})

@login_required
def new_process(request):
    request.session['process_pk'] = 0
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
    errors = ''

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data
            # test de l'onglet
            process = False
            if form_data['City'] and form_data['State'] and form_data['Zip']:
                process = True
            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(City=form_data['City'],
                                                           State=form_data['State'],
                                                           Zip=form_data['Zip'],
                                                           process_location=process,
                                                           process_status=process_validation(process, data.process_bank, data.process_activity, data.process_bank_loan, data.process_guaranteed_amount_requested))
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_bank')
        else:
            print(form.errors)
            errors = form.errors
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_location.html', {'Name': data.Name, 'form': form, 'errors': errors})

@login_required
def process_bank(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])
    errors = ''

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data
            # test de l'onglet
            process = False
            if form_data['Bank'] and form_data['BankState'] and form_data['NAICS'] is not None and form_data['NAICS'] != "":
                process = True
            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(Bank=form_data['Bank'],
                                                           BankState=form_data['BankState'],
                                                           NAICS=form_data['NAICS'],
                                                           process_bank=process,
                                                           process_status=process_validation(data.process_location, process, data.process_activity, data.process_bank_loan, data.process_guaranteed_amount_requested))
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_activity')
        else:
            print(form.errors)
            errors = form.errors
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_bank.html', {'Name': data.Name, 'form': form, 'errors': errors})

@login_required
def process_activity(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])
    errors = ''

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data

            # variables booléennes
            NewExist = 2
            if request.POST.get('r_NewExist') == '1':
                NewExist = 1
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

            # DiffJobs
            DiffJobs = 0
            if form_data['RetainedJob'] and form_data['CreateJob']:
                DiffJobs = form_data['RetainedJob'] - form_data['CreateJob']

            # test de l'onglet
            process = False
            if (form_data['NoEmp'] is not None and form_data['NoEmp'] != ""
                and form_data['CreateJob'] is not None and form_data['CreateJob'] != ""
                and form_data['RetainedJob'] is not None and form_data['RetainedJob'] != ""):
                process = True

            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(NewExist=NewExist,
                                                           NoEmp=form_data['NoEmp'],
                                                           CreateJob=form_data['CreateJob'],
                                                           RetainedJob=form_data['RetainedJob'],
                                                           DiffJobs=DiffJobs,
                                                           FranchiseCode=FranchiseCode,
                                                           UrbanRural=UrbanRural,
                                                           RevLineCr=RevLineCr,
                                                           LowDoc=LowDoc,
                                                           process_activity=process,
                                                           process_status=process_validation(data.process_location, data.process_bank, process, data.process_bank_loan, data.process_guaranteed_amount_requested))
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_bankloan')
        else:
            print(form.errors)
            errors = form.errors
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_activity.html', {'Name': data.Name, 'form': form, 'errors': errors})

@login_required
def process_bankloan(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])
    errors = ''

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data

            # ApprovalFY
            ApprovalFY = None
            if request.POST.get('date_ApprovalFY'):
                if re.match(r'^\d{4}$', request.POST.get('date_ApprovalFY')):
                    ApprovalFY = request.POST.get('date_ApprovalFY') + '-01-01'
                else:
                    errors = 'Approval FY is not valid'

            # test de l'onglet
            process = False
            if form_data['ApprovalDate'] and ApprovalFY and form_data['Term']:
                process = True

            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(ApprovalDate=form_data['ApprovalDate'],
                                                           ApprovalFY=ApprovalFY,
                                                           Term=form_data['Term'],
                                                           process_bank_loan=process,
                                                           process_status=process_validation(data.process_location, data.process_bank, data.process_activity, process, data.process_guaranteed_amount_requested))
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_guaranteedamountrequested')
        else:
            print(form.errors)
            errors = form.errors
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_bankloan.html', {'Name': data.Name, 'form': form, 'errors': errors})

@login_required
def process_guaranteedamountrequested(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])
    errors = ''
    try_approval = ''

    if request.method == 'POST':
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data
            
            # TEST D'APPROBATION
            if 'try_approval' in request.POST:
                try_approval = ''
                try:
                    min = int(float(request.POST['SBA_Appv_min']))
                    max = int(float(request.POST['SBA_Appv_max']))
                    step = int(float(request.POST['SBA_Appv_step']))

                    url = 'http://api_predict:8001/predict'
                    headers = {
                        'Accepts': 'application/json',
                        'Content-Type': 'application/json',
                    }
                    # session = Session()
                    # session.headers.update(headers)

                    data_dict = {
                        'City': data.City,
                        'State': data.State,
                        'Zip': data.Zip,
                        'Bank': data.Bank,
                        'BankState': data.BankState,
                        'NAICS': data.NAICS,
                        'ApprovalDate': data.ApprovalDate.strftime('%Y-%m-%d'),
                        'ApprovalFY': data.ApprovalFY.strftime('%Y-%m-%d'),
                        'Term': data.Term,
                        'NoEmp': data.NoEmp,
                        'NewExist': data.NewExist,
                        'CreateJob': data.CreateJob,
                        'RetainedJob': data.RetainedJob,
                        'DiffJobs': data.DiffJobs,
                        'FranchiseCode': data.FranchiseCode,
                        'UrbanRural': data.UrbanRural,
                        'RevLineCr': data.RevLineCr,
                        'LowDoc': data.LowDoc,
                        'GrAppv': data.GrAppv,
                        'SBA_Appv': 0,
                    }

                    i = 0
                    for i_try_approval in range(min, max, step):
                        i += 1
                        if i > 10: break

                        try:
                            data_dict['SBA_Appv'] = i_try_approval
                            json_data = json.dumps(data_dict)
                            response = requests.post(url, data=json_data, headers=headers)
                            response_json = response.json()
                            print('session:', response_json)
                        except Exception as e:
                            print()
                            print("try_approval error 2:", e)
                            print()
                            try_approval += 'API Error'
                            break
                        
                        response = "KO"
                        if response_json['predict']:
                            response = "OK"

                        try_approval += '<br>pour $' + str(i_try_approval) + ' > ' + response
                except Exception as e:
                    print()
                    print("try_approval error 1:", e)
                    print()
                    try_approval = "Inputs are not numerics."
                
            # test de l'onglet
            process = False
            if form_data['GrAppv']:
                process = True

            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(GrAppv=form_data['GrAppv'],
                                                           process_guaranteed_amount_requested=process,
                                                           process_status=process_validation(data.process_location, data.process_bank, data.process_activity, data.process_bank_loan, process))
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
            if 'submit_next' in request.POST:
                return redirect('process_sbaapprouval')
        else:
            print(form.errors)
            errors = form.errors
    else:
        form = ModelApiForm(instance=instance)
    
    try:
        data = ModelApi.objects.get(pk=request.session['process_pk'])
        SBA_Appv_max = data.GrAppv + 1000
    except:
        SBA_Appv_max = 0
    return render(request, 'predict/process_guaranteedamountrequested.html', {'Name': data.Name, 'form': form, 'errors': errors, 'SBA_Appv_max': SBA_Appv_max, 'try_approval': try_approval})

@login_required
def process_sbaapprouval(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])
    errors = ''

    if request.method == 'POST':
        if 'delete' in request.POST:
            return redirect('process_delete_validation')
        
        form = ModelApiForm(request.POST, instance=instance)
        if form.is_valid():
            # Récupérer les données valides du formulaire
            form_data = form.cleaned_data

            # test de l'onglet
            process = False
            if form_data['GrAppv']:
                process = True

            # Mettre à jour uniquement certains champs du modèle
            ModelApi.objects.filter(pk=instance.pk).update(GrAppv=form_data['GrAppv'],
                                                           process_sba_approuval=process)
            # Recharger l'instance du modèle pour refléter les changements
            instance.refresh_from_db()
            form = ModelApiForm(instance=instance)
        else:
            print(form.errors)
            errors = form.errors
    else:
        form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_sbaapprouval.html', {'Name': data.Name, 'form': form, 'errors': errors})

@login_required
def process_delete_validation(request):
    instance = get_object_or_404(ModelApi, pk=request.session['process_pk'])
    data = ModelApi.objects.get(pk=request.session['process_pk'])
    
    if request.method == 'POST':
        if 'Confirm' in request.POST:
            ModelApi.objects.get(id=request.session['process_pk']).delete()
            request.session['process_pk'] = 0
            return redirect('predict_homepage')
        
        if 'Deny' in request.POST:
            return redirect('process_sbaapprouval')
        
    form = ModelApiForm(instance=instance)
        
    return render(request, 'predict/process_delete_validation.html', {'Name': data.Name, 'form': form})