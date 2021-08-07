from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elect.models import election, vote_token, users, votes, position, winner
from django.db.models import Count
import datetime
from django.core.paginator import Paginator
from django.conf import settings
import string
import random
import pytz


@api_view(['POST'])
def create_election(request):
    """
    Create election
    -----
        {
           
            name:Roshie's election,
            description: adams okode likes roshie and goretti,
            startdate : 11
            enddate: 12
            endmonth: 12
            startmonth:12
            endyear:2018
            startyear:2018
            tokentime: 24
        }
    """
    try:
        if request.method == 'GET':
            snippets = 'success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            elections = election(
                name=request.data['name'],
                description=request.data['description'],
                startdate=datetime.datetime(int(request.data['startyear']), int(request.data['startmonth']),
                                            int(request.data['startdate']), tzinfo=pytz.UTC),
                enddate=datetime.datetime(int(request.data['endyear']), int(request.data['endmonth']),
                                          int(request.data['enddate']), tzinfo=pytz.UTC),
                tokentime=request.data['tokentime'],
                status='1',
                created_at=datetime.datetime.now(tz=pytz.UTC),
                updated_at=datetime.datetime.now(tz=pytz.UTC)
            )
            elections.save()
            success = {
                'message': 'success',
                'status_code': 200
            }
            return Response(success)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
        }
        return Response(error)

    # update existing election


@api_view(['POST'])
def update_election(request):
    """
    Update election details
    -----
        {
            id:1,
            name:Roshie's election,
            description: adams okode likes roshie and goretti,
            startdate : 11
            enddate: 12
            endmonth: 12
            startmonth:12
            endyear:2018
            startyear:2018
            tokentime: 24
        }
    """
    try:
        if request.method == 'GET':
            snippets = 'success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            elections = election.objects.get(id=request.data['id'])
            elections.name = request.data['name']
            elections.description = request.data['description']
            elections.startdate = datetime.datetime(int(request.data['startyear']), int(request.data['startmonth']),
                                                    int(request.data['startdate']), tzinfo=pytz.UTC),
            elections.enddate = datetime.datetime(int(request.data['endyear']), int(request.data['endmonth']),
                                                  int(request.data['enddate']), tzinfo=pytz.UTC),
            elections.tokentime = request.data['tokentime'],
            elections.updated_at = datetime.datetime.now(tz=pytz.UTC)
            elections.save()
            success = {'message': 'success', 'status_code': 200}
            return Response(success)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # get all existing elections


@api_view(['POST'])
def get_all_elections(request):
    """
    See all elections 
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        elections = election.objects.all()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(elections, request.data['items'])
        details = []
        for elect in paginator.page(page):
            values = {
                'id': elect.id,
                'name': elect.name,
                'description': elect.description,
                'startdate': elect.startdate,
                'enddate': elect.enddate,
                'tokentime': elect.tokentime,
                'created_at': elect.created_at,
                'updated_at': elect.updated_at
            }

            details.append(values)

        data = {
            'data': details,
            'message': 'success',
            'status_code': 200
        }
        return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # get one particelar election details


@api_view(['POST'])
def get_particular_election_details(request):
    """
    Get particular election details
    -----
        {
            id:1,
        }
    """
    try:
        if request.method == 'GET':
            success = {'message': 'method not allowed', 'status_code': 401}
            return Response(success)

        elif request.method == 'POST':

            id = request.data['id']
            elect = election.objects.get(id=id)
            details = {
                'id': elect.id,
                'name': elect.name,
                'description': elect.description,
                'startdate': elect.startdate,
                'enddate': elect.enddate,
                'tokentime': elect.tokentime,
                'created_at': elect.created_at,
                'updated_at': elect.updated_at
            }

            data = {'data': details, 'message': 'success', 'status_code': 200}

            return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)


@api_view(['DELETE'])
def delete_election(request):
    """
    remove election
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method == 'DELETE':
            _id = request.data['id']
            delete = election.objects.filter(id=_id).delete()
            data = {
                "data": "Election deleted",
                "message": delete,
                "status_code": 200
            }
            return Response(data)
        else:
            snippets = {

                'message': "invalid request",
                "status_code": 401
            }
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # Create vote token for voter


