interface ChildProcessByStdio<I extends null | Writable, O extends null | Readable, E extends null | Readable>
        extends ChildProcess
    {
        stdin: I;
        stdout: O;
        stderr: E;
        readonly stdio: [
            I,
            O,
            E,
            Readable | Writable | null | undefined,
            // extra, no modification
            Readable | Writable | null | undefined, // extra, no modification
        ];
    }
    interface MessageOptions {
        keepOpen?: boolean | undefined;
    }
    type IOType = "overlapped" | "pipe" | "ignore" | "inherit";
    type StdioOptions = IOType | Array<IOType | "ipc" | Stream | number | null | undefined>;
    type SerializationType = "json" | "advanced";
    interface MessagingOptions extends Abortable {
        /**
         * Specify the kind of serialization used for sending messages between processes.
         * @default 'json'
         */
        serialization?: SerializationType | undefined;
        /**
         * The signal value to be used when the spawned process will be killed by the abort signal.
         * @default 'SIGTERM'
         */
        killSignal?: NodeJS.Signals | number | undefined;
        /**
         * In milliseconds the maximum amount of time the process is allowed to run.
         */
        timeout?: number | undefined;
    }
    interface ProcessEnvOptions {
        uid?: number | undefined;
        gid?: number | undefined;
        cwd?: string | URL | undefined;
        env?: NodeJS.ProcessEnv | undefined;
    }
    interface CommonOptions extends ProcessEnvOptions {
        /**
         * @default false
         */
        windowsHide?: boolean | undefined;
        /**
         * @default 0
         */
        timeout?: number | undefined;
    }
    interface CommonSpawnOptions extends CommonOptions, MessagingOptions, Abortable {
        argv0?: string | undefined;
        /**
         * Can be set to 'pipe', 'inherit', 'overlapped', or 'ignore', or an array of these strings.
         * If passed as an array, the first element is used for `stdin`, the second for
         * `stdout`, and the third for `stderr`. A fourth element can be used to
         * specify the `stdio` behavior beyond the standard streams. See
         * {@link ChildProcess.stdio} for more information.
         *
         * @default 'pipe'
         */
        stdio?: StdioOptions | undefined;
        shell?: boolean | string | undefined;
        windowsVerbatimArguments?: boolean | undefined;
    }
    interface SpawnOptions extends CommonSpawnOptions {
        detached?: boolean | undefined;
    }
    interface SpawnOptionsWithoutStdio extends SpawnOptions {
        stdio?: StdioPipeNamed | StdioPipe[] | undefined;
    }
    type StdioNull = "inherit" | "ignore" | Stream;
    type StdioPipeNamed = "pipe" | "overlapped";
    type StdioPipe = undefined | null | StdioPipeNamed;
    interface SpawnOptionsWithStdioTuple<
        Stdin extends StdioNull | StdioPipe,
        Stdout extends StdioNull | StdioPipe,
        Stderr extends StdioNull | StdioPipe,
    > extends SpawnOptions {
        stdio: [Stdin, Stdout, Stderr];
    }
    /**
     * The `child_process.spawn()` method spawns a new process using the given`command`, with command-line arguments in `args`. If omitted, `args` defaults
     * to an empty array.
     *
     * **If the `shell` option is enabled, do not pass unsanitized user input to this**
     * **function. Any input containing shell metacharacters may be used to trigger**
     * **arbitrary command execution.**
     *
     * A third argument may be used to specify additional options, with these defaults:
     *
     * ```js
     * const defaults = {
     *   cwd: undefined,
     *   env: process.env
     * };
     * ```
     *
     * Use `cwd` to specify the working directory from which the process is spawned.
     * If not given, the default is to inherit the current working directory. If given,
     * but the path does not exist, the child process emits an `ENOENT` error
     * and exits immediately. `ENOENT` is also emitted when the command
     * does not exist.
     *
     * Use `env` to specify environment variables that will be visible to the new
     * process, the default is `process.env`.
     *
     * `undefined` values in `env` will be ignored.
     *
     * Example of running `ls -lh /usr`, capturing `stdout`, `stderr`, and the
     * exit code:
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
     * Example: A very elaborate way to run `ps ax | grep ssh`
     *
     * ```js
     * import { spawn } from 'node:child_process';
     * const ps = spawn('ps', ['ax']);
     * const grep = spawn('grep', ['ssh']);
     *
     * ps.stdout.on('data', (data) => {
     *   grep.stdin.write(data);
     * });
     *
     * ps.stderr.on('data', (data) => {
     *   console.error(`ps stderr: ${data}`);
     * });
     *
     * ps.on('close', (code) => {
     *   if (code !== 0) {
     *     console.log(`ps process exited with code ${code}`);
     *   }
     *   grep.stdin.end();
     * });
     *
     * grep.stdout.on('data', (data) => {
     *   console.log(data.toString());
     * });
     *
     * grep.stderr.on('data', (data) => {
     *   console.error(`grep stderr: ${data}`);
     * });
     *
     * grep.on('close', (code) => {
     *   if (code !== 0) {
     *     console.log(`grep process exited with code ${code}`);
     *   }
     * });
     * ```
     *
     * Example of checking for failed `spawn`:
     *
     * ```js
     * import { spawn } from 'node:child_process';
     * const subprocess = spawn('bad_command');
     *
     * subprocess.on('error', (err) => {
     *   console.error('Failed to start subprocess.');
     * });
     * ```
     *
     * Certain platforms (macOS, Linux) will use the value of `argv[0]` for the process
     * title while others (Windows, SunOS) will use `command`.
     *
     * Node.js currently overwrites `argv[0]` with `process.execPath` on startup, so`process.argv[0]` in a Node.js child process will not match the `argv0`parameter passed to `spawn` from the parent,
     * retrieve it with the`process.argv0` property instead.
     *
     * If the `signal` option is enabled, calling `.abort()` on the corresponding`AbortController` is similar to calling `.kill()` on the child process except
     * the error passed to the callback will be an `AbortError`:
     *
     * ```js
     * import { spawn } from 'node:child_process';
     * const controller = new AbortController();
     * const { signal } = controller;
     * const grep = spawn('grep', ['ssh'], { signal });
     * grep.on('error', (err) => {
     *   // This will be called with err being an AbortError if the controller aborts
     * });
     * controller.abort(); // Stops the child process
     * ```
     * @since v0.1.90
     * @param command The command to run.
     * @param args List of string arguments.
     */
    function spawn(command: string, options?: SpawnOptionsWithoutStdio): ChildProcessWithoutNullStreams;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioPipe, StdioPipe>,
    ): ChildProcessByStdio<Writable, Readable, Readable>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioPipe, StdioNull>,
    ): ChildProcessByStdio<Writable, Readable, null>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioNull, StdioPipe>,
    ): ChildProcessByStdio<Writable, null, Readable>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioPipe, StdioPipe>,
    ): ChildProcessByStdio<null, Readable, Readable>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioNull, StdioNull>,
    ): ChildProcessByStdio<Writable, null, null>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioPipe, StdioNull>,
    ): ChildProcessByStdio<null, Readable, null>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioNull, StdioPipe>,
    ): ChildProcessByStdio<null, null, Readable>;
    function spawn(
        command: string,
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioNull, StdioNull>,
    ): ChildProcessByStdio<null, null, null>;
    function spawn(command: string, options: SpawnOptions): ChildProcess;
    // overloads of spawn with 'args'
    function spawn(
        command: string,
        args?: readonly string[],
        options?: SpawnOptionsWithoutStdio,
    ): ChildProcessWithoutNullStreams;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioPipe, StdioPipe>,
    ): ChildProcessByStdio<Writable, Readable, Readable>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioPipe, StdioNull>,
    ): ChildProcessByStdio<Writable, Readable, null>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioNull, StdioPipe>,
    ): ChildProcessByStdio<Writable, null, Readable>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioPipe, StdioPipe>,
    ): ChildProcessByStdio<null, Readable, Readable>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioPipe, StdioNull, StdioNull>,
    ): ChildProcessByStdio<Writable, null, null>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioPipe, StdioNull>,
    ): ChildProcessByStdio<null, Readable, null>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioNull, StdioPipe>,
    ): ChildProcessByStdio<null, null, Readable>;
    function spawn(
        command: string,
        args: readonly string[],
        options: SpawnOptionsWithStdioTuple<StdioNull, StdioNull, StdioNull>,
    ): ChildProcessByStdio<null, null, null>;
    function spawn(command: string, args: readonly string[], options: SpawnOptions): ChildProcess;
    interface ExecOptions extends CommonOptions {
        shell?: string | undefined;
        signal?: AbortSignal | undefined;
        maxBuffer?: number | undefined;
        killSignal?: NodeJS.Signals | number | undefined;
    }
    interface ExecOptionsWithStringEncoding extends ExecOptions {
        encoding: BufferEncoding;
    }
    interface ExecOptionsWithBufferEncoding extends ExecOptions {
        encoding: BufferEncoding | null; // specify `null`.
    }
    interface ExecException extends Error {
        cmd?: string | undefined;
        killed?: boolean | undefined;
        code?: number | undefined;
        signal?: NodeJS.Signals | undefined;
    }
    /**
     * Spawns a shell then executes the `command` within that shell, buffering any
     * generated output. The `command` string passed to the exec function is processed
     * directly by the shell and special characters (vary based on [shell](https://en.wikipedia.org/wiki/List_of_command-line_interpreters))
     * need to be dealt with accordingly:
     *
     * ```js
     * import { exec } from 'node:child_process';
     *
     * exec('"/path/to/test file/test.sh" arg1 arg2');
     * // Double quotes are used so that the space in the path is not interpreted as
     * // a delimiter of multiple arguments.
     *
     * exec('echo "The \\$HOME variable is $HOME"');
     * // The $HOME variable is escaped in the first instance, but not in the second.
     * ```
     *
     * **Never pass unsanitized user input to this function. Any input containing shell**
     * **metacharacters may be used to trigger arbitrary command execution.**
     *
     * If a `callback` function is provided, it is called with the arguments`(error, stdout, stderr)`. On success, `error` will be `null`. On error,`error` will be an instance of `Error`. The
     * `error.code` property will be
     * the exit code of the process. By convention, any exit code other than `0`indicates an error. `error.signal` will be the signal that terminated the
     * process.
     *
     * The `stdout` and `stderr` arguments passed to the callback will contain the
     * stdout and stderr output of the child process. By default, Node.js will decode
     * the output as UTF-8 and pass strings to the callback. The `encoding` option
     * can be used to specify the character encoding used to decode the stdout and
     * stderr output. If `encoding` is `'buffer'`, or an unrecognized character
     * encoding, `Buffer` objects will be passed to the callback instead.
     *
     * ```js
     * import { exec } from 'node:child_process';
     * exec('cat *.js missing_file | wc -l', (error, stdout, stderr) => {
     *   if (error) {
     *     console.error(`exec error: ${error}`);
     *     return;
     *   }
     *   console.log(`stdout: ${stdout}`);
     *   console.error(`stderr: ${stderr}`);
     * });
     * ```
     *
     * If `timeout` is greater than `0`, the parent will send the signal
     * identified by the `killSignal` property (the default is `'SIGTERM'`) if the
     * child runs longer than `timeout` milliseconds.
     *
     * Unlike the [`exec(3)`](http://man7.org/linux/man-pages/man3/exec.3.html) POSIX system call, `child_process.exec()` does not replace
     * the existing process and uses a shell to execute the command.
     *
     * If this method is invoked as its `util.promisify()` ed version, it returns
     * a `Promise` for an `Object` with `stdout` and `stderr` properties. The returned`ChildProcess` instance is attached to the `Promise` as a `child` property. In
     * case of an error (including any error resulting in an exit code other than 0), a
     * rejected promise is returned, with the same `error` object given in the
     * callback, but with two additional properties `stdout` and `stderr`.
     *
     * ```js
     * import util from 'node:util';
     * import child_process from 'node:child_process';
     * const exec = util.promisify(child_process.exec);
     *
     * async function lsExample() {
     *   const { stdout, stderr } = await exec('ls');
     *   console.log('stdout:', stdout);
     *   console.error('stderr:', stderr);
     * }
     * lsExample();
     * ```
     *
     * If the `signal` option is enabled, calling `.abort()` on the corresponding`AbortController` is similar to calling `.kill()` on the child process except
     * the error passed to the callback will be an `AbortError`:
     *
     * ```js
     * import { exec } from 'node:child_process';
     * const controller = new AbortController();
     * const { signal } = controller;
     * const child = exec('grep ssh', { signal }, (error) => {
     *   console.log(error); // an AbortError
     * });
     * controller.abort();
     * ```
     * @since v0.1.90
     * @param command The command to run, with space-separated arguments.
     * @param callback called with the output when process terminates.
     */
    function exec(
        command: string,
        callback?: (error: ExecException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    // `options` with `"buffer"` or `null` for `encoding` means stdout/stderr are definitely `Buffer`.
    function exec(
        command: string,
        options: {
            encoding: "buffer" | null;
        } & ExecOptions,
        callback?: (error: ExecException | null, stdout: Buffer, stderr: Buffer) => void,
    ): ChildProcess;
    // `options` with well known `encoding` means stdout/stderr are definitely `string`.
    function exec(
        command: string,
        options: {
            encoding: BufferEncoding;
        } & ExecOptions,
        callback?: (error: ExecException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    // `options` with an `encoding` whose type is `string` means stdout/stderr could either be `Buffer` or `string`.
    // There is no guarantee the `encoding` is unknown as `string` is a superset of `BufferEncoding`.
    function exec(
        command: string,
        options: {
            encoding: BufferEncoding;
        } & ExecOptions,
        callback?: (error: ExecException | null, stdout: string | Buffer, stderr: string | Buffer) => void,
    ): ChildProcess;
    // `options` without an `encoding` means stdout/stderr are definitely `string`.
    function exec(
        command: string,
        options: ExecOptions,
        callback?: (error: ExecException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    // fallback if nothing else matches. Worst case is always `string | Buffer`.
    function exec(
        command: string,
        options: (ObjectEncodingOptions & ExecOptions) | undefined | null,
        callback?: (error: ExecException | null, stdout: string | Buffer, stderr: string | Buffer) => void,
    ): ChildProcess;
    interface PromiseWithChild<T> extends Promise<T> {
        child: ChildProcess;
    }
    namespace exec {
        function __promisify__(command: string): PromiseWithChild<{
            stdout: string;
            stderr: string;
        }>;
        function __promisify__(
            command: string,
            options: {
                encoding: "buffer" | null;
            } & ExecOptions,
        ): PromiseWithChild<{
            stdout: Buffer;
            stderr: Buffer;
        }>;
        function __promisify__(
            command: string,
            options: {
                encoding: BufferEncoding;
            } & ExecOptions,
        ): PromiseWithChild<{
            stdout: string;
            stderr: string;
        }>;
        function __promisify__(
            command: string,
            options: ExecOptions,
        ): PromiseWithChild<{
            stdout: string;
            stderr: string;
        }>;
        function __promisify__(
            command: string,
            options?: (ObjectEncodingOptions & ExecOptions) | null,
        ): PromiseWithChild<{
            stdout: string | Buffer;
            stderr: string | Buffer;
        }>;
    }
    interface ExecFileOptions extends CommonOptions, Abortable {
        maxBuffer?: number | undefined;
        killSignal?: NodeJS.Signals | number | undefined;
        windowsVerbatimArguments?: boolean | undefined;
        shell?: boolean | string | undefined;
        signal?: AbortSignal | undefined;
    }
    interface ExecFileOptionsWithStringEncoding extends ExecFileOptions {
        encoding: BufferEncoding;
    }
    interface ExecFileOptionsWithBufferEncoding extends ExecFileOptions {
        encoding: "buffer" | null;
    }
    interface ExecFileOptionsWithOtherEncoding extends ExecFileOptions {
        encoding: BufferEncoding;
    }
    type ExecFileException =
        & Omit<ExecException, "code">
        & Omit<NodeJS.ErrnoException, "code">
        & { code?: string | number | undefined | null };
    /**
     * The `child_process.execFile()` function is similar to {@link exec} except that it does not spawn a shell by default. Rather, the specified
     * executable `file` is spawned directly as a new process making it slightly more
     * efficient than {@link exec}.
     *
     * The same options as {@link exec} are supported. Since a shell is
     * not spawned, behaviors such as I/O redirection and file globbing are not
     * supported.
     *
     * ```js
     * import { execFile } from 'node:child_process';
     * const child = execFile('node', ['--version'], (error, stdout, stderr) => {
     *   if (error) {
     *     throw error;
     *   }
     *   console.log(stdout);
     * });
     * ```
     *
     * The `stdout` and `stderr` arguments passed to the callback will contain the
     * stdout and stderr output of the child process. By default, Node.js will decode
     * the output as UTF-8 and pass strings to the callback. The `encoding` option
     * can be used to specify the character encoding used to decode the stdout and
     * stderr output. If `encoding` is `'buffer'`, or an unrecognized character
     * encoding, `Buffer` objects will be passed to the callback instead.
     *
     * If this method is invoked as its `util.promisify()` ed version, it returns
     * a `Promise` for an `Object` with `stdout` and `stderr` properties. The returned`ChildProcess` instance is attached to the `Promise` as a `child` property. In
     * case of an error (including any error resulting in an exit code other than 0), a
     * rejected promise is returned, with the same `error` object given in the
     * callback, but with two additional properties `stdout` and `stderr`.
     *
     * ```js
     * import util from 'node:util';
     * import child_process from 'node:child_process';
     * const execFile = util.promisify(child_process.execFile);
     * async function getVersion() {
     *   const { stdout } = await execFile('node', ['--version']);
     *   console.log(stdout);
     * }
     * getVersion();
     * ```
     *
     * **If the `shell` option is enabled, do not pass unsanitized user input to this**
     * **function. Any input containing shell metacharacters may be used to trigger**
     * **arbitrary command execution.**
     *
     * If the `signal` option is enabled, calling `.abort()` on the corresponding`AbortController` is similar to calling `.kill()` on the child process except
     * the error passed to the callback will be an `AbortError`:
     *
     * ```js
     * import { execFile } from 'node:child_process';
     * const controller = new AbortController();
     * const { signal } = controller;
     * const child = execFile('node', ['--version'], { signal }, (error) => {
     *   console.log(error); // an AbortError
     * });
     * controller.abort();
     * ```
     * @since v0.1.91
     * @param file The name or path of the executable file to run.
     * @param args List of string arguments.
     * @param callback Called with the output when process terminates.
     */
    function execFile(file: string): ChildProcess;
    function execFile(
        file: string,
        options: (ObjectEncodingOptions & ExecFileOptions) | undefined | null,
    ): ChildProcess;
    function execFile(file: string, args?: readonly string[] | null): ChildProcess;
    function execFile(
        file: string,
        args: readonly string[] | undefined | null,
        options: (ObjectEncodingOptions & ExecFileOptions) | undefined | null,
    ): ChildProcess;
    // no `options` definitely means stdout/stderr are `string`.
    function execFile(
        file: string,
        callback: (error: ExecFileException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    function execFile(
        file: string,
        args: readonly string[] | undefined | null,
        callback: (error: ExecFileException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    // `options` with `"buffer"` or `null` for `encoding` means stdout/stderr are definitely `Buffer`.
    function execFile(
        file: string,
        options: ExecFileOptionsWithBufferEncoding,
        callback: (error: ExecFileException | null, stdout: Buffer, stderr: Buffer) => void,
    ): ChildProcess;
    function execFile(
        file: string,
        args: readonly string[] | undefined | null,
        options: ExecFileOptionsWithBufferEncoding,
        callback: (error: ExecFileException | null, stdout: Buffer, stderr: Buffer) => void,
    ): ChildProcess;
    // `options` with well known `encoding` means stdout/stderr are definitely `string`.
    function execFile(
        file: string,
        options: ExecFileOptionsWithStringEncoding,
        callback: (error: ExecFileException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    function execFile(
        file: string,
        args: readonly string[] | undefined | null,
        options: ExecFileOptionsWithStringEncoding,
        callback: (error: ExecFileException | null, stdout: string, stderr: string) => void,
    ): ChildProcess;
    // `options` with an `encoding` whose type is `string` means stdout/stderr 