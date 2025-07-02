# yauzl

[![Build Status](https://travis-ci.org/thejoshwolfe/yauzl.svg?branch=master)](https://travis-ci.org/thejoshwolfe/yauzl)
[![Coverage Status](https://img.shields.io/coveralls/thejoshwolfe/yauzl.svg)](https://coveralls.io/r/thejoshwolfe/yauzl)

yet another unzip library for node. For zipping, see
[yazl](https://github.com/thejoshwolfe/yazl).

Design principles:

 * Follow the spec.
   Don't scan for local file headers.
   Read the central directory for file metadata.
   (see [No Streaming Unzip API](#no-streaming-unzip-api)).
 * Don't block the JavaScript thread.
   Use and provide async APIs.
 * Keep memory usage under control.
   Don't attempt to buffer entire files in RAM at once.
 * Never crash (if used properly).
   Don't let malformed zip files bring down client applications who are trying to catch errors.
 * Catch unsafe file names.
   See `validateFileName()`.

## Usage

```js
var yauzl = require("yauzl");

yauzl.open("path/to/file.zip", {lazyEntries: true}, function(err, zipfile) {
  if (err) throw err;
  zipfile.readEntry();
  zipfile.on("entry", function(entry) {
    if (/\/$/.test(entry.fileName)) {
      // Directory file names end with '/'.
      // Note that entires for directories themselves are optional.
      // An entry's fileName implicitly requires its parent directories to exist.
      zipfile.readEntry();
    } else {
      // file entry
      zipfile.openReadStream(entry, function(err, readStream) {
        if (err) throw err;
        readStream.on("end", function() {
          zipfile.readEntry();
        });
        readStream.pipe(somewhere);
      });
    }
  });
});
```

See also `examples/` for more usage examples.

## API

The default for every optional `callback` parameter is:

```js
function defaultCallback(err) {
  if (err) throw err;
}
```

### open(path, [options], [callback])

Calls `fs.open(path, "r")` and reads the `fd` effectively the same as `fromFd()` would.

`options` may be omitted or `null`. The defaults are `{autoClose: true, lazyEntries: false, decodeStrings: true, validateEntrySizes: true, strictFileNames: false}`.

`autoClose` is effectively equivalent to:

```js
zipfile.once("end", function() {
  zipfile.close();
});
```

`lazyEntries` indicates that entries should be read only when `readEntry()` is called.
If `lazyEntries` is `false`, `entry` events will be emitted as fast as possible to allow `pipe()`ing
file data from all entries in parallel.
This is not recommended, as it can lead to out of control memory usage for zip files with many entries.
See [issue #22](https://github.com/thejoshwolfe/yauzl/issues/22).
If `lazyEntries` is `true`, an `entry` or `end` event will be emitted in response to each call to `readEntry()`.
This allows processing of one entry at a time, and will keep memory usage under control for zip files with many entries.

`decodeStrings` is the default and causes yauzl to decode strings with `CP437` or `UTF-8` as required by the spec.
The exact effects of turning this option off are:

* `zipfile.comment`, `entry.fileName`, and `entry.fileComment` will be `Buffer` objects instead of `String`s.
* Any Info-ZIP Unicode Path Extra Field will be ignored. See `extraFields`.
* Automatic file name validation will not be performed. See `validateFileName()`.

`validateEntrySizes` is the default and ensures that an entry's reported uncompressed size matches its actual uncompressed size.
This check happens as early as possible, which is either before emitting each `"entry"` event (for entries with no compression),
or during the `readStream` piping after calling `openReadStream()`.
See `openReadStream()` for more information on defending against zip bomb attacks.

When `strictFileNames` is `false` (the default) and `decodeStrings` is `true`,
all backslash (`\`) characters in each `entry.fileName` are replaced with forward slashes (`/`).
The spec forbids file names with backslashes,
but Microsoft's `System.IO.Compression.ZipFile` class in .NET versions 4.5.0 until 4.6.1
creates non-conformant zipfiles with backslashes in file names.
`strictFileNames` is `false` by default so that clients can read these
non-conformant zipfiles without knowing about this Microsoft-specific bug.
When `strictFileNames` is `true` and `decodeStrings` is `true`,
entries with backslashes in their file names will result in an error. See `validateFileName()`.
When `decodeStrings` is `false`, `strictFileNames` has no effect.

The `callback` is given the arguments `(err, zipfile)`.
An `err` is provided if the End of Central Directory Record cannot be found, or if its metadata appears malformed.
This kind of error usually indicates that this is not a zip file.
Otherwise, `zipfile` is an instance of `ZipFile`.

### fromFd(fd, [options], [callback])

Reads from the fd, which is presumed to be an open .zip file.
Note that random access is required by the zip file specification,
so the fd cannot be an open socket or any other fd that does not support random access.

`options` may be omitted or `null`. The defaults are `{autoClose: false, lazyEntries: false, decodeStrings: true, validateEntrySizes: true, strictFileNames: false}`.

See `open()` for the meaning of the options and callback.

### fromBuffer(buffer, [options], [callback])

Like `fromFd()`, but reads from a RAM buffer instead of an open file.
`buffer` is a `Buffer`.

If a `ZipFile` is acquired from this method,
it will never emit the `close` event,
and calling `close()` is not necessary.

`options` may be omitted or `null`. The defaults are `{lazyEntries: false, decodeStrings: true, validateEntrySizes: true, strictFileNames: false}`.

See `open()` for the meaning of the options and callback.
The `autoClose` option is ignored for this method.

### fromRandomAccessReader(reader, totalSize, [options], [callback])

This method of reading a zip file allows clients to implement their own back-end file system.
For example, a client might translate read calls into network requests.

The `reader` parameter must be of a type that is a subclass of
[RandomAccessReader](#class-randomaccessreader) that implements the required methods.
The `totalSize` is a Number and indicates the total file size of the zip file.

`options` may be omitted or `null`. The defaults are `{autoClose: true, lazyEntries: false, decodeStrings: true, validateEntrySizes: true, strictFileNames: false}`.

See `open()` for the meaning of the options and callback.

### dosDateTimeToDate(date, time)

Converts MS-DOS `date` and `time` data into a JavaScript `Date` object.
Each parameter is a `Number` treated as an unsigned 16-bit integer.
Note that this format does not support timezones,
so the returned object will use the local timezone.

### validateFileName(fileName)

Returns `null` or a `String` error message depending on the validity of `fileName`.
If `fileName` starts with `"/"` or `/[A-Za-z]:\//` or if it contains `".."` path segments or `"\\"`,
this function returns an error message appropriate for use like this:

```js
var errorMessage = yauzl.validateFileName(fileName);
if (errorMessage != null) throw new Error(errorMessage);
```

This function is automatically run for each entry, as long as `decodeStrings` is `true`.
See `open()`, `strictFileNames`, and `Event: "entry"` for more information.

### Class: ZipFile

The constructor for the class is not part of the public API.
Use `open()`, `fromFd()`, `fromBuffer()`, or `fromRandomAccessReader()` instead.

#### Event: "entry"

Callback gets `(entry)`, which is an `Entry`.
See `open()` and `readEntry()` for when this event is emitted.

If `decodeStrings` is `true`, entries emitted via this event have already passed file name validation.
See `validateFileName()` and `open()` for more information.

If `validateEntrySizes` is `true` and this entry's `compressionMethod` is `0` (stored without compression),
this entry has already passed entry size validation.
See `open()` for more information.

#### Event: "end"

Emitted after the last `entry` event has been emitted.
See `open()` and `readEntry()` for more info on when this event is emitted.

#### Event: "close"

Emitted after the fd is actually closed.
This is after calling `close()` (or after the `end` event when `autoClose` is `true`),
and after all stream pipelines created from `openReadStream()` have finished reading data from the fd.

If this `ZipFile` was acquired from `fromRandomAccessReader()`,
the "fd" in the previous paragraph refers to the `RandomAccessReader` implemented by the client.

If this `ZipFile` was acquired from `fromBuffer()`, this event is never emitted.

#### Event: "error"

Emitted in the case of errors with reading the zip file.
(Note that other errors can be emitted from the streams created from `openReadStream()` as well.)
After this event has been emitted, no further `entry`, `end`, or `error` events will be emitted,
but the `close` event may still be emitted.

#### readEntry()

Causes this `ZipFile` to emit an `entry` or `end` event (or an `error` event).
This method must only be called when this `ZipFile` was created with the `lazyEntries` option set to `true` (see `open()`).
When this `ZipFile` was created with the `lazyEntries` option set to `true`,
`entry` and `end` events are only ever emitted in response to this method call.

The event that is emitted in response to this method will not be emitted until after this method has returned,
so it is safe to call this method before attaching event listeners.

After calling this method, calling this method again before the response event has been emitted will cause undefined behavior.
Calling this method after the `end` event has been emitted will cause undefined behavior.
Calling this method after calling `close()` will cause undefined behavior.

#### openReadStream(entry, [options], callback)

`entry` must be an `Entry` object from this `ZipFile`.
`callback` gets `(err, readStream)`, where `readStream` is a `Readable Stream` that provides the file data for this entry.
If this zipfile is already closed (see `close()`), the `callback` will receive an `err`.

`options` may be omitted or `null`, and has the following defaults:

```js
{
  decompress: entry.isCompressed() ? true : null,
  decrypt: null,
  start: 0,                  // actually the default is null, see below
  end: entry.compressedSize, // actually the default is null, see below
}
```

If the entry is compressed (with a supported compression method),
and the `decompress` option is `true` (or omitted),
the read stream provides the decompressed data.
Omitting the `decompress` option is what most clients should do.

The `decompress` option must be `null` (or omitted) when the entry is not compressed (see `isCompressed()`),
and either `true` (or omitted) or `false` when the entry is compressed.
Specifying `decompress: false` for a compressed entry causes the read stream
to provide the raw compressed file data without going through a zlib inflate transform.

If the entry is encrypted (see `isEncrypted()`), clients may want to avoid calling `openReadStream()` on the entry entirely.
Alternatively, clients may call `openReadStream()` for encrypted entries and specify `decrypt: false`.
If the entry is also compressed, clients must *also* specify `decompress: false`.
Specifying `decrypt: false` for an encrypted entry causes the read stream to provide the raw, still-encrypted file data.
(This data includes the 12-byte header described in the spec.)

The `decrypt` option must be `null` (or omitted) for non-encrypted entries, and `false` for encrypted entries.
Omitting the `decrypt` option (or specifying it as `null`) for an encrypted entry
will result in the `callback` receiving an `err`.
This default behavior is so that clients not accounting for encrypted files aren't surprised by bogus file data.

The `start` (inclusive) and `end` (exclusive) options are byte offsets into this entry's file data,
and can be used to obtain part of an entry's file data rather than the whole thing.
If either of these options are specified and non-`null`,
then the above options must be used to obain the file's raw data.
Speficying `{start: 0, end: entry.compressedSize}` will result in the complete file,
which is effectively the default values for these options,
but note that unlike omitting the options, when you specify `start` or `end` as any non-`null` value,
the above requirement is still enforced that you must also pass the appropriate options to get the file's raw data.

It's possible for the `readStream` provided to the `callback` to emit errors for several reasons.
For example, if zlib cannot decompress the data, the zlib error will be emitted from the `readStream`.
Two more error cases (when `validateEntrySizes` is `true`) are if the decompressed data has too many
or too few actual bytes compared to the reported byte count from the entry's `uncompressedSize` field.
yauzl notices this false information and emits an error from the `readStream`
after some number of bytes have already been piped through the stream.

This check allows clients to trust the `uncompressedSize` field in `Entry` objects.
Guarding against [zip bomb](http://en.wikipedia.org/wiki/Zip_bomb) attacks can be accomplished by
doing some heuristic checks on the size metadata and then watching out for the above errors.
Such heuristics are outside the scope of this library,
but enforcing the `uncompressedSize` is implemented here as a security feature.

It is possible to destroy the `readStream` before it has piped all of its data.
To do this, call `readStream.destroy()`.
You must `unpipe()` the `readStream` from any destination before calling `readStream.destroy()`.
If this zipfile was created using `fromRandomAccessReader()`, the `RandomAccessReader` implementation
must provide readable streams that implement a `.destroy()` method (see `randomAccessReader._readStreamForRange()`)
in order for calls to `readStream.destroy()` to work in this context.

#### close()

Causes all future calls to `openReadStream()` to fail,
and closes the fd, if any, after all streams created by `openReadStream()` have emitted their `end` events.

If the `autoClose` option is set to `true` (see `open()`),
this function will be called automatically effectively in response to this object's `end` event.

If the `lazyEntries` option is set to `false` (see `open()`) and this object's `end` event has not been emitted yet,
this function causes undefined behavior.
If the `lazyEntries` option is set to `true`,
you can call this function instead of calling `readEntry()` to abort reading the entries of a zipfile.

It is safe to call this function multiple times; after the first call, successive calls have no effect.
This includes situations where the `autoClose` option effectively calls this function for you.

If `close()` is never called, then the zipfile is "kept open".
For zipfiles created with `fromFd()`, this will leave the `fd` open, which may be desirable.
For zipfiles created with `open()`, this will leave the underlying `fd` open, thereby "leaking" it, which is probably undesirable.
For zipfiles created with `fromRandomAccessReader()`, the reader's `close()` method will never be called.
For zipfiles created with `fromBuffer()`, the `close()` function has no effect whether called or not.

Regardless of how this `ZipFile` was created, there are no resources other than those listed above that require cleanup from this function.
This means it may be desirable to never call `close()` in some usecases.

#### isOpen

`Boolean`. `true` until `close()` is called; then it's `false`.

#### entryCount

`Number`. Total number of central directory records.

#### comment

`String`. Always decoded with `CP437` per the spec.

If `decodeStrings` is `false` (see `open()`), this field is the undecoded `Buffer` instead of a decoded `String`.

### Class: Entry

Objects of this class represent Central Directory Records.
Refer to the zipfile specification for more details about these fields.

These fields are of type `Number`:

 * `versionMadeBy`
 * `versionNeededToExtract`
 * `generalPurposeBitFlag`
 * `compressionMethod`
 * `lastModFileTime` (MS-DOS format, see `getLastModDateTime`)
 * `lastModFileDate` (MS-DOS format, see `getLastModDateTime`)
 * `crc32`
 * `compressedSize`
 * `uncompressedSize`
 * `fileNameLength` (bytes)
 * `extraFieldLength` (bytes)
 * `fileCommentLength` (bytes)
 * `inte'use strict';
const {PassThrough: PassThroughStream} = require('stream');

module.exports = options => {
	options = {...options};

	const {array} = options;
	let {encoding} = options;
	const isBuffer = encoding === 'buffer';
	let objectMode = false;

	if (array) {
		objectMode = !(encoding || isBuffer);
	} else {
		encoding = encoding || 'utf8';
	}

	if (isBuffer) {
		encoding = null;
	}

	const stream = new PassThroughStream({objectMode});

	if (encoding) {
		stream.setEncoding(encoding);
	}

	let length = 0;
	const chunks = [];

	stream.on('data', chunk => {
		chunks.push(chunk);

		if (objectMode) {
			length = chunks.length;
		} else {
			length += chunk.length;
		}
	});

	stream.getBufferedValue = () => {
		if (array) {
			return chunks;
		}

		return isBuffer ? Buffer.concat(chunks, length) : chunks.join('');
	};

	stream.getBufferedLength = () => length;

	return stream;
};
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  /*
Copyright 2019 Mark Lee and contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

declare function sumchecker(algorithm: string, checksumFilename: string, baseDir: string, filesToCheck: string[] | string): Promise<void>;

declare namespace sumchecker {
  type ChecksumOptions = {
    defaultTextEncoding?: string;
  };

  class ErrorWithFilename extends Error {
    constructor(filename: string);
  }

  class ChecksumMismatchError extends ErrorWithFilename {
    constructor(filename: string);
  }

  class ChecksumParseError extends Error {
    constructor(lineNumber: number, line: string);
  }

  class NoChecksumFoundError extends ErrorWithFilename {
    constructor(filename: string);
  }

  class ChecksumValidator {
    constructor(algorithm: string, checksumFilename: string, options?: ChecksumOptions);
    encoding(binary: boolean): string;
    parseChecksumFile(data: string): void;
    readFile(filename: string, binary: boolean): Promise<string>;
    validate(baseDir: string, filesToCheck: string[] | string): Promise<void>;
    validateFile(baseDir: string, filename: string): Promise<void>;
    validateFiles(baseDir: string, filesToCheck: string[]): Promise<void>;
  }
}

export = sumchecker
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           8.1.0 / 2019-06-28
------------------

- Add support for promisified `fs.realpath.native` in Node v9.2+ ([#650](https://github.com/jprichardson/node-fs-extra/issues/650), [#682](https://github.com/jprichardson/node-fs-extra/pull/682))
- Update `graceful-fs` dependency ([#700](https://github.com/jprichardson/node-fs-extra/pull/700))
- Use `graceful-fs` everywhere ([#700](https://github.com/jprichardson/node-fs-extra/pull/700))

8.0.1 / 2019-05-13
------------------

- Fix bug `Maximum call stack size exceeded` error in `util/stat` ([#679](https://github.com/jprichardson/node-fs-extra/pull/679))

8.0.0 / 2019-05-11
------------------

**NOTE:** Node.js v6 support is deprecated, and will be dropped in the next major release.

- Use `renameSync()` under the hood in `moveSync()`
- Fix bug with bind-mounted directories in `copy*()` ([#613](https://github.com/jprichardson/node-fs-extra/issues/613), [#618](https://github.com/jprichardson/node-fs-extra/pull/618))
- Fix bug in `move()` with case-insensitive file systems
- Use `fs.stat()`'s `bigint` option in `copy*()` & `move*()` where possible ([#657](https://github.com/jprichardson/node-fs-extra/issues/657))

7.0.1 / 2018-11-07
------------------

- Fix `removeSync()` on Windows, in some cases, it would error out with `ENOTEMPTY` ([#646](https://github.com/jprichardson/node-fs-extra/pull/646))
- Document `mode` option for `ensureDir*()` ([#587](https://github.com/jprichardson/node-fs-extra/pull/587))
- Don't include documentation files in npm package tarball ([#642](https://github.com/jprichardson/node-fs-extra/issues/642), [#643](https://github.com/jprichardson/node-fs-extra/pull/643))

7.0.0 / 2018-07-16
------------------

- **BREAKING:** Refine `copy*()` handling of symlinks to properly detect symlinks that point to the same file. ([#582](https://github.com/jprichardson/node-fs-extra/pull/582))
- Fix bug with copying write-protected directories ([#600](https://github.com/jprichardson/node-fs-extra/pull/600))
- Universalify `fs.lchmod()` ([#596](https://github.com/jprichardson/node-fs-extra/pull/596))
- Add `engines` field to `package.json` ([#580](https://github.com/jprichardson/node-fs-extra/pull/580))

6.0.1 / 2018-05-09
------------------

- Fix `fs.promises` `ExperimentalWarning` on Node v10.1.0 ([#578](https://github.com/jprichardson/node-fs-extra/pull/578))

6.0.0 / 2018-05-01
------------------

- Drop support for Node.js versions 4, 5, & 7 ([#564](https://github.com/jprichardson/node-fs-extra/pull/564))
- Rewrite `move` to use `fs.rename` where possible ([#549](https://github.com/jprichardson/node-fs-extra/pull/549))
- Don't convert relative paths to absolute paths for `filter` ([#554](https://github.com/jprichardson/node-fs-extra/pull/554))
- `copy*`'s behavior when `preserveTimestamps` is `false` has been OS-dependent since 5.0.0, but that's now explicitly noted in the docs ([#563](https://github.com/jprichardson/node-fs-extra/pull/563))
- Fix subdirectory detection for `copy*` & `move*` ([#541](https://github.com/jprichardson/node-fs-extra/pull/541))
- Handle case-insensitive paths correctly in `copy*` ([#568](https://github.com/jprichardson/node-fs-extra/pull/568))

5.0.0 / 2017-12-11
------------------

Significant refactor of `copy()` & `copySync()`, including breaking changes. No changes to other functions in this release.

Huge thanks to **[@manidlou](https://github.com/manidlou)** for doing most of the work on this release.

- The `filter` option can no longer be a RegExp (must be a function). This was deprecated since fs-extra v1.0.0. [#512](https://github.com/jprichardson/node-fs-extra/pull/512)
- `copy()`'s `filter` option can now be a function that returns a Promise. [#518](https://github.com/jprichardson/node-fs-extra/pull/518)
- `copy()` & `copySync()` now use `fs.copyFile()`/`fs.copyFileSync()` in environments that support it (currently Node 8.5.0+). Older Node versions still get the old implementation. [#505](https://github.com/jprichardson/node-fs-extra/pull/505)
- Don't allow copying a directory into itself. [#83](https://github.com/jprichardson/node-fs-extra/issues/83)
- Handle copying between identical files. [#198](https://github.com/jprichardson/node-fs-extra/issues/198)
- Error out when copying an empty folder to a path that already exists. [#464](https://github.com/jprichardson/node-fs-extra/issues/464)
- Don't create `dest`'s parent if the `filter` function aborts the `copy()` operation. [#517](https://github.com/jprichardson/node-fs-extra/pull/517)
- Fix `writeStream` not being closed if there was an error in `copy()`. [#516](https://github.com/jprichardson/node-fs-extra/pull/516)

4.0.3 / 2017-12-05
------------------

- Fix wrong `chmod` values in `fs.remove()` [#501](https://github.com/jprichardson/node-fs-extra/pull/501)
- Fix `TypeError` on systems that don't have some `fs` operations like `lchown` [#520](https://github.com/jprichardson/node-fs-extra/pull/520)

4.0.2 / 2017-09-12
------------------

- Added `EOL` option to `writeJson*` & `outputJson*` (via upgrade to jsonfile v4)
- Added promise support to [`fs.copyFile()`](https://nodejs.org/api/fs.html#fs_fs_copyfile_src_dest_flags_callback) in Node 8.5+
- Added `.js` extension to `main` field in `package.json` for better tooling compatibility. [#485](https://github.com/jprichardson/node-fs-extra/pull/485)

4.0.1 / 2017-07-31
------------------

### Fixed

- Previously, `ensureFile()` & `ensureFileSync()` would do nothing if the path was a directory. Now, they error out for consistency with `ensureDir()`. [#465](https://github.com/jprichardson/node-fs-extra/issues/465), [#466](https://github.com/jprichardson/node-fs-extra/pull/466), [#470](https://github.com/jprichardson/node-fs-extra/issues/470)

4.0.0 / 2017-07-14
------------------

### Changed

- **BREAKING:** The promisified versions of `fs.read()` & `fs.write()` now return objects. See [the docs](docs/fs-read-write.md) for details. [#436](https://github.com/jprichardson/node-fs-extra/issues/436), [#449](https://github.com/jprichardson/node-fs-extra/pull/449)
- `fs.move()` now errors out when destination is a subdirectory of source. [#458](https://github.com/jprichardson/node-fs-extra/pull/458)
- Applied upstream fixes from `rimraf` to `fs.remove()` & `fs.removeSync()`. [#459](https://github.com/jprichardson/node-fs-extra/pull/459)

### Fixed

- Got `fs.outputJSONSync()` working again; it was broken due to refactoring. [#428](https://github.com/jprichardson/node-fs-extra/pull/428)

Also clarified the docs in a few places.

3.0.1 / 2017-05-04
------------------

- Fix bug in `move()` & `moveSync()` when source and destination are the same, and source does not exist. [#415](https://github.com/jprichardson/node-fs-extra/pull/415)

3.0.0 / 2017-04-27
------------------

### Added

- **BREAKING:** Added Promise support. All asynchronous native fs methods and fs-extra methods now return a promise if the callback is not passed. [#403](https://github.com/jprichardson/node-fs-extra/pull/403)
- `pathExists()`, a replacement for the deprecated `fs.exists`. `pathExists` has a normal error-first callback signature. Also added `pathExistsSync`, an alias to `fs.existsSync`, for completeness. [#406](https://github.com/jprichardson/node-fs-extra/pull/406)

### Removed

- **BREAKING:** Removed support for setting the default spaces for `writeJson()`, `writeJsonSync()`, `outputJson()`, & `outputJsonSync()`. This was undocumented. [#402](https://github.com/jprichardson/node-fs-extra/pull/402)

### Changed

- Upgraded jsonfile dependency to v3.0.0:
  - **BREAKING:** Changed behavior of `throws` option for `readJsonSync()`; now does not throw filesystem errors when `throws` is `false`.
- **BREAKING:** `writeJson()`, `writeJsonSync()`, `outputJson()`, & `outputJsonSync()` now output minified JSON by default for consistency with `JSON.stringify()`; set the `spaces` option to `2` to override this new behavior. [#402](https://github.com/jprichardson/node-fs-extra/pull/402)
- Use `Buffer.allocUnsafe()` instead of `new Buffer()` in environments that support it. [#394](https://github.com/jprichardson/node-fs-extra/pull/394)

### Fixed

- `removeSync()` silently failed on Windows in some cases. Now throws an `EBUSY` error. [#408](https://github.com/jprichardson/node-fs-extra/pull/408)

2.1.2 / 2017-03-16
------------------

### Fixed

- Weird windows bug that resulted in `ensureDir()`'s callback being called twice in some cases. This bug may have also affected `remove()`. See [#392](https://github.com/jprichardson/node-fs-extra/issues/392), [#393](https://github.com/jprichardson/node-fs-extra/pull/393)

2.1.1 / 2017-03-15
------------------

### Fixed

- Reverted [`5597bd`](https://github.com/jprichardson/node-fs-extra/commit/5597bd5b67f7d060f5f5bf26e9635be48330f5d7), this broke compatibility with Node.js versions v4+ but less than `v4.5.0`.
- Remove `Buffer.alloc()` usage in `moveSync()`.

2.1.0 / 2017-03-15
------------------

Thanks to [Mani Maghsoudlou (@manidlou)](https://github.com/manidlou) & [Jan Peer Stöcklmair (@JPeer264)](https://github.com/JPeer264) for their extraordinary help with this release!

### Added
- `moveSync()` See [#309], [#381](https://github.com/jprichardson/node-fs-extra/pull/381). ([@manidlou](https://github.com/manidlou))
- `copy()` and `copySync()`'s `filter` option now gets the destination path passed as the second parameter. [#366](https://github.com/jprichardson/node-fs-extra/pull/366) ([@manidlou](https://github.com/manidlou))

### Changed
- Use `Buffer.alloc()` instead of deprecated `new Buffer()` in `copySync()`. [#380](https://github.com/jprichardson/node-fs-extra/pull/380) ([@manidlou](https://github.com/manidlou))
- Refactored entire codebase to use ES6 features supported by Node.js v4+ [#355](https://github.com/jprichardson/node-fs-extra/issues/355). [(@JPeer264)](https://github.com/JPeer264)
- Refactored docs. ([@manidlou](https://github.com/manidlou))

### Fixed

- `move()` shouldn't error out when source and dest are the same. [#377](https://github.com/jprichardson/node-fs-extra/issues/377), [#378](https://github.com/jprichardson/node-fs-extra/pull/378) ([@jdalton](https://github.com/jdalton))

2.0.0 / 2017-01-16
------------------

### Removed
- **BREAKING:** Removed support for Node `v0.12`. The Node foundation stopped officially supporting it
on Jan 1st, 2017.
- **BREAKING:** Remove `walk()` and `walkSync()`. `walkSync()` was only part of `fs-extra` for a little
over two months. Use [klaw](https://github.com/jprichardson/node-klaw) instead of `walk()`, in fact, `walk()` was just
an alias to klaw. For `walkSync()` use [klaw-sync](https://github.com/mawni/node-klaw-sync). See: [#338], [#339]

### Changed
- **BREAKING:** Renamed `clobber` to `overwrite`. This affects `copy()`, `copySync()`, and `move()`. [#330], [#333]
- Moved docs, to `docs/`. [#340]

### Fixed
- Apply filters to directories in `copySync()` like in `copy()`. [#324]
- A specific condition when disk is under heavy use, `copy()` can fail. [#326]


1.0.0 / 2016-11-01
------------------

After five years of development, we finally have reach the 1.0.0 milestone! Big thanks goes
to [Ryan Zim](https://github.com/RyanZim) for leading the charge on this release!

### Added
- `walkSync()`

### Changed
- **BREAKING**: dropped Node v0.10 support.
- disabled `rimaf` globbing, wasn't used. [#280]
- deprecate `copy()/copySync()` option `filter` if it's a `RegExp`. `filter` should now be a function.
- inline `rimraf`. This is temporary and was done because `rimraf` depended upon the beefy `glob` which `fs-extra` does not use. [#300]

### Fixed
- bug fix proper closing of file handle on `utimesMillis()` [#271]
- proper escaping of files with dollar signs [#291]
- `copySync()` failed if user didn't own file. [#199], [#301]


0.30.0 / 2016-04-28
-------------------
- Brought back Node v0.10 support. I didn't realize there was still demand. Official support will end **2016-10-01**.

0.29.0 / 2016-04-27
-------------------
- **BREAKING**: removed support for Node v0.10. If you still want to use Node v0.10, everything should work except for `ensureLink()/ensureSymlink()`. Node v0.12 is still supported but will be dropped in the near future as well.

0.28.0 / 2016-04-17
-------------------
- **BREAKING**: removed `createOutputStream()`. Use https://www.npmjs.com/package/create-output-stream. See: [#192][#192]
- `mkdirs()/mkdirsSync()` check for invalid win32 path chars. See: [#209][#209], [#237][#237]
- `mkdirs()/mkdirsSync()` if drive not mounted, error. See: [#93][#93]

0.27.0 / 2016-04-15
-------------------
- add `dereference` option to `copySync()`. [#235][#235]

0.26.7 / 2016-03-16
-------------------
- fixed `copy()` if source and dest are the same. [#230][#230]

0.26.6 / 2016-03-15
-------------------
- fixed if `emptyDir()` does not have a callback: [#229][#229]

0.26.5 / 2016-01-27
-------------------
- `copy()` with two arguments (w/o callback) was broken. See: [#215][#215]

0.26.4 / 2016-01-05
-------------------
- `copySync()` made `preserveTimestamps` default consistent with `copy()` which is `false`. See: [#208][#208]

0.26.3 / 2015-12-17
-------------------
- fixed `copy()` hangup in copying blockDevice / characterDevice / `/dev/null`. See: [#193][#193]

0.26.2 / 2015-11-02
-------------------
- fixed `outputJson{Sync}()` spacing adherence to `fs.spaces`

0.26.1 / 2015-11-02
-------------------
- fixed `copySync()` when `clogger=true` and the destination is read only. See: [#190][#190]

0.26.0 / 2015-10-25
-------------------
- extracted the `walk()` function into its own module [`klaw`](https://github.com/jprichardson/node-klaw).

0.25.0 / 2015-10-24
-------------------
- now has a file walker `walk()`

0.24.0 / 2015-08-28
-------------------
- removed alias `delete()` and `deleteSync()`. See: [#171][#171]

0.23.1 / 2015-08-07
-------------------
- Better handling of errors for `move()` when moving across devices. [#170][#170]
- `ensureSymlink()` and `ensureLink()` should not throw errors if link exists. [#169][#169]

0.23.0 / 2015-08-06
-------------------
- added `ensureLink{Sync}()` and `ensureSymlink{Sync}()`. See: [#165][#165]

0.22.1 / 2015-07-09
-------------------
- Prevent calling `hasMillisResSync()` on module load. See: [#149][#149].
Fixes regression that was introduced in `0.21.0`.

0.22.0 / 2015-07-09
-------------------
- preserve permissions / ownership in `copy()`. See: [#54][#54]

0.21.0 / 2015-07-04
-------------------
- add option to preserve timestamps in `copy()` and `copySync()`. See: [#141][#141]
- updated `graceful-fs@3.x` to `4.x`. This brings in features from `amazing-graceful-fs` (much cleaner code / less hacks)

0.20.1 / 2015-06-23
-------------------
- fixed regression caused by latest jsonfile update: See: https://github.com/jprichardson/node-jsonfile/issues/26

0.20.0 / 2015-06-19
-------------------
- removed `jsonfile` aliases with `File` in the name, they weren't documented and probably weren't in use e.g.
this package had both `fs.readJsonFile` and `fs.readJson` that were aliases to each other, now use `fs.readJson`.
- preliminary walker created. Intentionally not documented. If you use it, it will almost certainly change and break your code.
- started moving tests inline
- upgraded to `jsonfile@2.1.0`, can now pass JSON revivers/replacers to `readJson()`, `writeJson()`, `outputJson()`

0.19.0 / 2015-06-08
-------------------
- `fs.copy()` had support for Node v0.8, dropped support

0.18.4 / 2015-05-22
-------------------
- fixed license field according to this: [#136][#136] and https://github.com/npm/npm/releases/tag/v2.10.0

0.18.3 / 2015-05-08
-------------------
- bugfix: handle `EEXIST` when clobbering on some Linux systems. [#134][#134]

0.18.2 / 2015-04-17
-------------------
- bugfix: allow `F_OK` ([#120][#120])

0.18.1 / 2015-04-15
-------------------
- improved windows support for `move()` a bit. https://github.com/jprichardson/node-fs-extra/commit/92838980f25dc2ee4ec46b43ee14d3c4a1d30c1b
- fixed a lot of tests for Windows (appveyor)

0.18.0 / 2015-03-31
-------------------
- added `emptyDir()` and `emptyDirSync()`

0.17.0 / 2015-03-28
-------------------
- `copySync` added `clobber` option (before always would clobber, now if `clobber` is `false` it throws an error if the destination exists).
**Only works with files at the moment.**
- `createOutputStream('use strict';
const path = require('path');
const os = require('os');

const homedir = os.homedir();
const tmpdir = os.tmpdir();
const {env} = process;

const macos = name => {
	const library = path.join(homedir, 'Library');

	return {
		data: path.join(library, 'Application Support', name),
		config: path.join(library, 'Preferences', name),
		cache: path.join(library, 'Caches', name),
		log: path.join(library, 'Logs', name),
		temp: path.join(tmpdir, name)
	};
};

const windows = name => {
	const appData = env.APPDATA || path.join(homedir, 'AppData', 'Roaming');
	const localAppData = env.LOCALAPPDATA || path.join(homedir, 'AppData', 'Local');

	return {
		// Data/config/cache/log are invented by me as Windows isn't opinionated about this
		data: path.join(localAppData, name, 'Data'),
		config: path.join(appData, name, 'Config'),
		cache: path.join(localAppData, name, 'Cache'),
		log: path.join(localAppData, name, 'Log'),
		temp: path.join(tmpdir, name)
	};
};

// https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
const linux = name => {
	const username = path.basename(homedir);

	return {
		data: path.join(env.XDG_DATA_HOME || path.join(homedir, '.local', 'share'), name),
		config: path.join(env.XDG_CONFIG_HOME || path.join(homedir, '.config'), name),
		cache: path.join(env.XDG_CACHE_HOME || path.join(homedir, '.cache'), name),
		// https://wiki.debian.org/XDGBaseDirectorySpecification#state
		log: path.join(env.XDG_STATE_HOME || path.join(homedir, '.local', 'state'), name),
		temp: path.join(tmpdir, username, name)
	};
};

const envPaths = (name, options) => {
	if (typeof name !== 'string') {
		throw new TypeError(`Expected string, got ${typeof name}`);
	}

	options = Object.assign({suffix: 'nodejs'}, options);

	if (options.suffix) {
		// Add suffix to prevent possible conflict with native apps
		name += `-${options.suffix}`;
	}

	if (process.platform === 'darwin') {
		return macos(name);
	}

	if (process.platform === 'win32') {
		return windows(name);
	}

	return linux(name);
};

module.exports = envPaths;
// TODO: Remove this for the next major release
module.exports.default = envPaths;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Copyright (c) 2007-present, Alexandru Mărășteanu <hello@alexei.ro>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name of this software nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            