@api_view(['POST'])
def create_voter_token(request):
    """
    Create vote token for voter
    -----
        {
            user_id:1,
            election_id: 1
        }
    """
    try:
        if request.method == 'GET':
            success = {'message': 'method not allowed', 'status_code': 401}
            return Response(success)

        elif request.method == 'POST':

            user_id = request.data['user_id']
            user = users.objects.get(id=user_id)

            if user.role != 'ADMIN':
                size = 100
                chars = string.ascii_uppercase + string.digits
                token = ''.join(random.choice(chars) for _ in range(size))
                vote_tokens = vote_token(
                    token=token,
                    user_id=user_id,
                    election_id=request.data['election_id'],
                    status='1',
                    created_at=datetime.datetime.now(tz=pytz.UTC),
                    updated_at=datetime.datetime.now(tz=pytz.UTC)
                )
                vote_tokens.save()

                data = {'message': 'success', 'status_code': 200}

                return Response(data)

            else:
                data = {'message': 'User is not a voter', 'status_code': 500}

                return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)


@api_view(['GET'])
def create_all_voter_tokens(request):
    """
    Create vote token for all voters
    -----
    """
    try:
        if request.method == 'POST':
            success = {'message': 'method not allowed', 'status_code': 401}
            return Response(success)

        elif request.method == 'GET':
            user = users.objects.all()
            elections = election.objects.all()
            for userss in user:
                for elec in elections:
                    size = 100
                    chars = string.ascii_uppercase + string.digits
                    token = ''.join(random.choice(chars) for _ in range(size))
                    tokens = vote_token.objects.filter(user_id=userss.id)
                    tokens.delete()
                    vote_tokens = vote_token(
                        token=token,
                        user_id=userss.id,
                        election_id=elec.id,
                        status='1',
                        created_at=datetime.datetime.now(tz=pytz.UTC),
                        updated_at=datetime.datetime.now(tz=pytz.UTC)
                    )
                    vote_tokens.save()

            data = {'message': 'success', 'status_code': 200}

            return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # get all vote tokens


