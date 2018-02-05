# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import sys

# Create your views here.
def home(request):
	# render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
	

	prevInputIsNum = False
	display = 0
	new_val = 0
	prev_value = 0
	prev_oper = '+'
	error = ''

	context = {'display': 0}
	try:
	#initialize variables if there's a client-side value
		if 'new_val' in request.POST and request.POST['new_val'] != '':
			new_val = int(request.POST['new_val'])
			context['new_val'] = new_val

		if 'prevInputIsNum' in request.POST and request.POST['prevInputIsNum'] != '':
			prevInputIsNum = (request.POST['prevInputIsNum'] == 'True')
			context['prevInputIsNum'] = prevInputIsNum

		if 'prev_value' in request.POST and request.POST['prev_value'] != '':
			prev_value = int(request.POST['prev_value'])
			context['prev_value'] = prev_value

		if 'prev_oper' in request.POST and request.POST['prev_oper'] != '':
			prev_oper = request.POST['prev_oper']
			context['prev_oper'] = prev_oper
		
		#------------processing-------------------------------
		if 'number' in request.POST:
			input = int(request.POST['number'])
			if (input<0) or (input > 9):
				error = "Input should be 0~9!!"
				new_val = 0
				prev_value = 0
				prev_oper = '+'
				context['error'] = error
				context['new_val'] = new_val
				context['prev_value'] = prev_value
				context['prev_oper'] = prev_oper
			else:
				context['prevInputIsNum'] = True;
				new_val = new_val * 10+ input
				context['display'] = new_val
				context['new_val'] = new_val


		if 'operator' in request.POST:
			input = request.POST['operator']

			flag = False;
			# print "prevInputIsNum",prevInputIsNum
			if prevInputIsNum:
				if prev_oper == '+':
					prev_value = prev_value + new_val

				elif prev_oper == '-':
					prev_value = prev_value - new_val

				elif prev_oper == '*':
					prev_value = prev_value * new_val

				elif prev_oper == '/':
					if new_val == 0:
						error = "Can't divide by 0!"
						new_val = 0
						prev_value = 0
						prev_oper = '+'
						flag = True
					else:
						prev_value = prev_value // new_val

				elif prev_oper == '=':
					prev_value = new_val

				else:
					error = "Invalid input!!"
					new_val = 0
					prev_value = 0
					prev_oper = '+'
					flag = True

			# update value and send to client side
			if not flag:
				# print "is not flag",flag
				# print "input",input
				prev_oper = input
			context['display'] = prev_value
			context['prevInputIsNum'] = False
			context['new_val'] = 0
			context['prev_oper'] = prev_oper
			context['prev_value'] = prev_value
			context['error'] = error

		if 'clear' in request.POST:
			context['new_val'] = 0
			context['prev_value'] = 0
			context['prev_oper'] = '+'
			context['prevInputIsNum'] = False
			context['display'] = 0

	except:
		context['error'] = "Error: Invalid input!"
		context['new_val'] = 0
		context['prev_value'] = 0
		context['prev_oper'] = '+'
        # print out error message
        #print(sys.exc_info())


	return render(request, 'calculator/calculator.html', context)

 