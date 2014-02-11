# -*- coding: utf-8 -*-
# Bot de Votation extreme
#
# Par Double Z.
#
# ---------------------
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                     Version 2, December 2004
# 
#  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
# 
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies of this license document, and changing it is allowed as long
#  as the name is changed.
# 
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
# 
#   0. You just DO WHAT THE FUCK YOU WANT TO.
#
# =============================================

import irclib
import ircbot

nick = "LaurentBrayage"
description = "Bot permettant le vote des auditeurs de Riff"
room = "#riff"
server = "irc.worldnet.net"
port = 6667

utilisateurs = ["Herondil"]
pause = True
aVote = {}	#Dict dans lequel chaque pseudo indique celui auquel il a voté
choix = []	#Les choix possible lors du vote
blacklist = []	#Les pseudos interdit de vote

class BotVote(ircbot.SingleServerIRCBot):
  def __init__(self):
    global nick
    global room
    global server
    global port
    
    ircbot.SingleServerIRCBot.__init__(self, [(server, port)],nick,description)
    
  def on_welcome(self,serv,ev):
    serv.join(room)
    serv.privmsg(room,"Bonsoir à tous et bienvenue dans On Est Bien Dans Katamariff, ce soir c'est moi qui vais gérer vos votes !")
    serv.privmsg(room,"Utilisez !LaurentBrayage pour plus d'informations !")
  
  #Les commandes a utiliser via MP
  def on_privmsg(self,serv,ev):
    auteur = irclib.nm_to_n(ev.source())
    canal = ev.target()
    message = ev.arguments()[0].split(" ")
    
    global pause
    global aVote
    global choix
    
    #Commande réalisable par tout le monde sauf les blacklistés
    if pause == False :
      interdit = False
      for black in blacklist :
	if auteur == black :
	  serv.privmsg(auteur,"Je vous rappelle que vous êtes interdit de vote !")
	  interdit = True
      
      if interdit == False :

        if message[0] == "!list" :
	  serv.privmsg(auteur,"Les choix possibles sont : " + str(choix))
        
	if message[0] == "!vote" :
          if len(message) == 2 :
            if message[1] in choix:
              for reponse in choix :
                if reponse == message[1] :
                  aVote[auteur] = message[1]
                  serv.privmsg(auteur, auteur+" a voté pour " + message[1])
            else :
              serv.privmsg(auteur,"La personne citée n'est pas dans la liste ! Utilisez !list pour afficher la liste !")
            
          else :
            serv.privmsg(room,"Il faut m'écrire ''!vote Nom'', avec Nom issu de la liste accessible avec !list")
            
    else :
      if message[0] == "!LaurentBrayage" or message[0] == "!aide" :
          serv.privmsg(auteur,"Pour envoyer son vote au concours, il faut attendre le lancement des votes !")
          serv.privmsg(auteur,"Une fois que le vote est commencé, il suffit de m'écrire ''!vote X'' pour voter pour X !")
          serv.privmsg(auteur,"Pour voir la liste des participants, envoyez moi ''!liste'' !")
      else :
          if not auteur in utilisateurs and message[0] in ["!vote","!list"]:
            serv.privmsg(auteur,"Les votes n'ont pas encore commencés, un peu de patience !")
      
    
    #Commandes réalisable par les modos uniquement
    for i in utilisateurs:
	if i == auteur :
	  if message[0] == "!help" or message[0] == "!aide" :
	    serv.privmsg(auteur,"Commandes possibles : !add !delete !publicscore !privatescore !force !modo !nomodo !start !fin !end !addblack !deleteblack !deletevote")
	  
	  if message[0] == "!add" :
	    try :
	      choix.append(message[1])
	      serv.privmsg(room,message[1] + " a été rajouté(e) dans la liste des participants de ce soir !")
	      serv.privmsg(auteur,message[1] + " rajouté(e) dans la liste ")
	    except :
	      pass
	    
	  if message[0] == "!delete" :
	    try :
	      if len(message) == 2 :
		for index,name in enumerate(choix) :
		  if name == message[1] :
		    choix.pop(index)
		    serv.privmsg(room,message[1] + " a été supprimé de la liste des choix possible")

	    except :
	      pass
	    
	  if message[0] == "!deletevote" :
	    for vote in aVote :
	      if vote == message[1] :
		aVote[message[1]] = ""
		serv.privmsg(room,"Le vote de " + message[1] + " a été supprimé")
	  
	  if message[0] == "!publicscore" :
	    for reponse in choix :
	      serv.privmsg(room,str(list(aVote.values()).count(reponse)) + " point(s) (a) ont été donné(s) à " + reponse)
	  
	  if message[0] == "!privatescore" :
	    for reponse in choix :
	      serv.privmsg(auteur,str(list(aVote.values()).count(reponse)) + " point(s) (a) ont été donné(s) à " + reponse)
	      
	  if message[0] == "!force" :
	    pass #force un vote pour quelqu'un meme si le pseudo n'existe pas
	    
	  if message[0] == "!modo" :
	      try :
		utilisateurs.append(message[1])
		serv.privmsg(room,message[1] + " peut maintenant me controler ...")
		serv.privmsg(message[1],"Vous êtes maintenant un modo de ce bot")
	      except :
		pass

	  if message[0] == "!nomodo" :
	    try :
	      for index,name in enumerate(utilisateurs):
		if name == message[1]:
		  utilisateurs.pop(index)
		  serv.privmsg(room,message[1] + " ne peut plus utiliser les commandes du bot")
		  serv.privmsg(message[1],"Vous n'êtes plus un modo de ce bot")
	    except :
	      pass
	  
	  if message[0] == "!start" :
	    pause = False
	    aVote = {}
	    serv.privmsg(room,"Le vote a commencé ! Pour voter, utilisez la commande '!vote pseudo' en privé ou en public ! Un message vous dira si votre vote a été pris en compte.")
	    serv.privmsg(room,"Tout changement de vote est possible jusqu'à ce que les votes soient terminés !")
	    serv.privmsg(auteur,"Vote commencé")
	    if len(choix) :
	      serv.privmsg(room,"Les choix possibles sont : " + str(choix))
	    
	  if message[0] == "!fin" or message[0] == "!end" :
	    pause = True
	    serv.privmsg(room,"Les votes sont terminés !")
	    serv.privmsg(auteur,"Vote clôturé")
	    
	  if message[0] == "!addblack" :
	    try :
	      blacklist.append(message[1])
	      serv.privmsg(room,message[1] + " ne peut plus voter")
	      serv.privmsg(message[1],"Vous êtes interdit de vote ! Fallait pas être méchant avec le père noel !")
	    except :
	      pass
	    
	  if message[0] == "!deleteblack" :
	    try :
	      for index,name in enumerate(blacklist):
		if name == message[1]:
		  blacklist.pop(index)
		  serv.privmsg(room,message[1] + " peut à nouveau voter")
		  serv.privmsg(message[1],"Vous pouvez à nouveau voter")
	    except :
	      pass
  
  #Commandes a réaliser sur le chan
  def on_pubmsg(self,serv,ev):
    auteur = irclib.nm_to_n(ev.source())
    canal = ev.target()
    message = ev.arguments()[0].split(" ")
    
    global pause
    global aVote
    global choix

    #Accessible par tout le monde sauf les clacklistés
    if pause == False :
      interdit = False
      for black in blacklist :
	if auteur == black :
	  serv.privmsg(auteur,"Je vous rappelle que vous êtes interdit de vote !")
	  interdit = True
      
      if interdit == False :
	if message[0] == "!vote" :
          if len(message) == 2 :
            if message[1] in choix:
              for reponse in choix :
                if reponse == message[1] :
                  aVote[auteur] = message[1]
                  serv.privmsg(room, auteur+" a voté pour " + message[1])
            else :
              serv.privmsg(room,"Désolé "+auteur+", la personne n'est pas dans la liste ! Utilise !list !")
          else :
            serv.privmsg(room,"Il faut m'écrire ''!vote Nom'', avec Nom issu de la liste accessible avec !list")
      
	      
	if message[0] == "!list" :
	  serv.privmsg(auteur,"Les choix possibles sont : " + str(choix))
	  
    else :
        if message[0] == "!LaurentBrayage" :
          serv.privmsg(room,"J'ai envoyé un message d'aide en privé à "+auteur+" !")
          serv.privmsg(auteur,"Pour envoyer son vote au concours, il faut attendre le lancement des votes !")
          serv.privmsg(auteur,"Une fois que le vote est commencé, il suffit de m'écrire ''!vote X'' pour voter pour X !")
          serv.privmsg(auteur,"Pour voir la liste des participants, envoyez moi ''!liste'' !")
        if message[0] in ["!vote","!list"] :
          serv.privmsg(auteur,"Merci d'attendre le début des votes avant de tenter quelque chose, je l'annoncerai sur le chat !")
    
if __name__ == "__main__":
  BotVote().start()
