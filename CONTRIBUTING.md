# How to Contribute

With Dark Horizon's continuous integration functionality and rolling updates pipeline, structure is essential to maintaining a functional and healthy codebase. There are a few guidelines to keep in mind when contributing to the Dark Horizons 3 codebase.

## Developer vs Master Branches

There are two main branches for Dark Horizons 3 that are directly tied to the two live environments. 

### Developer Branch

Exists for the QA/Dev environment. Commits made here are sucked up by TeamCity's continuous integration process and applied to the QA environment immediately. This branch is backed with a MariaDB database that is isolated from local SQLLite changes.

### Master Branch

Represents that 'live' or production code that's used by the live Dark Horizons 3 codebase. Code that is merged here is not automatically sucked up by TeamCity and must be deployed manually through the TeamCity production deploy interface. This branch is backed with a MariaDB database that is isolated from local SQLLite changes.

## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free)
* Make sure you've completed Evennia's [Getting Started](https://github.com/evennia/evennia/wiki/Getting-Started)
  * A python virtualenv is necessary for development on DH3.
  * Evennia's installation is necessary.
  * evennia --init is unnecessary.
* If you are a contributor, clone the repository from Git.
  * If you are not a contributor, fork the repository.
* Create a new branch off of the Developer branch.
  * This new branch's name should be the name of the feature/system you are adding.
* Execute setup_local_database.ps1 in /tools.
  * This will create a local database with all the information that exists in schema_populate.sql.

## Making Changes

* Create a new branch off of the Developer branch.
  * This new branch's name should be the name of the feature/system you are adding.
  * Please avoid working in the master branch.
* File a pull request, or commit the branch back into Developer.
  * Please be absolutely certain that no regressions have appeared as a result of your work.
  * If world data was added, add it to sql/schema_populate.sql.
  * If an issue exists for your work, attach the issue to the commits.

## Developer Environment

As stated in Getting Started, development for DH3 at a local developer level happens with a SQLLite backed instance. This is different than how the QA and Production environments operate. The reason for this is that local experimental data and schema changes (as a result of Django ORM updates) need to be isolated from the QA environment to ensure that all developers, working on vastly different features, can work in harmony without disrupting dev environment components. 

It's important to note that if you add data that MUST exist for your module or feature or fix to work, it should be added to the schema_populate.sql file in sql/. This file is run every time updates are merged into Dark Horizons QA or Production. Because of this, it's absolutely critical that inserts follow the format of the file (in the style of INSERT IGNORE) with a specific ID assigned to that item.
