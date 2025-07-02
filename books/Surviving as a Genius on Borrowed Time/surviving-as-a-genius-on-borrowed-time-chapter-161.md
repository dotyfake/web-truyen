/**
 * The `fs/promises` API provides asynchronous file system methods that return
 * promises.
 *
 * The promise APIs use the underlying Node.js threadpool to perform file
 * system operations off the event loop thread. These operations are not
 * synchronized or threadsafe. Care must be taken when performing multiple
 * concurrent modifications on the same file or data corruption may occur.
 * @since v10.0.0
 */
declare module "fs/promises" {
    import { Abortable } from "node:events";
    import { Stream } from "node:stream";
    import { ReadableStream } from "node:stream/web";
    import {
        BigIntStats,
        BigIntStatsFs,
        BufferEncodingOption,
        constants as fsConstants,
        CopyOptions,
        Dir,
        Dirent,
        MakeDirectoryOptions,
        Mode,
        ObjectEncodingOptions,
        OpenDirOptions,
        OpenMode,
        PathLike,
        ReadStream,
        ReadVResult,
        RmDirOptions,
        RmOptions,
        StatFsOptions,
        StatOptions,
        Stats,
        StatsFs,
        TimeLike,
        WatchEventType,
        WatchOptions,
        WriteStream,
        WriteVResult,
    } from "node:fs";
    import { Interface as ReadlineInterface } from "node:readline";

