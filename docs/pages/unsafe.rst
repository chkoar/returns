Unsafe operations
=================

This doc describes compatibility functions and escape mechanisms
that we consider unsafe to your types and code-base.

Use them with great responsibility!


unsafe_perform_io
-----------------

Sometimes you really need to get the raw value from ``IO`` container.
For example:

.. code:: python

  def index_view(request, user_id):
      user: IO[User] = get_user(user_id)
      return render('index.html', { user: user })  # ???

In this case your web-framework will not render your user correctly.
Since it does not expect it to be wrapped inside ``IO`` containers.
And we obviously cannot ``map`` or ``bind`` this function.

What to do? Use :func:`unsafe_perform_io <returns.unsafe.unsafe_perform_io>`:

.. code::

  from returns.unsafe import unsafe_perform_io

  def index_view(request, user_id):
      user: IO[User] = get_user(user_id)
      return render('index.html', { user: unsafe_perform_io(user) })  # Ok

We need it as an escape and compatibility mechanism for our imperative shell.

It is recommended
to use `import-linter <https://github.com/seddonym/import-linter>`_
to restrict imports from ``returns.unsafe`` expect the top-level modules.

Inspired by Haskell's
`unsafePerformIO <https://hackage.haskell.org/package/base-4.12.0.0/docs/System-IO-Unsafe.html#v:unsafePerformIO>`_


API Reference
-------------

.. automodule:: returns.unsafe
   :members:
