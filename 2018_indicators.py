#!/usr/bin/env python
from tkinter import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time as t
from pybittrex.client import Client
from colorama import *

# ---------------------------------------------INTERFAZ----------------------------------------------------- #

window = Tk()
menu = Menu(window)
miFrame = Frame(window)
miFrame.pack(fill="none", expand="True")

window.resizable(0, 0)
window.geometry("300x470")
op = IntVar()

window.title("Indicadores Criptomercado")
logo = PhotoImage(file="t1.png")
lbllogo = Label(window, image=logo).place(x=-7, y=372)

# ------------------------------------------------FUNCIONES-------------------------------------------- #


def market_history():

    if op.get() == 1:

        c = Client(api_key='abc', api_secret='123')

        # ----------------------------- Parameters ----------------------------- #

        symbol = input("Mercado (Ejemplo: usdt-btc):  ")
        time = int(input("Tiempo en segundos: "))

        market = symbol
        time_seconds = 2
        trials = time
        file_name = 'market.csv'

        # ----------------------------- Getting Data ----------------------------- #

        i = 1
        fails = 0
        dfm = pd.DataFrame({})

        while i in range(1, trials + 1):

            while True:

                try:

                    hist = c.get_market_history(market).json()['result']
                    df = pd.DataFrame(hist)
                    df["csv"] = i
                    dfm = dfm.append(df)
                    percent = round(100 * (i / trials), 2)
                    print("Procesando... ", percent, "% completado")

                    if i % 3 == 0:
                        dfm.drop_duplicates("Id", keep="first", inplace=True)
                        dfm.to_csv(file_name)

                    i += 1

                    break

                except:

                    print(" El internet esta fallando, intentaremos de nuevo..")
                    t.sleep(1)
                    fails += 1

        dfm.drop_duplicates("Id", keep="first", inplace=True)
        dfm["mk_page"] = np.floor(np.array(range(0, dfm.shape[0])) / 100) + 1
        dfm.reset_index(drop=True, inplace=True)
        dfm.to_csv(file_name)

        print("Proceso terminado!")


def volumen():
    if op.get() == 1:

        data = pd.read_csv('market.csv')
        data = data.sort_values(['TimeStamp'], ascending=True)

        line = []
        line1 = []

        op1 = int(input("\nComo desea visualizar los datos? 1 = Tiempo real | 2 = Completos: "))

        for i in range(0, len(data)):

            if data.OrderType[i] == "BUY":

                quantity = data.Quantity[i]
                line.append(quantity)
                plt.plot(quantity)

                print(Fore.GREEN + "Fecha: %s Cantidad: %s Precio: %s [BUY]" %
                      (data.TimeStamp[i], quantity, round(data.Price[i], 2)))

            else:

                quantity = data.Quantity[i]
                line1.append(quantity)
                plt.plot(quantity)

                print(Fore.RED + "Fecha: %s Cantidad: %s Precio: %s [SELL]" %
                      (data.TimeStamp[i], quantity, round(data.Price[i], 2)))

            plt.plot(line, linestyle='-', color='G', label="BUY")
            plt.plot(line1, linestyle='-', color='R', label="SELL")

            plt.title('Volume BUY/SELL Market History last 100 orders', fontsize=15, color='0',
                      verticalalignment='baseline', horizontalalignment='center')

            if op1 == 1:
                plt.pause(0.2)
                plt.cla()

        if op1 == 2:
            plt.show()


def price():
    if op.get() == 1:

        data = pd.read_csv('market.csv')
        linea2 = []

        op1 = int(input(Fore.WHITE + "\nComo desea visualizar los datos? 1 = Tiempo real | 2 = Completos: "))

        for i in range(0, len(data)):

            linea2.append(data.Price[i])
            plt.plot(linea2)

            if data.OrderType[i] == 'BUY':
                print(Fore.GREEN + "Fecha: %s Cantidad: %s Precio: %s [%s]" % (
                    data.TimeStamp[i], data.Quantity[i], round(data.Price[i], 2), data.OrderType[i]))

            else:
                print(Fore.RED + "Fecha: %s Cantidad: %s Precio: %s [%s]" % (
                    data.TimeStamp[i], data.Quantity[i], round(data.Price[i], 2), data.OrderType[i]))

            plt.plot(linea2, linestyle='-', color='BLACK', label="PRICE")
            plt.title("Grafica de Precio")

            if op1 == 1:
                plt.pause(0.2)
                plt.cla()

        if op1 == 2:
            plt.show()