@api_view(['POST'])
def get_all_vote_tokens(request):
    """
    See all vote tokens 
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        tokens = vote_token.objects.all()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(tokens, request.data['items'])
        details = []
        deta = []
        da = []
        for token in paginator.page(page):
            values = {
                'id': token.id,
                'user_id': token.user_id,
                'token': token.token,
                'election_id': token.election_id,
                'status': token.status,
                'created_at': token.created_at,
                'updated_at': token.updated_at
            }

            details.append(values)

        for cats in details:
            user = users.objects.get(id=cats['user_id'])
            val = {
                'id': cats['id'],
                'fname': user.fname,
                'lname': user.lname,
                'email': user.email,
                'password': user.password,
                'status': cats['status'],
                'election_id': cats['election_id'],
                'msisdn': user.msisdn,
                'role': user.role,
                'token': cats['token'],
                'created_at': cats['created_at'],
                'updated_at': cats['updated_at']
            }
            deta.append(val)

        for ca in deta:
            elect = election.objects.get(id=ca['election_id'])
            va = {
                'id': ca['id'],
                'fname': ca['fname'],
                'lname': ca['lname'],
                'email': ca['email'],
                'password': ca['password'],
                'token_status': cats['status'],
                'msisdn': ca['msisdn'],
                'role': ca['role'],
                'token': ca['token'],
                'election_name': elect.name,
                'lection_description': elect.description,
                'token_created_at': ca['created_at'],
                'token_updated_at': ca['updated_at']
            }
            da.append(va)
        data = {
            'data': da,
            'message': 'success',
            'status_code': 200
        }
        return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # get one particular voter token details


@api_view(['POST'])
def get_particular_voter_token(request):
    """
    Get particular voter token details
    -----
        {
            user_id:1,
        }
    """
    try:
        if request.method == 'GET':
            success = {'message': 'method not allowed', 'status_code': 401}
            return Response(success)

        elif request.method == 'POST':

            id = request.data['user_id']
            token = vote_token.objects.get(user_id=id)
            data = []
            da = []
            deta = []
            details = {
                'id': token.id,
                'user_id': token.user_id,
                'token': token.token,
                'status': token.status,
                'election_id': token.election_id,
                'created_at': token.created_at,
                'updated_at': token.updated_at
            }

            data.append(details)

            for cats in data:
                user = users.objects.get(id=cats['user_id'])
                val = {
                    'id': user.id,
                    'fname': user.fname,
                    'lname': user.lname,
                    'email': user.email,
                    'password': user.password,
                    'status': user.status,
                    'msisdn': user.msisdn,
                    'role': user.role,
                    'election_id': cats['election_id'],
                    'token': cats['token'],
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }
                deta.append(val)

            for ca in deta:
                elect = election.objects.get(id=ca['election_id'])
                va = {
                    'id': ca['id'],
                    'fname': ca['fname'],
                    'lname': ca['lname'],
                    'email': ca['email'],
                    'password': ca['password'],
                    'token_status': cats['status'],
                    'msisdn': ca['msisdn'],
                    'role': ca['role'],
                    'token': cats['token'],
                    'election_name': elect.name,
                    'election_description': elect.description,
                    'token_created_at': ca['created_at'],
                    'token_updated_at': ca['updated_at']
                }
                da.append(va)
            data = {
                'data': da,
                'message': 'success',
                'status_code': 200
            }
            return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # Check if user is elligible to vote


@api_view(['POST'])
def voter_elligibility(request):
    """
    Check if user is elligible to vote
    -----
        {
            user_id:1,
            election_id:1
        }
    """
    try:
        if request.method == 'GET':
            success = {'message': 'method not allowed', 'status_code': 401}
            return Response(success)

        elif request.method == 'POST':

            id = request.data['user_id']
            token = vote_token.objects.get(id=id)
            election_id = request.data['election_id']
            elect = election.objects.get(id=election_id)
            if token is None:
                data = {
                    'message': 'User is not a voter',
                    'status_code': 500
                }
                return Response(data)

            elif token is not None:
                tokens = vote_token.objects.filter(election_id=election_id).get(id=id)
                day = datetime.datetime.now(tz=pytz.UTC) - elect.startdate
                if elect.enddate > datetime.datetime.now(tz=pytz.UTC) and day.seconds < elect.tokentime * 3600:
                    data = {
                        'message': 'success',
                        'status_code': 200
                    }
                    return Response(data)
                elif day.seconds > elect.tokentime * 3600:
                    data = {
                        'message': 'Token has expired',
                        'status_code': 500
                    }
                    return Response(data)

                elif elect.enddate < datetime.datetime.now(tz=pytz.UTC):
                    data = {
                        'message': 'Election ended',
                        'status_code': 500
                    }
                    return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # vote


@api_view(['POST'])
def vote(request):
    """
    Vote for a particular candidate
    -----
        {
            voter_id:1,
            position_id:1,
            candidate_id: 1,

        }
    """
    try:
        if request.method == 'GET':
            success = {'message': 'method not allowed', 'status_code': 401}
            return Response(success)

        elif request.method == 'POST':

            vote = votes.objects.filter(voter_id=request.data['voter_id']).filter(
                position_id=request.data['position_id']).get(candidate_id=request.data['candidate_id'])
            if vote is None:
                voter = votes(
                    voter_id=request.data['voter_id'],
                    position_id=request.data['position_id'],
                    candidate_id=request.data['candidate_id'],
                    status='1',
                    created_at=datetime.datetime.now(tz=pytz.UTC),
                    updated_at=datetime.datetime.now(tz=pytz.UTC)
                )
                voter.save()
                success = {
                    'message': 'success',
                    'status_code': 200
                }
                return Response(success)
            else:
                success = {
                    'message': 'Voter already voted',
                    'status_code': 500
                }
                return Response(success)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # get all existing votes


@api_view(['POST'])
def get_all_votes(request):
    """
    See all votes
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        vote = votes.objects.all()
        numbers = votes.objects.all().count()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(vote, request.data['items'])
        details = []
        deta = []
        for voter in paginator.page(page):
            values = {
                'id': voter.id,
                'voter_id': voter.voter_id,
                'position_id': voter.position_id,
                'candidate_id': voter.candidate_id,
                'status': voter.status,
                'created_at': voter.created_at,
                'updated_at': voter.updated_at
            }

            details.append(values)

        for cats in details:
            user = users.objects.get(id=cats['voter_id'])
            us = users.objects.get(id=cats['candidate_id'])
            positions = position.objects.get(id=cats['position_id'])
            val = {
                'id': cats['id'],
                'voter_fname': user.fname,
                'voter_lname': user.lname,
                'candidate_fname': us.fname,
                'candidate_lname': us.lname,
                'position_name': positions.name,
                'created_at': cats['created_at'],
                'updated_at': cats['updated_at']
            }

            deta.append(val)

        data = {
            'data': deta,
            'total': numbers,
            'message': 'success',
            'status_code': 200
        }
        return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # get all existing votes for candidate


