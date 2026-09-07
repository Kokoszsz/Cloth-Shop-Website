"""One-off migration: replace plaintext passwords in the accounts table with hashes.

The accounts table originally stored passwords as plaintext. This script rewrites
each one as a salted PBKDF2 hash so that existing logins keep working after the
switch to hashed credentials.

Safe to run more than once: rows that already hold a hash are skipped.

Usage:
    python scripts/migrate_passwords.py [path/to/mydb.db]
"""
import sqlite3
import sys

from werkzeug.security import generate_password_hash

DEFAULT_DB = "Databases/mydb.db"

# Werkzeug hashes are self-describing and always start with the algorithm name.
KNOWN_HASH_PREFIXES = ("pbkdf2:", "scrypt:", "argon2")


def looks_hashed(value: str | None) -> bool:
    return bool(value) and value.startswith(KNOWN_HASH_PREFIXES)


def migrate(db_path: str) -> None:
    connection = sqlite3.connect(db_path)
    try:
        rows = connection.execute("SELECT id, name, password FROM accounts").fetchall()

        migrated = skipped = 0
        for user_id, name, password in rows:
            if looks_hashed(password):
                print(f"  skip  id={user_id} {name!r} (already hashed)")
                skipped += 1
                continue

            connection.execute(
                "UPDATE accounts SET password = ? WHERE id = ?",
                (generate_password_hash(password), user_id),
            )
            print(f"  hash  id={user_id} {name!r}")
            migrated += 1

        connection.commit()
        print(f"\nMigrated {migrated} account(s), skipped {skipped}.")
    finally:
        connection.close()


if __name__ == "__main__":
    migrate(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB)
