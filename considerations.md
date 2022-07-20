## Questions to have in mind

What will be the amount of tenants in our system?
How frequently do we expect to update a database scheme?
How frequently will the employees structure be updated?
Will we need to implement privacy operations (GRPD)?


# Multi tenancy

Pros
- Ease of onboarding
- Quick Mantainance

Cons
- Harder to implement
- Security


# Multi hierarchy in DB

Pros
- Slower when consulting

Cons
- Does not require complicated inserts, updates and deletes

LTree

Pros
- Faster when consulting

Cons
- Requires complicated inserts, updates and deletes

# JWT Authentication
Never make your own authentication implementation

Pros
- Better than cookies in session
- No need to store sessions at db

Cons
- Man in the middle -> impersonation
- Cannot revoke token


## Keywords

Isolation
Neighborhood noise
Monitoring
Logging
Cache
Security

# Architectural Characteristics
- Extensibility
- Consistency
- Availability
- Usability
- Observability
- Deployability
- Configurability
- Maintainability
- Resiliency
- Durability
- Security
- Scalability