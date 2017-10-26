alohomora
=========

.. image:: https://travis-ci.com/razorpay/alohomora.svg?token=qzqszeBhnN4z5pes5mg9&branch=master
    :target: https://travis-ci.com/razorpay/alohomora

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

This is how the template file looks in our app
repository:

.. code:: j2

    # {{ alohomora_managed }}
    DB_PASSWORD      = {{ lookup('db_password') }}
    APP_ENV          = {{ env }}
    ENV_DEBUG        = {{ ENV['DEBUG'] }}
    APP_NAME         = {{ app }}

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
2. Render the template with these files and 3 extra variables: ``env``,
   ``app``, and ``ENV`` variables.

``ENV`` is same as `os.environ` inside the jinja template.

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
