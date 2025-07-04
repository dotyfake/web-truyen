/**
 * The `node:v8` module exposes APIs that are specific to the version of [V8](https://developers.google.com/v8/) built into the Node.js binary. It can be accessed using:
 *
 * ```js
 * import v8 from 'node:v8';
 * ```
 * @see [source](https://github.com/nodejs/node/blob/v18.19.0/lib/v8.js)
 */
declare module "v8" {
    import { Readable } from "node:stream";
    interface HeapSpaceInfo {
        space_name: string;
        space_size: number;
        space_used_size: number;
        space_available_size: number;
        physical_space_size: number;
    }
    // ** Signifies if the --zap_code_space option is enabled or not.  1 == enabled, 0 == disabled. */
    type DoesZapCodeSpaceFlag = 0 | 1;
    interface HeapInfo {
        total_heap_size: number;
        total_heap_size_executable: number;
        total_physical_size: number;
        total_available_size: number;
        used_heap_size: number;
        heap_size_limit: number;
        malloced_memory: number;
        peak_malloced_memory: number;
        does_zap_garbage: DoesZapCodeSpaceFlag;
        number_of_native_contexts: number;
        number_of_detached_contexts: number;
        total_global_handles_size: number;
        used_global_handles_size: number;
        external_memory: number;
    }
    interface HeapCodeStatistics {
        code_and_metadata_size: number;
        bytecode_and_metadata_size: number;
        external_script_source_size: number;
    }
    /**
     * Returns an integer representing a version tag derived from the V8 version,
     * command-line flags, and detected CPU features. This is useful for determining
     * whether a `vm.Script` `cachedData` buffer is compatible with this instance
     * of V8.
     *
     * ```js
     * console.log(v8.cachedDataVersionTag()); // 3947234607
     * // The value returned by v8.cachedDataVersionTag() is derived from the V8
     * // version, command-line flags, and detected CPU features. Test that the value
     * // does indeed update when flags are toggled.
     * v8.setFlagsFromString('--allow_natives_syntax');
     * console.log(v8.cachedDataVersionTag()); // 183726201
     * ```
     * @since v8.0.0
     */
    function cachedDataVersionTag(): number;
    /**
     * Returns an object with the following properties:
     *
     * `does_zap_garbage` is a 0/1 boolean, which signifies whether the`--zap_code_space` option is enabled or not. This makes V8 overwrite heap
     * garbage with a bit pattern. The RSS footprint (resident set size) gets bigger
     * because it continuously touches all heap pages and that makes them less likely
     * to get swapped out by the operating system.
     *
     * `number_of_native_contexts` The value of native\_context is the number of the
     * top-level contexts currently active. Increase of this number over time indicates
     * a memory leak.
     *
     * `number_of_detached_contexts` The value of detached\_context is the number
     * of contexts that were detached and not yet garbage collected. This number
     * being non-zero indicates a potential memory leak.
     *
     * `total_global_handles_size` The value of total\_global\_handles\_size is the
     * total memory size of V8 global handles.
     *
     * `used_global_handles_size` The value of used\_global\_handles\_size is the
     * used memory size of V8 global handles.
     *
     * `external_memory` The value of external\_memory is the memory size of array
     * buffers and external strings.
     *
     * ```js
     * {
     *   total_heap_size: 7326976,
     *   total_heap_size_executable: 4194304,
     *   total_physical_size: 7326976,
     *   total_available_size: 1152656,
     *   used_heap_size: 3476208,
     *   heap_size_limit: 1535115264,
     *   malloced_memory: 16384,
     *   peak_malloced_memory: 1127496,
     *   does_zap_garbage: 0,
     *   number_of_native_contexts: 1,
     *   number_of_detached_contexts: 0,
     *   total_global_handles_size: 8192,
     *   used_global_handles_size: 3296,
     *   external_memory: 318824
     * }
     * ```
     * @since v1.0.0
     */
    function getHeapStatistics(): HeapInfo;
    /**
     * Returns statistics about the V8 heap spaces, i.e. the segments which make up
     * the V8 heap. Neither the ordering of heap spaces, nor the availability of a
     * heap space can be guaranteed as the statistics are provided via the
     * V8 [`GetHeapSpaceStatistics`](https://v8docs.nodesource.com/node-13.2/d5/dda/classv8_1_1_isolate.html#ac673576f24fdc7a33378f8f57e1d13a4) function and may change from one V8 version to the
     * next.
     *
     * The value returned is an array of objects containing the following properties:
     *
     * ```json
     * [
     *   {
     *     "space_name": "new_space",
     *     "space_size": 2063872,
     *     "space_used_size": 951112,
     *     "space_available_size": 80824,
     *     "physical_space_size": 2063872
     *   },
     *   {
     *     "space_name": "old_space",
     *     "space_size": 3090560,
     *     "space_used_size": 2493792,
     *     "space_available_size": 0,
     *     "physical_space_size": 3090560
     *   },
     *   {
     *     "space_name": "code_space",
     *     "space_size": 1260160,
     *     "space_used_size": 644256,
     *     "space_available_size": 960,
     *     "physical_space_size": 1260160
     *   },
     *   {
     *     "space_name": "map_space",
     *     "space_size": 1094160,
     *     "space_used_size": 201608,
     *     "space_available_size": 0,
     *     "physical_space_size": 1094160
     *   },
     *   {
     *     "space_name": "large_object_space",
     *     "space_size": 0,
     *     "space_used_size": 0,
     *     "space_available_size": 1490980608,
     *     "physical_space_size": 0
     *   }
     * ]
     * ```
     * @since v6.0.0
     */
    function getHeapSpaceStatistics(): HeapSpaceInfo[];
    /**
     * The `v8.setFlagsFromString()` method can be used to programmatically set
     * V8 command-line flags. This method should be used with care. Changing settings
     * after the VM has started may result in unpredictable behavior, including
     * crashes and data loss; or it may simply do nothing.
     *
     * The V8 options available for a version of Node.js may be determined by running`node --v8-options`.
     *
     * Usage:
     *
     * ```js
     * // Print GC events to stdout for one minute.
     * import v8 from 'node:v8';
     * v8.setFlagsFromString('--trace_gc');
     * setTimeout(() => { v8.setFlagsFromString('--notrace_gc'); }, 60e3);
     * ```
     * @since v1.0.0
     */
    function setFlagsFromString(flags: string): void;
    /**
     * Generates a snapshot of the current V8 heap and returns a Readable
     * Stream that may be used to read the JSON serialized representation.
     * This JSON stream format is intended to be used with tools such as
     * Chrome DevTools. The JSON schema is undocumented and specific to the
     * V8 engine. Therefore, the schema may change from one version of V8 to the next.
     *
     * Creating a heap snapshot requires memory about twice the size of the heap at
     * the time the snapshot is created. This results in the risk of OOM killers
     * terminating the process.
     *
     * Generating a snapshot is a synchronous operation which blocks the event loop
     * for a duration depending on the heap size.
     *
     * ```js
     * // Print heap snapshot to the console
     * import v8 from 'node:v8';
     * const stream = v8.getHeapSnapshot();
     * stream.pipe(process.stdout);
     * ```
     * @since v11.13.0
     * @return A Readable Stream containing the V8 heap snapshot
     */
    function getHeapSnapshot(): Readable;
    /**
     * Generates a snapshot of the current V8 heap and writes it to a JSON
     * file. This file is intended to be used with tools such as Chrome
     * DevTools. The JSON schema is undocumented and specific to the V8
     * engine, and may change from one version of V8 to the next.
     *
     * A heap snapshot is specific to a single V8 isolate. When using `worker threads`, a heap snapshot generated from the main thread will
     * not contain any information about the workers, and vice versa.
     *
     * Creating a heap snapshot requires memory about twice the size of the heap at
     * the time the snapshot is created. This results in the risk of OOM killers
     * terminating the process.
     *
     * Generating a snapshot is a synchronous operation which blocks the event loop
     * for a duration depending on the heap size.
     *
     * ```js
     * import { writeHeapSnapshot } from 'node:v8';
     * import {
     *   Worker,
     *   isMainThread,
     *   parentPort,
     * } from 'node:worker_threads';
     *
     * if (isMainThread) {
     *   const worker = new Worker(__filename);
     *
     *   worker.once('message', (filename) => {
     *     console.log(`worker heapdump: ${filename}`);
     *     // Now get a heapdump for the main thread.
     *     console.log(`main thread heapdump: ${writeHeapSnapshot()}`);
     *   });
     *
     *   // Tell the worker to create a heapdump.
     *   worker.postMessage('heapdump');
     * } else {
     *   parentPort.once('message', (message) => {
     *     if (message === 'heapdump') {
     *       // Generate a heapdump for the worker
     *       // and return the filename to the parent.
     *       parentPort.postMessage(writeHeapSnapshot());
     *     }
     *   });
     * }
     * ```
     * @since v11.13.0
     * @param filename The file path where the V8 heap snapshot is to be saved. If not specified, a file name with the pattern `'Heap-${yyyymmdd}-${hhmmss}-${pid}-${thread_id}.heapsnapshot'` will be
     * generated, where `{pid}` will be the PID of the Node.js process, `{thread_id}` will be `0` when `writeHeapSnapshot()` is called from the main Node.js thread or the id of a
     * worker thread.
     * @return The filename where the snapshot was saved.
     */
    function writeHeapSnapshot(filename?: string): string;
    /**
     * Get statistics about code and its metadata in the heap, see
     * V8 [`GetHeapCodeAndMetadataStatistics`](https://v8docs.nodesource.com/node-13.2/d5/dda/classv8_1_1_isolate.html#a6079122af17612ef54ef3348ce170866) API. Returns an object with the
     * following properties:
     *
     * ```js
     * {
     *   code_and_metadata_size: 212208,
     *   bytecode_and_metadata_size: 161368,
     *   external_script_source_size: 1410794,
     *   cpu_profiler_metadata_size: 0,
     * }
     * ```
     * @since v12.8.0
     */
    function getHeapCodeStatistics(): HeapCodeStatistics;
    /**
     * @since v8.0.0
     */
    class Serializer {
        /**
         * Writes out a header, which includes the serialization format version.
         */
        writeHeader(): void;
        /**
         * Serializes a JavaScript value and adds the serialized representation to the
         * internal buffer.
         *
         * This throws an error if `value` cannot be serialized.
         */
        writeValue(val: any): boolean;
        /**
         * Returns the stored internal buffer. This serializer should not be used once
         * the buffer is released. Calling this method results in undefined behavior
         * if a previous write has failed.
         */
        releaseBuffer(): Buffer;
        /**
         * Marks an `ArrayBuffer` as having its contents transferred out of band.
         * Pass the corresponding `ArrayBuffer` in the deserializing context to `deserializer.transferArrayBuffer()`.
         * @param id A 32-bit unsigned integer.
         * @param arrayBuffer An `ArrayBuffer` instance.
         */
        transferArrayBuffer(id: number, arrayBuffer: ArrayBuffer): void;
        /**
         * Write a raw 32-bit unsigned integer.
         * For use inside of a custom `serializer._writeHostObject()`.
         */
        writeUint32(value: number): void;
        /**
         * Write a raw 64-bit unsigned integer, split into high and low 32-bit parts.
         * For use inside of a custom `serializer._writeHostObject()`.
         */
        writeUint64(hi: number, lo: number): void;
        /**
         * Write a JS `number` value.
         * For use inside of a custom `serializer._writeHostObject()`.
         */
        writeDouble(value: number): void;
        /**
         * Write raw bytes into the serializer's internal buffer. The deserializer
         * will require a way to compute the length of the buffer.
         * For use inside of a custom `serializer._writeHostObject()`.
         */
        writeRawBytes(buffer: NodeJS.TypedArray): void;
    }
    /**
     * A subclass of `Serializer` that serializes `TypedArray`(in particular `Buffer`) and `DataView` objects as host objects, and only
     * stores the part of their underlying `ArrayBuffer`s that they are referring to.
     * @since v8.0.0
     */
    class DefaultSerializer extends Serializer {}
    /**
     * @since v8.0.0
     */
    class Deserializer {
        constructor(data: NodeJS.TypedArray);
        /**
         * Reads and validates a header (including the format version).
         * May, for example, reject an invalid or unsupported wire format. In that case,
         * an `Error` is thrown.
         */
        readHeader(): boolean;
        /**
         * Deserializes a JavaScript value from the buffer and returns it.
         */
        readValue(): any;
        /**
         * Marks an `ArrayBuffer` as having its contents transferred out of band.
         * Pass the corresponding `ArrayBuffer` in the serializing context to `serializer.transferArrayBuffer()` (or return the `id` from `serializer._getSharedArrayBufferId()` in the case of
         * `SharedArrayBuffer`s).
         * @param id A 32-bit unsigned integer.
         * @param arrayBuffer An `ArrayBuffer` instance.
         */
        transferArrayBuffer(id: number, arrayBuffer: ArrayBuffer): void;
        /**
         * Reads the underlying wire format version. Likely mostly to be useful to
         * legacy code reading old wire format versions. May not be called before`.readHeader()`.
         */
        getWireFormatVersion(): number;
        /**
         * Read a raw 32-bit unsigned integer and return it.
         * For use inside of a custom `deserializer._readHostObject()`.
         */
        readUint32(): number;
        /**
         * Read a raw 64-bit unsigned integer and return it as an array `[hi, lo]`with two 32-bit unsigned integer entries.
         * For use inside of a custom `deserializer._readHostObject()`.
         */
        readUint64(): [number, number];
        /**
         * Read a JS `number` value.
         * For use inside of a custom `deserializer._readHostObject()`.
         */
        readDouble(): number;
        /**
         * Read raw bytes from the deserializer's internal buffer. The `length` parameter
         * must correspond to the length of the buffer that was passed to `serializer.writeRawBytes()`.
         * For use inside of a custom `deserializer._readHostObject()`.
         */
        readRawBytes(length: number): Buffer;
    }
    /**
     * A subclass of `Deserializer` corresponding to the format written by `DefaultSerializer`.
     * @since v8.0.0
     */
    class DefaultDeserializer extends Deserializer {}
    /**
     * Uses a `DefaultSerializer` to serialize `value` into a buffer.
     *
     * `ERR_BUFFER_TOO_LARGE` will be thrown when trying to
     * serialize a huge object which requires buffer
     * larger than `buffer.constants.MAX_LENGTH`.
     * @since v8.0.0
     */
    function serialize(value: any): Buffer;
    /**
     * Uses a `DefaultDeserializer` with default options to read a JS value
     * from a buffer.
     * @since v8.0.0
     * @param buffer A buffer returned by {@link serialize}.
     */
    function deserialize(buffer: NodeJS.ArrayBufferView): any;
    /**
     * The `v8.takeCoverage()` method allows the user to write the coverage started by `NODE_V8_COVERAGE` to disk on demand. This method can be invoked multiple
     * times during the lifetime of the process. Each time the execution counter will
     * be reset and a new coverage report will be written to the directory specified
     * by `NODE_V8_COVERAGE`.
     *
     * When the process is about to exit, one last coverage will still be written to
     * disk unless {@link stopCoverage} is invoked before the process exits.
     * @since v15.1.0, v14.18.0, v12.22.0
     */
    function takeCoverage(): void;
    /**
     * The `v8.stopCoverage()` method allows the user to stop the coverage collection
     * started by `NODE_V8_COVERAGE`, so that V8 can release the execution count
     * records and optimize code. This can be used in conjunction with {@link takeCoverage} if the user wants to collect the coverage on demand.
     * @since v15.1.0, v14.18.0, v12.22.0
     */
    function stopCoverage(): void;
    /**
     * The API is a no-op if `--heapsnapshot-near-heap-limit` is already set from the command line or the API is called more than once.
     * `limit` must be a positive integer. See [`--heapsnapshot-near-heap-limit`](https://nodejs.org/docs/latest-v18.x/api/cli.html#--heapsnapshot-near-heap-limitmax_count) for more information.
     * @experimental
     * @since v18.10.0, v16.18.0
     */
    function setHeapSnapshotNearHeapLimit(limit: number): void;
    /**
     * This API collects GC data in current thread.
     * @since v18.15.0
     */
    class GCProfiler {
        /**
         * Start collecting GC data.
         * @since v18.15.0
         */
        start(): void;
        /**
         * Stop collecting GC data and return an object.The content of object
         * is as follows.
         *
         * ```json
         * {
         *   "version": 1,
         *   "startTime": 1674059033862,
         *   "statistics": [
         *     {
         *       "gcType": "Scavenge",
         *       "beforeGC": {
         *         "heapStatistics": {
         *           "totalHeapSize": 5005312,
         *           "totalHeapSizeExecutable": 524288,
         *           "totalPhysicalSize": 5226496,
         *           "totalAvailableSize": 4341325216,
         *           "totalGlobalHandlesSize": 8192,
         *           "usedGlobalHandlesSize": 2112,
         *           "usedHeapSize": 4883840,
         *           "heapSizeLimit": 4345298944,
         *           "mallocedMemory": 254128,
         *           "externalMemory": 225138,
         *           "peakMallocedMemory": 181760
         *         },
         *         "heapSpaceStatistics": [
         *           {
         *             "spaceName": "read_only_space",
         *             "spaceSize": 0,
         *             "spaceUsedSize": 0,
         *             "spaceAvailableSize": 0,
         *             "physicalSpaceSize": 0
         *           }
         *         ]
         *       },
         *       "cost": 1574.14,
         *       "afterGC": {
         *         "heapStatistics": {
         *           "totalHeapSize": 6053888,
         *           "totalHeapSizeExecutable": 524288,
         *           "totalPhysicalSize": 5500928,
         *           "totalAvailableSize": 4341101384,
         *           "totalGlobalHandlesSize": 8192,
         *           "usedGlobalHandlesSize": 2112,
         *           "usedHeapSize": 4059096,
         *           "heapSizeLimit": 4345298944,
         *           "mallocedMemory": 254128,
         *           "externalMemory": 225138,
         *           "peakMallocedMemory": 181760
         *         },
         *         "heapSpaceStatistics": [
         *           {
         *             "spaceName": "read_only_space",
         *             "spaceSize": 0,
         *             "spaceUsedSize": 0,
         *             "spaceAvailableSize": 0,
         *             "physicalSpaceSize": 0
         *           }
         *         ]
         *       }
         *     }
         *   ],
         *   "endTime": 1674059036865
         * }
         * ```
         *
         * Here's an example.
         *
         * ```js
         * import { GCProfiler } from 'node:v8';
         * const profiler = new GCProfiler();
         * profiler.start();
         * setTimeout(() => {
         *   console.log(profiler.stop());
         * }, 1000);
         * ```
         * @since v18.15.0
         */
        stop(): GCProfilerResult;
    }
    interface GCProfilerResult {
        version: number;
        startTime: number;
        endTime: number;
        statistics: Array<{
            gcType: string;
            cost: number;
            beforeGC: {
                heapStatistics: HeapStatistics;
                heapSpaceStatistics: HeapSpaceStatistics[];
            };
            afterGC: {
                heapStatistics: HeapStatistics;
                heapSpaceStatistics: HeapSpaceStatistics[];
            };
        }>;
    }
    interface HeapStatistics {
        totalHeapSize: number;
        totalHeapSizeExecutable: number;
        totalPhysicalSize: number;
        totalAvailableSize: number;
        totalGlobalHandlesSize: number;
        usedGlobalHandlesSize: number;
        usedHeapSize: number;
        heapSizeLimit: number;
        mallocedMemory: number;
        externalMemory: number;
        peakMallocedMemory: number;
    }
    interface HeapSpaceStatistics {
        spaceName: string;
        spaceSize: number;
        spaceUsedSize: number;
        spaceAvailableSize: number;
        physicalSpaceSize: number;
    }
    /**
     * Called when a promise is constructed. This does not mean that corresponding before/after events will occur, only that the possibility exists. This will
     * happen if a promise is created without ever getting a continuation.
     * @since v17.1.0, v16.14.0
     * @param promise The promise being created.
     * @param parent The promise continued from, if applicable.
     */
    interface Init {
        (promise: Promise<unknown>, parent: Promise<unknown>): void;
    }
    /**
     * Called before a promise continuation executes. This can be in the form of `then()`, `catch()`, or `finally()` handlers or an await resuming.
     *
     * The before callback will be called 0 to N times. The before callback will typically be called 0 times if no continuation was ever made for the promise.
     * The before callback may be called many times in the case where many continuations have been made from the same promise.
     * @since v17.1.0, v16.14.0
     */
    interface Before {
        (promise: Promise<unknown>): void;
    }
    /**
     * Called immediately after a promise continuation executes. This may be after a `then()`, `catch()`, or `finally()` handler or before an await after another await.
     * @since v17.1.0, v16.14.0
     */
    in