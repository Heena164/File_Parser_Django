import csv
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Data
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer, LoginSerializer,UserSerializer

@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Here, you can perform additional actions like generating tokens, etc.
        return Response({"msg":"You have Login Successfully"}, status=status.HTTP_200_OK)
    else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)



class UploadDataView(APIView):
    def post(self, request):
        file = request.FILES.get('File')
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
                # Check if the row is empty or contains only empty values
                if not any(row):
                    continue
                
                # Process each non-empty row of the CSV file
                data.append(dict(zip(header, row)))
            
            # Save or update the data in the Data model
            for row in data:
                emp_id = row['Emp_id'] if row['Emp_id'] else None
                existing_data = Data.objects.filter(Emp_id=emp_id).first()
                if existing_data:
                    existing_data.Name = row['Name']
                    existing_data.Domain = row['Domain']
                    existing_data.Year = row['Year'] if row['Year'] else None
                    existing_data.Industry = row['Industry']
                    existing_data.Size = row['Size']
                    existing_data.Locality = row['Locality']
                    existing_data.Country = row['Country']
                    existing_data.Url = row['Url']
                    existing_data.Current_Emp = row['Current_Emp'] if row['Current_Emp'] else None
                    existing_data.Total_Emp = row['Total_Emp'] if row['Total_Emp'] else None
                    existing_data.save()
                else:
                    Data.objects.create(
                        Emp_id=emp_id,
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
            
            return Response({'message': 'Data uploaded successfully.'})
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class QueryBuilderView(APIView):
    def post(self, request):
        emp_id = request.data.get('Emp_id')
        name = request.data.get('Name')
        domain = request.data.get('Domain')
        year = request.data.get('Year')
        industry = request.data.get('Industry')
        size = request.data.get('Size')
        locality = request.data.get('Locality')
        country = request.data.get('Country')
        url = request.data.get('Url')
        current_emp = request.data.get('Current_Emp')
        total_emp = request.data.get('Total_Emp')

        filters = Q()

        # Add conditions to the Q object based on the provided parameters
        if emp_id:
            filters &= Q(Emp_id=emp_id)
        if name:
            filters &= Q(Name=name)
        if domain:
            filters &= Q(Domain=domain)
        if industry:
            filters &= Q(Industry=industry)
        if size:
            filters &= Q(Size=size)
        if locality:
            filters &= Q(Locality=locality)            
        if country:
            filters &= Q(Country=country) 
        if url:
            filters &= Q(Url=url)
        if current_emp:
            filters &= Q(Current_Emp=current_emp)
        if total_emp:
            filters &= Q(Total_Emp=total_emp)
        if year:
            filters &= Q(Year=year) & Q(Year__isnull=True)
        if year:
            filters &= Q(Year__isnull=False)
        # else:
        #     filters &= Q(Year__isnull=False) 
        


        print("Filter------------------", filters)


        queryset = Data.objects.filter(filters)
        count = queryset.count()

        return Response({'count': count})


class UsersView(APIView):
    def get(self, request):
        # Add your users logic here
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