def filtrar_market_precio():

    if op.get() == 1:

        data = pd.read_csv('market.csv')

        print(Fore.WHITE + "")
        min = float(input("Precio minimo: "))
        max = float(input("Precio máximo: "))

        total = 0
        total2 = 0

        for i in range(0, len(data)):

            if data.Price[i] >= min and data.Price[i] <= max:

                if data.OrderType[i] == 'BUY':
                    total += data.Quantity[i]

                else:
                    total2 += data.Quantity[i]

        print(Fore.GREEN + "Total tranzado [BUY]: %s" % (round(total, 2)))
        print(Fore.RED + "Total tranzado [SELL] %s" % (round(total2, 2)))
        print(Fore.WHITE + "Total: %s BTC" % (round(total + total2, 2)))


def market():
    if op.get() == 1:

        data = pd.read_csv('market.csv', header=0)

        cantidad_buy = 0
        cantidad_sell = 0

        for i in range(0, len(data)):

            if data.OrderType[i] == "BUY":
                cantidad_buy = (cantidad_buy + data['Quantity'][i])

            else:
                cantidad_sell = (cantidad_sell + data['Quantity'][i])

        print(Fore.GREEN + "\n[ASK-BUY]: Cantidad: %s " % (round(cantidad_buy, 2)))
        print(Fore.RED + "[BID-SELL] Cantidad: %s \n" % (round(cantidad_sell, 2)))

        maxi = max(data.Price)
        mini = min(data.Price)
        i = 0
        count = 0
        count1 = 0

        for i in range(0, len(data)):

            if maxi == data.Price[i]:
                count += 1

            if mini == data.Price[i]:
                count1 += 1

        print(Fore.WHITE + "Precio máximo: %s se repitió %s veces" % (maxi, count))
        print(Fore.WHITE + "Precio mínimo: %s se repitió %s veces \n" % (mini, count1))
        print("Porcentaje de cambio: %s%%" % (round(100 - (mini * 100) / maxi, 2)))


def orderbook():

    if op.get() == 1:

        c = Client(api_key='abc', api_secret='123')

        # ----------------------------- Parameters ----------------------------- #

        symbol = input("Mercado (Ejemplo USDT-BTC): ")
        time = int(input("Tiempo en segundos: "))

        time_seconds = time
        trials = time
        market = symbol
        file_name = 'order.csv'
        # ----------------------------- Getting Data ----------------------------- #

        i = 1
        dfm = pd.DataFrame({})

        while i in range(1, trials + 1):
            while True:
                try:

                    order = c.get_orderbook(market, type="both").json()['result']
                    buy = order["buy"]
                    sell = order["sell"]

                    buy_df = pd.DataFrame(buy)
                    buy_df["type"] = "buy"
                    buy_df["trial"] = i

                    sell_df = pd.DataFrame(sell)
                    sell_df["trial"] = i
                    sell_df["type"] = "sell"

                    dfm = dfm.append(buy_df)
                    dfm = dfm.append(sell_df)

                    percent = round(100 * (i / trials), 2)
                    print("Working in progress... ", percent, "% Completed")

                    dfm.to_csv(file_name)

                    t.sleep(time_seconds)
                    i += 1

                    break
                except:

                    print(" El internet esta fallando, intentaremos de nuevo..")
                    t.sleep(5)


def order():
    if op.get() == 1:

        print(Fore.WHITE + "")
        moneda = input("Moneda - Ejemplo BTC: ")
        min = float(input("Cantidades  inferiores a: "))
        max = float(input("Cantidades  superiores a : "))

        data = pd.read_csv('order.csv', header=0)

        k = 0
        k1 = 0
        k2 = 0
        k3 = 0

        for i in range(0, len(data)):

            if data.type[i] == "buy":

                if data.Quantity[i] < min:
                    k += 1
                    print(Fore.RED + "[ASK] Cantidad: %s Precio: %s \n" % (data.Quantity[i], data.Rate[i]))

                if data.Quantity[i] > max:
                    k1 += 1
                    print(Fore.MAGENTA + "[ASK] Cantidad: %s Precio: %s \n" % (data.Quantity[i], data.Rate[i]))

            else:

                if data.Quantity[i] < min:
                    k2 += 1
                    print(Fore.MAGENTA + "[BID] Cantidad: %s Precio: %s \n" % (data.Quantity[i], data.Rate[i]))

                if data.Quantity[i] > max:
                    k3 += 1
                    print(Fore.MAGENTA + "[BID] Cantidad: %s Precio: %s \n" % (data.Quantity[i], data.Rate[i]))

        print(Fore.WHITE + "________________________________________________________________\n")
        print(Fore.RED + "ASK: " + Fore.WHITE + "[Ordenes menores a %s %s ] = %s" % (min, moneda, k2))
        print(Fore.GREEN + "BID: " + Fore.WHITE + "[Ordenes menores a %s %s ] = %s\n" % (min, moneda, k))
        print(Fore.RED + "ASK: " + Fore.WHITE + "[Ordenes mayores a %s %s ] = %s " % (max, moneda, k3))
        print(Fore.GREEN + "BID: " + Fore.WHITE + "[Ordenes mayores a %s %s ] = %s " % (max, moneda, k1))


