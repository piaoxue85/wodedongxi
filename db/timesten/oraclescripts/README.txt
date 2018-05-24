 Copyright (c) 1998, 2012, Oracle and/or its affiliates. All rights reserved. 

This directory contains the following Oracle SQL scripts. The scripts 
are intended to be used with SQL*Plus.

1. initCacheGlobalSchema.sql

This script is the first script to be run to set up Oracle In-Memory
Database Cache. It creates the TIMESTEN schema and TT_CACHE_ADMIN_ROLE
required for proper operation of Oracle In-Memory Database Cache. This
script requires the user to be connected to Oracle as a DBA or a
superuser with privileges to CREATE USERS, ROLES to other
users. Oracle administrator user needs to create a table space for
TIMESTEN user and run this script with this table space as an argument.


2. grantCacheAdminPrivileges.sql 

This script is the second script (after initCacheGlobalSchema.sql) to
be run to set up Oracle In-Memory Database Cache in a use case where
the Oracle DBA grants all the privileges/roles recommended by
TimesTen. We refer to this as automatic installation case. This script
does not create the cache administrator user and requires the cache administrator user
to be already created by the DBA. Once a cache administrator user is created
by the DBA or a superuser with equivalent privileges, this script is
to be run. It grants all the necessary privileges and roles on Oracle
to the cache administrator user. This script requires the user to be
connected to Oracle as a DBA or a superuser with privileges to CREATE
USERS, ROLES and grant privileges such as CONNECT, RESOURCE, EXECUTE
on DBMS_LOCK, CREATE ANY TRIGGER, CREATE ANY PROCEDURE to other users.
This script grants CONNECT, RESOURCE, EXECUTE on DBMS_LOCK, CREATE ANY 
TRIGGER, CREATE ANY PROCEDURE to the cache administrator user.

3. cacheCleanUp.sql 

It is designed to run on Oracle using sqlplus to clean all autorefresh 
objects related to a TimesTen data store when that data store is no longer
available. The script requires that the user is connected to the Oracle 
database as a cache administrator user. 

4. cacheInfo.sql 

This script assumes that user is connected to the Oracle database as cache 
admin user. It prints information for each log table corresponding to a
cached table on each TimesTen data store & host.


5. initCacheAdminSchema.sql (only for MANUAL INSTALLATION case)

This script is the second script (after initCacheGlobalSchema.sql) to
be run to set up Oracle In-Memory Database Cache in a use case where
the Oracle DBA does not want to grant privileges such as RESOURCE,
CREATE ANY TRIGGER, CREATE ANY PROCEDURE to the cache administrator
user. We refer to this as the manual installation use case (please
refer to Oracle In-Memory Database Cache documentation) as the script
manually creates all the required Cache Connect objects on Oracle
under the cache administrator user. This script does not create the cache
admin user and requires the cache administrator user to be already created by
the DBA. Once a cache administrator user is created by the DBA or a superuser
with equivalent privileges, this script is needed to be run (with
cache administrator user as an argument) in the case of manual
installation. It grants all the necessary minimum privileges and
creates the necessary objects on Oracle. This script requires the user
to be connected to Oracle as a DBA or a superuser with privileges to
CREATE USERS, ROLES and grant privileges such as CONNECT, EXECUTE on
DBMS_LOCK to other users.

NOTE: Unless absolutely necessary, we recommend the user to use
grantCacheAdminPrivileges.sql to grant all the required privileges for
cache administrator user.

6. initCacheGridSchema.sql (only for MANUAL INSTALLATION case)

This script is to be run to set up Cache Grid in the case of manual
installation (please refer to Oracle In-Memory Database Cache
documentation). This script is to be run after
initCacheAdminSchema.sql is run. This script requires the cache
administrator user name and the cache grid name as arguments. It
creates the necessary objects on Oracle for proper usage of the grid
and updates the necessary grid related tables. This script requires
the user to be connected to Oracle as a DBA or a superuser with
privileges to CREATE USERS, ROLES and grant privileges such as
CONNECT, RESOURCE, EXECUTE on DBMS_LOCK to other users.

7.  ttca_sysdbaSetupTarget.sql

Use this script to setup a target Oracle Database for use with
the TimesTen Cache Advisor (ttCacheAdvisor).

You must log in as SYSDBA before invoking this script.

This script performs the following operations:

  o  Creates the TTCA_TARGET_ROLE role that defines privileges to be
     granted to the target Oracle user.

  o  Creates or specify an Oracle directory object used for file
     operations into and out of the target database.

See the "Using the Cache Advisor" chapter in the Oracle In-Memory Database
Cache User's Guide for more information about the TimesTen Cache Advisor.

8. ttca_sysdbaSetupRepository.sql

Use this script to setup a repository Oracle database for use with
the TimesTen Cache Advisor (ttCacheAdvisor).

You must log in as SYSDBA before invoking this script.

This script performs the following operations:

  o  Creates a user that owns the objects in the repository database
     that are used to analyze the SQL workload run on the target Oracle
     database. Creates the TTCA_TS tablespace used to store these
     objects.

  o  Creates objects in the SYS schema that are required by the
     TimesTen Cache Advisor.

  o  Creates or specifies an Oracle directory object used for file
     operations into and out of the repository database.

See the "Using the Cache Advisor" chapter in the Oracle In-Memory Database
Cache User's Guide for more information about the TimesTen Cache Advisor.
