# Local development environment

Status: Living record (last checked 2026-11-20)

How the development machine runs the application and its tests. Steps that need a choice of installer or path are recorded here so that a rebuild of the machine repeats them. The project's own commands are in the [README](../../README.md).

## Tools

| Tool | Version | Where it lives | How it was installed |
| --- | --- | --- | --- |
| uv | 0.13.9 | `%LOCALAPPDATA%\Microsoft\WinGet\Packages\astral-sh.uv_*`, hard links in `%USERPROFILE%\bin` | `winget install --id astral-sh.uv --exact --scope user`, then hard links for `uv.exe`, `uvx.exe` and `uvw.exe` |
| Python | 3.12 | System installation, found by uv | Already present, not installed by this procedure |
| PostgreSQL | 18.7 | `%LOCALAPPDATA%\PostgreSQL\18.7-2\pgsql`, executables and DLLs hard-linked in `%USERPROFILE%\bin` | The EDB binaries archive, see below |
| PostgreSQL data | Cluster of PostgreSQL 18 | `%LOCALAPPDATA%\PostgreSQL\data-18` | `initdb`, see below |

## PostgreSQL without administrator rights

The Windows installer for PostgreSQL (`PostgreSQL.PostgreSQL.18` in winget) is an executable that installs a service and needs administrator rights. The binaries archive from EnterpriseDB runs without them:

1. Download `postgresql-18.7-2-windows-x64-binaries.zip` from `https://get.enterprisedb.com/postgresql/` and extract it to `%LOCALAPPDATA%\PostgreSQL\18.7-2`.
2. Check that `postgres.exe`, `initdb.exe`, `pg_ctl.exe` and `psql.exe` carry a valid Authenticode signature from EnterpriseDB Corporation. The archive has no published checksum to compare against.
3. Hard-link the executables and DLLs of `pgsql\bin` into `%USERPROFILE%\bin`.
4. The server finds its `share` and `lib` directories relative to the executable, so with hard-linked executables it looks in `%USERPROFILE%\share` and `%USERPROFILE%\lib`. Create directory junctions there (`New-Item -ItemType Junction`), pointing at `pgsql\share` and `pgsql\lib`. Junctions need no administrator rights. Without `lib`, the text search dictionaries (`dict_snowball`) cannot be created.
5. Initialize the cluster with SCRAM authentication, and keep the superuser password out of the repository. The password is generated, stored in the user environment variable `GUESTBOOK_DB_PASSWORD`, and given to `initdb` through a password file that is deleted afterwards. The cluster is created with `initdb -D <data directory> -U guestbook_admin -A scram-sha-256 -E UTF8 --no-locale --pwfile=<file>`.
6. Start the server with `pg_ctl -D <data directory> -l <log file> start`. The server listens on 127.0.0.1 and ::1 only, and does not run as a service, so it stops at logout.
7. Create the development database: `CREATE DATABASE guestbook ENCODING 'UTF8' TEMPLATE template0;`.

## Checks

- `postgres --version` reports 18.7.
- The `french`, `english` and `simple` text search configurations exist in the `guestbook` database.
- The test suite connects to PostgreSQL and fails on any other server, so no test runs against SQLite.