    interface FileChangeInfo<T extends string | Buffer> {
        eventType: WatchEventType;
        filename: T | null;
    }
    interface FlagAndOpenMode {
        mode?: Mode | undefined;
        flag?: OpenMode | undefined;
    }
    interface FileReadResult<T extends NodeJS.ArrayBufferView> {
        bytesRead: number;
        buffer: T;
    }
    interface FileReadOptions<T extends NodeJS.ArrayBufferView = Buffer> {
        /**
         * @default `Buffer.alloc(0xffff)`
         */
        buffer?: T;
        /**
         * @default 0
         */
        offset?: number | null;
        /**
         * @default `buffer.byteLength`
         */
        length?: number | null;
        position?: number | null;
    }
    interface CreateReadStreamOptions {
        encoding?: BufferEncoding | null | undefined;
        autoClose?: boolean | undefined;
        emitClose?: boolean | undefined;
        start?: number | undefined;
        end?: number | undefined;
        highWaterMark?: number | undefined;
    }
    interface CreateWriteStreamOptions {
        encoding?: BufferEncoding | null | undefined;
        autoClose?: boolean | undefined;
        emitClose?: boolean | undefined;
        start?: number | undefined;
        highWaterMark?: number | undefined;
    }
    interface ReadableWebStreamOptions {
        /**
         * Whether to open a normal or a `'bytes'` stream.
         * @since v18.17.0
         */
        type?: "bytes" | undefined;
    }
    // TODO: Add `EventEmitter` close
    interface FileHandle {
        /**
         * The numeric file descriptor managed by the {FileHandle} object.
         * @since v10.0.0
         */
        readonly fd: number;
        /**
         * Alias of `filehandle.writeFile()`.
         *
         * When operating on file handles, the mode cannot be changed from what it was set
         * to with `fsPromises.open()`. Therefore, this is equivalent to `filehandle.writeFile()`.
         * @since v10.0.0
         * @return Fulfills with `undefined` upon success.
         */
        appendFile(
            data: string | Uint8Array,
            options?: (ObjectEncodingOptions & Abortable) | BufferEncoding | null,
        ): Promise<void>;
        /**
         * Changes the ownership of the file. A wrapper for [`chown(2)`](http://man7.org/linux/man-pages/man2/chown.2.html).
         * @since v10.0.0
         * @param uid The file's new owner's user id.
         * @param gid The file's new group's group id.
         * @return Fulfills with `undefined` upon success.
         */
        chown(uid: number, gid: number): Promise<void>;
        /**
         * Modifies the permissions on the file. See [`chmod(2)`](http://man7.org/linux/man-pages/man2/chmod.2.html).
         * @since v10.0.0
         * @param mode the file mode bit mask.
         * @return Fulfills with `undefined` upon success.
         */
        chmod(mode: Mode): Promise<void>;
        /**
         * Unlike the 16 kb default `highWaterMark` for a `stream.Readable`, the stream
         * returned by this method has a default `highWaterMark` of 64 kb.
         *
         * `options` can include `start` and `end` values to read a range of bytes from
         * the file instead of the entire file. Both `start` and `end` are inclusive and
         * start counting at 0, allowed values are in the
         * \[0, [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)\] range. If `start` is
         * omitted or `undefined`, `filehandle.createReadStream()` reads sequentially from
         * the current file position. The `encoding` can be any one of those accepted by `Buffer`.
         *
         * If the `FileHandle` points to a character device that only supports blocking
         * reads (such as keyboard or sound card), read operations do not finish until data
         * is available. This can prevent the process from exiting and the stream from
         * closing naturally.
         *
         * By default, the stream will emit a `'close'` event after it has been
         * destroyed.  Set the `emitClose` option to `false` to change this behavior.
         *
         * ```js
         * import { open } from 'fs/promises';
         *
         * const fd = await open('/dev/input/event0');
         * // Create a stream from some character device.
         * const stream = fd.createReadStream();
         * setTimeout(() => {
         *   stream.close(); // This may not close the stream.
         *   // Artificially marking end-of-stream, as if the underlying resource had
         *   // indicated end-of-file by itself, allows the stream to close.
         *   // This does not cancel pending read operations, and if there is such an
         *   // operation, the process may still not be able to exit successfully
         *   // until it finishes.
         *   stream.push(null);
         *   stream.read(0);
         * }, 100);
         * ```
         *
         * If `autoClose` is false, then the file descriptor won't be closed, even if
         * there's an error. It is the application's responsibility to close it and make
         * sure there's no file descriptor leak. If `autoClose` is set to true (default
         * behavior), on `'error'` or `'end'` the file descriptor will be closed
         * automatically.
         *
         * An example to read the last 10 bytes of a file which is 100 bytes long:
         *
         * ```js
         * import { open } from 'fs/promises';
         *
         * const fd = await open('sample.txt');
         * fd.createReadStream({ start: 90, end: 99 });
         * ```
         * @since v16.11.0
         */
        createReadStream(options?: CreateReadStreamOptions): ReadStream;
        /**
         * `options` may also include a `start` option to allow writing data at some
         * position past the beginning of the file, allowed values are in the
         * \[0, [`Number.MAX_SAFE_INTEGER`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER)\] range. Modifying a file rather than
         * replacing it may require the `flags` `open` option to be set to `r+` rather than
         * the default `r`. The `encoding` can be any one of those accepted by `Buffer`.
         *
         * If `autoClose` is set to true (default behavior) on `'error'` or `'finish'`the file descriptor will be closed automatically. If `autoClose` is false,
         * then the file descriptor won't be closed, even if there's an error.
         * It is the application's responsibility to close it and make sure there's no
         * file descriptor leak.
         *
         * By default, the stream will emit a `'close'` event after it has been
         * destroyed.  Set the `emitClose` option to `false` to change this behavior.
         * @since v16.11.0
         */
        createWriteStream(options?: CreateWriteStreamOptions): WriteStream;
        /**
         * Forces all currently queued I/O operations associated with the file to the
         * operating system's synchronized I/O completion state. Refer to the POSIX [`fdatasync(2)`](http://man7.org/linux/man-pages/man2/fdatasync.2.html) documentation for details.
         *
         * Unlike `filehandle.sync` this method does not flush modified metadata.
         * @since v10.0.0
         * @return Fulfills with `undefined` upon success.
         */
        datasync(): Promise<void>;
        /**
         * Request that all data for the open file descriptor is flushed to the storage
         * device. The specific implementation is operating system and device specific.
         * Refer to the POSIX [`fsync(2)`](http://man7.org/linux/man-pages/man2/fsync.2.html) documentation for more detail.
         * @since v10.0.0
         * @return Fufills with `undefined` upon success.
         */
        sync(): Promise<void>;
        /**
         * Reads data from the file and stores that in the given buffer.
         *
         * If the file is not modified concurrently, the end-of-file is reached when the
         * number of bytes read is zero.
         * @since v10.0.0
         * @param buffer A buffer that will be filled with the file data read.
         * @param offset The location in the buffer at which to start filling.
         * @param length The number of bytes to read.
         * @param position The location where to begin reading data from the file. If `null`, data will be read from the current file position, and the position will be updated. If `position` is an
         * integer, the current file position will remain unchanged.
         * @return Fulfills upon success with an object with two properties:
         */
        read<T extends NodeJS.ArrayBufferView>(
            buffer: T,
            offset?: number | null,
            length?: number | null,
            position?: number | null,
        ): Promise<FileReadResult<T>>;
        read<T extends NodeJS.ArrayBufferView = Buffer>(options?: FileReadOptions<T>): Promise<FileReadResult<T>>;
        /**
         * Returns a `ReadableStream` that may be used to read the files data.
         *
         * An error will be thrown if this method is called more than once or is called after the `FileHandle` is closed
         * or closing.
         *
         * ```js
         * import { open } from 'node:fs/promises';
         *
         * const file = await open('./some/file/to/read');
         *
         * for await (const chunk of file.readableWebStream())
         *   console.log(chunk);
         *
         * await file.close();
         * ```
         *
         * While the `ReadableStream` will read the file to completion, it will not close the `FileHandle` automatically. User code must still call the `fileHandle.close()` method.
         *
         * @since v17.0.0
         * @experimental
         */
        readableWebStream(options?: ReadableWebStreamOptions): ReadableStream;
        /**
         * Asynchronously reads the entire contents of a file.
         *
         * If `options` is a string, then it specifies the `encoding`.
         *
         * The `FileHandle` has to support reading.
         *
         * If one or more `filehandle.read()` calls are made on a file handle and then a`filehandle.readFile()` call is made, the data will be read from the current
         * position till the end of the file. It doesn't always read from the beginning
         * of the file.
         * @since v10.0.0
         * @return Fulfills upon a successful read with the contents of the file. If no encoding is specified (using `options.encoding`), the data is returned as a {Buffer} object. Otherwise, the
         * data will be a string.
         */
        readFile(
            options?:
                | ({ encoding?: null | undefined } & Abortable)
                | null,
        ): Promise<Buffer>;
        /**
         * Asynchronously reads the entire contents of a file. The underlying file will _not_ be closed automatically.
         * The `FileHandle` must have been opened for reading.
         */
        readFile(
            options:
                | ({ encoding: BufferEncoding } & Abortable)
                | BufferEncoding,
        ): Promise<string>;
        /**
         * Asynchronously reads the entire contents of a file. The underlying file will _not_ be closed automatically.
         * The `FileHandle` must have been opened for reading.
         */
        readFile(
            options?:
                | (ObjectEncodingOptions & Abortable)
                | BufferEncoding
                | null,
        ): Promise<string | Buffer>;
        /**
         * Convenience method to create a `readline` interface and stream over the file. For example:
         *
         * ```js
         * import { open } from 'node:fs/promises';
         *
         * const file = await open('./some/file/to/read');
         *
         * for await (const line of file.readLines()) {
         *   console.log(line);
         * }
         * ```
         *
         * @since v18.11.0
         * @param options See `filehandle.createReadStream()` for the options.
         */
        readLines(options?: CreateReadStreamOptions): ReadlineInterface;
        /**
         * @since v10.0.0
         * @return Fulfills with an {fs.Stats} for the file.
         */
        stat(
            opts?: StatOptions & {
                bigint?: false | undefined;
            },
        ): Promise<Stats>;
        stat(
            opts: StatOptions & {
                bigint: true;
            },
        ): Promise<BigIntStats>;
        stat(opts?: StatOptions): Promise<Stats | BigIntStats>;
        /**
         * Truncates the file.
         *
         * If the file was larger than `len` bytes, only the first `len` bytes will be
         * retained in the file.
         *
         * The following example retains only the first four bytes of the file:
         *
         * ```js
         * import { open } from 'fs/promises';
         *
         * let filehandle = null;
         * try {
         *   filehandle = await open('temp.txt', 'r+');
         *   await filehandle.truncate(4);
         * } finally {
         *   await filehandle?.close();
         * }
         * ```
         *
         * If the file previously was shorter than `len` bytes, it is extended, and the
         * extended part is filled with null bytes (`'\0'`):
         *
         * If `len` is negative then `0` will be used.
         * @since v10.0.0
         * @param [len=0]
         * @return Fulfills with `undefined` upon success.
         */
        truncate(len?: number): Promise<void>;
        /**
         * Change the file system timestamps of the object referenced by the `FileHandle` then resolves the promise with no arguments upon success.
         * @since v10.0.0
         */
        utimes(atime: TimeLike, mtime: TimeLike): Promise<void>;
        /**
         * Asynchronously writes data to a file, replacing the file if it already exists.`data` can be a string, a buffer, an
         * [AsyncIterable](https://tc39.github.io/ecma262/#sec-asynciterable-interface) or
         * [Iterable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#The_iterable_protocol) object.
         * The promise is resolved with no arguments upon success.
         *
         * If `options` is a string, then it specifies the `encoding`.
         *
         * The `FileHandle` has to support writing.
         *
         * It is unsafe to use `filehandle.writeFile()` multiple times on the same file
         * without waiting for the promise to be resolved (or rejected).
         *
         * If one or more `filehandle.write()` calls are made on a file handle and then a`filehandle.writeFile()` call is made, the data will be written from the
         * current position till the end of the file. It doesn't always write from the
         * beginning of the file.
         * @since v10.0.0
         */
        writeFile(
            data: string | Uint8Array,
            options?: (ObjectEncodingOptions & Abortable) | BufferEncoding | null,
        ): Promise<void>;
        /**
         * Write `buffer` to the file.
         *
         * The promise is resolved with an object containing two properties:
         *
         * It is unsafe to use `filehandle.write()` multiple times on the same file
         * without waiting for the promise to be resolved (or rejected). For this
         * scenario, use `filehandle.createWriteStream()`.
         *
         * On Linux, positional writes do not work when the file is opened in append mode.
         * The kernel ignores the position argument and always appends the data to
         * the end of the file.
         * @since v10.0.0
         * @param [offset=0] The start position from within `buffer` where the data to write begins.
         * @param [length=buffer.byteLength - offset] The number of bytes from `buffer` to write.
         * @param position The offset from the beginning of the file where the data from `buffer` should be written. If `position` is not a `number`, the data will be written at the current position.
         * See the POSIX pwrite(2) documentation for more detail.
         */
        write<TBuffer extends Uint8Array>(
            buffer: TBuffer,
            offset?: number | null,
            length?: number | null,
            position?: number | null,
        ): Promise<{
            bytesWritten: number;
            buffer: TBuffer;
        }>;
        write(
            data: string,
            position?: number | null,
            encoding?: BufferEncoding | null,
        ): Promise<{
            bytesWritten: number;
            buffer: string;
        }>;
        /**
         * Write an array of [ArrayBufferView](https://developer.mozilla.org/en-US/docs/Web/API/ArrayBufferView) s to the file.
         *
         * The promise is resolved with an object containing a two properties:
         *
         * It is unsafe to call `writev()` multiple times on the same file without waiting
         * for the promise to be resolved (or rejected).
         *
         * On Linux, positional writes don't work when the file is opened in append mode.
         * The kernel ignores the position argument and always appends the data to
         * the end of the file.
         * @since v12.9.0
         * @param position The offset from the beginning of the file where the data from `buffers` should be written. If `position` is not a `number`, the data will be written at the current
         * position.
         */
        writev(buffers: readonly NodeJS.ArrayBufferView[], position?: number): Promise<WriteVResult>;
        /**
         * Read from a file and write to an array of [ArrayBufferView](https://developer.mozilla.org/en-US/docs/Web/API/ArrayBufferView) s
         * @since v13.13.0, v12.17.0
         * @param position The offset from the beginning of the file where the data should be read from. If `position` is not a `number`, the data will be read from the current position.
         * @return Fulfills upon success an object containing two properties:
         */
        readv(buffers: readonly NodeJS.ArrayBufferView[], position?: number): Promise<ReadVResult>;
        /**
         * Closes the file handle after waiting for any pending operation on the handle to
         * complete.
         *
         * ```js
         * import { open } from 'fs/promises';
         *
         * let filehandle;
         * try {
         *   filehandle = await open('thefile.txt', 'r');
         * } finally {
         *   await filehandle?.close();
         * }
         * ```
         * @since v10.0.0
         * @return Fulfills with `undefined` upon success.
         */
        close(): Promise<void>;
        /**
         * An alias for {@link FileHandle.close()}.
         * @since v18.18.0
         */
        [Symbol.asyncDispose](): Promise<void>;
    }

