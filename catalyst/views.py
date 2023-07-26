import csv
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Data
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, DataSerializer
from rest_framework import viewsets

@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response("You Have Register Successfully", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Here, you can perform additional actions like generating tokens, etc.
        return Response("Login Successfully", status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadDataView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded.'}, status=400)
        
        if not file.name.endswith('.csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)
        
        try:
            data = []
            decoded_file = file.read().decode('utf-8')
            reader = csv.reader(decoded_file.splitlines())
            rows = list(reader)
            header = rows[0]  # Extract header row
            for row in rows[1:]:  # Skip header row
                print(header)
                # Check if the row is empty or contains only empty values
                if not any(row):
                    continue
                
                # Process each non-empty row of the CSV file
                data.append(dict(zip(header, row)))
            
            # Save the data to the Data model
            for row in data:
                try:
                    Data.objects.create(
                        Emp_id=row['Emp_id'] if row['Emp_id'] else None,
                        Name=row['Name'],
                        Domain=row['Domain'],
                        Year=row['Year'] if row['Year'] else None,
                        Industry=row['Industry'],
                        Size=row['Size'],
                        Locality=row['Locality'],
                        Country=row['Country'],
                        Url=row['Url'],
                        Current_Emp=row['Current_Emp'] if row['Current_Emp'] else None,
                        Total_Emp=row['Total_Emp'] if row['Total_Emp'] else None
                    )
                except ValueError:
                    Data.objects.create(
                        Emp_id=None,
                        Name=row['Name'],
                        Domain=row['Domain'],
                        Year=None,
                        Industry=row['Industry'],
                        Size=row['Size'],
                        Locality=row['Locality'],
                        Country=row['Country'],
                        Url=row['Url'],
                        Current_Emp=None,
                        Total_Emp=None
                    )

            return Response({'message': 'Data uploaded successfully.'})
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QueryBuilderView(APIView):
    def post(self, request):
        emp_id = request.data.get('Emp_id')
        country = request.data.get('Country')
        industry = request.data.get('Industry')
        name = request.data.get('Name')
        year = request.data.get('Year')

        queryset = Data.objects.all()

        # Apply filters based on the provided parameters
        if country:
            queryset = queryset.filter(Country=country)
        if industry:
            queryset = queryset.filter(Industry=industry)
        if name:
            queryset = queryset.filter(Name=name)
        if year:
            queryset = queryset.filter(Year=year)

        count = queryset.count()

        return Response({'count': count})


    

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class UsersView(APIView):
    def get(self, request):
        # Add your users logic here
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

