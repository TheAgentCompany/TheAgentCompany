FROM ghcr.io/theagentcompany/servers-owncloud:1.0.0

# Original task-author attachments, pinned by SHA-256. See provenance.md.
ADD --checksum=sha256:5fde7f7334504fdc2f5d46e6e110f0461bbba9049b1da486f32127992c435351 --chown=www-data:www-data --chmod=0644 ["https://github.com/user-attachments/files/17966152/contracts.xlsx", "/var/www/html/data/theagentcompany/files/Documents/Human Resources Team/Contracts/contracts.xlsx"]
ADD --checksum=sha256:cd1e6684d6191415a7aff0ae241befdb208f421bac20d8b3874138587426d07b --chown=www-data:www-data --chmod=0644 ["https://github.com/user-attachments/files/17966150/revenue_schedule.xlsx", "/var/www/html/data/theagentcompany/files/Documents/Human Resources Team/Contracts/revenue_schedule.xlsx"]
ADD --checksum=sha256:0d24827a7482d6b6cfea948ffa3ce9562d9da401a80275507392c7936b715214 --chown=www-data:www-data --chmod=0644 ["https://github.com/user-attachments/files/17966153/employee_contracts.xlsx", "/var/www/html/data/theagentcompany/files/Documents/Human Resources Team/Contracts/employee_contracts.xlsx"]
ADD --checksum=sha256:3bcc67667327871f3b1b1e71552bbd7b230195cd988d6bfe26586062a8580343 --chown=www-data:www-data --chmod=0644 ["https://github.com/user-attachments/assets/c78154e1-f666-48d9-a6fb-4b19a254c4d5", "/var/www/html/data/theagentcompany/files/Documents/Research/test_image.jpg"]

ADD --checksum=sha256:708c6f4b060b90f962ff24833269301469c314560a0a8a2468f694cf38a8c587 --chown=www-data:www-data --chmod=0644 ["https://github.com/user-attachments/files/17966249/category_rules.txt", "/var/www/html/data/theagentcompany/files/Documents/Financials/Expenses/category_rules.txt"]

# Update ownCloud's existing file index using its native CLI, including after container resets.
RUN su -s /bin/sh www-data -c 'php /var/www/html/occ files:scan --all'
