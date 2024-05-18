# Import delle librerie necessarie
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from telethon import TelegramClient, events
import MetaTrader5 as mt5

# Definizione della classe principale dell'app
class MyApp(App):
    def build(self):
        # Creazione di un layout Box verticale
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Aggiunta di un titolo
        title = Label(text='Telegram Copier MT5')
        layout.add_widget(title)
        
        # Aggiunta dei radiobutton in un layout Box orizzontale
        radio_layout = BoxLayout(orientation='horizontal', spacing=10)
        
        def on_radio_button_press(instance):
            print("gruppo selezionato:", instance.text)
        
        radio_button1 = ToggleButton(text='Test', group='radio_group', on_press=on_radio_button_press)
        radio_layout.add_widget(radio_button1)
        
        radio_button2 = ToggleButton(text='TFXC', group='radio_group', on_press=on_radio_button_press)
        radio_layout.add_widget(radio_button2)
        
        layout.add_widget(radio_layout)
        
        # Aggiunta di un campo di input
        input_field = TextInput(hint_text='Inserisci lot...')
        layout.add_widget(input_field)
        
        # Definizione della funzione da eseguire quando viene premuto il bottone
        def on_button_press(instance):
            # Stampa il testo inserito nel campo di input e il gruppo selezionato
            print("Testo inserito:", input_field.text)
            selected_group = [button.text for button in radio_layout.children if isinstance(button, ToggleButton) and button.state == 'down']
            print("Gruppo selezionato:", selected_group)

                        
            api_id = 28102255
            api_hash = "6d0ad2615b0268fc6e9cd04056fe0d40"
            client = TelegramClient('session_name', api_id, api_hash)

            async def main():
                me = await client.get_me()
                print("BOT PYTHON PER TRADING DA TELEGRAM A MT5")
                username = me.username
                print(f"Numero collegato: {me.phone}")
                # print(username)
                # print(me.phone)
                
                # testo = input("cosa vuoi scrivere sul gruppo? ")
                # await client.send_message(-4147458196, testo)
                # id forex signals : -1001541002369
                # id gruppo prove : -4147458196
                # print(selected_group[0])
                if selected_group[0] == "Test":
                    group_id = -4147458196
                elif selected_group[0] == "TFXC":
                    group_id = -1001541002369

                if group_id == -4147458196:
                    print(f"Gruppo collegato: Gruppo prove {group_id}")
                elif group_id == -1001541002369:
                    print(f"Gruppo collegato: Gruppo Forex {group_id}")
                    
                lot = input_field.text
                print("lot: ", lot)

                group = await client.get_entity(group_id)
                    
                @client.on(events.NewMessage(chats=group))
                async def handler(event):
                    testo = event.message.text

                    if "signal alert" in testo.lower():
                        print("SEGNALE IN ARRIVO")
                        print(testo)
                        print()
                        list = testo.split()

                        buy_or_sell = list[2]
                        currency = list[3]

                        #correggi eventuali scambi tra valuta e azione dal gruppo telegram
                        if currency == "BUY" or currency == "SELL":
                            temp = buy_or_sell
                            buy_or_sell = currency
                            currency = temp

                        if len(list) > 13:
                            list.pop(5)
                            list.pop(7)
                            list.pop(9)
                            list.pop(11)
                        print(list)

                        enter = list[4]
                        take_profits = {"TP1": list[6], "TP2": list[8], "TP3": list[10]}
                        stop_loss = list[12]
                        #stampa i valori singoli
                        print("BUY OR SELL:", buy_or_sell)
                        print("CURRENCY:", currency)
                        print("ENTER AT:", enter)
                        print("TP1:", take_profits["TP1"])
                        print("TP2:", take_profits["TP2"])
                        print("TP3:", take_profits["TP3"])
                        print("SL:", stop_loss)

                        mt5.initialize()

                        login = 1128453
                        password = 'BKv^6JO&'
                        server = 'VantageInternational-Demo'
                        mt5.login(login, password, server)
                        #lot = 0.04


                        # BUY
                        if buy_or_sell == "BUY":
                            #TP1
                            request1 = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": currency,
                                "volume": float(lot),
                                "type": mt5.ORDER_TYPE_BUY,
                                "price": mt5.symbol_info_tick(currency).ask,
                                "sl": float(stop_loss),
                                "tp": float(take_profits["TP1"]),
                                "comment": "TP1",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC
                            }
                            print(request1)
                            result1 = mt5.order_send(request1)
                            print(result1)

                            if result1.retcode == mt5.TRADE_RETCODE_DONE:
                                print("Ordine eseguito con successo")
                            else:
                                print("Errore durante l'esecuzione dell'ordine:", result1.comment)

                            #TP2
                            request1 = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": currency,
                                "volume": float(lot),
                                "type": mt5.ORDER_TYPE_BUY,
                                "price": mt5.symbol_info_tick(currency).ask,
                                "sl": float(stop_loss),
                                "tp": float(take_profits["TP2"]),
                                "comment": "TP2",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC
                            }
                            print(request1)
                            result1 = mt5.order_send(request1)
                            print(result1)

                            if result1.retcode == mt5.TRADE_RETCODE_DONE:
                                print("Ordine eseguito con successo")
                            else:
                                print("Errore durante l'esecuzione dell'ordine:", result1.comment)

                            #TP3
                            request1 = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": currency,
                                "volume": float(lot),
                                "type": mt5.ORDER_TYPE_BUY,
                                "price": mt5.symbol_info_tick(currency).ask,
                                "sl": float(stop_loss),
                                "tp": float(take_profits["TP3"]),
                                "comment": "TP3",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC
                            }
                            print(request1)
                            result1 = mt5.order_send(request1)
                            print(result1)

                            if result1.retcode == mt5.TRADE_RETCODE_DONE:
                                print("Ordine eseguito con successo")
                            else:
                                print("Errore durante l'esecuzione dell'ordine:", result1.comment)
                            
                        #SELL
                        if buy_or_sell == "SELL":
                            #TP1
                            request2 = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": currency,
                                "volume": float(lot),
                                "type": mt5.ORDER_TYPE_SELL,
                                "price": mt5.symbol_info_tick(currency).bid,
                                "sl": float(stop_loss),
                                "tp": float(take_profits["TP1"]),
                                "comment": "TP1",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC
                            }
                            print(request2)
                            result2 = mt5.order_send(request2)
                            print(result2)

                            if result2.retcode == mt5.TRADE_RETCODE_DONE:
                                print("Ordine eseguito con successo")
                            else:
                                print("Errore durante l'esecuzione dell'ordine:", result2.comment)

                            #TP2
                            request2 = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": currency,
                                "volume": float(lot),
                                "type": mt5.ORDER_TYPE_SELL,
                                "price": mt5.symbol_info_tick(currency).bid,
                                "sl": float(stop_loss),
                                "tp": float(take_profits["TP2"]),
                                "comment": "TP2",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC
                            }
                            print(request2)
                            result2 = mt5.order_send(request2)
                            print(result2)

                            if result2.retcode == mt5.TRADE_RETCODE_DONE:
                                print("Ordine eseguito con successo")
                            else:
                                print("Errore durante l'esecuzione dell'ordine:", result2.comment)

                            #TP3
                            request2 = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": currency,
                                "volume": float(lot),
                                "type": mt5.ORDER_TYPE_SELL,
                                "price": mt5.symbol_info_tick(currency).bid,
                                "sl": float(stop_loss),
                                "tp": float(take_profits["TP3"]),
                                "comment": "TP3",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC
                            }
                            print(request2)
                            result2 = mt5.order_send(request2)
                            print(result2)

                            if result2.retcode == mt5.TRADE_RETCODE_DONE:
                                print("Ordine eseguito con successo")
                            else:
                                print("Errore durante l'esecuzione dell'ordine:", result2.comment)
                        
                        mt5.shutdown()

                    else:
                        print(testo)

                # Start the client
                await client.run_until_disconnected()
                

            with client:
                client.loop.run_until_complete(main())

        
        # Aggiunta di un bottone
        button = Button(text='Avvia', on_press=on_button_press)
        layout.add_widget(button)
        
        return layout

# Esecuzione dell'app
if __name__ == '__main__':
    MyApp().run()
