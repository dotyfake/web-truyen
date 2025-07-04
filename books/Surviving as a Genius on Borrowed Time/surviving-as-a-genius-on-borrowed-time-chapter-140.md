/**
 * The `assert` module provides a set of assertion functions for verifying
 * invariants.
 * @see [source](https://github.com/nodejs/node/blob/v18.0.0/lib/assert.js)
 */
declare module "assert" {
    /**
     * An alias of {@link ok}.
     * @since v0.5.9
     * @param value The input that is checked for being truthy.
     */
    function assert(value: unknown, message?: string | Error): asserts value;
    namespace assert {
        /**
         * Indicates the failure of an assertion. All errors thrown by the `assert` module
         * will be instances of the `AssertionError` class.
         */
        class AssertionError extends Error {
            actual: unknown;
            expected: unknown;
            operator: string;
            generatedMessage: boolean;
            code: "ERR_ASSERTION";
            constructor(options?: {
                /** If provided, the error message is set to this value. */
                message?: string | undefined;
                /** The `actual` property on the error instance. */
                actual?: unknown | undefined;
                /** The `expected` property on the error instance. */
                expected?: unknown | undefined;
                /** The `operator` property on the error instance. */
                operator?: string | undefined;
                /** If provided, the generated stack trace omits frames before this function. */
                // eslint-disable-next-line @typescript-eslint/no-unsafe-function-type
                stackStartFn?: Function | undefined;
            });
        }
        /**
         * This feature is currently experimental and behavior might still change.
         * @since v14.2.0, v12.19.0
         * @experimental
         */
        class CallTracker {
            /**
             * The wrapper function is expected to be called exactly `exact` times. If the
             * function has not been called exactly `exact` times when `tracker.verify()` is called, then `tracker.verify()` will throw an
             * error.
             *
             * ```js
             * import assert from 'assert';
             *
             * // Creates call tracker.
             * const tracker = new assert.CallTracker();
             *
             * function func() {}
             *
             * // Returns a function that wraps func() that must be called exact times
             * // before tracker.verify().
             * const callsfunc = tracker.calls(func);
             * ```
             * @since v14.2.0, v12.19.0
             * @param [fn='A no-op function']
             * @param [exact=1]
             * @return that wraps `fn`.
             */
            calls(exact?: number): () => void;
            calls(fn: undefined, exact?: number): () => void;
            calls<Func extends (...args: any[]) => any>(fn: Func, exact?: number): Func;
            calls<Func extends (...args: any[]) => any>(fn?: Func, exact?: number): Func | (() => void);
            /**
             * Example:
             *
             * ```js
             * import assert from 'node:assert';
             *
             * const tracker = new assert.CallTracker();
             *
             * function func() {}
             * const callsfunc = tracker.calls(func);
             * callsfunc(1, 2, 3);
             *
             * assert.deepStrictEqual(tracker.getCalls(callsfunc),
             *                        [{ thisArg: this, arguments: [1, 2, 3 ] }]);
             * ```
             *
             * @since v18.8.0, v16.18.0
             * @param fn
             * @returns An Array with the calls to a tracked function.
             */
            getCalls(fn: Function): CallTrackerCall[];
            /**
             * The arrays contains information about the expected and actual number of calls of
             * the functions that have not been called the expected number of times.
             *
             * ```js
             * import assert from 'assert';
             *
             * // Creates call tracker.
             * const tracker = new assert.CallTracker();
             *
             * function func() {}
             *
             * function foo() {}
             *
             * // Returns a function that wraps func() that must be called exact times
             * // before tracker.verify().
             * const callsfunc = tracker.calls(func, 2);
             *
             * // Returns an array containing information on callsfunc()
             * tracker.report();
             * // [
             * //  {
             * //    message: 'Expected the func function to be executed 2 time(s) but was
             * //    executed 0 time(s).',
             * //    actual: 0,
             * //    expected: 2,
             * //    operator: 'func',
             * //    stack: stack trace
             * //  }
             * // ]
             * ```
             * @since v14.2.0, v12.19.0
             * @return of objects containing information about the wrapper functions returned by `calls`.
             */
            report(): CallTrackerReportInformation[];
            /**
             * Reset calls of the call tracker.
             * If a tracked function is passed as an argument, the calls will be reset for it.
             * If no arguments are passed, all tracked functions will be reset.
             *
             * ```js
             * import assert from 'node:assert';
             *
             * const tracker = new assert.CallTracker();
             *
             * function func() {}
             * const callsfunc = tracker.calls(func);
             *
             * callsfunc();
             * // Tracker was called once
             * tracker.getCalls(callsfunc).length === 1;
             *
             * tracker.reset(callsfunc);
             * tracker.getCalls(callsfunc).length === 0;
             * ```
             *
             * @since v18.8.0, v16.18.0
             * @param fn a tracked function to reset.
             */
            reset(fn?: Function): void;
            /**
             * Iterates through the list of functions passed to `tracker.calls()` and will throw an error for functions that
             * have not been called the expected number of times.
             *
             * ```js
             * import assert from 'assert';
             *
             * // Creates call tracker.
             * const tracker = new assert.CallTracker();
             *
             * function func() {}
             *
             * // Returns a function that wraps func() that must be called exact times
             * // before tracker.verify().
             * const callsfunc = tracker.calls(func, 2);
             *
             * callsfunc();
             *
             * // Will throw an error since callsfunc() was only called once.
             * tracker.verify();
             * ```
             * @since v14.2.0, v12.19.0
             */
            verify(): void;
        }
        interface CallTrackerCall {
            thisArg: object;
            arguments: unknown[];
        }
        interface CallTrackerReportInformation {
            message: string;
            /** The actual number of times the function was called. */
            actual: number;
            /** The number of times the function was expected to be called. */
            expected: number;
            /** The name of the function that is wrapped. */
            operator: string;
            /** A stack trace of the function. */
            stack: object;
        }
        type AssertPredicate = RegExp | (new() => object) | ((thrown: unknown) => boolean) | object | Error;
        /**
         * Throws an `AssertionError` with the provided error message or a default
         * error message. If the `message` parameter is an instance of an `Error` then
         * it will be thrown instead of the `AssertionError`.
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * assert.fail();
         * // AssertionError [ERR_ASSERTION]: Failed
         *
         * assert.fail('boom');
         * // AssertionError [ERR_ASSERTION]: boom
         *
         * assert.fail(new TypeError('need array'));
         * // TypeError: need array
         * ```
         *
         * Using `assert.fail()` with more than two arguments is possible but deprecated.
         * See below for further details.
         * @since v0.1.21
         * @param [message='Failed']
         */
        function fail(message?: string | Error): never;
        /** @deprecated since v10.0.0 - use fail([message]) or other assert functions instead. */
        function fail(
            actual: unknown,
            expected: unknown,
            message?: string | Error,
            operator?: string,
            // eslint-disable-next-line @typescript-eslint/no-unsafe-function-type
            stackStartFn?: Function,
        ): never;
        /**
         * Tests if `value` is truthy. It is equivalent to`assert.equal(!!value, true, message)`.
         *
         * If `value` is not truthy, an `AssertionError` is thrown with a `message`property set equal to the value of the `message` parameter. If the `message`parameter is `undefined`, a default
         * error message is assigned. If the `message`parameter is an instance of an `Error` then it will be thrown instead of the`AssertionError`.
         * If no arguments are passed in at all `message` will be set to the string:`` 'No value argument passed to `assert.ok()`' ``.
         *
         * Be aware that in the `repl` the error message will be different to the one
         * thrown in a file! See below for further details.
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * assert.ok(true);
         * // OK
         * assert.ok(1);
         * // OK
         *
         * assert.ok();
         * // AssertionError: No value argument passed to `assert.ok()`
         *
         * assert.ok(false, 'it\'s false');
         * // AssertionError: it's false
         *
         * // In the repl:
         * assert.ok(typeof 123 === 'string');
         * // AssertionError: false == true
         *
         * // In a file (e.g. test.js):
         * assert.ok(typeof 123 === 'string');
         * // AssertionError: The expression evaluated to a falsy value:
         * //
         * //   assert.ok(typeof 123 === 'string')
         *
         * assert.ok(false);
         * // AssertionError: The expression evaluated to a falsy value:
         * //
         * //   assert.ok(false)
         *
         * assert.ok(0);
         * // AssertionError: The expression evaluated to a falsy value:
         * //
         * //   assert.ok(0)
         * ```
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * // Using `assert()` works the same:
         * assert(0);
         * // AssertionError: The expression evaluated to a falsy value:
         * //
         * //   assert(0)
         * ```
         * @since v0.1.21
         */
        function ok(value: unknown, message?: string | Error): asserts value;
        /**
         * **Strict assertion mode**
         *
         * An alias of {@link strictEqual}.
         *
         * **Legacy assertion mode**
         *
         * > Stability: 3 - Legacy: Use {@link strictEqual} instead.
         *
         * Tests shallow, coercive equality between the `actual` and `expected` parameters
         * using the [`==` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Equality). `NaN` is specially handled
         * and treated as being identical if both sides are `NaN`.
         *
         * ```js
         * import assert from 'assert';
         *
         * assert.equal(1, 1);
         * // OK, 1 == 1
         * assert.equal(1, '1');
         * // OK, 1 == '1'
         * assert.equal(NaN, NaN);
         * // OK
         *
         * assert.equal(1, 2);
         * // AssertionError: 1 == 2
         * assert.equal({ a: { b: 1 } }, { a: { b: 1 } });
         * // AssertionError: { a: { b: 1 } } == { a: { b: 1 } }
         * ```
         *
         * If the values are not equal, an `AssertionError` is thrown with a `message`property set equal to the value of the `message` parameter. If the `message`parameter is undefined, a default
         * error message is assigned. If the `message`parameter is an instance of an `Error` then it will be thrown instead of the`AssertionError`.
         * @since v0.1.21
         */
        function equal(actual: unknown, expected: unknown, message?: string | Error): void;
        /**
         * **Strict assertion mode**
         *
         * An alias of {@link notStrictEqual}.
         *
         * **Legacy assertion mode**
         *
         * > Stability: 3 - Legacy: Use {@link notStrictEqual} instead.
         *
         * Tests shallow, coercive inequality with the [`!=` operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Inequality). `NaN` is
         * specially handled and treated as being identical if both sides are `NaN`.
         *
         * ```js
         * import assert from 'assert';
         *
         * assert.notEqual(1, 2);
         * // OK
         *
         * assert.notEqual(1, 1);
         * // AssertionError: 1 != 1
         *
         * assert.notEqual(1, '1');
         * // AssertionError: 1 != '1'
         * ```
         *
         * If the values are equal, an `AssertionError` is thrown with a `message`property set equal to the value of the `message` parameter. If the `message`parameter is undefined, a default error
         * message is assigned. If the `message`parameter is an instance of an `Error` then it will be thrown instead of the`AssertionError`.
         * @since v0.1.21
         */
        function notEqual(actual: unknown, expected: unknown, message?: string | Error): void;
        /**
         * **Strict assertion mode**
         *
         * An alias of {@link deepStrictEqual}.
         *
         * **Legacy assertion mode**
         *
         * > Stability: 3 - Legacy: Use {@link deepStrictEqual} instead.
         *
         * Tests for deep equality between the `actual` and `expected` parameters. Consider
         * using {@link deepStrictEqual} instead. {@link deepEqual} can have
         * surprising results.
         *
         * _Deep equality_ means that the enumerable "own" properties of child objects
         * are also recursively evaluated by the following rules.
         * @since v0.1.21
         */
        function deepEqual(actual: unknown, expected: unknown, message?: string | Error): void;
        /**
         * **Strict assertion mode**
         *
         * An alias of {@link notDeepStrictEqual}.
         *
         * **Legacy assertion mode**
         *
         * > Stability: 3 - Legacy: Use {@link notDeepStrictEqual} instead.
         *
         * Tests for any deep inequality. Opposite of {@link deepEqual}.
         *
         * ```js
         * import assert from 'assert';
         *
         * const obj1 = {
         *   a: {
         *     b: 1
         *   }
         * };
         * const obj2 = {
         *   a: {
         *     b: 2
         *   }
         * };
         * const obj3 = {
         *   a: {
         *     b: 1
         *   }
         * };
         * const obj4 = Object.create(obj1);
         *
         * assert.notDeepEqual(obj1, obj1);
         * // AssertionError: { a: { b: 1 } } notDeepEqual { a: { b: 1 } }
         *
         * assert.notDeepEqual(obj1, obj2);
         * // OK
         *
         * assert.notDeepEqual(obj1, obj3);
         * // AssertionError: { a: { b: 1 } } notDeepEqual { a: { b: 1 } }
         *
         * assert.notDeepEqual(obj1, obj4);
         * // OK
         * ```
         *
         * If the values are deeply equal, an `AssertionError` is thrown with a`message` property set equal to the value of the `message` parameter. If the`message` parameter is undefined, a default
         * error message is assigned. If the`message` parameter is an instance of an `Error` then it will be thrown
         * instead of the `AssertionError`.
         * @since v0.1.21
         */
        function notDeepEqual(actual: unknown, expected: unknown, message?: string | Error): void;
        /**
         * Tests strict equality between the `actual` and `expected` parameters as
         * determined by [`Object.is()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * assert.strictEqual(1, 2);
         * // AssertionError [ERR_ASSERTION]: Expected inputs to be strictly equal:
         * //
         * // 1 !== 2
         *
         * assert.strictEqual(1, 1);
         * // OK
         *
         * assert.strictEqual('Hello foobar', 'Hello World!');
         * // AssertionError [ERR_ASSERTION]: Expected inputs to be strictly equal:
         * // + actual - expected
         * //
         * // + 'Hello foobar'
         * // - 'Hello World!'
         * //          ^
         *
         * const apples = 1;
         * const oranges = 2;
         * assert.strictEqual(apples, oranges, `apples ${apples} !== oranges ${oranges}`);
         * // AssertionError [ERR_ASSERTION]: apples 1 !== oranges 2
         *
         * assert.strictEqual(1, '1', new TypeError('Inputs are not identical'));
         * // TypeError: Inputs are not identical
         * ```
         *
         * If the values are not strictly equal, an `AssertionError` is thrown with a`message` property set equal to the value of the `message` parameter. If the`message` parameter is undefined, a
         * default error message is assigned. If the`message` parameter is an instance of an `Error` then it will be thrown
         * instead of the `AssertionError`.
         * @since v0.1.21
         */
        function strictEqual<T>(actual: unknown, expected: T, message?: string | Error): asserts actual is T;
        /**
         * Tests strict inequality between the `actual` and `expected` parameters as
         * determined by [`Object.is()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is).
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * assert.notStrictEqual(1, 2);
         * // OK
         *
         * assert.notStrictEqual(1, 1);
         * // AssertionError [ERR_ASSERTION]: Expected "actual" to be strictly unequal to:
         * //
         * // 1
         *
         * assert.notStrictEqual(1, '1');
         * // OK
         * ```
         *
         * If the values are strictly equal, an `AssertionError` is thrown with a`message` property set equal to the value of the `message` parameter. If the`message` parameter is undefined, a
         * default error message is assigned. If the`message` parameter is an instance of an `Error` then it will be thrown
         * instead of the `AssertionError`.
         * @since v0.1.21
         */
        function notStrictEqual(actual: unknown, expected: unknown, message?: string | Error): void;
        /**
         * Tests for deep equality between the `actual` and `expected` parameters.
         * "Deep" equality means that the enumerable "own" properties of child objects
         * are recursively evaluated also by the following rules.
         * @since v1.2.0
         */
        function deepStrictEqual<T>(actual: unknown, expected: T, message?: string | Error): asserts actual is T;
        /**
         * Tests for deep strict inequality. Opposite of {@link deepStrictEqual}.
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * assert.notDeepStrictEqual({ a: 1 }, { a: '1' });
         * // OK
         * ```
         *
         * If the values are deeply and strictly equal, an `AssertionError` is thrown
         * with a `message` property set equal to the value of the `message` parameter. If
         * the `message` parameter is undefined, a default error message is assigned. If
         * the `message` parameter is an instance of an `Error` then it will be thrown
         * instead of the `AssertionError`.
         * @since v1.2.0
         */
        function notDeepStrictEqual(actual: unknown, expected: unknown, message?: string | Error): void;
        /**
         * Expects the function `fn` to throw an error.
         *
         * If specified, `error` can be a [`Class`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes),
         * [`RegExp`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions), a validation function,
         * a validation object where each property will be tested for strict deep equality,
         * or an instance of error where each property will be tested for strict deep
         * equality including the non-enumerable `message` and `name` properties. When
         * using an object, it is also possible to use a regular expression, when
         * validating against a string property. See below for examples.
         *
         * If specified, `message` will be appended to the message provided by the`AssertionError` if the `fn` call fails to throw or in case the error validation
         * fails.
         *
         * Custom validation object/error instance:
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * const err = new TypeError('Wrong value');
         * err.code = 404;
         * err.foo = 'bar';
         * err.info = {
         *   nested: true,
         *   baz: 'text'
         * };
         * err.reg = /abc/i;
         *
         * assert.throws(
         *   () => {
         *     throw err;
         *   },
         *   {
         *     name: 'TypeError',
         *     message: 'Wrong value',
         *     info: {
         *       nested: true,
         *       baz: 'text'
         *     }
         *     // Only properties on the validation object will be tested for.
         *     // Using nested objects requires all properties to be present. Otherwise
         *     // the validation is going to fail.
         *   }
         * );
         *
         * // Using regular expressions to validate error properties:
         * throws(
         *   () => {
         *     throw err;
         *   },
         *   {
         *     // The `name` and `message` properties are strings and using regular
         *     // expressions on those will match against the string. If they fail, an
         *     // error is thrown.
         *     name: /^TypeError$/,
         *     message: /Wrong/,
         *     foo: 'bar',
         *     info: {
         *       nested: true,
         *       // It is not possible to use regular expressions for nested properties!
         *       baz: 'text'
         *     },
         *     // The `reg` property contains a regular expression and only if the
         *     // validation object contains an identical regular expression, it is going
         *     // to pass.
         *     reg: /abc/i
         *   }
         * );
         *
         * // Fails due to the different `message` and `name` properties:
         * throws(
         *   () => {
         *     const otherErr = new Error('Not found');
         *     // Copy all enumerable properties from `err` to `otherErr`.
         *     for (const [key, value] of Object.entries(err)) {
         *       otherErr[key] = value;
         *     }
         *     throw otherErr;
         *   },
         *   // The error's `message` and `name` properties will also be checked when using
         *   // an error as validation object.
         *   err
         * );
         * ```
         *
         * Validate instanceof using constructor:
         *
         * ```js
         * import assert from 'assert/strict';
         *
         * assert.throws(
         *   () => {
         *     throw new Error('Wrong value');
         *   },
         *   Error
   