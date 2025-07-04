/**
 * The `child_process` module provides the ability to spawn subprocesses in
 * a manner that is similar, but not identical, to [`popen(3)`](http://man7.org/linux/man-pages/man3/popen.3.html). This capability
 * is primarily provided by the {@link spawn} function:
 *
 * ```js
 * import { spawn } from 'node:child_process';
 * const ls = spawn('ls', ['-lh', '/usr']);
 *
 * ls.stdout.on('data', (data) => {
 *   console.log(`stdout: ${data}`);
 * });
 *
 * ls.stderr.on('data', (data) => {
 *   console.error(`stderr: ${data}`);
 * });
 *
 * ls.on('close', (code) => {
 *   console.log(`child process exited with code ${code}`);
 * });
 * ```
 *
 * By default, pipes for `stdin`, `stdout`, and `stderr` are established between
 * the parent Node.js process and the spawned subprocess. These pipes have
 * limited (and platform-specific) capacity. If the subprocess writes to
 * stdout in excess of that limit without the output being captured, the
 * subprocess blocks waiting for the pipe buffer to accept more data. This is
 * identical to the behavior of pipes in the shell. Use the `{ stdio: 'ignore' }`option if the output will not be consumed.
 *
 * The command lookup is performed using the `options.env.PATH` environment
 * variable if `env` is in the `options` object. Otherwise, `process.env.PATH` is
 * used. If `options.env` is set without `PATH`, lookup on Unix is performed
 * on a default search path search of `/usr/bin:/bin` (see your operating system's
 * manual for execvpe/execvp), on Windows the current processes environment
 * variable `PATH` is used.
 *
 * On Windows, environment variables are case-insensitive. Node.js
 * lexicographically sorts the `env` keys and uses the first one that
 * case-insensitively matches. Only first (in lexicographic order) entry will be
 * passed to the subprocess. This might lead to issues on Windows when passing
 * objects to the `env` option that have multiple variants of the same key, such as`PATH` and `Path`.
 *
 * The {@link spawn} method spawns the child process asynchronously,
 * without blocking the Node.js event loop. The {@link spawnSync} function provides equivalent functionality in a synchronous manner that blocks
 * the event loop until the spawned process either exits or is terminated.
 *
 * For convenience, the `child_process` module provides a handful of synchronous
 * and asynchronous alternatives to {@link spawn} and {@link spawnSync}. Each of these alternatives are implemented on
 * top of {@link spawn} or {@link spawnSync}.
 *
 * * {@link exec}: spawns a shell and runs a command within that
 * shell, passing the `stdout` and `stderr` to a callback function when
 * complete.
 * * {@link execFile}: similar to {@link exec} except
 * that it spawns the command directly without first spawning a shell by
 * default.
 * * {@link fork}: spawns a new Node.js process and invokes a
 * specified module with an IPC communication channel established that allows
 * sending messages between parent and child.
 * * {@link execSync}: a synchronous version of {@link exec} that will block the Node.js event loop.
 * * {@link execFileSync}: a synchronous version of {@link execFile} that will block the Node.js event loop.
 *
 * For certain use cases, such as automating shell scripts, the `synchronous counterparts` may be more convenient. In many cases, however,
 * the synchronous methods can have significant impact on performance due to
 * stalling the event loop while spawned processes complete.
 * @see [source](https://github.com/nodejs/node/blob/v18.0.0/lib/child_process.js)
 */
