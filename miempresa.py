#!/usr/bin/env python2.5

from asterisk.agi import *
from time import sleep, time

def prueba():
	unixepoch = str(time()).split(".")[0]
	# TODO: guardarlas grabaciones separadas en directorios por fecha
	recordir = "/var/lib/asterisk/sounds/miempresavoicemail/"
	miagi = AGI()
	callerId = miagi.env['agi_callerid']
	miagi.verbose("Llamada desde %s" % callerId)
	miagi.set_variable('empresa', "miempresa")
	miagi.set_variable('callerid', str(callerId))
	miagi.set_variable('voicemailfile', recordir + str(callerId) + "_" + unixepoch+'.gsm')
	miagi.answer()
	miagi.stream_file('miempresa/hola')
	# el -1 es para sin timeout
	miagi.record_file(recordir + str(callerId) + "_" + unixepoch , "gsm", "#", -1 , beep="beep")
	miagi.hangup()

if __name__ == "__main__":
	prueba()
