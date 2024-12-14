An attempt at comingling async-code and nonasync-code-in-a-thread in an argonomic way.

*Latest release 20241214.1*:
Doc update.

One of the difficulties in adapting non-async code for use in
an async world is that anything asynchronous needs to be turtles
all the way down: a single blocking sychornous call anywhere
in the call stack blocks the async event loop.

This module presently provides a pair of decorators for
asynchronous generators andfunctions which dispatches them in
a `Thread` and presents an async wrapper.

## <a name="afunc"></a>`afunc(*da, **dkw)`

A decorator for a synchronous function which turns it into
an asynchronous function.

The parameters are the same as for `@agen` excluding `maxsize`,
as this wraps the function in an asynchronous generator which
just yields the function result.

Example:

    @afunc
    def func(count):
        time.sleep(count)
        return count

    slept = await func(5)

## <a name="agen"></a>`agen(*da, **dkw)`

A decorator for a synchronous generator which turns it into
an asynchronous generator.

Parameters:
* `maxsize`: the size of the `Queue` used for communication,
  default `1`; this governs how greedy the generator may be
* `poll_delay`: the async delay between polls of the `Queue`
  after it was found to be empty twice in succession, default `0.25`s
* `fast_poll_delay`: the async delay between polls of the
  `Queue` after it was found to be empty the first time after the
  start or after an item was obtained

Exceptions in the generator are reraised in the synchronous generator.

Example:

    @agen
    def gen(count):
        for i in range(count):
            yield i
            time.sleep(1.0)

    async for item in gen(5):
        print(item)

# Release Log



*Release 20241214.1*:
Doc update.

*Release 20241214*:
Initial release with @agen and @afunc decorators.
