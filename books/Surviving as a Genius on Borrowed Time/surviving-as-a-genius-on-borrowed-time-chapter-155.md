t to the other party.
         * If the server wishes to hide the fact that the PSK identity was not known,
         * the callback must provide some random data as `psk` to make the connection
         * fail with "decrypt_error" before negotiation is finished.
         * PSK ciphers are disabled by default, and using TLS-PSK thus
         * requires explicitly specifying a cipher suite with the `ciphers` option.
         * More information can be found in the RFC 4279.
         */
        pskCallback?(socket: TLSSocket, identity: string): DataView | NodeJS.TypedArray | null;
        /**
         * hint to send to a client to help
         * with selecting the identity during TLS-PSK negotiation. Will be ignored
         * in TLS 1.3. Upon failing to set pskIdentityHint `tlsClientError` will be
         * emitted with `ERR_TLS_PSK_SET_IDENTIY_HINT_FAILED` code.
         */
        pskIdentityHint?: string | undefined;
    }
    interface PSKCallbackNegotation {
        psk: DataView | NodeJS.TypedArray;
        identity: string;
    }
    interface ConnectionOptions extends SecureContextOptions, CommonConnectionOptions {
        host?: string | undefined;
        port?: number | undefined;
        path?: string | undefined; // Creates unix socket connection to path. If this option is specified, `host` and `port` are ignored.
        socket?: stream.Duplex | undefined; // Establish secure connection on a given socket rather than creating a new socket
        checkServerIdentity?: typeof checkServerIdentity | undefined;
        servername?: string | undefined; // SNI TLS Extension
        session?: Buffer | undefined;
        minDHSize?: number | undefined;
        lookup?: net.LookupFunction | undefined;
        timeout?: number | undefined;
        /**
         * When negotiating TLS-PSK (pre-shared keys), this function is called
         * with optional identity `hint` provided by the server or `null`
         * in case of TLS 1.3 where `hint` was removed.
         * It will be necessary to provide a custom `tls.checkServerIdentity()`
         * for the connection as the default one will try to check hostname/IP
         * of the server against the certificate but that's not applicable for PSK
         * because there won't be a certificate present.
         * More information can be found in the RFC 4279.
         *
         * @param hint message sent from the server to help client
         * decide which identity to use during negotiation.
         * Always `null` if TLS 1.3 is used.
         * @returns Return `null` to stop the negotiation process. `psk` must be
         * compatible with the selected cipher's digest.
         * `identity` must use UTF-8 encoding.
         */
        pskCallback?(hint: string | null): PSKCallbackNegotation | null;
    }
    /**
     * Accepts encrypted connections using TLS or SSL.
     * @since v0.3.2
     */
    class Server extends net.Server {
        constructor(secureConnectionListener?: (socket: TLSSocket) => void);
        constructor(options: TlsOptions, secureConnectionListener?: (socket: TLSSocket) => void);
        /**
         * The `server.addContext()` method adds a secure context that will be used if
         * the client request's SNI name matches the supplied `hostname` (or wildcard).
         *
         * When there are multiple matching contexts, the most recently added one is
         * used.
         * @since v0.5.3
         * @param hostname A SNI host name or wildcard (e.g. `'*'`)
         * @param context An object containing any of the possible properties from the {@link createSecureContext} `options` arguments (e.g. `key`, `cert`, `ca`, etc), or a TLS context object created
         * with {@link createSecureContext} itself.
         */
        addContext(hostname: string, context: SecureContextOptions | SecureContext): void;
        /**
         * Returns the session ticket keys.
         *
         * See `Session Resumption` for more information.
         * @since v3.0.0
         * @return A 48-byte buffer containing the session ticket keys.
         */
        getTicketKeys(): Buffer;
        /**
         * The `server.setSecureContext()` method replaces the secure context of an
         * existing server. Existing connections to the server are not interrupted.
         * @since v11.0.0
         * @param options An object containing any of the possible properties from the {@link createSecureContext} `options` arguments (e.g. `key`, `cert`, `ca`, etc).
         */
        setSecureContext(options: SecureContextOptions): void;
        /**
         * Sets the session ticket keys.
         *
         * Changes to the ticket keys are effective only for future server connections.
         * Existing or currently pending server connections will use the previous keys.
         *
         * See `Session Resumption` for more information.
         * @since v3.0.0
         * @param keys A 48-byte buffer containing the session ticket keys.
         */
        setTicketKeys(keys: Buffer): void;
        /**
         * events.EventEmitter
         * 1. tlsClientError
         * 2. newSession
         * 3. OCSPRequest
         * 4. resumeSession
         * 5. secureConnection
         * 6. keylog
         */
        addListener(event: string, listener: (...args: any[]) => void): this;
        addListener(event: "tlsClientError", listener: (err: Error, tlsSocket: TLSSocket) => void): this;
        addListener(
            event: "newSession",
            listener: (sessionId: Buffer, sessionData: Buffer, callback: () => void) => void,
        ): this;
        addListener(
            event: "OCSPRequest",
            listener: (
                certificate: Buffer,
                issuer: Buffer,
                callback: (err: Error | null, resp: Buffer) => void,
            ) => void,
        ): this;
        addListener(
            event: "resumeSession",
            listener: (sessionId: Buffer, callback: (err: Error | null, sessionData: Buffer | null) => void) => void,
        ): this;
        addListener(event: "secureConnection", listener: (tlsSocket: TLSSocket) => void): this;
        addListener(event: "keylog", listener: (line: Buffer, tlsSocket: TLSSocket) => void): this;
        emit(event: string | symbol, ...args: any[]): boolean;
        emit(event: "tlsClientError", err: Error, tlsSocket: TLSSocket): boolean;
        emit(event: "newSession", sessionId: Buffer, sessionData: Buffer, callback: () => void): boolean;
        emit(
            event: "OCSPRequest",
            certificate: Buffer,
            issuer: Buffer,
            callback: (err: Error | null, resp: Buffer) => void,
        ): boolean;
        emit(
            event: "resumeSession",
            sessionId: Buffer,
            callback: (err: Error | null, sessionData: Buffer | null) => void,
        ): boolean;
        emit(event: "secureConnection", tlsSocket: TLSSocket): boolean;
        emit(event: "keylog", line: Buffer, tlsSocket: TLSSocket): boolean;
        on(event: string, listener: (...args: any[]) => void): this;
        on(event: "tlsClientError", listener: (err: Error, tlsSocket: TLSSocket) => void): this;
        on(event: "newSession", listener: (sessionId: Buffer, sessionData: Buffer, callback: () => void) => void): this;
        on(
            event: "OCSPRequest",
            listener: (
                certificate: Buffer,
                issuer: Buffer,
                callback: (err: Error | null, resp: Buffer) => void,
            ) => void,
        ): this;
        on(
            event: "resumeSession",
            listener: (sessionId: Buffer, callback: (err: Error | null, sessionData: Buffer | null) => void) => void,
        ): this;
        on(event: "secureConnection", listener: (tlsSocket: TLSSocket) => void): this;
        on(event: "keylog", listener: (line: Buffer, tlsSocket: TLSSocket) => void): this;
        once(event: string, listener: (...args: any[]) => void): this;
        once(event: "tlsClientError", listener: (err: Error, tlsSocket: TLSSocket) => void): this;
        once(
            event: "newSession",
            listener: (sessionId: Buffer, sessionData: Buffer, callback: () => void) => void,
        ): this;
        once(
            event: "OCSPRequest",
            listener: (
                certificate: Buffer,
                issuer: Buffer,
                callback: (err: Error | null, resp: Buffer) => void,
            ) => void,
        ): this;
        once(
            event: "resumeSession",
            listener: (sessionId: Buffer, callback: (err: Error | null, sessionData: Buffer | null) => void) => void,
        ): this;
        once(event: "secureConnection", listener: (tlsSocket: TLSSocket) => void): this;
        once(event: "keylog", listener: (line: Buffer, tlsSocket: TLSSocket) => void): this;
        prependListener(event: string, listener: (...args: any[]) => void): this;
        prependListener(event: "tlsClientError", listener: (err: Error, tlsSocket: TLSSocket) => void): this;
        prependListener(
            event: "newSession",
            listener: (sessionId: Buffer, sessionData: Buffer, callback: () => void) => void,
        ): this;
        prependListener(
            event: "OCSPRequest",
            listener: (
                certificate: Buffer,
                issuer: Buffer,
                callback: (err: Error | null, resp: Buffer) => void,
            ) => void,
        ): this;
        prependListener(
            event: "resumeSession",
            listener: (sessionId: Buffer, callback: (err: Error | null, sessionData: Buffer | null) => void) => void,
        ): this;
        prependListener(event: "secureConnection", listener: (tlsSocket: TLSSocket) => void): this;
        prependListener(event: "keylog", listener: (line: Buffer, tlsSocket: TLSSocket) => void): this;
        prependOnceListener(event: string, listener: (...args: any[]) => void): this;
        prependOnceListener(event: "tlsClientError", listener: (err: Error, tlsSocket: TLSSocket) => void): this;
        prependOnceListener(
            event: "newSession",
            listener: (sessionId: Buffer, sessionData: Buffer, callback: () => void) => void,
        ): this;
        prependOnceListener(
            event: "OCSPRequest",
            listener: (
                certificate: Buffer,
                issuer: Buffer,
                callback: (err: Error | null, resp: Buffer) => void,
            ) => void,
        ): this;
        prependOnceListener(
            event: "resumeSession",
            listener: (sessionId: Buffer, callback: (err: Error | null, sessionData: Buffer | null) => void) => void,
        ): this;
        prependOnceListener(event: "secureConnection", listener: (tlsSocket: TLSSocket) => void): this;
        prependOnceListener(event: "keylog", listener: (line: Buffer, tlsSocket: TLSSocket) => void): this;
    }
    /**
     * @deprecated since v0.11.3 Use `tls.TLSSocket` instead.
     */
    interface SecurePair {
        encrypted: TLSSocket;
        cleartext: TLSSocket;
    }
    type SecureVersion = "TLSv1.3" | "TLSv1.2" | "TLSv1.1" | "TLSv1";
    interface SecureContextOptions {
        /**
         * If set, this will be called when a client opens a connection using the ALPN extension.
         * One argument will be passed to the callback: an object containing `servername` and `protocols` fields,
         * respectively containing the server name from the SNI extension (if any) and an array of
         * ALPN protocol name strings. The callback must return either one of the strings listed in `protocols`,
         * which will be returned to the client as the selected ALPN protocol, or `undefined`,
         * to reject the connection with a fatal alert. If a string is returned that does not match one of
         * the client's ALPN protocols, an error will be thrown.
         * This option cannot be used with the `ALPNProtocols` option, and setting both options will throw an error.
         * @since v18.19.0
         */
        ALPNCallback?: ((arg: { servername: string; protocols: string[] }) => string | undefined) | undefined;
        /**
         * Optionally override the trusted CA certificates. Default is to trust
         * the well-known CAs curated by Mozilla. Mozilla's CAs are completely
         * replaced when CAs are explicitly specified using this option.
         */
        ca?: string | Buffer | Array<string | Buffer> | undefined;
        /**
         *  Cert chains in PEM format. One cert chain should be provided per
         *  private key. Each cert chain should consist of the PEM formatted
         *  certificate for a provided private key, followed by the PEM
         *  formatted intermediate certificates (if any), in order, and not
         *  including the root CA (the root CA must be pre-known to the peer,
         *  see ca). When providing multiple cert chains, they do not have to
         *  be in the same order as their private keys in key. If the
         *  intermediate certificates are not provided, the peer will not be
         *  able to validate the certificate, and the handshake will fail.
         */
        cert?: string | Buffer | Array<string | Buffer> | undefined;
        /**
         *  Colon-separated list of supported signature algorithms. The list
         *  can contain digest algorithms (SHA256, MD5 etc.), public key
         *  algorithms (RSA-PSS, ECDSA etc.), combination of both (e.g
         *  'RSA+SHA384') or TLS v1.3 scheme names (e.g. rsa_pss_pss_sha512).
         */
        sigalgs?: string | undefined;
        /**
         * Cipher suite specification, replacing the default. For more
         * information, see modifying the default cipher suite. Permitted
         * ciphers can be obtained via tls.getCiphers(). Cipher names must be
         * uppercased in order for OpenSSL to accept them.
         */
        ciphers?: string | undefined;
        /**
         * Name of an OpenSSL engine which can provide the client certificate.
         */
        clientCertEngine?: string | undefined;
        /**
         * PEM formatted CRLs (Certificate Revocation Lists).
         */
        crl?: string | Buffer | Array<string | Buffer> | undefined;
        /**
         * `'auto'` or custom Diffie-Hellman parameters, required for non-ECDHE perfect forward secrecy.
         * If omitted or invalid, the parameters are silently discarded and DHE ciphers will not be available.
         * ECDHE-based perfect forward secrecy will still be available.
         */
        dhparam?: string | Buffer | undefined;
        /**
         * A string describing a named curve or a colon separated list of curve
         * NIDs or names, for example P-521:P-384:P-256, to use for ECDH key
         * agreement. Set to auto to select the curve automatically. Use
         * crypto.getCurves() to obtain a list of available curve names. On
         * recent releases, openssl ecparam -list_curves will also display the
         * name and description of each available elliptic curve. Default:
         * tls.DEFAULT_ECDH_CURVE.
         */
        ecdhCurve?: string | undefined;
        /**
         * Attempt to use the server's cipher suite preferences instead of the
         * client's. When true, causes SSL_OP_CIPHER_SERVER_PREFERENCE to be
         * set in secureOptions
         */
        honorCipherOrder?: boolean | undefined;
        /**
         * Private keys in PEM format. PEM allows the option of private keys
         * being encrypted. Encrypted keys will be decrypted with
         * options.passphrase. Multiple keys using different algorithms can be
         * provided either as an array of unencrypted key strings or buffers,
         * or an array of objects in the form {pem: <string|buffer>[,
         * passphrase: <string>]}. The object form can only occur in an array.
         * object.passphrase is optional. Encrypted keys will be decrypted with
         * object.passphrase if provided, or options.passphrase if it is not.
         */
        key?: string | Buffer | Array<string | Buffer | KeyObject> | undefined;
        /**
         * Name of an OpenSSL engine to get private key from. Should be used
         * together with privateKeyIdentifier.
         */
        privateKeyEngine?: string | undefined;
        /**
         * Identifier of a private key managed by an OpenSSL engine. Should be
         * used together with privateKeyEngine. Should not be set together with
         * key, because both options define a private key in different ways.
         */
        privateKeyIdentifier?: string | undefined;
        /**
         * Optionally set the maximum TLS version to allow. One
         * of `'TLSv1.3'`, `'TLSv1.2'`, `'TLSv1.1'`, or `'TLSv1'`. Cannot be specified along with the
         * `secureProtocol` option, use one or the other.
         * **Default:** `'TLSv1.3'`, unless changed using CLI options. Using
         * `--tls-max-v1.2` sets the default to `'TLSv1.2'`. Using `--tls-max-v1.3` sets the default to
         * `'TLSv1.3'`. If multiple of the options are provided, the highest maximum is used.
         */
        maxVersion?: SecureVersion | undefined;
        /**
         * Optionally set the minimum TLS version to allow. One
         * of `'TLSv1.3'`, `'TLSv1.2'`, `'TLSv1.1'`, or `'TLSv1'`. Cannot be specified along with the
         * `secureProtocol` option, use one or the other.  It is not recommended to use
         * less than TLSv1.2, but it may be required for interoperability.
         * **Default:** `'TLSv1.2'`, unless changed using CLI options. Using
         * `--tls-v1.0` sets the default to `'TLSv1'`. Using `--tls-v1.1` sets the default to
         * `'TLSv1.1'`. Using `--tls-min-v1.3` sets the default to
         * 'TLSv1.3'. If multiple of the options are provided, the lowest minimum is used.
         */
        minVersion?: SecureVersion | undefined;
        /**
         * Shared passphrase used for a single private key and/or a PFX.
         */
        passphrase?: string | undefined;
        /**
         * PFX or PKCS12 encoded private key and certificate chain. pfx is an
         * alternative to providing key and cert individually. PFX is usually
         * encrypted, if it is, passphrase will be used to decrypt it. Multiple
         * PFX can be provided either as an array of unencrypted PFX buffers,
         * or an array of objects in the form {buf: <string|buffer>[,
         * passphrase: <string>]}. The object form can only occur in an array.
         * object.passphrase is optional. Encrypted PFX will be decrypted with
         * object.passphrase if provided, or options.passphrase if it is not.
         */
        pfx?: string | Buffer | Array<string | Buffer | PxfObject> | undefined;
        /**
         * Optionally affect the OpenSSL protocol behavior, which is not
         * usually necessary. This should be used carefully if at all! Value is
         * a numeric bitmask of the SSL_OP_* options from OpenSSL Options
         */
        secureOptions?: number | undefined; // Value is a numeric bitmask of the `SSL_OP_*` options
        /**
         * Legacy mechanism to select the TLS protocol version to use, it does
         * not support independent control of the minimum and maximum version,
         * and does not support limiting the protocol to TLSv1.3. Use
         * minVersion and maxVersion instead. The possible values are listed as
         * SSL_METHODS, use the function names as strings. For example, use
         * 'TLSv1_1_method' to force TLS version 1.1, or 'TLS_method' to allow
         * any TLS protocol version up to TLSv1.3. It is not recommended to use
         * TLS versions less than 1.2, but it may be required for
         * interoperability. Default: none, see minVersion.
         */
        secureProtocol?: string | undefined;
        /**
         * Opaque identifier used by servers to ensure session state is not
         * shared between applications. Unused by clients.
         */
        sessionIdContext?: string | undefined;
        /**
         * 48-bytes of cryptographically strong pseudo-random data.
         * See Session Resumption for more information.
         */
        ticketKeys?: Buffer | undefined;
        /**
         * The number of seconds after which a TLS session created by the
         * server will no longer be resumable. See Session Resumption for more
         * information. Default: 300.
         */
        sessionTimeout?: number | undefined;
    }
    interface SecureContext {
        context: any;
    }
    /**
     * Verifies the certificate `cert` is issued to `hostname`.
     *
     * Returns [Error](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error) object, populating it with `reason`, `host`, and `cert` on
     * failure. On success, returns [undefined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Undefined_type).
     *
     * This function is intended to be used in combination with the`checkServerIdentity` option that can be passed to {@link connect} and as
     * such operates on a `certificate object`. For other purposes, consider using `x509.checkHost()` instead.
     *
     * This function can be overwritten by providing an alternative function as the`options.checkServerIdentity` option that is passed to `tls.connect()`. The
     * overwriting function can call `tls.checkServerIdentity()` of course, to augment
     * the checks done with additional verification.
     *
     * This function is only called if the certificate passed all other checks, such as
     * being issued by trusted CA (`options.ca`).
     *
     * Earlier versions of Node.js incorrectly accepted certificates for a given`hostname` if a matching `uniformResourceIdentifier` subject alternative name
     * was present (see [CVE-2021-44531](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44531)). Applications that wish to accept`uniformResourceIdentifier` subject alternative names can use
     * a custom`options.checkServerIdentity` function that implements the desired behavior.
     * @since v0.8.4
     * @param hostname The host name or IP address to verify the certificate against.
     * @param cert A `certificate object` representing the peer's certificate.
     */
    function checkServerIdentity(hostname: string, cert: PeerCertificate): Error | undefined;
    /**
     * Creates a new {@link Server}. The `secureConnectionListener`, if provided, is
     * automatically set as a listener for the `'secureConnection'` event.
     *
     * The `ticketKeys` options is automatically shared between `cluster` module
     * workers.
     *
     * The following illustrates a simple echo server:
     *
     * ```js
     * import tls from 'node:tls';
     * import fs from 'node:fs';
     *
     * const options = {
     *   key: fs.readFileSync('server-key.pem'),
     *   cert: fs.readFileSync('server-cert.pem'),
     *
     *   // This is necessary only if using client certificate authentication.
     *   requestCert: true,
     *
     *   // This is necessary only if the client uses a self-signed certificate.
     *   ca: [ fs.readFileSync('client-cert.pem') ]
     * };
     *
     * const server = tls.createServer(options, (socket) => {
     *   console.log('server connected',
     *               socket.authorized ? 'authorized' : 'unauthorized');
     *   socket.write('welcome!\n');
     *   socket.setEncoding('utf8');
     *   socket.pipe(socket);
     * });
     * server.listen(8000, () => {
     *   console.log('server bound');
     * });
     * ```
     *
     * The server can be tested by connecting to it using the example client from {@link connect}.
     * @since v0.3.2
     */
    function createServer(secureConnectionListener?: (socket: TLSSocket) => void): Server;
    function createServer(options: TlsOptions, secureConnectionListener?: (socket: TLSSocket) => void): Server;
    /**
     * The `callback` function, if specified, will be added as a listener for the `'secureConnect'` event.
     *
     * `tls.connect()` returns a {@link TLSSocket} object.
     *
     * Unlike the `https` API, `tls.connect()` does not enable the
     * SNI (Server Name Indication) extension by default, which may cause some
     * servers to return an incorrect certificate or reject the connection
     * altogether. To enable SNI, set the `servername` option in addition
     * to `host`.
     *
     * The following illustrates a client for the echo server example from {@link createServer}:
     *
     * ```js
     * // Assumes an echo server that is listening on port 8000.
     * import tls from 'node:tls';
     * import fs from 'node:fs';
     *
     * const options = {
     *   // Necessary only if the server requires client certificate authentication.
     *   key: fs.readFileSync('client-key.pem'),
     *   cert: fs.readFileSync('client-cert.pem'),
     *
     *   // Necessary only if the server uses a self-signed certificate.
     *   ca: [ fs.readFileSync('server-cert.pem') ],
     *
     *   // Necessary only if the server's cert isn't for "localhost".
     *   checkServerIdentity: () => { return null; },
     * };
     *
     * const socket = tls.connect(8000, options, () => {
     *   console.log('client connected',
     *               socket.authorized ? 'authorized' : 'unauthorized');
     *   process.stdin.pipe(socket);
     *   process.stdin.resume();
     * });
     * socket.setEncoding('utf8');
     * socket.on('data', (data) => {
     *   console.log(data);
     * });
     * socket.on('end', () => {
     *   console.log('server ends connection');
     * });
     * ```
     * @since v0.11.3
     */
    function connect(options: ConnectionOptions, secureConnectListener?: () => void): TLSSocket;
    function connect(
        port: number,
        host?: string,
        options?: ConnectionOptions,
        secureConnectListener?: () => void,
    ): TLSSocket;
    function connect(port: number, options?: ConnectionOptions, secureConnectListener?: () => void): TLSSocket;
    /**
     * Creates a new secure pair object with two streams, one of which reads and writes
     * the encrypted data and the other of which reads and writes the cleartext data.
     * Generally, the encrypted stream is piped to/from an incoming encrypted data
     * stream and the cleartext one is used as a replacement for the initial encrypted
     * stream.
     *
     * `tls.createSecurePair()` returns a `tls.SecurePair` object with `cleartext` and `encrypted` stream properties.
     *
     * Using `cleartext` has the same API as {@link TLSSocket}.
     *
     * The `tls.createSecurePair()` method is now deprecated in favor of`tls.TLSSocket()`. For example, the code:
     *
     * ```js
     * pair = tls.createSecurePair(// ... );
     * pair.encrypted.pipe(socket);
     * socket.pipe(pair.encrypted);
     * ```
     *
     * can be replaced by:
     *
     * ```js
     * secureSocket = tls.TLSSocket(socket, options);
     * ```
     *
     * where `secureSocket` has the same API as `pair.cleartext`.
     * @since v0.3.2
     * @deprecated Since v0.11.3 - Use {@link TLSSocket} instead.
     * @param context A secure context object as returned by `tls.createSecureContext()`
     * @param isServer `true` to specify that this TLS connection should be opened as a server.
     * @param requestCert `true` to specify whether a server should request a certificate from a connecting client. Only applies when `isServer` is `true`.
     * @param rejectUnauthorized If not `false` a server automatically reject clients with invalid certificates. Only applies when `isServer` is `true`.
     */
    function createSecurePair(
        context?: SecureContext,
        isServer?: boolean,
        requestCert?: boolean,
        rejectUnauthorized?: boolean,
    ): SecurePair;
    /**
     * {@link createServer} sets the default value of the `honorCipherOrder` option
     * to `true`, other APIs that create secure contexts leave it unset.
     *
     * {@link