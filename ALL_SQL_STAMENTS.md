# OrgChat

## All SQL Statements

### User

1. Show all users
```
select * from users;
```

2. Show all users that match a queried string
```
select * from user
where   name like '%%{query}%%' or
        email like '%%{query}%%' or
        phone_number like '%%{query}%%';
```

3. Get all information of a particular user
```
select * from user
where   ID=%(ID)s;
```

4. Insert user into user table
```
insert into user (ID, name, phone_number, email) values 
(   %(ID)s,
    %(name)s,
    %(phone_number)s,
    %(email)s
);
```

5. Get all organizations a user is registered in. Filters results using query string
```
select  organization.ID, 
                    organization.name,
                    type.name as type,
                    organization.location 
            from registration join organization join type
            where   registration.OID = organization.ID and
                    organization.type = type.ID and (
                    organization.name like '%%{query}%%' or
                    organization.location like '%%{query}%%')
                    and
                    registration.UID = '{user_id}';
```

6. `Update user
```
update user set 
    name=%(name)s,
    phone_number=%(phone_numer)s,
    email=%(email)s
where user.ID=%(id);
``` 

7. `Delete user
```
delete from user where ID=%(id)s;
```

### Type

Type refers to a category. For example "Education", "Business", "Entertainment"

1. Get all types
```
select  ID, name 
from type;
```

2. `Insert type
```
insert into type (name) values (
    %(name)s
);
```

3. `Update type
```
update type set
    name=%(name)s
where type.ID=%(id)s;
```

4. `Delete type
```
delete from type where ID=%(id)s;
```

### Organization

1. Get all organizations
```
select  organization.ID,
        organization.name,
        type.name as type,
        organization.location 
from organization join type
where organization.type = type.ID;
```

2. Get all organizations filtered by query
```
select  organization.ID, 
        organization.name,
        type.name as type,
        organization.location 
from organization join type
where   organization.type = type.ID and 
        (
            organization.name like '%%{query}%%' or
            organization.location like '%%{query}%%'
        );
```

3. See all users in an organization
```
select 	user.ID as user_id,
	    user.name as user_name,
	    user.phone_number as user_phone_number,
	    user.email as user_email

from 	user join registration join organization

where 	user.ID = registration.UID and 
        organization.id = registration.OID
        and            
        organization.ID = {organization_id};
```

4. Register a user to an organization
```
insert into registration values (%(uid)s, %(oid)s);
```

5. See all rooms in an organization
```
select 	room.ID,
        room.name,
        room.public,
        organization.name as organization
from	room join organization
where   room.organization = organization.ID and
        room.organization = {organization_id};
```

6. See all rooms in an organization that a particular user can see
```
select  room.ID,
        room.name,
        room.public,
        room.organization
from    room_user join room
where   room_user.UID='{user_id}' and
        room_user.RID=room.ID and
        room.organization={organization_id}

union

select  room.ID,
        room.name,
        room.public,
        room.organization
from    room
where   room.organization={organization_id} and
        room.public=1;
```

7. Add an organization
```
insert into organization (name, type, location) values 
(   %(name)s,
    %(type)s,
    %(location)s
);
```

8. Update an organization
```
update organization set
    name=%(name)s,
    type=%(type)s,
    location=%(location)s
where ID=%(ID);
```

9. Delete an organization
```
delete from organization where ID=%(ID)s;
```

### Registration

1. See all the registrations. ie. all the user, organization pairs
```
select 	user.ID as user_id,
        user.name as user_name,
        user.phone_number as user_phone_number,
        user.email as user_email,
        organization.ID as organization_id,
        organization.name as organization_name,
        type.name as organization_type,
        organization.location as organization_location

from 	user join registration
        join organization join type

where 	user.ID = registration.UID and 
        organization.id = registration.OID and
        organization.type = type.ID;
```

### Room

1. See all rooms
```
select 	room.ID,
        room.name,
        room.public,
        organization.name as organization
from	room join organization
where   room.organization = organization.ID;
```

2. Insert room in an organization
```
insert into room (name, public, organization) values 
(   %(name)s,
    %(public)s,
    %(organization)s
);
```

3. See all messages in a room
```
select  message.ID,
        message.message,
        message.sender,
        user.name,
        UNIX_TIMESTAMP(timestamp) as timestamp
from message join user on message.sender=user.ID
where room={room_id} order by message.ID desc;
```

4. Send a message in a room
```
insert into message (message, sender, timestamp, room) values 
(   %(message)s,
    %(sender)s,
    now(),
    %(room)s
);
```

### Room_user

1. Get all room, user pairs. ie. all users that have join a room pairs
```
select  room_user.RID,
        room_user.UID,
        user.name as user_name,
        organization.name as organization_name
from room_user join user join organization join room
where RID=room.ID and UID=user.ID and UOID=organization.ID;
```

2. User joins a room in an organization
```
insert into room_user values (%(RID)s, %(UID)s);
```

### Message

1. See all messages
```
select  message.ID,
        message.message,
        message.timestamp,
        user.name as user_name,
        room.name as room_name,
        organization.name as organization_name
from message join user join room join organization
where   message.sender = user.ID and
        message.room = room.ID and
        room.organization = organization.ID;
```

2. `Delete message
```
delete from message where ID=%(ID)s;
```