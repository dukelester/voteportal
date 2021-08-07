from django.urls import include, path
from django.contrib.auth.models import User 
from rest_framework import routers, serializers, viewsets
from elect.logic import users, election, position


urlpatterns = [
    
    #User routes
    path('users/createuser/', users.create_user),
    path('users/updateuser/', users.update_user),
    path('users/user_device_uid/', users.user_device_uid),
    path('users/deleteuser/', users.delete_user),
    path('users/getallusers/', users.get_all_users),
    path('users/email_login/', users.get_user_email_login),
    path('users/resetuserpassword/',users.update_user_password),
    path('users/getparticularuser/', users.get_particular_user_details),

    #Election routes
    path('election/createelection/', election.create_election),
    path('election/updateelection/', election.update_election),
    path('election/deleteelection/', election.delete_election),
    path('election/getallelections/', election.get_all_elections),
    path('election/getparticularelection/', election.get_particular_election_details),

    #Token routes
    path('token/createtoken/', election.create_voter_token),
    path('token/getalltokens/', election.get_all_vote_tokens),
    path('token/getparticularvotertoken/', election.get_particular_voter_token),
    path('token/allusers/', election.create_all_voter_tokens),

    #Voter routes
    path('voter/voter_elligibility/', election.voter_elligibility),
    path('voter/vote/', election.vote),
    path('voter/get_all_votes/', election.get_all_votes),
    path('voter/get_all_votes_for_candidate/', election.get_all_votes_for_candidate),
    path('voter/winner/', election.winner_for_position),

    #Position routes
    path('position/createposition/', position.create_position),
    path('position/updateposition/', position.update_position),
    path('position/deleteposition/', position.delete_position),
    path('position/getallpositions/', position.get_all_positions),
    path('position/getallcandidatesparticularposition/', position.get_all_candidates_positions),
    path('position/getparticularposition/', position.get_particular_position_details),
    path('position/getallpositionsforelection/', position.get_all_positions_for_an_election),

]