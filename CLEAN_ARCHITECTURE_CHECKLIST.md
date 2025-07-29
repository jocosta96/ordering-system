# Clean Architecture Development Checklist

## Phase 1: Value Objects (Start Here)

### Step 1: Create Value Object File
**File Path:** `src/entities/value_objects/[object_name].py`

**What to do:**
- Create the file with your value object class
- Make it immutable with `@dataclass(frozen=True)`
- Add validation in `__post_init__`
- Add factory method `create()`
- Add `__str__` and `__repr__` methods

### Step 2: Update Value Objects __init__.py
**File Path:** `src/entities/value_objects/__init__.py`

**What to do:**
- Add import for your new value object
- Add it to the `__all__` list

## Phase 2: Entity

### Step 3: Create Entity File
**File Path:** `src/entities/[entity_name].py`

**What to do:**
- Create the entity class with `@dataclass`
- Add business logic and validation in `__post_init__`
- Add properties for computed values
- Add factory methods `create_*()`
- Add business rule methods

### Step 4: Update Entities __init__.py
**File Path:** `src/entities/__init__.py`

**What to do:**
- Add import for your new entity
- Add import for your new value objects
- Add them to the `__all__` list

## Phase 3: Application Layer

### Step 5: Create Repository Interface
**File Path:** `src/application/repositories/[entity_name]_repository.py`

**What to do:**
- Create abstract class inheriting from `ABC`
- Define abstract methods for CRUD operations
- Use your entity type in method signatures

### Step 6: Create DTOs
**File Path:** `src/application/dto/[entity_name]_dto.py`

**What to do:**
- Create request DTOs (for input data)
- Create response DTOs (for output data)
- Add `from_entity()` class method to convert entities to DTOs

### Step 7: Create Use Cases
**File Path:** `src/application/use_cases/[entity_name]_use_cases.py`

**What to do:**
- Create use case classes (Create, Read, Update, Delete, List)
- Inject repository dependencies in constructor
- Implement business logic orchestration
- Use DTOs for input/output

### Step 8: Update Application __init__.py
**File Path:** `src/application/__init__.py`

**What to do:**
- Add imports for your new use cases
- Add imports for your new repository interface
- Add imports for your new DTOs
- Add them to the `__all__` list

## Phase 4: Interface Adapters Layer

### Step 9: Create Gateway Implementation
**File Path:** `src/adapters/gateways/sql_[entity_name]_repository.py`

**What to do:**
- Create SQLAlchemy model class
- Implement your repository interface
- Inject `DatabaseInterface` dependency
- Add `_to_entity()` and `_to_model()` conversion methods

### Step 10: Create Controller
**File Path:** `src/adapters/controllers/[entity_name]_controller.py`

**What to do:**
- Create controller class
- Inject repository and presenter dependencies
- Create use case instances in constructor
- Add HTTP endpoint methods
- Handle authentication and error presentation

### Step 11: Create Routes
**File Path:** `src/adapters/routes/[entity_name]_routes.py`

**What to do:**
- Create FastAPI router
- Define Pydantic models for request/response
- Create dependency injection function
- Add route decorators with endpoints

### Step 12: Update Container
**File Path:** `src/adapters/di/container.py`

**What to do:**
- Add import for your new repository interface
- Add import for your new gateway implementation
- Add property method for your repository
- Initialize it with database dependency

### Step 13: Update Presenter
**File Path:** `src/adapters/presenters/implementations/json_presenter.py`

**What to do:**
- Add import for your new DTOs
- Add `_present_[entity_name]()` method
- Update the main `present()` method to handle your DTOs

### Step 14: Update Main App
**File Path:** `src/main.py`

**What to do:**
- Add import for your new router
- Include the router in the FastAPI app

## Phase 5: Testing

### Step 15: Test Your Implementation
**Commands to run:**
```bash
# Build and deploy
./dev/k8s/update_app.sh

# Check pod status
kubectl get pods

# Test your endpoints
curl -X POST http://localhost:8080/fastfood/api/[your-endpoint] \
  -H "Content-Type: application/json" \
  -d '{"your": "data"}'
```

