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
    * `Django>=2.1.3,<2.2.0`
    * `djangorestframework>=3.9.4,<3.10.0`
    
* Modules
    * `django-mysql==2.2.0`
    * `mysqlclient==1.3.12`
    
* Linting
    * `flake8>=3.6.0,<3.7.0`

## Documentation
Please find the API Documentation on Swagger:

[Swagger API documentation](https://app.swaggerhub.com/apis-docs/CriticalNameError/pet-api/1.0.0#/)

## docker-compose
**Services:**
* pet_api:
    * djangorestframework-based REST-API-Service for managing pets model
    and providing endpoints for listing pets (GET-Request) and 
    updating existing pets by id (PUT- and PATCH-Request) running on `port 8000`
    
* db:
    * MySQL-based database-service running on `port 3306`. Provided dump is stored here 
    during docker image build using following statement in Dockerfile:
    
```bash 
COPY ./SQLModel.sql /docker-entrypoint-initdb.d/SQLModel.sql
```

## pet_api - service app structure
 <h4>core</h4>
    
* Management of models, especially pets model defined in `models.py` as following:
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
connection under path `management/commands/wait_for_db.py`

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
    
* Defining logic for interaction with stored data using PetsSerializer in `serializers.py`
 ```python
  class PetsSerializer(serializers.ModelSerializer):
    """Serializer for pets objects"""

    class Meta:
        model = Pets
        fields = ('id', 'name', 'species', 'gender', 'birthday')
        read_only_fields = ('id', )
```


   
* Definitions for endpoints using ViewSets in `views.py`
 ```python
class PetsViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    """Manage tags in the database"""
    queryset = Pets.objects.all()
    serializer_class = serializers.PetsSerializer
```
    
  
* Unit tests in `tests/test_api.py`
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
    
* Fixtures stored in `fixtures/test_fixture.json` containing provided dump for Django unit testing   

## Usage
<h4>Spin up Services</h4>
<h5>Requirement: Docker Tool such as Docker Desktop installed and running</h5>
* Clone Repo
 * In Command Line navigate to your cloned repo: `<yourPath>`
 * Start built process:
 ```bash
 <yourPath>docker-compose build
 ```
* Start Services:
 ```bash
 <yourPath>docker-compose up
```
Services `db` and `pet_api` will start, `pet_api` will wait until connection
to `db` is established
* Wait for lines in command line response:
```bash
System check identified no issues (0 silenced).
pet_api_1  | <ServerTimeStamp>
pet_api_1  | Django version 2.1.10, using settings 'pet_api.settings'
pet_api_1  | Starting development server at http://0.0.0.0:8000/
```

Services `db` and `pet_api` will start, `pet_api` will wait until connection
to `db` is established
* Wait for  following lines in command line response:
```bash
System check identified no issues (0 silenced).
pet_api_1  | <ServerTimeStamp>
pet_api_1  | Django version 2.1.10, using settings 'pet_api.settings'
pet_api_1  | Starting development server at http://0.0.0.0:8000/
```
* Check if it's working in Browser @ `http://localhost:8000/api/pets/`
* Use browser frontend to test interactively if preferred. There are two endpoints active:
    * GET on `http://localhost:8000/api/pets/`
    * GET / PUT / PATCH on `http://localhost:8000/api/pets/<pet_id>`

See provided [Swagger API documentation](https://app.swaggerhub.com/apis-docs/CriticalNameError/pet-api/1.0.0#/).


<h4>Connect to MySQL db service directly </h4>
<h5>Use MySQL Workbench or alternative</h5>
Connect to service to inspect schema / process SQL scripts with connection:
* Hostname: 127.0.0.1
* Port: 3306
* Username: root
* Password: 12345

You are up and running!
<h4>Run Unit Tests</h4>
* Run Unit Tests from `pet_logic/tests/` on provided fixture stored 
in in-memory sqlite3 test database:
Open **new Command Line Prompt** and type
 ```bash
 <yourPath>docker-compose run pet_api sh -c "python manage.py test"
```
* Response should look like this
```bash
Starting pet-api_db_1 ... done
Pets model set to "managed = True" for testing!
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.082s

OK
Destroying test database for alias 'default'...
```
There is a machanism implemented to detect testing mode in order  to set Pets model to be managed.
Otherwise migrations would not execute on sqlite test database.





