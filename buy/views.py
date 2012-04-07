# Create your views here.
from tracker.buy.models import *

def counts(request):
    pp=Purchase.objects.all()