from django.shortcuts import render
from myapp.models import Result
import pandas as pd
import tabula
import os
from django.http import JsonResponse, HttpResponse

def form_view(request):
    return render(request, 'form.html')


def process_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        pdf_url = request.POST.get('pdf_url')
        template_path = request.POST.get('template_path')
        view_mode = request.GET.get('view_mode')

        # Ler o PDF com o template
        if pdf_url:
            tables = tabula.read_pdf_with_template(pdf_url, template_path)
        elif pdf_file:
            pdf_file_path = save_uploaded_file(pdf_file)
            tables = tabula.read_pdf_with_template(pdf_file_path, template_path)
        else:
            return render(request, 'form.html', {'error': 'Por favor, forneça um PDF válido.'})

        # Concatenar as tabelas em um dataframe
        df = pd.concat(tables).drop_duplicates()

        # Salvar o resultado no banco de dados
        result = Result(pdf_url=pdf_url, template_path=template_path)
        result.data = df.to_dict('records')
        result.save()

        # Exibir o resultado na página
        if view_mode == 'table':
            columns = list(df.columns)
            rows = df.to_dict('records')
            return render(request, 'table.html', {'columns': columns, 'rows': rows})
        else:
            return HttpResponse(result.result_csv, content_type='text/csv')

    return render(request, 'form.html')


def save_uploaded_file(uploaded_file):
    with open('temp.pdf', 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return 'temp.pdf'


def get_templates_list(request):
    template_dir = 'C:\\Users\\alexa\\Documents\\Templates_json\\'
    template_files = [f for f in os.listdir(template_dir) if os.path.isfile(os.path.join(template_dir, f))]
    return JsonResponse({'template_files': template_files}, safe=False)
