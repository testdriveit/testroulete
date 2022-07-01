from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import RouleteRounds
from django.http import JsonResponse
from django.db.models import Max

from datetime import datetime
import random

JACK_POT_NUMBER = 11

# Create your views here.
def index(request):
    random.seed(datetime.now())
    if not request.session.get('user_id'):      
        request.session['user_id'] = random.randint(0, 100000)
        user_id = request.session.get('user_id')
    else:
        user_id = request.session.get('user_id')
    round_id = None
    lucky_number = None
    template = loader.get_template('myfirst.html')
    if request.method == 'POST':
        round_id, lucky_number = get_lucky_number(user_id)
        context = {
            'round_id': round_id,
            'lucky_number': lucky_number
        }
        return JsonResponse(context)
    else:
        if request.GET.get('command') == 'stat':    
            context = get_statistic()
            return JsonResponse(context, safe = False)
        context = {
            'round_id': round_id,
            'lucky_number': lucky_number
        }  
        return HttpResponse(template.render(context, request))

def get_lucky_number(user_id = None):
    round_id = RouleteRounds.objects.aggregate(Max('round_id'))
    if round_id['round_id__max'] != None:
        round_id =  round_id['round_id__max']
    else:
        round_id = 1
    lucky_numbers = RouleteRounds.objects.filter(round_id=round_id).values()
    roulette = [i for i in range(1, 11, 1)]

    if len(lucky_numbers) > len(roulette):
        round_id += 1
        rand_num = random.randint(0, len(roulette)-1)
        lucky_number = roulette[rand_num]
        r_round = RouleteRounds(round_id = round_id, lucky_number = lucky_number, user_id = user_id)
        r_round.save()
        return round_id, lucky_number

    if len(lucky_numbers) == len(roulette):
        r_round = RouleteRounds(round_id = round_id, lucky_number = JACK_POT_NUMBER, user_id = user_id)
        r_round.save()
        return round_id, 'Jack Pot!'

    for number in lucky_numbers:
        if number.get('lucky_number') != JACK_POT_NUMBER:
            roulette[number.get('lucky_number')-1] = 0

    while True:
        rand_num = random.randint(0, len(roulette)-1)
        if roulette[rand_num] != 0:
            r_round = RouleteRounds(round_id = round_id, lucky_number = roulette[rand_num], user_id = user_id)
            r_round.save()
            return round_id, roulette[rand_num]


def get_statistic():
    max_round_id = RouleteRounds.objects.aggregate(Max('round_id'))
    max_round_id =  max_round_id['round_id__max']

    round_users = RouleteRounds.objects.values_list('round_id', 'user_id')
    stat_1 = {}
    for round_user in round_users:
        stat_1.setdefault(round_user[0], set())
        stat_1[round_user[0]].add(round_user[1])
    for key, value in stat_1.items():
        stat_1[key] = len(value)
    
    round_users2 = RouleteRounds.objects.values_list('user_id', 'round_id')

    stat_2 = {}
    for round_user in round_users2:
        stat_2.setdefault(round_user[0], {'round_nums': set(), 
            'round_clicks_avg': [0 for _ in range(max_round_id)]})
        stat_2[round_user[0]]['round_nums'].add(round_user[1])
        stat_2[round_user[0]]['round_clicks_avg'][round_user[1]-1] += 1
    for key, value in stat_2.items():
        stat_2[key]['round_nums'] = len(value['round_nums'])
        stat_2[key]['round_clicks_avg'] = sum(value['round_clicks_avg']) / len(value['round_clicks_avg'])

    return [stat_1, stat_2]

