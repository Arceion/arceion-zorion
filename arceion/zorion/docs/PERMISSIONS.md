# Authorization & Permissions in Arceion-Zorion

## Overview

The Arceion-Zorion framework provides a SpringBoot-like authorization system using Django's standard permission framework with custom decorators for easy access control.

---

## Core Concepts

### 1. Users & Authentication

Every user in the system has:
- **Authentication Status**: Authenticated or Anonymous
- **User Type**: Regular user, Staff, or Superuser
- **Permissions**: Specific permissions granted directly or through groups

```python
class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)        # Staff user?
    is_superuser = models.BooleanField(default=False)    # Superuser/Admin?
    groups = ManyToManyField(Group)                      # User groups
    user_permissions = ManyToManyField(Permission)       # Direct permissions
```

### 2. Permission Format

Permissions follow Django's standard format:
```
app_label.codename
```

Examples:
- `main.view_patient` - Permission to view patients
- `main.add_patient` - Permission to create patients
- `main.change_patient` - Permission to update patients
- `main.delete_patient` - Permission to delete patients

These permissions are automatically created for each model with `default_permissions`.

---

## @Authorized Decorator

The `@Authorized` decorator (alias for `@Authorize`) provides role and permission-based access control.

### Syntax

```python
@Authorized(
    authorized: bool = False,           # Require authentication?
    staff: bool = False,                # Require staff role?
    admin: bool = False,                # Require superuser/admin role?
    permissions: list[str] | None = None  # Required permissions
)
```

### Parameters

| Parameter | Type | Default | Meaning |
|-----------|------|---------|---------|
| `authorized` | `bool` | `False` | Must user be authenticated? |
| `staff` | `bool` | `False` | Must user have staff role? |
| `admin` | `bool` | `False` | Must user be superuser/admin? |
| `permissions` | `list[str]` | `None` | Required permission codes |

### Behavior

The decorator performs checks in this order:

1. **Authentication Check** - Returns 401 Unauthorized if `authorized=True` and user not authenticated
2. **Role Check** - Raises `PermissionDenied` if role requirements not met
3. **Permission Check** - Raises `PermissionDenied` if required permissions not held

---

## Usage Examples

### 1. Public Endpoint (No Authorization)

```python
from arceion.zorion.views import API
from arceion.zorion.auth import Authorized
from arceion.zorion.views.Mapping import GetMapping

@Mapping('api/v1/public')
class V1Public(API):
    @GetMapping('/health')
    def health_check(self, request):
        """No authorization required"""
        return Return.ok({'status': 'healthy'})
```

### 2. Authenticated Users Only

```python
@GetMapping('/profile')
@Authorized(authorized=True)
def get_profile(self, request, data):
    """Any authenticated user can access"""
    return Return.ok(ProfileSerializer(request.user).data)
```

### 3. Staff Only

```python
@PostMapping('/reports')
@Authorized(authorized=True, staff=True)
def create_report(self, request, data: ReportSerializer):
    """Only staff members can create reports"""
    if not data.is_valid():
        return Return.badRequest(data.errors)
    report = self.reportService.create(data.validated_data)
    return Return.created(ReportSerializer(report).data)
```

### 4. Superuser/Admin Only

```python
@DeleteMapping('/users/<int:user_id>')
@Authorized(admin=True)
def delete_user(self, request, user_id: int):
    """Only admins can delete users"""
    user = User.objects.get(id=user_id)
    user.delete()
    return Return.ok({'message': 'User deleted'})
```

### 5. Specific Permissions

```python
@PostMapping('/')
@Authorized(authorized=True, permissions=['main.add_patient'])
def create_patient(self, request, data: PatientSerializer):
    """User must have 'add_patient' permission"""
    if not data.is_valid():
        return Return.badRequest(data.errors)
    patient = self.patientService.create(data.validated_data)
    return Return.created(PatientSerializer(patient).data)
```

### 6. Multiple Permissions (AND logic)

```python
@DeleteMapping('/studies/<int:study_id>')
@Authorized(
    authorized=True,
    permissions=['main.delete_study', 'main.view_study']
)
def delete_study(self, request, study_id: int):
    """User must have BOTH delete AND view permissions"""
    study = self.studyService.getById(study_id)
    self.studyService.delete(study_id)
    return Return.ok({'message': 'Study deleted'})
```

---

## Service Layer Pattern

Combine authorization with the Service layer for clean separation:

```python
@Mapping('api/v1/patient')
class V1Patient(API):
    patientService: PatientService = PatientService()
    
    @PostMapping('/')
    @Authorized(authorized=True, permissions=['main.view_patient'])
    def list_patients(self, request, data: FilterPatientRequest):
        """List patients with filtering"""
        if not data.is_valid():
            return Return.badRequest(data.errors)
        
        # Business logic in service layer
        patients = self.patientService.search(data.validated_data)
        
        return Return.ok(PatientResponse(patients, many=True).data)
    
    @PostMapping('/create')
    @Authorized(authorized=True, permissions=['main.add_patient'])
    def create_patient(self, request, data: PatientSerializer):
        """Create new patient"""
        if not data.is_valid():
            return Return.badRequest(data.errors)
        
        # Service handles creation logic
        patient = self.patientService.create(data.validated_data)
        
        return Return.created(PatientResponse(patient).data)
```

---

## Permission Assignment

### Option 1: Django Admin

Navigate to `/admin/` and assign permissions to users or groups.

### Option 2: Programmatically

```python
from django.contrib.auth.models import Permission, User, Group

# Assign to user
user = User.objects.get(email='user@example.com')
permission = Permission.objects.get(codename='view_patient')
user.user_permissions.add(permission)

# Assign to group
group = Group.objects.get(name='clinicians')
group.permissions.add(permission)
```

---

## Best Practices

1. **Always validate input** before processing
2. **Use least privilege** - grant minimum necessary permissions
3. **Combine with Service layer** for clean separation of concerns
4. **Use consistent permission naming** following Django conventions
5. **Handle authorization errors** gracefully

---

## See Also

- Django Permissions: https://docs.djangoproject.com/en/5.2/topics/auth/
- Service Layer: See `arceion/zorion/core/Service.py`
- Validation Patterns: See `arceion/zorion/views/API.py`

