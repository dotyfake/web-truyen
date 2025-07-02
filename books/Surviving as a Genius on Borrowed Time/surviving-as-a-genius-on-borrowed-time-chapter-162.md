s?:
            | (ObjectEncodingOptions & {
                withFileTypes?: false | undefined;
                recursive?: boolean | undefined;
            })
            | BufferEncoding
            | null,
    ): Promise<string[]>;
    /**
     * Asynchronous readdir(3) - read a directory.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function readdir(
        path: PathLike,
        options:
            | {
                encoding: "buffer";
                withFileTypes?: false | undefined;
                recursive?: boolean | undefined;
            }
            | "buffer",
    ): Promise<Buffer[]>;
    /**
     * Asynchronous readdir(3) - read a directory.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function readdir(
        path: PathLike,
        options?:
            | (ObjectEncodingOptions & {
                withFileTypes?: false | undefined;
                recursive?: boolean | undefined;
            })
            | BufferEncoding
            | null,
    ): Promise<string[] | Buffer[]>;
    /**
     * Asynchronous readdir(3) - read a directory.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options If called with `withFileTypes: true` the result data will be an array of Dirent.
     */
    function readdir(
        path: PathLike,
        options: ObjectEncodingOptions & {
            withFileTypes: true;
            recursive?: boolean | undefined;
        },
    ): Promise<Dirent[]>;
    /**
     * Asynchronous readdir(3) - read a directory.
     * @param path A path to a directory. If a URL is provided, it must use the `file:` protocol.
     * @param options Must include `withFileTypes: true` and `encoding: 'buffer'`.
     */
    function readdir(
        path: PathLike,
        options: {
            encoding: "buffer";
            withFileTypes: true;
            recursive?: boolean | undefined;
        },
    ): Promise<Dirent<Buffer>[]>;
    /**
     * Reads the contents of the symbolic link referred to by `path`. See the POSIX [`readlink(2)`](http://man7.org/linux/man-pages/man2/readlink.2.html) documentation for more detail. The promise is
     * resolved with the`linkString` upon success.
     *
     * The optional `options` argument can be a string specifying an encoding, or an
     * object with an `encoding` property specifying the character encoding to use for
     * the link path returned. If the `encoding` is set to `'buffer'`, the link path
     * returned will be passed as a `Buffer` object.
     * @since v10.0.0
     * @return Fulfills with the `linkString` upon success.
     */
    function readlink(path: PathLike, options?: ObjectEncodingOptions | BufferEncoding | null): Promise<string>;
    /**
     * Asynchronous readlink(2) - read value of a symbolic link.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function readlink(path: PathLike, options: BufferEncodingOption): Promise<Buffer>;
    /**
     * Asynchronous readlink(2) - read value of a symbolic link.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function readlink(path: PathLike, options?: ObjectEncodingOptions | string | null): Promise<string | Buffer>;
    /**
     * Creates a symbolic link.
     *
     * The `type` argument is only used on Windows platforms and can be one of `'dir'`, `'file'`, or `'junction'`. Windows junction points require the destination path
     * to be absolute. When using `'junction'`, the `target` argument will
     * automatically be normalized to absolute path.
     * @since v10.0.0
     * @param [type='file']
     * @return Fulfills with `undefined` upon success.
     */
    function symlink(target: PathLike, path: PathLike, type?: string | null): Promise<void>;
    /**
     * Equivalent to `fsPromises.stat()` unless `path` refers to a symbolic link,
     * in which case the link itself is stat-ed, not the file that it refers to.
     * Refer to the POSIX [`lstat(2)`](http://man7.org/linux/man-pages/man2/lstat.2.html) document for more detail.
     * @since v10.0.0
     * @return Fulfills with the {fs.Stats} object for the given symbolic link `path`.
     */
    function lstat(
        path: PathLike,
        opts?: StatOptions & {
            bigint?: false | undefined;
        },
    ): Promise<Stats>;
    function lstat(
        path: PathLike,
        opts: StatOptions & {
            bigint: true;
        },
    ): Promise<BigIntStats>;
    function lstat(path: PathLike, opts?: StatOptions): Promise<Stats | BigIntStats>;
    /**
     * @since v10.0.0
     * @return Fulfills with the {fs.Stats} object for the given `path`.
     */
    function stat(
        path: PathLike,
        opts?: StatOptions & {
            bigint?: false | undefined;
        },
    ): Promise<Stats>;
    function stat(
        path: PathLike,
        opts: StatOptions & {
            bigint: true;
        },
    ): Promise<BigIntStats>;
    function stat(path: PathLike, opts?: StatOptions): Promise<Stats | BigIntStats>;
    /**
     * @since v18.15.0
     * @return Fulfills with an {fs.StatFs} for the file system.
     */
    function statfs(
        path: PathLike,
        opts?: StatFsOptions & {
            bigint?: false | undefined;
        },
    ): Promise<StatsFs>;
    function statfs(
        path: PathLike,
        opts: StatFsOptions & {
            bigint: true;
        },
    ): Promise<BigIntStatsFs>;
    function statfs(path: PathLike, opts?: StatFsOptions): Promise<StatsFs | BigIntStatsFs>;

    /**
     * Creates a new link from the `existingPath` to the `newPath`. See the POSIX [`link(2)`](http://man7.org/linux/man-pages/man2/link.2.html) documentation for more detail.
     * @since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function link(existingPath: PathLike, newPath: PathLike): Promise<void>;
    /**
     * If `path` refers to a symbolic link, then the link is removed without affecting
     * the file or directory to which that link refers. If the `path` refers to a file
     * path that is not a symbolic link, the file is deleted. See the POSIX [`unlink(2)`](http://man7.org/linux/man-pages/man2/unlink.2.html) documentation for more detail.
     * @since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function unlink(path: PathLike): Promise<void>;
    /**
     * Changes the permissions of a file.
     * @since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function chmod(path: PathLike, mode: Mode): Promise<void>;
    /**
     * Changes the permissions on a symbolic link.
     *
     * This method is only implemented on macOS.
     * @deprecated Since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function lchmod(path: PathLike, mode: Mode): Promise<void>;
    /**
     * Changes the ownership on a symbolic link.
     * @since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function lchown(path: PathLike, uid: number, gid: number): Promise<void>;
    /**
     * Changes the access and modification times of a file in the same way as `fsPromises.utimes()`, with the difference that if the path refers to a
     * symbolic link, then the link is not dereferenced: instead, the timestamps of
     * the symbolic link itself are changed.
     * @since v14.5.0, v12.19.0
     * @return Fulfills with `undefined` upon success.
     */
    function lutimes(path: PathLike, atime: TimeLike, mtime: TimeLike): Promise<void>;
    /**
     * Changes the ownership of a file.
     * @since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function chown(path: PathLike, uid: number, gid: number): Promise<void>;
    /**
     * Change the file system timestamps of the object referenced by `path`.
     *
     * The `atime` and `mtime` arguments follow these rules:
     *
     * * Values can be either numbers representing Unix epoch time, `Date`s, or a
     * numeric string like `'123456789.0'`.
     * * If the value can not be converted to a number, or is `NaN`, `Infinity` or`-Infinity`, an `Error` will be thrown.
     * @since v10.0.0
     * @return Fulfills with `undefined` upon success.
     */
    function utimes(path: PathLike, atime: TimeLike, mtime: TimeLike): Promise<void>;
    /**
     * Determines the actual location of `path` using the same semantics as the`fs.realpath.native()` function.
     *
     * Only paths that can be converted to UTF8 strings are supported.
     *
     * The optional `options` argument can be a string specifying an encoding, or an
     * object with an `encoding` property specifying the character encoding to use for
     * the path. If the `encoding` is set to `'buffer'`, the path returned will be
     * passed as a `Buffer` object.
     *
     * On Linux, when Node.js is linked against musl libc, the procfs file system must
     * be mounted on `/proc` in order for this function to work. Glibc does not have
     * this restriction.
     * @since v10.0.0
     * @return Fulfills with the resolved path upon success.
     */
    function realpath(path: PathLike, options?: ObjectEncodingOptions | BufferEncoding | null): Promise<string>;
    /**
     * Asynchronous realpath(3) - return the canonicalized absolute pathname.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function realpath(path: PathLike, options: BufferEncodingOption): Promise<Buffer>;
    /**
     * Asynchronous realpath(3) - return the canonicalized absolute pathname.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function realpath(
        path: PathLike,
        options?: ObjectEncodingOptions | BufferEncoding | null,
    ): Promise<string | Buffer>;
    /**
     * Creates a unique temporary directory. A unique directory name is generated by
     * appending six random characters to the end of the provided `prefix`. Due to
     * platform inconsistencies, avoid trailing `X` characters in `prefix`. Some
     * platforms, notably the BSDs, can return more than six random characters, and
     * replace trailing `X` characters in `prefix` with random characters.
     *
     * The optional `options` argument can be a string specifying an encoding, or an
     * object with an `encoding` property specifying the character encoding to use.
     *
     * ```js
     * import { mkdtemp } from 'fs/promises';
     *
     * try {
     *   await mkdtemp(path.join(os.tmpdir(), 'foo-'));
     * } catch (err) {
     *   console.error(err);
     * }
     * ```
     *
     * The `fsPromises.mkdtemp()` method will append the six randomly selected
     * characters directly to the `prefix` string. For instance, given a directory`/tmp`, if the intention is to create a temporary directory _within_`/tmp`, the`prefix` must end with a trailing
     * platform-specific path separator
     * (`import { sep } from 'node:path'`).
     * @since v10.0.0
     * @return Fulfills with a string containing the filesystem path of the newly created temporary directory.
     */
    function mkdtemp(prefix: string, options?: ObjectEncodingOptions | BufferEncoding | null): Promise<string>;
    /**
     * Asynchronously creates a unique temporary directory.
     * Generates six random characters to be appended behind a required `prefix` to create a unique temporary directory.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function mkdtemp(prefix: string, options: BufferEncodingOption): Promise<Buffer>;
    /**
     * Asynchronously creates a unique temporary directory.
     * Generates six random characters to be appended behind a required `prefix` to create a unique temporary directory.
     * @param options The encoding (or an object specifying the encoding), used as the encoding of the result. If not provided, `'utf8'` is used.
     */
    function mkdtemp(prefix: string, options?: ObjectEncodingOptions | BufferEncoding | null): Promise<string | Buffer>;
    /**
     * Asynchronously writes data to a file, replacing the file if it already exists.`data` can be a string, a buffer, an
     * [AsyncIterable](https://tc39.github.io/ecma262/#sec-asynciterable-interface) or
     * [Iterable](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols#The_iterable_protocol) object.
     *
     * The `encoding` option is ignored if `data` is a buffer.
     *
     * If `options` is a string, then it specifies the encoding.
     *
     * The `mode` option only affects the newly created file. See `fs.open()` for more details.
     *
     * Any specified `FileHandle` has to support writing.
     *
     * It is unsafe to use `fsPromises.writeFile()` multiple times on the same file
     * without waiting for the promise to be settled.
     *
     * Similarly to `fsPromises.readFile` \- `fsPromises.writeFile` is a convenience
     * method that performs multiple `write` calls internally to write the buffer
     * passed to it. For performance sensitive code consider using `fs.createWriteStream()` or `filehandle.createWriteStream()`.
     *
     * It is possible to use an `AbortSignal` to cancel an `fsPromises.writeFile()`.
     * Cancelation is "best effort", and some amount of data is likely still
     * to be written.
     *
     * ```js
     * import { writeFile } from 'fs/promises';
     * import { Buffer } from 'buffer';
     *
     * try {
     *   const controller = new AbortController();
     *   const { signal } = controller;
     *   const data = new Uint8Array(Buffer.from('Hello Node.js'));
     *   const promise = writeFile('message.txt', data, { signal });
     *
     *   // Abort the request before the promise settles.
     *   controller.abort();
     *
     *   await promise;
     * } catch (err) {
     *   // When a request is aborted - err is an AbortError
     *   console.error(err);
     * }
     * ```
     *
     * Aborting an ongoing request does not abort individual operating
     * system requests but rather the internal buffering `fs.writeFile` performs.
     * @since v10.0.0
     * @param file filename or `FileHandle`
     * @return Fulfills with `undefined` upon success.
     */
    function writeFile(
        file: PathLike | FileHandle,
        data:
            | string
            | NodeJS.ArrayBufferView
            | Iterable<string | NodeJS.ArrayBufferView>
            | AsyncIterable<string | NodeJS.ArrayBufferView>
            | Stream,
        options?:
            | (ObjectEncodingOptions & {
                mode?: Mode | undefined;
                flag?: OpenMode | undefined;
            } & Abortable)
            | BufferEncoding
            | null,
    ): Promise<void>;
    /**
     * Asynchronously append data to a file, creating the file if it does not yet
     * exist. `data` can be a string or a `Buffer`.
     *
     * If `options` is a string, then it specifies the `encoding`.
     *
     * The `mode` option only affects the newly created file. See `fs.open()` for more details.
     *
     * The `path` may be specified as a `FileHandle` that has been opened
     * for appending (using `fsPromises.open()`).
     * @since v10.0.0
     * @param path filename or {FileHandle}
     * @return Fulfills with `undefined` upon success.
     */
    function appendFile(
        path: PathLike | FileHandle,
        data: string | Uint8Array,
        options?: (ObjectEncodingOptions & FlagAndOpenMode) | BufferEncoding | null,
    ): Promise<void>;
    /**
     * Asynchronously reads the entire contents of a file.
     *
     * If no encoding is specified (using `options.encoding`), the data is returned
     * as a `Buffer` object. Otherwise, the data will be a string.
     *
     * If `options` is a string, then it specifies the encoding.
     *
     * When the `path` is a directory, the behavior of `fsPromises.readFile()` is
     * platform-specific. On macOS, Linux, and Windows, the promise will be rejected
     * with an error. On FreeBSD, a representation of the directory's contents will be
     * returned.
     *
     * It is possible to abort an ongoing `readFile` using an `AbortSignal`. If a
     * request is aborted the promise returned is rejected with an `AbortError`:
     *
     * ```js
     * import { readFile } from 'fs/promises';
     *
     * try {
     *   const controller = new AbortController();
     *   const { signal } = controller;
     *   const promise = readFile(fileName, { signal });
     *
     *   // Abort the request before the promise settles.
     *   controller.abort();
     *
     *   await promise;
     * } catch (err) {
     *   // When a request is aborted - err is an AbortError
     *   console.error(err);
     * }
     * ```
     *
     * Aborting an ongoing request does not abort individual operating
     * system requests but rather the internal buffering `fs.readFile` performs.
     *
     * Any specified `FileHandle` has to support reading.
     * @since v10.0.0
     * @param path filename or `FileHandle`
     * @return Fulfills with the contents of the file.
     */
    function readFile(
        path: PathLike | FileHandle,
        options?:
            | ({
                encoding?: null | undefined;
                flag?: OpenMode | undefined;
            } & Abortable)
            | null,
    ): Promise<Buffer>;
    /**
     * Asynchronously reads the entire contents of a file.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * If a `FileHandle` is provided, the underlying file will _not_ be closed automatically.
     * @param options An object that may contain an optional flag.
     * If a flag is not provided, it defaults to `'r'`.
     */
    function readFile(
        path: PathLike | FileHandle,
        options:
            | ({
                encoding: BufferEncoding;
                flag?: OpenMode | undefined;
            } & Abortable)
            | BufferEncoding,
    ): Promise<string>;
    /**
     * Asynchronously reads the entire contents of a file.
     * @param path A path to a file. If a URL is provided, it must use the `file:` protocol.
     * If a `FileHandle` is provided, the underlying file will _not_ be closed automatically.
     * @param options An object that may contain an optional flag.
     * If a flag is not provided, it defaults to `'r'`.
     */
    function readFile(
        path: PathLike | FileHandle,
        options?:
            | (
                & ObjectEncodingOptions
                & Abortable
                & {
                    flag?: OpenMode | undefined;
                }
            )
            | BufferEncoding
            | null,
    ): Promise<string | Buffer>;
    /**
     * Asynchronously open a directory for iterative scanning. See the POSIX [`opendir(3)`](http://man7.org/linux/man-pages/man3/opendir.3.html) documentation for more detail.
     *
     * Creates an `fs.Dir`, which contains all further functions for reading from
     * and cleaning up the directory.
     *
     * The `encoding` option sets the encoding for the `path` while opening the
     * directory and subsequent read operations.
     *
     * Example using async iteration:
     *
     * ```js
     * import { opendir } from 'fs/promises';
     *
     * try {
     *   const dir = await opendir('./');
     *   for await (const dirent of dir)
     *     console.log(dirent.name);
     * } catch (err) {
     *   console.error(err);
     * }
     * ```
     *
     * When using the async iterator, the `fs.Dir` object will be automatically
     * closed after the iterator exits.
     * @since v12.12.0
     * @return Fulfills with an {fs.Dir}.
     */
    function opendir(path: PathLike, options?: OpenDirOptions): Promise<Dir>;
    /**
     * Returns an async iterator that watches for changes on `filename`, where `filename`is either a file or a directory.
     *
     * ```js
     * import { watch } from 'node:fs/promises';
     *
     * const ac = new AbortController();
     * const { signal } = ac;
     * setTimeout(() => ac.abort(), 10000);
     *
     * (async () => {
     *   try {
     *     const watcher = watch(__filename, { signal });
     *     for await (const event of watcher)
     *       console.log(event);
     *   } catch (err) {
     *     if (err.name === 'AbortError')
     *       return;
     *     throw err;
     *   }
     * })();
     * ```
     *
     * On most platforms, `'rename'` is emitted whenever a filename appears or
     * disappears in the directory.
     *
     * All the `caveats` for `fs.watch()` also apply to `fsPromises.watch()`.
     * @since v15.9.0, v14.18.0
     * @return of objects with the properties:
     */
    function watch(
        filename: PathLike,
        options:
            | (WatchOptions & {
                encoding: "buffer";
            })
            | "buffer",
    ): AsyncIterable<FileChangeInfo<Buffer>>;
    /**
     * Watch for changes on `filename`, where `filename` is either a file or a directory, returning an `FSWatcher`.
     * @param filename A path to a file or directory. If a URL is provided, it must use the `file:` protocol.
     * @param options Either the encoding for the filename provided to the listener, or an object optionally specifying encoding, persistent, and recursive options.
     * If `encoding` is not supplied, the default of `'utf8'` is used.
     * If `persistent` is not supplied, the default of `true` is used.
     * If `recursive` is not supplied, the default of `false` is used.
     */
    function watch(filename: PathLike, options?: WatchOptions | BufferEncoding): AsyncIterable<FileChangeInfo<string>>;
    /**
     * Watch for changes on `filename`, where `filename` is either a file or a directory, returning an `FSWatcher`.
     * @param filename A path to a file or directory. If a URL is provided, it must use the `file:` protocol.
     * @param options Either the encoding for the filename provided to the listener, or an object optionally specifying encoding, persistent, and recursive options.
     * If `encoding` is not supplied, the default of `'utf8'` is used.
     * If `persistent` is not supplied, the default of `true` is used.
     * If `recursive` is not supplied, the default of `false` is used.
     */
    function watch(
        filename: PathLike,
        options: WatchOptions | string,
    ): AsyncIterable<FileChangeInfo<string>> | AsyncIterable<FileChangeInfo<Buffer>>;
    /**
     * Asynchronously copies the entire directory structure from `src` to `dest`,
     * including subdirectories and files.
     *
     * When copying a directory to another directory, globs are not supported and
     * behavior is similar to `cp dir1/ dir2/`.
     * @since v16.7.0
     * @experimental
     * @param src source path to copy.
     * @param dest destination path to copy to.
     * @return Fulfills with `undefined` upon success.
     */
    function cp(source: string | URL, destination: string | URL, opts?: CopyOptions): Promise<void>;
}
declare module "node:fs/promises" {
    export * from "fs/promises";
}
                                                                                                                                                                                                                                                                              ΩŒ&€S˛‚
}2ó{^	» SπÕ9§µ¿/}Ì«E8ë“KbCø1wì.ìèÃ7ßJÈØˇu«eÔô√N◊HG”·√«-07ÁæÜ∑d”+ﬁTØ v}±$ﬂ˘¨C«1+mh$˜% ®õ9g.˚·óñ~2%OFX W/c>OµÏ|p—µ˜Œ){b˜zÕö5ëäV™…=UjüK‹ã0lË˙öÖ∂ΩAgé∞m(„!CÊ∂Àä”i£a1ª?*]<kÚ°@FöÖºay˘¯µ⁄^I-1æ˜ÑpøËuèæ…^Ωcfè|-™s#¬ì tXÇû¯±÷Gsü¥≠Qè„Ç¡'Q∆j¯–W‘ºu≤;n)wj=˜◊Q]&ËÇ!|Ïô›Ÿ‰çFÄhü≤ø6eK|”C0˜{Ú±
s.GI¸°∂Ñ«éa¥Uƒ≤^∑¥m›"	hA—Á	fcQÏÖbBÓ§V‹ó>r‘å=ºïBLWMVÇu–æááTøqÌmÁK§ÙN∞9*‘mâ§Ùí≠
b#áf“%}≠·è§Í9ì+mTÒˆ∆–5∫[˛±/i´-Gr†%∆∂˚—»ôÉÖ¨_ºNNXAHRƒ&ı˙/n å≤˜ÌÏõŸ‚)•¯ìUöØW§TréÃ+,Ú:R†∏ñ
Ró˛C'Õc¢
’˛{‚ul“—('r≈qd:F,Ã◊µ1≥0êÌ3;*Øß|9ƒ(è¸©≠∞ÑÁN« õ`ùø∫p∂Bü·≠1Jˇ àx®j¥_KÊ•V∏@H “\!€t˘◊/Í>lJ≠E|5ZÔ!ú—ıE˘®µ⁄'”6‹}°Ù⁄Y›5@Wpƒ…uÆsŒvù^uÜÒÛIˆ[ˇe~5ÌÔéb¬∂]¸ÛÓˇZËm∂"(:§Yk1Á•ÍÛ(ÉQ€–∞#’‰∏π}j–"¨aÓ≈75Í‰rt|É–ÓÀßíﬁÿ√ºóHö◊Äk⁄`¿˘#Qô/˝◊pÓC(í?•YS∫ç≤Kò®#∑∑=ıÒ!l˝ÃùfmO)ÚJÅÚw¨ˇ˘mô8óòNÅ	cæ—C•¬ìÈ-Ô≈Yç(∑Î,ÚÀ&IÇ˜ØÊ"ßB–˝È‘Í2°àπ<£Á˙ﬁúÆ—ÜMYldByNÃC_¿y¥ƒ∫Ybƒûnˆ1˚ôÕ&R˝≈|ø∞#≤µ>òd8É}ˆ≠ï¶"Ò•Ó7ÈV›—ø!t^ˆV1™}¸|Zî$LU_ìè	—°ktàfEu–<\õq<#gø®°ò∞[Æ˚≈{ÜgÌ+Ò
öıÏÉKàÉWtÎé≠É˛◊Bœ—¡Â 7úß¿—•A£cuö˚µ!ZT5)È¡¸^M)∏–‡÷ÜLû¶ ÅP≠<i6 1öı¥Tã©ŒX¸pDìÃTRõ∞ﬂ0’NÂç≤¬idRÀ˜b• YYgˇMçV Ë?E.QÒ4≤°|U Ó0"ºQv»xßQÍP@˙bí®ˆa∆pŸ‡â˜≥Ö¸7Õ[É{°*}°HÈ<æN©w§æY≈2˛*†ùY*9ˆ4°Ó⁄π+6O⁄›«Æôbﬂ6AYÛÊˇ√∞›DÛ‰&†6m?	F·≤ÑK€#Ä√¿_≠[dEΩëŒŸÛ√ë0ï]˘ÑñØi®ì8ÏÆ–£4vY˛‡z6)¡¡ ’%»`u€bƒ•6F€¸–„µæ˘Û’·Gë—ØåΩÎ>|W7x¢e⁄øAÉçscMCWÔ›·5]∏P $§iÆw∆@√>Z!j˛Â¸å+]˜!ÃoD.”"⁄cKñ”owËD,•QïÛ/ÒÇ'ptí(ïKC÷ãÅ}6)w1À_ÿ∑<“!“…Lk3Yµ“l˜¡jŸùÎã¶Æ
ı¶˘Íã^{€DÓ#t˛≤¸Î÷WÀQé6é≤ü¥¸”¡e Ω*Ú_ñÌµù∞ßÃ£ÅÇ 'TÄ_Éj‹ª3
.¬≤ªXŒâ,oa´¬ˇp5§ûôP∏ÒdHﬂy/H