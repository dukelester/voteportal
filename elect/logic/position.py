from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elect.models import position, election, users
import datetime
from django.core.paginator import Paginator
from django.conf import settings

@api_view(['POST'])
def create_position(request):
    """
    Create Position
    -----
        {
           
            name:Secretary General,
            description: adams okode likes roshie and goretti,
            election_id: 1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            positions = position(
                name=request.data['name'],
                description=request.data['description'], 
                election_id = request.data['election_id'], 
                status='1', 
                created_at = datetime.datetime.today(),
                updated_at= datetime.datetime.today()
            )
            positions.save()
            success={
                'message':'success',
                'status_code':200
            }
            return Response(success)
            
    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
        }
        return Response(error)        



#update existing Position    
@api_view(['POST'])
def update_position(request):    
    """
    Update position details
    -----
        {
            id:1,
            name:Chairman,
            description: adams okode likes roshie and goretti,
            election_id : 1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            positions = position.objects.get(id=request.data['id'])
            positions.name = request.data['name']
            positions.description=request.data['description']
            positions.election_id = request.data['election_id']
            positions.updated_at = datetime.datetime.today()
            positions.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)    
            

#get all existing positions
@api_view(['POST'])  
def get_all_positions(request):  
    """
    See all positions 
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        positions = position.objects.all()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(positions, request.data['items'])
        details=[]
        deta = []
        for pose in paginator.page(page):
            values={
                'id':pose.id,
                'name': pose.name,
                'description': pose.description,
                'election_id': pose.election_id,
                'created_at': pose.created_at,
                'updated_at': pose.updated_at
            }

            details.append(values)

        for cats in details:
            elect=election.objects.get(id=cats['election_id'])
            val={
                'id':cats['id'],
                'name': cats['name'],
                'description': cats['description'],
                'election_name': elect.name,
                'election_description': elect.description,
                'created_at': cats['created_at'],
                'updated_at': cats['updated_at']
            }
            deta.append(val)

        data={
            'data':deta,
            'message':'success',
            'status_code':200
            }
        return Response(data)

    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)   

#get all candidates for a position
@api_view(['POST'])  
def get_all_candidates_positions(request):  
    """
    Get all candidates for a position
    -----
        {
            page:1
            items: 5,
            position_id:1
        }
    """
    try:
        
        userss = users.objects.filter(position_id=request.data['position_id'])
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(userss, request.data['items'])
        details=[]
        deta = []
        for user in paginator.page(page):
            if user.role == 'CANDIDATE':
                val={
                    'id':user.id,
                    'fname': user.fname,
                    'lname': user.lname,
                    'email': user.email,
                    'status': user.status,
                    'msisdn': user.msisdn,
                    'role': user.role,
                    'position_id': user.position_id,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                }
                deta.append(val)

        data={
            'data':deta,
            'message':'success',
            'status_code':200
            }
        return Response(data)

    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)   


#get one particular position details
@api_view(['POST'])  
def get_particular_position_details(request):

    """
    Get particular position details
    -----
        {
            id:1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            id=request.data['id']
            positions=position.objects.get(id=id)
            deta=[]
            details={
                'id':positions.id,
                'name': positions.name,
                'description': positions.description,
                'election_id':positions.election_id,
                'created_at': positions.created_at,
                'updated_at': positions.updated_at
            }

            for cats in details:
                elect=election.objects.get(id=cats['election_id'])
                val={
                    'id':cats['id'],
                    'name': cats['name'],
                    'description': cats['description'],
                    'election_name': elect.name,
                    'election_description': elect.description,
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }
                deta.append(val)

            data={'data':deta,'message':'success','status_code':200}

            return Response(data)
    
    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)   

#get all positions details for an election
@api_view(['POST'])  
def get_all_positions_for_an_election(request):

    """
    Get all positions details for an election
    -----
        {
            election_id:1,
            page: 1,
            items: 5
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            electer=request.data['election_id']
            positions=position.objects.filter(election_id=electer)
            page = request.GET.get('page', request.data['page'])
            paginator = Paginator(positions, request.data['items'])
            details=[]
            deta = []
            for pose in paginator.page(page):
                values={
                    'id':pose.id,
                    'name': pose.name,
                    'description': pose.description,
                    'election_id': pose.election_id,
                    'created_at': pose.created_at,
                    'updated_at': pose.updated_at
                }

                details.append(values)

            for cats in details:
                elect=election.objects.get(id=cats['election_id'])
                val={
                    'id':cats['id'],
                    'name': cats['name'],
                    'description': cats['description'],
                    'election_name': elect.name,
                    'election_description': elect.description,
                    'created_at': cats['created_at'],
                    'updated_at': cats['updated_at']
                }
                deta.append(val)

            data={'data':deta,'message':'success','status_code':200}

            return Response(data)
    
    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)   


@api_view(['DELETE'])
def delete_position(request):
    """
    remove position
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']
            delete=position.objects.get(id=_id).delete()
            data={
                "data":"Position deleted",
                "message":delete,
                "status_code":200
            }
            return Response(data)
        else:
            snippets={
                
                'message':"invalid request",
                "status_code":401
            }
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)  