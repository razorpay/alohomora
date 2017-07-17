alohomora
=========

Razorpay's Secret Credential management system.

Installation
------------

alohomora is distributed via PyPi:

.. code:: shell
    pip install razorpay.alohomora

What?
-----

Alohomora is an opinionated project that relies on our conventions to
intelligently fetch secrets at run-time.

We don't do our own crypto. We rely on these libraries instead:

-  https://github.com/fugue/credstash

This is how the template file [STRIKEOUT:looks] will look in our app
repository:

.. code:: j2

    # {{ alohomora_managed }}
    DB_PASSWORD      = {{ lookup('db_password') }}

This repo runs directly on the same template and generates the
equivalent file as the output.

The steps it follows are the following:

1. Figure out the tables from which to read. All secrets are stored in a
   ``credstash-env-app`` table structure in dynamoDB.
2. Fetch all secrets from that table using credstash
3. Render the template with the secrets using jinja

How it Works?
-------------

Alohomora expects the secrets for any application to be stored in a
table called ``credstash-{env}-{app}``. The IAM roles for this table
must be configured by you. Once you try to render a template, alohomora
will do the following:

1. Read the entire table and decrypt all secrets and cache them locally.
2. Render the template with these files and 2 extra variables: ``env``,
   and ``app`` variables.
3. Generate a diff report with any secrets that have been updated, and
   send it to a log file. The report should contain number of secrets
   updated, and their keys only.
4. Overwrite the file with the new one if *everything looks cool*.

Configuration?
--------------

Alohomora is designed to be a zero-config solution.

We perform a few transforms on the arguments that are passed:

-  Change both ``app`` and ``env`` to lowercase
-  Replace ``production`` with ``prod`` in the ``env`` name
-  Ignore anything after ``-`` in the environment. So ``beta-birdie`` becomes ``beta``

Usage
-----

Please see the wiki regarding alohomora binary usage.

LICENSE
-------

``alohomora`` is released under the same license as credstash.
