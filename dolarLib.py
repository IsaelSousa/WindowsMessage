#!/usr/bin/env python3
## This lib powered by RafaelWinter
## https://github.com/rafaelwinter/dolar

from http.client import HTTPConnection
from datetime import datetime

import json

AWESOMEAPI_HOST = "economia.awesomeapi.com.br"
AWESOMEAPI_PATH = "/json/all/USD-BRL"


def symbol_request(host, request_string):
    def decorator(func):
        def request_dispatcher():
            try:
                connection = HTTPConnection(host)
                connection.request("GET", request_string)
                response = connection.getresponse()
            except Exception as e:
                print("Ocorreu um erro ao conectar ao servidor:", e)
                raise e

            if response.status != 200:
                print("O servidor retornou uma resposta inesperada:", response.status, response.reason)
                raise Exception("Invalid response")

            try:
                json_data = response.read()
                data = json.loads(json_data)
            except Exception as e:
                print("Ocorreu um erro ao decodificar a resposta do servidor:", e)
                raise e

            return func(data)

        return request_dispatcher

    return decorator


@symbol_request(AWESOMEAPI_HOST, AWESOMEAPI_PATH)
def get_awesomeapi_value(data=None):
    if not data['USD']:
        print("O servidor não conseguiu processar a requisição:", data['retorno'])
        raise Exception("Invalid response")

    cotacao = float(data['USD']['ask'])
    atualizacao = int(data['USD']['timestamp'])

    return (cotacao, atualizacao)


def format_date(utc_timestamp):
    d = datetime.utcfromtimestamp(utc_timestamp)
    offset = datetime.now() - datetime.utcnow()
    date = d + offset

    return date.strftime("%d/%m às %H:%M")

def dolarPriceValue():
    cotacao, atualizacao = get_awesomeapi_value()
    dolar = "Cotação USD: R$ {:.2f}".format(cotacao)
    return dolar

def dolarAttValue():
  cotacao, atualizacao = get_awesomeapi_value()
  att = str("Last Att: " + format_date(atualizacao))
  return att