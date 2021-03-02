Changelog
=========

1.6.1 - October 9, 2020
-----------------------

- `Pull request #46 <https://github.com/wichert/pyramid_jwt/pull/46>`_:
  allow configurating the path for JWT cookies.
  From `surfjudge <https://github.com/surfjudge>`_


1.6.0 - July 9, 2020
--------------------

- `Pull request #27 <https://github.com/wichert/pyramid_jwt/pull/27>`_:
  add support for JWT tokens in cookies.
  From `phrfpeixoto <https://github.com/phrfpeixoto>`_

1.5.1 - May 5, 2020
-------------------

- Fix release versioning error.


1.5.0 - May 5, 2020
-------------------

- Drop official support for Python 2.7.

- Use GitHub actions for CI and automated releases.

- `Pull request #42 <https://github.com/wichert/pyramid_jwt/pull/42>`_:
  use the JSON encoder from Pyramid as default.
  From `phrfpeixoto <https://github.com/phrfpeixoto>`_

1.4.1 - August 10, 2018
-----------------------

- `Pull request #23 <https://github.com/wichert/pyramid_jwt/pull/21>`_:
  Allow specifying the audience in the app configuration, from `John Stevens II
  <https://github.com/jstevensfit>`_.


1.4 - August 9, 2018
--------------------

- `Pull request #21 <https://github.com/wichert/pyramid_jwt/pull/21>`_:
  add support for JWT aud claims, from `Luke Crooks
  <https://github.com/crooksey>`_.

1.3 - March 20, 2018
---------------------

- `Issue #20 <https://github.com/wichert/pyramid_jwt/issues/20>`_:
  Fix handling of public keys.
- `Pull request #17 <https://github.com/wichert/pyramid_jwt/pull/17>`_:
  a lot of documentation improvements from `Luke Crooks
  <https://github.com/crooksey>`_.


1.2 - May 25, 2017
------------------

- Fix a `log.warn` deprecation warning on Python 3.6.

- Documentation improvements, courtesy of `Éric Araujo <https://github.com/merwok>`_
  and `Guillermo Cruz <https://github.com/webjunkie01>`_.

- `Pull request #10 <https://github.com/wichert/pyramid_jwt/pull/10>`_
  Allow use of a custom JSON encoder.
  Submitted by `Julien Meyer <https://github.com/julienmeyer>`_.


1.1 - May 4, 2016
-----------------

- `Issue #2 <https://github.com/wichert/pyramid_jwt/issues/2>`_:
  Support setting and reading extra claims in a JWT token.

- `Pull request #4 <https://github.com/wichert/pyramid_jwt/pull/4>`_:
  Fix parsing of expiration and leeway settings from a configuration value.
  Submitted by `Daniel Kraus <https://github.com/dakra>`_.

- `Pull request #3 <https://github.com/wichert/pyramid_jwt/pull/3>`_:
  Allow overriding the expiration timestamp for a token when creating a new
  token. Submitted by `Daniel Kraus`_.


1.0 - December 17, 2015
-----------------------

- First release
