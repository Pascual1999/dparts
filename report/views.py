from django.shortcuts import render


def report_view(request):
    """
    Vista para generar el reporte
    """
    return render(request, 'templates/report.html')