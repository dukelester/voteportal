from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from elect.models import users
from django.contrib.auth.hashers import make_password
from passlib.hash import django_pbkdf2_sha256 as password_handler
import datetime
from django.core.paginator import Paginator

@api_view(['POST'])
def create_user(request):
    """
    Create User
    -----
        {
           
            fname:leon,
            lname:lishenga,
            email:leon@yahoo.com,
            msisdn:254682312,
            password:roshie,
            role: VOTER or ADMIN or CANDIDATE,
            position_id: 1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users(
                fname=request.data['fname'],
                lname=request.data['lname'], 
                email=request.data['email'],  
                password=make_password(request.data['password']), 
                role=request.data['role'], 
                status='1', 
                msisdn=request.data['msisdn'],
                position_id=request.data['position_id'],
                created_at = datetime.datetime.today(),
                updated_at= datetime.datetime.today()
            )
            user.save()
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



#update existing user    
@api_view(['POST'])
def update_user(request):    
    """
    Update user details
    -----
        {
            id:1,
            fname:leon,
            lname:lishenga,
            email:leon@yahoo.com,
            msisdn:254682312,
            password:roshie,
            role: VOTER or ADMIN or CANDIDATE,
            position_id: 1
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users.objects.get(id=request.data['id'])
            user.fname = request.data['fname']
            user.lname=request.data['lname']
            user.email=request.data['email']
            user.msisdn=request.data['msisdn'],
            user.role=request.data['role'],
            user.position_id=request.data['position_id'],
            user.updated_at=datetime.datetime.today(),
            user.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)     


#update existing user    
@api_view(['POST'])
def user_device_uid(request):    
    """
    Update user details
    -----
        {
            user_id:1,
            device_uid:aksdhjashja65546,
        }
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users.objects.get(id=request.data['user_id'])
            user.device_uid = request.data['device_uid'],
            user.save()
            success={'message':'success','status_code':200}
            return Response(success)

    except BaseException as e:

        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)     

#update existing user  password   
@api_view(['POST'])
def update_user_password(request):   
    """ 
    Update User Password
    -----
        {
            id:1,
            password:123456
        } 
    """
    try:
        if request.method == 'GET':
            snippets='success'
            return Response(snippets, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'POST':
            user = users.objects.get(id=request.data['id'])
            user.password = make_password(request.data['password'])
            user.save()
            success={
                'message':'success',
                'status_code':200,
                'data':{}
            }
            return Response(success)

    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)            



#get all existing users
@api_view(['POST'])  
def get_all_users(request):  
    """
    See all users 
    -----
        {
            page:1
            items: 5
        }
    """
    try:
        userss= users.objects.all()
        page = request.GET.get('page', request.data['page'])
        paginator = Paginator(userss, request.data['items'])
        details=[]
        for user in paginator.page(page):
            values={
                'id':user.id,
                'fname': user.fname,
                'lname': user.lname,
                'email': user.email,
                'password': user.password,
                'status': user.status,
                'msisdn': user.msisdn,
                'role': user.role,
                'position_id': user.position_id,
                'updated_at': user.updated_at
            }

            details.append(values)

        data={
            'data':details,
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


#get one particelar users details
@api_view(['POST'])  
def get_particular_user_details(request):

    """
    Get particular user details
    -----
        {
            user_id:1,
        }
    """
    try:
        if request.method == 'GET':
            success={'message':'method not allowed','status_code':401}
            return Response(success)

        elif request.method == 'POST':

            user_id=request.data['user_id']
            user=users.objects.get(id=user_id)
            details={
                'id':user.id,
                'fname': user.fname,
                'lname': user.lname,
                'email': user.email,
                'password': user.password,
                'status': user.status,
                'msisdn': user.msisdn,
                'role': user.role,
                'position_id': user.position_id,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }

            data={'data':details,'message':'success','status_code':200}

            return Response(data)
    
    except BaseException as e:
        
        error={
            'status_code':500,
            'message':'error:'+ str(e),
            'data':{}
        }
        return Response(error)   


@api_view(['DELETE'])

def delete_user(request):
    """
    remove user
    -----
        {
            id:1,
        }
    
    """
    try:
        if request.method=='DELETE':
            _id=request.data['id']
            delete=users.objects.filter(id=_id).delete()
            data={
                "data":"user deleted",
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



@api_view(['POST'])
def get_user_email_login(request):  

    """
    Update user details
    -----
        {
            email:roshie@gmail.com,
            password:roshie,
        }
    """

    try:
        user_id=request.data['email']
        user_input_pass=request.data['password']
        user=users.objects.get(email=user_id)

        if password_handler.verify(user_input_pass, user.password):
            success={
                'data':{
                    'id':user.id,
                    'fname': user.fname,
                    'lname': user.lname,
                    'email': user.email,
                    'password': user.password,
                    'status': user.status,
                    'msisdn': user.msisdn,
                    'role': user.role,
                    'position_id': user.position_id,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                    },
                'status_code':200,
            }
                
            return Response(success)

        else:
            success={
                'message':'Error',
                'status_code':500
            }
                
            return Response(success)    
    except BaseException as e :
        
        error={
            'status_code':500,
            'message':'error'+str(e),
            'data':{
               
            }
        }
        return Response(error)