def spread():

    if op.get() == 1:

        c = Client(api_key='abc', api_secret='123')

        # ----------------------------- Parameters ----------------------------- #

        market = input("Mercado (Ejemplo USDT-BTC): ")
        time_seconds = int(input("Tiempo en segundos: "))
        file_name = 'order.csv'
        trials = 1

        # ----------------------------- Getting Data ----------------------------- #

        i = 1
        dfm = pd.DataFrame({})
        n = 0

        while n < time_seconds:
            try:

                order = c.get_orderbook(market, type="both").json()['result']
                buy = order["buy"]
                sell = order["sell"]

                buy_df = pd.DataFrame(buy)
                buy_df["type"] = "buy"
                buy_df["trial"] = i

                sell_df = pd.DataFrame(sell)
                sell_df["trial"] = i
                sell_df["type"] = "sell"

                dfm = dfm.append(buy_df)
                dfm = dfm.append(sell_df)

                dfm.to_csv(file_name)

                t.sleep(1)
                i += 1

            except:

                print(" The internet has fallen apart!!! We must wait 10 sec and try it again!! ")
                t.sleep(5)

            data = pd.read_csv(file_name)

            spread = data['Rate'][0] - data['Rate'][9]

            spread1 = data['Rate'][109] - data['Rate'][100]

            if spread < 100:
                print("")
                print("Spread BID Orden [1-10] -> %s USDT" % (round(spread, 4)))
            if spread1 < 100:
                print("Spread ASK Orden [1-10] -> %s USDT" % (round(spread1, 4)))
                print("")
                print("Spread entre BID/ASK -> %s " % (round(data.Rate[100] - data.Rate[0], 5)))
                print("_______________________________")

            dfm = pd.DataFrame({})
            n += 1


def buscar_ordenes():

    if op.get() == 1:

        data = pd.read_csv('order.csv')

        orden = float(input("Cantidad: "))

        counter = 0

        for i in range(0, len(data)):

            if orden == data.Quantity[i]:

                if data.type[i] == 'buy':

                    print(Fore.RED + "[ASK] Existe una orden de %s en %s \n" % (
                        data.Quantity[i], data.Rate[i]))

                else:
                    print(Fore.GREEN + "[BID] Existe una orden de %s en %s \n" % (
                        data.Quantity[i], data.Rate[i]))

                counter = counter + 1

        print(Fore.WHITE + "Total: %s ordenes \n" % counter)


# ----------------------------------------------BOTONES------------------------------------------------------- #

Exchange = Label(window, text="Exchange:").place(x=7, y=10)
Text = Label(window, text="Herramientas:").place(x=10, y=60)
Text1 = Label(window, text='______________________________________________').place(x=0, y=77)

bittrex = Radiobutton(window,text="Bittrex", value=1, variable=op).place(x=15, y=35)

boton1 = Button(miFrame, text="Market History", width=36, command=market_history)
boton1.grid(row=1, column=0)

boton2 = Button(miFrame, text="Order Book", width=36, command=orderbook)
boton2.grid(row=2, column=0)

boton3 = Button(miFrame,text="Gráfica │ Precio Market", width=36, command=price)
boton3.grid(row=3, column=0)

boton4 = Button(miFrame, text="Gráfica │ Volumen Market History", width=36, command=volumen)
boton4.grid(row=4, column=0)

boton5 = Button(miFrame,text="MarketHistory │ Volumen", width=36, command=market)
boton5.grid(row=5, column=0)

boton6 = Button(miFrame,text="MarketHistory │ Filtrar Precio", width=36, command=filtrar_market_precio)
boton6.grid(row=6, column=0)

boton7 = Button(miFrame,text="Orderbook │ Ordenes Grandes/Pequeñas", width=36, command=order)
boton7.grid(row=7, column=0)

boton8 = Button(miFrame,text="Orderbook │ Filtrar ordenes", width=36, command=buscar_ordenes)
boton8.grid(row=7, column=0)

boton9 = Button(miFrame,text="Orderbook │ Spread", width=36, command=spread)
boton9.grid(row=8, column=0)

boton10 = Button(miFrame, text="Salir", width=36, command=window.quit)
boton10.grid(row=12, column=0)

window.mainloop()
