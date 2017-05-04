# alohomora

Razorpay's Secret Credential management system.

We don't do our own crypto. We rely on these libraries instead:

- https://github.com/singleton11/aws-credential-replacer
- https://docs.ansible.com/ansible/playbooks_lookups.html#the-credstash-lookup
- https://github.com/fugue/credstash

This is how the template file looks in our ansible repository:

```j2
DB_PASSWORD      = {{ lookup('credstash', 'birdie_beta_db_password' , region='ap-south-1') }}
```

This repo runs directly on the same template and generates the equivalent file as the output.

The steps it follows are the following:

1. Figure out the tables from which to read. All secrets are stored in either a global `credstash` table or a `env/app` table structure in dynamoDB. This is configured via the config file.
2. Once it figures out which tables to read

## What?

Alohomora is an opinionated project that relies on our conventions to intelligently guess where the secrets should be stored. If it finds a secret that it cannot find in the store, it will re-use the original value.

## How it Works?

Alohomora expects the secrets for any application to be stored in a table called `credstash-{env}-{app}`. The IAM roles for this table must be configured by you. Once you try to render a template, alohomora will do the following:

1. Read the entire table and decrypt all secrets and cache them locally.
2. Parse the template as well as the current rendered file
3. If a global secret lookup matches `{app}_{env}_key` format, read it against the local table.
4. If a global secret lookup doesn't match the above format, ignore it
5. If a local secret lookup uses the same table name, render it accordingly
6. If we face an exception in any case, use the value in (2)
7. Generate a diff report with any secrets that have been updated, and send it to a log file. The report should contain number of secrets updated, and their keys only.
8. Overwrite the file with the new one if _everything looks cool_.

This project uses poet for managing dependencies.
