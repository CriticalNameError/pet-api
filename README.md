# Pet API

Documentation for Pet API

## Requirements
Specify, implement and test a RESTful HTTP-Web-Service to list and update pet information. In detail your tasks are:

* Write a RESTful HTTP-Web-API specification in [Swagger](http://swagger.io/specification/)
  * API requests and responses shall be in JSON
* Store the pet data in a MySQL database
  * `SQLModel.sql` contains the schema definition and initial dump of data
* Provide an RESTful HTTP-Web-Service Service with:
  * An endpoint to list all stored pets
  * An endpoint to update one pet by its id
  * Implement those endpoints in Python 3
* Write unit / integration tests for your endpoints

## Implementation Outline
**Environment:**

* Docker Version 3

**Frameworks, modules and tools used for implementation:**


* Frameworks:
    * Django>=2.1.3,<2.2.0
    * djangorestframework>=3.9.4,<3.10.0
    
* Modules
    * django-mysql==2.2.0
    * mysqlclient==1.3.12
    
* Linting
    * flake8>=3.6.0,<3.7.0

## docker-compose
**Services:**
* pet_api:
    * djangorestframework-based REST-API-Service for managing pets model
    and providing endpoints for listing pets (GET-Request) and 
    updating existing pets by id (PUT- and PATCH-Request)
    
* db:
    * MySQL-based database-service. Provided dump is stored here 
    during docker image build using following statement in Dockerfile:
    
```bash 
COPY ./SQLModel.sql /docker-entrypoint-initdb.d/SQLModel.sql
```

## pet_api - service app structure
 <h4>core</h4>
    
* Management of models, especially pets model defined in models.py as following:
 ```python
    class Pets(models.Model):

    """Pet model to access via REST endpoint"""
    GENDER_CHOICES = (
        ('m', 'männlich'),
        ('w', 'weiblich'),
    )
    name = models.CharField(max_length=45, blank=True)
    species = models.CharField(max_length=45, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)
    birthday = models.DateField(blank=True)
```
* Providing custom management command for waiting for database 
connection under path management/commands/wait_for_db.py

```python
 def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write\
                    ("DATABASE UNAVAILABLE, try reconnect in 2 seconds...")
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS("DATABASE AVAILABLE! :-)"))
```
 <h4>pet_logic</h4>
    
* Defining logic for interaction with stored data using PetsSerializer in serializers.py 
 ```python
  class PetsSerializer(serializers.ModelSerializer):
    """Serializer for pets objects"""

    class Meta:
        model = Pets
        fields = ('id', 'name', 'species', 'gender', 'birthday')
        read_only_fields = ('id', )
```


   
* Definitions for endpoints using ViewSets in views.py
 ```python
class PetsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    """Manage tags in the database"""
    queryset = Pets.objects.all()
    serializer_class = serializers.PetsSerializer
```
    
  
* Unit tests in tests/test_api.py
 ```python
class PetsApiTests(TestCase):
    """Test pets API functionality"""

    fixtures = ['test_fixture']

    def setUp(self):
        self.client = APIClient()
        # Pets.objects.create(id=1,name='Dog', species='Dog', gender='m', birthday='2015-01-01')

    def test_listing_pets(self):
        """Test GET Request for retreiving list of pets"""
        res = self.client.get(PETS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 7)

    def test_partial_update_pets(self):
        """Test updating a pet with patch"""
        pet = sample_pet(id=1)

        payload = {'name': 'Fox', 'gender': 'w'}
        url = detail_url(pet.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        pet.refresh_from_db()
        self.assertIn(pet.name, payload['name'])
        self.assertIn(pet.gender, payload['gender'])
```    
    
    

## Packages

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)