## File Creation Checklist

**Phase 1 - Value Objects:**
- [ ] `src/entities/value_objects/[object_name].py`
- [ ] Update `src/entities/value_objects/__init__.py`

**Phase 2 - Entity:**
- [ ] `src/entities/[entity_name].py`
- [ ] Update `src/entities/__init__.py`

**Phase 3 - Application:**
- [ ] `src/application/repositories/[entity_name]_repository.py`
- [ ] `src/application/dto/[entity_name]_dto.py`
- [ ] `src/application/use_cases/[entity_name]_use_cases.py`
- [ ] Update `src/application/__init__.py`

**Phase 4 - Adapters:**
- [ ] `src/adapters/gateways/sql_[entity_name]_repository.py`
- [ ] `src/adapters/controllers/[entity_name]_controller.py`
- [ ] `src/adapters/routes/[entity_name]_routes.py`
- [ ] Update `src/adapters/di/container.py`
- [ ] Update `src/adapters/presenters/implementations/json_presenter.py`
- [ ] Update `src/main.py`

**Phase 5 - Testing:**
- [ ] Build and deploy
- [ ] Test endpoints

## Key Principles to Remember:

1. **Start with Value Objects** - They're the foundation
2. **Entities contain business logic** - Not just data
3. **Use Cases orchestrate** - They don't contain business rules
4. **Interfaces in Application layer** - Implementations in Adapters
5. **Dependencies point inward** - Always follow the dependency rule
6. **DTOs for data transfer** - Keep layers decoupled
7. **Presenters format output** - Controllers don't format data

## Naming Conventions:

- **Value Objects:** `Email`, `Phone`, `Address`
- **Entities:** `Customer`, `Order`, `Product`
- **Repositories:** `CustomerRepository`, `OrderRepository`
- **Use Cases:** `CustomerCreateUseCase`, `OrderReadUseCase`
- **DTOs:** `CustomerCreateRequest`, `OrderResponse`
- **Controllers:** `CustomerController`, `OrderController`
- **Routes:** `customer_router`, `order_router`
- **Files:** `customer.py`, `order_use_cases.py`, `sql_customer_repository.py`

## Import Patterns:

### Absolute Imports (Use these):
```python
from src.entities.customer import Customer
from src.application.repositories.customer_repository import CustomerRepository
from src.adapters.controllers.customer_controller import CustomerController
```

### Value Object Validation Pattern:
```python
def __post_init__(self):
    if not self._is_valid_value(self.value):
        raise ValueError(f"Invalid value: {self.value}")

@classmethod
def create(cls, value: str) -> 'YourValueObject':
    return cls(value.strip())
```

### Entity Business Rules Pattern:
```python
def __post_init__(self):
    self._validate_business_rules()

def _validate_business_rules(self):
    # Add your business rules here
    pass

@classmethod
def create_your_entity(cls, **kwargs) -> 'YourEntity':
    return cls(**kwargs)
```

### Use Case Pattern:
```python
class YourEntityCreateUseCase:
    def __init__(self, repository: YourEntityRepository):
        self.repository = repository
    
    def execute(self, request: YourEntityCreateRequest) -> YourEntityResponse:
        # Business logic orchestration
        pass
```

### Controller Pattern:
```python
class YourEntityController:
    def __init__(self, repository: YourEntityRepository, presenter: PresenterInterface):
        self.repository = repository
        self.presenter = presenter
        self.create_use_case = YourEntityCreateUseCase(repository)
    
    def create_your_entity(self, data: dict, login: str) -> dict:
        try:
            request = YourEntityCreateRequest(**data)
            result = self.create_use_case.execute(request)
            return self.presenter.present(result)
        except ValueError as e:
            error_response = self.presenter.present_error(e)
            raise HTTPException(status_code=400, detail=error_response)
```

This sequence ensures you follow Clean Architecture principles and maintain proper dependency direction! 