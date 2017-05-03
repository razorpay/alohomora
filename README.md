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

This project uses poet for managing dependencies.