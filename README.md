#Elo From Tournaments in a Challonge Subdomain
##
This code relies on the python dateutil >= 1.5 module and the challonge 
bindings from [here](https://github.com/russ-/pychallonge). Once you install 
the challonge python bindings you need to add in my included versions of the 
python bindings.

create a config.txt file with

 * username:username
 * APIKey:apikey
 * subdomain:subdomain_name

Currently there is an error, seems to not be able to handle multi-stage 
tournaments.  

People with multiple names are a large problem, going back and making 
consistant names seem the easy course of action. 
