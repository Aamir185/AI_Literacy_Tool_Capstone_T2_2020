from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.linear_model import LinearRegression
import numpy as np
import subprocess
from django.template import loader
import os


def index(request):
    return render(request, 'index.html')


def aipipeline(request):
    return render(request, 'aipipeline.html')


def example(request):
    if request.GET.get('q1'):
        rslt = "The machine has learned to draw a line"
        # val = int(input("\nEnter the value of x(y=x): "));
        # val = int(10)
        val = int(request.GET.get('q1'))
        plt.plot(range(val), '-r')
        plt.title('Graph of y-x=0')
        plt.xlabel('x', color='#1C2833')
        plt.ylabel('y', color='#1C2833')
        plt.grid()
        plt.savefig("static/images/Gout.png", bbox_inches='tight')
        # plt.show()

        return render(request, 'example.html', {'flagL': rslt})

    if request.GET.get('x') and request.GET.get('y'):
        print("The machine has learned to identify if the points specified is inside or outside the circle")
        # xval = int(input("\nEnter the value of x: "));
        # yval = int(input("\nEnter the value of y: "));
        xval = int(request.GET.get('x'))
        yval = int(request.GET.get('y'))
        if (xval * xval) + (yval * yval) > 25:
            rslt = "Outside circle"
            xlimt = xval + 1
            ylimt = yval + 1
        else:
            rslt = "Inside circle"
            xlimt = ylimt = 6
        circle1 = plt.Circle((0, 0), 5, color='r')

        fig, ax = plt.subplots(1)
        ax.set_aspect(1)
        plt.xlim(-xlimt, xlimt)
        plt.ylim(-ylimt, ylimt)
        ax.add_artist(circle1)
        ax.plot((xval), (yval), 'o', color='y')
        plt.plot(xval, yval)
        plt.grid(linestyle='--')
        plt.title('Circle with radius 5', fontsize=8)
        plt.savefig("static/images/Gout.png", bbox_inches='tight')
        # plt.show()

        return render(request, 'example.html', {'flag': rslt})

    if request.GET.get('a') and request.GET.get('b'):
        print("The machine has learned to identify if the points specified is inside or outside the square")
        xval = int(request.GET.get('a'))
        yval = int(request.GET.get('b'))
        if xval >= -4 and xval <= 4 and yval >= -4 and yval <= 4:
            rslt = "Inside Square"
            xlimt = ylimt = 6
        else:
            rslt = "Outside Outside"
            xlimt = xval + 1
            ylimt = yval + 1

        fig, ax = plt.subplots(1)
        ax.set_aspect(1)
        plt.xlim(-xlimt, xlimt)
        plt.ylim(-ylimt, ylimt)
        ax.add_patch(
            patches.Rectangle(
                xy=(-4, -4),  # point of origin.
                width=8,
                height=8,
                linewidth=1,
                color='red',
                fill=True
            )
        )
        ax.plot((xval), (yval), 'o', color='y')
        plt.plot(xval, yval)
        plt.grid(linestyle='--')
        plt.title('Square with width 5', fontsize=8)
        plt.savefig("static/images/Gout.png", bbox_inches='tight')
        # plt.show()

        return render(request, 'example.html', {'flag': rslt})

    if request.GET.get('addx') and request.GET.get('addy'):
        X = [[2, 3], [1, 5], [5, 6]]
        Y = [5, 6, 11]
        model = LinearRegression()
        model.fit(X, Y)
        first = int(request.GET.get('addx'))
        sec = int(request.GET.get('addy'))
        m = np.asarray(first, dtype='float64')
        n = np.asarray(sec, dtype='float64')
        b = (model.predict(np.array([m, n]).reshape(1, -1)))
        return render(request, 'example.html', {'totaladd': b})
    if request.GET.get('subx') and request.GET.get('suby'):
        X = [[5, 3], [9, 5], [7, 6]]
        Y = [2, 4, 1]
        model = LinearRegression()
        model.fit(X, Y)
        first = int(request.GET.get('subx'))
        sec = int(request.GET.get('suby'))
        m = np.asarray(first, dtype='float64')
        n = np.asarray(sec, dtype='float64')
        b = (model.predict(np.array([m, n]).reshape(1, -1)))
        return render(request, 'example.html', {'totalsub': b})

    # print("xx",request.GET.get('x'))

    # if request.POST.get('x'):
    #   print("YEA")
    # if request.GET.get('data'):
    #   print(request.GET.get('data'))
    if request.GET.get('age'):
        age = int(request.GET.get('age'))

        if age == 1:
            subprocess.call('python detect.py --image kid1.jpg')
            print("lookup")
            ageresult = 1
            return render(request, 'example.html', {'ageresult': ageresult})
        elif age == 2:
            subprocess.call('python detect.py --image girl1.jpg')
            ageresult = 1
            return render(request, 'example.html', {'ageresult': ageresult})
        elif age == 3:
            subprocess.call('python detect.py --image man1.jpg')
            ageresult = 1
            return render(request, 'example.html', {'ageresult': ageresult})
        else:
            return render(request, 'example.html')

    else:
        return render(request, 'example.html')