    const constants: typeof fsConstants;

    /**
     * Tests a user's permissions for the file or directory specified by `path`.
     * The `mode` argument is an optional integer that specifies the accessibility
     * checks to be performed. `mode` should be either the value `fs.constants.F_OK` or a mask consisting of the bitwise OR of any of `fs.constants.R_OK`, `fs.constants.W_OK`, and `fs.constants.X_OK`
     * (e.g.`fs.constants.W_OK | fs.constants.R_OK`). Check `File access constants` for
     * possible values of `mode`.
     *
     * If the accessibility check is successful, the promise is resolved with no
     * value. If any of the accessibility checks fail, the promise is rejected
     * with an [Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) object. The following example checks if the file`/etc/passwd` can be read and
     * written by the current process.
     *
     * ```js
     * import { access } from 'fs/promises';
     * import { constants } from 'fs';
     *
     * try {
     *   await access('/etc/passwd', constants.R_OK | constants.W_OK);
     *   console.log('can access');
     * } catch {
     *   console.error('cannot access');
     * }
     * ```
     *
     * Using `fsPromises.access()` to check for the accessibility of a file before
     * calling `fsPromises.open()` is not recommended. Doing so introduces a race
     * condition, since other processes may change the file's state between the two
     * calls. Instead, user code should open/read/write the file directly and handle
     * the error raised if the file is not accessible.
     * @since v10.0.0
     * @param [mode=fs.constants.F_OK]
     * @return Fulfills with `undefined` upon success.
     */
    function access(path: PathLike, mode?: number): Promise<void>;
    /**
     * Asynchronously copies `src` to `dest`. By default, `dest` is overwritten if it
     * already exists.
     *
     * No guarantees are made about the atomicity of the copy operation. If an
     * error occurs after the destination file has been opened for writing, an attempt
     * will be made to remove the destination.
     *
     * ```js
     * import { constants } from 'fs';
     * import { copyFile } from 'fs/promises';
     *
     * try {
     *   await copyFile('source.txt', 'destination.txt');
     *   console.log('source.txt was copied to destination.txt');
     * } catch {
     *   console.log('The file could not be copied');
     * }
     *
     * // By using COPYFILE_EXCL, the operation will fail if destination.txt exists.
     * try {
     *   await copyFile('source.txt', 'destination.txt', constants.COPYFILE_EXCL);
     *   console.log('source.txt was copied to destination.txt');
     * } catch {
     *   console.log('The file could not be copied');
     * }
     * ```
     * @since v10.0.0
     * @param src source filename to copy
     * @param dest destination filename of the copy operation
     * @param [mode=0] Optional modifiers that specify the behavior of the copy operation. It is possible to create a mask consisting of the bitwise OR of two or more values (e.g.
     * `fs.constants.COPYFILE_EXCL | fs.constants.COPYFILE_FICLONE`)
     * @return Fulfills with `undefined` upon success.
     */
    function copyFile(src: PathLike, dest: PathLike, mode?: number): Promise<void>;
    /**
     * Opens a `FileHandle`.
     *
     * Refer to the POSIX [`open(2)`](http://man7.org/linux/man-pages/man2/open.2.html) documentation for more detail.
     *
     * Some characters (`< > : " / \ | ? *`) are reserved under Windows as documented
     * by [Naming Files, Paths, and Namespaces](https://docs.microsoft.com/en-us/windows/desktop/FileIO/naming-a-file). Under NTFS, if the filename contains
     * a colon, Node.js will open a file system stream, as described by [this MSDN page](https://docs.microsoft.com/en-us/windows/desktop/FileIO/using-streams).
     * @since v10.0.0
     * @param [flags='r'] See `support of file system `flags``.
     * @param [mode=0o666] Sets the file mode (permission and sticky bits) if the file is created.
     * @return Fulfills with a {FileHandle} object.
     */
    function open(path: PathLike, flags?: string | number, mode?: Mode): Promise<FileHandle>;
    /**