@api_view(['POST'])
def get_all_votes_for_candidate(request):
    """
    See all votes for particular candidate
    -----
        {
            page:1
            items: 5
            candidate_id:1
        }
    """
    try:
        vote = votes.objects.filter(candidate_id=request.data['candidate_id'])
        numbers = votes.objects.filter(candidate_id=request.data['candidate_id']).count()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(vote, request.data['items'])
        details = []
        deta = []
        for voter in paginator.page(page):
            values = {
                'id': voter.id,
                'voter_id': voter.voter_id,
                'position_id': voter.position_id,
                'candidate_id': voter.candidate_id,
                'status': voter.status,
                'created_at': voter.created_at,
                'updated_at': voter.updated_at
            }

            details.append(values)

        for cats in details:
            user = users.objects.get(id=cats['voter_id'])
            us = users.objects.get(id=cats['candidate_id'])
            positions = position.objects.get(id=cats['position_id'])
            val = {
                'id': cats['id'],
                'voter_fname': user.fname,
                'voter_lname': user.lname,
                'candidate_fname': us.fname,
                'candidate_lname': us.lname,
                'position_name': positions.name,
                'created_at': cats['created_at'],
                'updated_at': cats['updated_at']
            }

            deta.append(val)

        data = {
            'data': deta,
            'total': numbers,
            'message': 'success',
            'status_code': 200
        }
        return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)

    # Get the winner for a particular position


@api_view(['POST'])
def winner_for_position(request):
    """
    Get the winner for a particular position
    -----
        {
            position_id:1
        }
    """
    try:
        vote = votes.objects.filter(position_id=request.data['position_id'])
        numbers = votes.objects.filter(position_id=request.data['position_id']).count()
        details = []
        deta = []
        for voter in vote:
            values = {
                'candidate_id': voter.candidate_id,
            }

            details.append(values)

        for cats in details:
            us = users.objects.get(id=cats['candidate_id'])
            total = votes.objects.filter(candidate_id=cats['candidate_id'])
            counter = votes.objects.filter(candidate_id=cats['candidate_id']).count()
            delete = winner.objects.filter(position_id=request.data['position_id'])
            for deleter in delete:
                deleter.delete()
            win = winner(
                position_id=request.data['position_id'],
                candidate_id=cats['candidate_id'],
                candidate_fname=us.fname,
                candidate_lname=us.lname,
                total=counter,
                created_at=datetime.datetime.now(tz=pytz.UTC),
                updated_at=datetime.datetime.now(tz=pytz.UTC)
            )
            win.save()

        winners = winner.objects.filter(position_id=request.data['position_id']).order_by('total')
        for results in winners:
            val = {
                'id': results.id,
                'candidate_fname': results.candidate_fname,
                'candidate_lname': results.candidate_lname,
                'total_votes': results.total,
                'created_at': results.created_at,
                'updated_at': results.updated_at
            }

            deta.append(val)

        data = {
            'data': deta,
            'total': numbers,
            'message': 'success',
            'status_code': 200
        }
        return Response(data)

    except BaseException as e:

        error = {
            'status_code': 500,
            'message': 'error:' + str(e),
            'data': {}
        }
        return Response(error)