declare module "child_process" {
    import { ObjectEncodingOptions } from "node:fs";
    import { Abortable, EventEmitter } from "node:events";
    import * as net from "node:net";
    import { Pipe, Readable, Stream, Writable } from "node:stream";
    import { URL } from "node:url";
    type Serializable = string | object | number | boolean | bigint;
    type SendHandle = net.Socket | net.Server;
    /**
     * Instances of the `ChildProcess` represent spawned child processes.
     *
     * Instances of `ChildProcess` are not intended to be created directly. Rather,
     * use the {@link spawn}, {@link exec},{@link execFile}, or {@link fork} methods to create
     * instances of `ChildProcess`.
     * @since v2.2.0
     */
    class ChildProcess extends EventEmitter {
        /**
         * A `Writable Stream` that represents the child process's `stdin`.
         *
         * If a child process waits to read all of its input, the child will not continue
         * until this stream has been closed via `end()`.
         *
         * If the child was spawned with `stdio[0]` set to anything other than `'pipe'`,
         * then this will be `null`.
         *
         * `subprocess.stdin` is an alias for `subprocess.stdio[0]`. Both properties will
         * refer to the same value.
         *
         * The `subprocess.stdin` property can be `undefined` if the child process could
         * not be successfully spawned.
         * @since v0.1.90
         */
        stdin: Writable | null;
        /**
         * A `Readable Stream` that represents the child process's `stdout`.
         *
         * If the child was spawned with `stdio[1]` set to anything other than `'pipe'`,
         * then this will be `null`.
         *
         * `subprocess.stdout` is an alias for `subprocess.stdio[1]`. Both properties will
         * refer to the same value.
         *
         * ```js
         * import { spawn } from 'node:child_process';
         *
         * const subprocess = spawn('ls');
         *
         * subprocess.stdout.on('data', (data) => {
         *   console.log(`Received chunk ${data}`);
         * });
         * ```
         *
         * The `subprocess.stdout` property can be `null` if the child process could
         * not be successfully spawned.
         * @since v0.1.90
         */
        stdout: Readable | null;
        /**
         * A `Readable Stream` that represents the child process's `stderr`.
         *
         * If the child was spawned with `stdio[2]` set to anything other than `'pipe'`,
         * then this will be `null`.
         *
         * `subprocess.stderr` is an alias for `subprocess.stdio[2]`. Both properties will
         * refer to the same value.
         *
         * The `subprocess.stderr` property can be `null` if the child process could
         * not be successfully spawned.
         * @since v0.1.90
         */
        stderr: Readable | null;
        /**
         * The `subprocess.channel` property is a reference to the child's IPC channel. If
         * no IPC channel currently exists, this property is `undefined`.
         * @since v7.1.0
         */
        readonly channel?: Pipe | null | undefined;
        /**
         * A sparse array of pipes to the child process, corresponding with positions in
         * the `stdio` option passed to {@link spawn} that have been set
         * to the value `'pipe'`. `subprocess.stdio[0]`, `subprocess.stdio[1]`, and`subprocess.stdio[2]` are also available as `subprocess.stdin`, `subprocess.stdout`, and `subprocess.stderr`,
         * respectively.
         *
         * In the following example, only the child's fd `1` (stdout) is configured as a
         * pipe, so only the parent's `subprocess.stdio[1]` is a stream, all other values
         * in the array are `null`.
         *
         * ```js
         * import assert from 'node:assert';
         * import fs from 'node:fs';
         * import child_process from 'node:child_process';
         *
         * const subprocess = child_process.spawn('ls', {
         *   stdio: [
         *     0, // Use parent's stdin for child.
         *     'pipe', // Pipe child's stdout to parent.
         *     fs.openSync('err.out', 'w'), // Direct child's stderr to a file.
         *   ]
         * });
         *
         * assert.strictEqual(subprocess.stdio[0], null);
         * assert.strictEqual(subprocess.stdio[0], subprocess.stdin);
         *
         * assert(subprocess.stdout);
         * assert.strictEqual(subprocess.stdio[1], subprocess.stdout);
         *
         * assert.strictEqual(subprocess.stdio[2], null);
         * assert.strictEqual(subprocess.stdio[2], subprocess.stderr);
         * ```
         *
         * The `subprocess.stdio` property can be `undefined` if the child process could
         * not be successfully spawned.
         * @since v0.7.10
         */
        readonly stdio: [
            Writable | null,
            // stdin
            Readable | null,
            // stdout
            Readable | null,
            // stderr
            Readable | Writable | null | undefined,
            // extra
            Readable | Writable | null | undefined, // extra
        ];
        /**
         * The `subprocess.killed` property indicates whether the child process
         * successfully received a signal from `subprocess.kill()`. The `killed` property
         * does not indicate that the child process has been terminated.
         * @since v0.5.10
         */
        readonly killed: boolean;
        /**
         * Returns the process identifier (PID) of the child process. If the child process
         * fails to spawn due to errors, then the value is `undefined` and `error` is
         * emitted.
         *
         * ```js
         * import { spawn } from 'node:child_process';
         * const grep = spawn('grep', ['ssh']);
         *
         * console.log(`Spawned child pid: ${grep.pid}`);
         * grep.stdin.end();
         * ```
         * @since v0.1.90
         */
        readonly pid?: number | undefined;
        /**
         * The `subprocess.connected` property indicates whether it is still possible to
         * send and receive messages from a child process. When `subprocess.connected` is`false`, it is no longer possible to send or receive messages.
         * @since v0.7.2
         */
        readonly connected: boolean;
        /**
         * The `subprocess.exitCode` property indicates the exit code of the child process.
         * If the child process is still running, the field will be `null`.
         */
        readonly exitCode: number | null;
        /**
         * The `subprocess.signalCode` property indicates the signal received by
         * the child process if any, else `null`.
         */
        readonly signalCode: NodeJS.Signals | null;
        /**
         * The `subprocess.spawnargs` property represents the full list of command-line
         * arguments the child process was launched with.
         */
        readonly spawnargs: string[];
        /**
         * The `subprocess.spawnfile` property indicates the executable file name of
         * the child process that is launched.
         *
         * For {@link fork}, its value will be equal to `process.execPath`.
         * For {@link spawn}, its value will be the name of
         * the executable file.
         * For {@link exec},  its value will be the name of the shell
         * in which the child process is launched.
         */
        readonly spawnfile: string;
        /**
         * The `subprocess.kill()` method sends a signal to the child process. If no
         * argument is given, the process will be sent the `'SIGTERM'` signal. See [`signal(7)`](http://man7.org/linux/man-pages/man7/signal.7.html) for a list of available signals. This function
         * returns `true` if [`kill(2)`](http://man7.org/linux/man-pages/man2/kill.2.html) succeeds, and `false` otherwise.
         *
         * ```js
         * import { spawn } from 'node:child_process';
         * const grep = spawn('grep', ['ssh']);
         *
         * grep.on('close', (code, signal) => {
         *   console.log(
         *     `child process terminated due to receipt of signal ${signal}`);
         * });
         *
         * // Send SIGHUP to process.
         * grep.kill('SIGHUP');
         * ```
         *
         * The `ChildProcess` object may emit an `'error'` event if the signal
         * cannot be delivered. Sending a signal to a child process that has already exited
         * is not an error but may have unforeseen consequences. Specifically, if the
         * process identifier (PID) has been reassigned to another process, the signal will
         * be delivered to that process instead which can have unexpected results.
         *
         * While the function is called `kill`, the signal delivered to the child process
         * may not actually terminate the process.
         *
         * See [`kill(2)`](http://man7.org/linux/man-pages/man2/kill.2.html) for reference.
         *
         * On Windows, where POSIX signals do not exist, the `signal` argument will be
         * ignored, and the process will be killed forcefully and abruptly (similar to`'SIGKILL'`).
         * See `Signal Events` for more details.
         *
         * On Linux, child processes of child processes will not be terminated
         * when attempting to kill their parent. This is likely to happen when running a
         * new process in a shell or with the use of the `shell` option of `ChildProcess`:
         *
         * ```js
         * 'use strict';
         * import { spawn } from 'node:child_process';
         *
         * const subprocess = spawn(
         *   'sh',
         *   [
         *     '-c',
         *     `node -e "setInterval(() => {
         *       console.log(process.pid, 'is alive')
         *     }, 500);"`,
         *   ], {
         *     stdio: ['inherit', 'inherit', 'inherit']
         *   }
         * );
         *
         * setTimeout(() => {
         *   subprocess.kill(); // Does not terminate the Node.js process in the shell.
         * }, 2000);
         * ```
         * @since v0.1.90
         */
        kill(signal?: NodeJS.Signals | number): boolean;
        /**
         * Calls {@link ChildProcess.kill} with `'SIGTERM'`.
         * @since v18.18.0
         */
        [Symbol.dispose](): void;
        /**
         * When an IPC channel has been established between the parent and child (
         * i.e. when using {@link fork}), the `subprocess.send()` method can
         * be used to send messages to the child process. When the child process is a
         * Node.js instance, these messages can be received via the `'message'` event.
         *
         * The message goes through serialization and parsing. The resulting
         * message might not be the same as what is originally sent.
         *
         * For example, in the parent script:
         *
         * ```js
         * import cp from 'node:child_process';
         * const n = cp.fork(`${__dirname}/sub.js`);
         *
         * n.on('message', (m) => {
         *   console.log('PARENT got message:', m);
         * });
         *
         * // Causes the child to print: CHILD got message: { hello: 'world' }
         * n.send({ hello: 'world' });
         * ```
         *
         * And then the child script, `'sub.js'` might look like this:
         *
         * ```js
         * process.on('message', (m) => {
         *   console.log('CHILD got message:', m);
         * });
         *
         * // Causes the parent to print: PARENT got message: { foo: 'bar', baz: null }
         * process.send({ foo: 'bar', baz: NaN });
         * ```
         *
         * Child Node.js processes will have a `process.send()` method of their own
         * that allows the child to send messages back to the parent.
         *
         * There is a special case when sending a `{cmd: 'NODE_foo'}` message. Messages
         * containing a `NODE_` prefix in the `cmd` property are reserved for use within
         * Node.js core and will not be emitted in the child's `'message'` event. Rather, such messages are emitted using the`'internalMessage'` event and are consumed internally by Node.js.
         * Applications should avoid using such messages or listening for`'internalMessage'` events as it is subject to change without notice.
         *
         * The optional `sendHandle` argument that may be passed to `subprocess.send()` is
         * for passing a TCP server or socket object to the child process. The child will
         * receive the object as the second argument passed to the callback function
         * registered on the `'message'` event. Any data that is received
         * and buffered in the socket will not be sent to the child.
         *
         * The optional `callback` is a function that is invoked after the message is
         * sent but before the child may have received it. The function is called with a
         * single argument: `null` on success, or an `Error` object on failure.
         *
         * If no `callback` function is provided and the message cannot be sent, an`'error'` event will be emitted by the `ChildProcess` object. This can
         * happen, for instance, when the child process has already exited.
         *
         * `subprocess.send()` will return `false` if the channel has closed or when the
         * backlog of unsent messages exceeds a threshold that makes it unwise to send
         * more. Otherwise, the method returns `true`. The `callback` function can be
         * used to implement flow control.
         *
         * #### Example: sending a server object
         *
         * The `sendHandle` argument can be used, for instance, to pass the handle of
         * a TCP server object to the child process as illustrated in the example below:
         *
         * ```js
         * import child_process from 'node:child_process';
         * const subprocess = child_process.fork('subprocess.js');
         *
         * // Open up the server object and send the handle.
         * import net from 'node:net';
         * const server = net.createServer();
         * server.on('connection', (socket) => {
         *   socket.end('handled by parent');
         * });
         * server.listen(1337, () => {
         *   subprocess.send('server', server);
         * });
         * ```
         *
         * The child would then receive the server object as:
         *
         * ```js
         * process.on('message', (m, server) => {
         *   if (m === 'server') {
         *     server.on('connection', (socket) => {
         *       socket.end('handled by child');
         *     });
         *   }
         * });
         * ```
         *
         * Once the server is now shared between the parent and child, some connections
         * can be handled by the parent and some by the child.
         *
         * While the example above uses a server created using the `net` module, `dgram`module servers use exactly the same workflow with the exceptions of listening on
         * a `'message'` event instead of `'connection'` and using `server.bind()` instead
         * of `server.listen()`. This is, however, currently only supported on Unix
         * platforms.
         *
         * #### Example: sending a socket object
         *
         * Similarly, the `sendHandler` argument can be used to pass the handle of a
         * socket to the child process. The example below spawns two children that each
         * handle connections with "normal" or "special" priority:
         *
         * ```js
         * import { fork } from 'node:child_process';
         * const normal = fork('subprocess.js', ['normal']);
         * const special = fork('subprocess.js', ['special']);
         *
         * // Open up the server and send sockets to child. Use pauseOnConnect to prevent
         * // the sockets from being read before they are sent to the child proces
         * import net from 'node:net';
         * const server = met.createServer({ pauseOnConnect: true });
         * server.on('connection', (socket) => {
         *
         *   // If this is special priority...
         *   if (socket.remoteAddress === '74.125.127.100') {
         *     special.send('socket', socket);
         *     return;
         *   }
         *   // This is normal priority.
         *   normal.send('socket', socket);
         * });
         * server.listen(1337);
         * ```
         *
         * The `subprocess.js` would receive the socket handle as the second argument
         * passed to the event callback function:
         *
         * ```js
         * process.on('message', (m, socket) => {
         *   if (m === 'socket') {
         *     if (socket) {
         *       // Check that the client socket exists.
         *       // It is possible for the socket to be closed between the time it is
         *       // sent and the time it is received in the child process.
         *       socket.end(`Request handled with ${process.argv[2]} priority`);
         *     }
         *   }
         * });
         * ```
         *
         * Do not use `.maxConnections` on a socket that has been passed to a subprocess.
         * The parent cannot track when the socket is destroyed.
         *
         * Any `'message'` handlers in the subprocess should verify that `socket` exists,
         * as the connection may have been closed during the time it takes to send the
         * connection to the child.
         * @since v0.5.9
         * @param options The `options` argument, if present, is an object used to parameterize the sending of certain types of handles. `options` supports the following properties:
         */
        send(message: Serializable, callback?: (error: Error | null) => void): boolean;
        send(message: Serializable, sendHandle?: SendHandle, callback?: (error: Error | null) => void): boolean;
        send(
            message: Serializable,
            sendHandle?: SendHandle,
            options?: MessageOptions,
            callback?: (error: Error | null) => void,
        ): boolean;
        /**
         * Closes the IPC channel between parent and child, allowing the child to exit
         * gracefully once there are no other connections keeping it alive. After calling
         * this method the `subprocess.connected` and `process.connected` properties in
         * both the parent and child (respectively) will be set to `false`, and it will be
         * no longer possible to pass messages between the processes.
         *
         * The `'disconnect'` event will be emitted when there are no messages in the
         * process of being received. This will most often be triggered immediately after
         * calling `subprocess.disconnect()`.
         *
         * When the child process is a Node.js instance (e.g. spawned using {@link fork}), the `process.disconnect()` method can be invoked
         * within the child process to close the IPC channel as well.
         * @since v0.7.2
         */
        disconnect(): void;
        /**
         * By default, the parent will wait for the detached child to exit. To prevent the
         * parent from waiting for a given `subprocess` to exit, use the`subprocess.unref()` method. Doing so will cause the parent's event loop to not
         * include the child in its reference count, allowing the parent to exit
         * independently of the child, unless there is an established IPC channel between
         * the child and the parent.
         *
         * ```js
         * import { spawn } from 'node:child_process';
         *
         * const subprocess = spawn(process.argv[0], ['child_program.js'], {
         *   detached: true,
         *   stdio: 'ignore'
         * });
         *
         * subprocess.unref();
         * ```
         * @since v0.7.10
         */
        unref(): void;
        /**
         * Calling `subprocess.ref()` after making a call to `subprocess.unref()` will
         * restore the removed reference count for the child process, forcing the parent
         * to wait for the child to exit before exiting itself.
         *
         * ```js
         * import { spawn } from 'node:child_process';
         *
         * const subprocess = spawn(process.argv[0], ['child_program.js'], {
         *   detached: true,
         *   stdio: 'ignore'
         * });
         *
         * subprocess.unref();
         * subprocess.ref();
         * ```
         * @since v0.7.10
         */
        ref(): void;
        /**
         * events.EventEmitter
         * 1. close
         * 2. disconnect
         * 3. error
         * 4. exit
         * 5. message
         * 6. spawn
         */
        addListener(event: string, listener: (...args: any[]) => void): this;
        addListener(event: "close", listener: (code: number | null, signal: NodeJS.Signals | null) => void): this;
        addListener(event: "disconnect", listener: () => void): this;
        addListener(event: "error", listener: (err: Error) => void): this;
        addListener(event: "exit", listener: (code: number | null, signal: NodeJS.Signals | null) => void): this;
        addListener(event: "message", listener: (message: Serializable, sendHandle: SendHandle) => void): this;
        addListener(event: "spawn", listener: () => void): this;
        emit(event: string | symbol, ...args: any[]): boolean;
        emit(event: "close", code: number | null, signal: NodeJS.Signals | null): boolean;
        emit(event: "disconnect"): boolean;
        emit(event: "error", err: Error): boolean;
        emit(event: "exit", code: number | null, signal: NodeJS.Signals | null): boolean;
        emit(event: "message", message: Serializable, sendHandle: SendHandle): boolean;
        emit(event: "spawn", listener: () => void): boolean;
        on(event: string, listener: (...args: any[]) => void): this;
        on(event: "close", listener: (code: number | null, signal: NodeJS.Signals | null) => void): this;
        on(event: "disconnect", listener: () => void): this;
        on(event: "error", listener: (err: Error) => void): this;
        on(event: "exit", listener: (code: number | null, signal: NodeJS.Signals | null) => void): this;
        on(event: "message", listener: (message: Ser