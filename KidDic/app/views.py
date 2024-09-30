from django.shortcuts import render
from django.views import View
# Create your views here.

class PortfolioView(View):
    def get(self, request):
        return render(request, "portfolio.html")
    