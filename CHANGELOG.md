# Table Of Contents
1. [Version 0.3.0](#v030)
1. [Version 0.2.1](#v021)
1. [Version 0.2.0](#v020)
1. [Version 0.1.0](#v010)
1. [Version 0.0.8](#v008)

---

## v0.3.0

### New Features

* Allow optional override of SSL verification parameter [[PR#18]](https://github.com/jsimpso/PyFortiAPI/pull/18)

### Enhancements

None

### Bug Fixes

None

---

## v0.2.1

### New Features

None

### Enhancements

None

### Bug Fixes

* Add URL encoding of addresses to escape special characters when using the `update_firewall_address` function [[PR#16]](https://github.com/jsimpso/PyFortiAPI/pull/16)

---

## v0.2.0

### New Features

Added ability to specify custom HTTPS port [[PR#10]](https://github.com/jsimpso/PyFortiAPI/pull/10)

### Enhancements

VDOM parameter added to `does_exist` function [[PR#10]](https://github.com/jsimpso/PyFortiAPI/pull/10)

### Bug Fixes

None

---

## v0.1.0

### New Features

Added capability for policies to include ISDB references [[PR#5]](https://github.com/jsimpso/PyFortiAPI/pull/5)

### Enhancements

Filters added to GET requests [[PR#4]](https://github.com/jsimpso/PyFortiAPI/pull/4)

### Bug Fixes

None

---

## v0.0.8

### New Features

Added Changelog to track future changes

### Enhancements

None

### Bug Fixes

* Logout added to does_exist function to prevent stale connections piling up [[PR#2]](https://github.com/jsimpso/PyFortiAPI/pull/2)
