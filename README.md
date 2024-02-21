# nrpe-check-password-age

Simple python nrpe plugin used to check the age of a password on linux machines.

## Options

```sh
-u username, default root
-w days since change, warning, default 90
-c days since change, critical, default 110
```