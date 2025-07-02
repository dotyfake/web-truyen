/**
 * The `tls` module provides an implementation of the Transport Layer Security
 * (TLS) and Secure Socket Layer (SSL) protocols that is built on top of OpenSSL.
 * The module can be accessed using:
 *
 * ```js
 * import tls from 'node:tls';
 * ```
 * @see [source](https://github.com/nodejs/node/blob/v18.0.0/lib/tls.js)
 */
declare module "tls" {
    import { X509Certificate } from "node:crypto";
    import * as net from "node:net";
    import * as stream from "stream";
    const CLIENT_RENEG_LIMIT: number;
    const CLIENT_RENEG_WINDOW: number;
    interface Certificate {
        /**
         * Country code.
         */
        C: string;
        /**
         * Street.
         */
        ST: string;
        /**
         * Locality.
         */
        L: string;
        /**
         * Organization.
         */
        O: string;
        /**
         * Organizational unit.
         */
        OU: string;
        /**
         * Common name.
         */
        CN: string;
    }
    interface PeerCertificate {
        /**
         * `true` if a Certificate Authority (CA), `false` otherwise.
         * @since v18.13.0
         */
        ca: boolean;
        /**
         * The DER encoded X.509 certificate data.
         */
        raw: Buffer;
        /**
         * The certificate subject.
         */
        subject: Certificate;
        /**
         * The certificate issuer, described in the same terms as the `subject`.
         */
        issuer: Certificate;
        /**
         * The date-time the certificate is valid from.
         */
        valid_from: string;
        /**
         * The date-time the certificate is valid to.
         */
        valid_to: string;
        /**
         * The certificate serial number, as a hex string.
         */
        serialNumber: string;
        /**
         * The SHA-1 digest of the DER encoded certificate.
         * It is returned as a `:` separated hexadecimal string.
         */
        fingerprint: string;
        /**
         * The SHA-256 digest of the DER encoded certificate.
         * It is returned as a `:` separated hexadecimal string.
         */
        fingerprint256: string;
        /**
         * The SHA-512 digest of the DER encoded certificate.
         * It is returned as a `:` separated hexadecimal string.
         */
        fingerprint512: string;
        /**
         * The extended key usage, a set of OIDs.
         */
        ext_key_usage?: string[];
        /**
         * A string containing concatenated names for the subject,
         * an alternative to the `subject` names.
         */
        subjectaltname?: string;
        /**
         * An array describing the AuthorityInfoAccess, used with OCSP.
         */
        infoAccess?: NodeJS.Dict<string[]>;
        /**
         * For RSA keys: The RSA bit size.
         *
         * For EC keys: The key size in bits.
         */
        bits?: number;
        /**
         * The RSA exponent, as a string in hexadecimal number notation.
         */
        exponent?: string;
        /**
         * The RSA modulus, as a hexadecimal string.
         */
        modulus?: string;
        /**
         * The public key.
         */
        pubkey?: Buffer;
        /**
         * The ASN.1 name of the OID of the elliptic curve.
         * Well-known curves are identified by an OID.
         * While it is unusual, it is possible that the curve
         * is identified by its mathematical properties,
         * in which case it will not have an OID.
         */
        asn1Curve?: string;
        /**
         * The NIST name for the elliptic curve,if it has one
         * (not all well-known curves have been assigned names by NIST).
         */
        nistCurve?: string;
    }
    interface DetailedPeerCertificate extends PeerCertificate {
        /**
         * The issuer certificate object.
         * For self-signed certificates, this may be a circular reference.
         */
        issuerCertificate: DetailedPeerCertificate;
    }
    interface CipherNameAndProtocol {
        /**
         * The cipher name.
         */
        name: string;
        /**
         * SSL/TLS protocol version.
         */
        version: string;
        /**
         * IETF name for the cipher suite.
         */
        standardName: string;
    }
    interface EphemeralKeyInfo {
        /**
         * The supported types are 'DH' and 'ECDH'.
         */
        type: string;
        /**
         * The name property is available only when type is 'ECDH'.
         */
        name?: string | undefined;
        /**
         * The size of parameter of an ephemeral key exchange.
         */
        size: number;
    }
    interface KeyObject {
        /**
         * Private keys in PEM format.
         */
        pem: string | Buffer;
        /**
         * Optional passphrase.
         */
        passphrase?: string | undefined;
    }
    interface PxfObject {
        /**
         * PFX or PKCS12 encoded private key and certificate chain.
         */
        buf: string | Buffer;
        /**
         * Optional passphrase.
         */
        passphrase?: string | undefined;
    }
    interface TLSSocketOptions extends SecureContextOptions, CommonConnectionOptions {
        /**
         * If true the TLS socket will be instantiated in server-mode.
         * Defaults to false.
         */
        isServer?: boolean | undefined;
        /**
         * An optional net.Server instance.
         */
        server?: net.Server | undefined;
        /**
         * An optional Buffer instance containing a TLS session.
         */
        session?: Buffer | undefined;
        /**
         * If true, specifies that the OCSP status request extension will be
         * added to the client hello and an 'OCSPResponse' event will be
         * emitted on the socket before establishing a secure communication
         */
        requestOCSP?: boolean | undefined;
    }
    /**
     * Performs transparent encryption of written data and all required TLS
     * negotiation.
     *
     * Instances of `tls.TLSSocket` implement the duplex `Stream` interface.
     *
     * Methods that return TLS connection metadata (e.g.{@link TLSSocket.getPeerCertificate} will only return data while the
     * connection is open.
     * @since v0.11.4
     */
    class TLSSocket extends net.Socket {
        /**
         * Construct a new tls.TLSSocket object from an existing TCP socket.
         */
        constructor(socket: net.Socket | stream.Duplex, options?: TLSSocketOptions);
        /**
         * This property is `true` if the peer certificate was signed by one of the CAs
         * specified when creating the `tls.TLSSocket` instance, otherwise `false`.
         * @since v0.11.4
         */
        authorized: boolean;
        /**
         * Returns the reason why the peer's certificate was not been verified. This
         * property is set only when `tlsSocket.authorized === false`.
         * @since v0.11.4
         */
        authorizationError: Error;
        /**
         * Always returns `true`. This may be used to distinguish TLS sockets from regular`net.Socket` instances.
         * @since v0.11.4
         */
        encrypted: true;
        /**
         * String containing the selected ALPN protocol.
         * Before a handshake has completed, this value is always null.
         * When a handshake is completed but not ALPN protocol was selected, tlsSocket.alpnProtocol equals false.
         */
        alpnProtocol: string | false | null;
        /**
         * Returns an object representing the local certificate. The returned object has
         * some properties corresponding to the fields of the certificate.
         *
         * See {@link TLSSocket.getPeerCertificate} for an example of the certificate
         * structure.
         *
         * If there is no local certificate, an empty object will be returned. If the
         * socket has been destroyed, `null` will be returned.
         * @since v11.2.0
         */
        getCertificate(): PeerCertificate | object | null;
        /**
         * Returns an object containing information on the negotiated cipher suite.
         *
         * For example:
         *
         * ```json
         * {
         *     "name": "AES128-SHA256",
         *     "standardName": "TLS_RSA_WITH_AES_128_CBC_SHA256",
         *     "version": "TLSv1.2"
         * }
         * ```
         *
         * See [SSL\_CIPHER\_get\_name](https://www.openssl.org/docs/man1.1.1/man3/SSL_CIPHER_get_name.html) for more information.
         * @since v0.11.4
         */
        getCipher(): CipherNameAndProtocol;
        /**
         * Returns an object representing the type, name, and size of parameter of
         * an ephemeral key exchange in `perfect forward secrecy` on a client
         * connection. It returns an empty object when the key exchange is not
         * ephemeral. As this is only supported on a client socket; `null` is returned
         * if called on a server socket. The supported types are `'DH'` and `'ECDH'`. The`name` property is available only when type is `'ECDH'`.
         *
         * For example: `{ type: 'ECDH', name: 'prime256v1', size: 256 }`.
         * @since v5.0.0
         */
        getEphemeralKeyInfo(): EphemeralKeyInfo | object | null;
        /**
         * As the `Finished` messages are message digests of the complete handshake
         * (with a total of 192 bits for TLS 1.0 and more for SSL 3.0), they can
         * be used for external authentication procedures when the authentication
         * provided by SSL/TLS is not desired or is not enough.
         *
         * Corresponds to the `SSL_get_finished` routine in OpenSSL and may be used
         * to implement the `tls-unique` channel binding from [RFC 5929](https://tools.ietf.org/html/rfc5929).
         * @since v9.9.0
         * @return The latest `Finished` message that has been sent to the socket as part of a SSL/TLS handshake, or `undefined` if no `Finished` message has been sent yet.
         */
        getFinished(): Buffer | undefined;
        /**
         * Returns an object representing the peer's certificate. If the peer does not
         * provide a certificate, an empty object will be returned. If the socket has been
         * destroyed, `null` will be returned.
         *
         * If the full certificate chain was requested, each certificate will include an`issuerCertificate` property containing an object representing its issuer's
         * certificate.
         * @since v0.11.4
         * @param detailed Include the full certificate chain if `true`, otherwise include just the peer's certificate.
         * @return A certificate object.
         */
        getPeerCertificate(detailed: true): DetailedPeerCertificate;
        getPeerCertificate(detailed?: false): PeerCertificate;
        getPeerCertificate(detailed?: boolean): PeerCertificate | DetailedPeerCertificate;
        /**
         * As the `Finished` messages are message digests of the complete handshake
         * (with a total of 192 bits for TLS 1.0 and more for SSL 3.0), they can
         * be used for external authentication procedures when the authentication
         * provided by SSL/TLS is not desired or is not enough.
         *
         * Corresponds to the `SSL_get_peer_finished` routine in OpenSSL and may be used
         * to implement the `tls-unique` channel binding from [RFC 5929](https://tools.ietf.org/html/rfc5929).
         * @since v9.9.0
         * @return The latest `Finished` message that is expected or has actually been received from the socket as part of a SSL/TLS handshake, or `undefined` if there is no `Finished` message so
         * far.
         */
        getPeerFinished(): Buffer | undefined;
        /**
         * Returns a string containing the negotiated SSL/TLS protocol version of the
         * current connection. The value `'unknown'` will be returned for connected
         * sockets that have not completed the handshaking process. The value `null` will
         * be returned for server sockets or disconnected client sockets.
         *
         * Protocol versions are:
         *
         * * `'SSLv3'`
         * * `'TLSv1'`
         * * `'TLSv1.1'`
         * * `'TLSv1.2'`
         * * `'TLSv1.3'`
         *
         * See the OpenSSL [`SSL_get_version`](https://www.openssl.org/docs/man1.1.1/man3/SSL_get_version.html) documentation for more information.
         * @since v5.7.0
         */
        getProtocol(): string | null;
        /**
         * Returns the TLS session data or `undefined` if no session was
         * negotiated. On the client, the data can be provided to the `session` option of {@link connect} to resume the connection. On the server, it may be useful
         * for debugging.
         *
         * See `Session Resumption` for more information.
         *
         * Note: `getSession()` works only for TLSv1.2 and below. For TLSv1.3, applications
         * must use the `'session'` event (it also works for TLSv1.2 and below).
         * @since v0.11.4
         */
        getSession(): Buffer | undefined;
        /**
         * See [SSL\_get\_shared\_sigalgs](https://www.openssl.org/docs/man1.1.1/man3/SSL_get_shared_sigalgs.html) for more information.
         * @since v12.11.0
         * @return List of signature algorithms shared between the server and the client in the order of decreasing preference.
         */
        getSharedSigalgs(): string[];
        /**
         * For a client, returns the TLS session ticket if one is available, or`undefined`. For a server, always returns `undefined`.
         *
         * It may be useful for debugging.
         *
         * See `Session Resumption` for more information.
         * @since v0.11.4
         */
        getTLSTicket(): Buffer | undefined;
        /**
         * See `Session Resumption` for more information.
         * @since v0.5.6
         * @return `true` if the session was reused, `false` otherwise.
         */
        isSessionReused(): boolean;
        /**
         * The `tlsSocket.renegotiate()` method initiates a TLS renegotiation process.
         * Upon completion, the `callback` function will be passed a single argument
         * that is either an `Error` (if the request failed) or `null`.
         *
         * This method can be used to request a peer's certificate after the secure
         * connection has been established.
         *
         * When running as the server, the socket will be destroyed with an error after`handshakeTimeout` timeout.
         *
         * For TLSv1.3, renegotiation cannot be initiated, it is not supported by the
         * protocol.
         * @since v0.11.8
         * @param callback If `renegotiate()` returned `true`, callback is attached once to the `'secure'` event. If `renegotiate()` returned `false`, `callback` will be called in the next tick with
         * an error, unless the `tlsSocket` has been destroyed, in which case `callback` will not be called at all.
         * @return `true` if renegotiation was initiated, `false` otherwise.
         */
        renegotiate(
            options: {
                rejectUnauthorized?: boolean | undefined;
                requestCert?: boolean | undefined;
            },
            callback: (err: Error | null) => void,
        ): undefined | boolean;
        /**
         * The `tlsSocket.setMaxSendFragment()` method sets the maximum TLS fragment size.
         * Returns `true` if setting the limit succeeded; `false` otherwise.
         *
         * Smaller fragment sizes decrease the buffering latency on the client: larger
         * fragments are buffered by the TLS layer until the entire fragment is received
         * and its integrity is verified; large fragments can span multiple roundtrips
         * and their processing can be delayed due to packet loss or reordering. However,
         * smaller fragments add extra TLS framing bytes and CPU overhead, which may
         * decrease overall server throughput.
         * @since v0.11.11
         * @param [size=16384] The maximum TLS fragment size. The maximum value is `16384`.
         */
        setMaxSendFragment(size: number): boolean;
        /**
         * Disables TLS renegotiation for this `TLSSocket` instance. Once called, attempts
         * to renegotiate will trigger an `'error'` event on the `TLSSocket`.
         * @since v8.4.0
         */
        disableRenegotiation(): void;
        /**
         * When enabled, TLS packet trace information is written to `stderr`. This can be
         * used to debug TLS connection problems.
         *
         * The format of the output is identical to the output of`openssl s_client -trace` or `openssl s_server -trace`. While it is produced by
         * OpenSSL's `SSL_trace()` function, the format is undocumented, can change
         * without notice, and should not be relied on.
         * @since v12.2.0
         */
        enableTrace(): void;
        /**
         * Returns the peer certificate as an `X509Certificate` object.
         *
         * If there is no peer certificate, or the socket has been destroyed,`undefined` will be returned.
         * @since v15.9.0
         */
        getPeerX509Certificate(): X509Certificate | undefined;
        /**
         * Returns the local certificate as an `X509Certificate` object.
         *
         * If there is no local certificate, or the socket has been destroyed,`undefined` will be returned.
         * @since v15.9.0
         */
        getX509Certificate(): X509Certificate | undefined;
        /**
         * Keying material is used for validations to prevent different kind of attacks in
         * network protocols, for example in the specifications of IEEE 802.1X.
         *
         * Example
         *
         * ```js
         * const keyingMaterial = tlsSocket.exportKeyingMaterial(
         *   128,
         *   'client finished');
         *
         * /*
         *  Example return value of keyingMaterial:
         *  <Buffer 76 26 af 99 c5 56 8e 42 09 91 ef 9f 93 cb ad 6c 7b 65 f8 53 f1 d8 d9
         *     12 5a 33 b8 b5 25 df 7b 37 9f e0 e2 4f b8 67 83 a3 2f cd 5d 41 42 4c 91
         *     74 ef 2c ... 78 more bytes>
         *
         * ```
         *
         * See the OpenSSL [`SSL_export_keying_material`](https://www.openssl.org/docs/man1.1.1/man3/SSL_export_keying_material.html) documentation for more
         * information.
         * @since v13.10.0, v12.17.0
         * @param length number of bytes to retrieve from keying material
         * @param label an application specific label, typically this will be a value from the [IANA Exporter Label
         * Registry](https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#exporter-labels).
         * @param context Optionally provide a context.
         * @return requested bytes of the keying material
         */
        exportKeyingMaterial(length: number, label: string, context: Buffer): Buffer;
        addListener(event: string, listener: (...args: any[]) => void): this;
        addListener(event: "OCSPResponse", listener: (response: Buffer) => void): this;
        addListener(event: "secureConnect", listener: () => void): this;
        addListener(event: "session", listener: (session: Buffer) => void): this;
        addListener(event: "keylog", listener: (line: Buffer) => void): this;
        emit(event: string | symbol, ...args: any[]): boolean;
        emit(event: "OCSPResponse", response: Buffer): boolean;
        emit(event: "secureConnect"): boolean;
        emit(event: "session", session: Buffer): boolean;
        emit(event: "keylog", line: Buffer): boolean;
        on(event: string, listener: (...args: any[]) => void): this;
        on(event: "OCSPResponse", listener: (response: Buffer) => void): this;
        on(event: "secureConnect", listener: () => void): this;
        on(event: "session", listener: (session: Buffer) => void): this;
        on(event: "keylog", listener: (line: Buffer) => void): this;
        once(event: string, listener: (...args: any[]) => void): this;
        once(event: "OCSPResponse", listener: (response: Buffer) => void): this;
        once(event: "secureConnect", listener: () => void): this;
        once(event: "session", listener: (session: Buffer) => void): this;
        once(event: "keylog", listener: (line: Buffer) => void): this;
        prependListener(event: string, listener: (...args: any[]) => void): this;
        prependListener(event: "OCSPResponse", listener: (response: Buffer) => void): this;
        prependListener(event: "secureConnect", listener: () => void): this;
        prependListener(event: "session", listener: (session: Buffer) => void): this;
        prependListener(event: "keylog", listener: (line: Buffer) => void): this;
        prependOnceListener(event: string, listener: (...args: any[]) => void): this;
        prependOnceListener(event: "OCSPResponse", listener: (response: Buffer) => void): this;
        prependOnceListener(event: "secureConnect", listener: () => void): this;
        prependOnceListener(event: "session", listener: (session: Buffer) => void): this;
        prependOnceListener(event: "keylog", listener: (line: Buffer) => void): this;
    }
    interface CommonConnectionOptions {
        /**
         * An optional TLS context object from tls.createSecureContext()
         */
        secureContext?: SecureContext | undefined;
        /**
         * When enabled, TLS packet trace information is written to `stderr`. This can be
         * used to debug TLS connection problems.
         * @default false
         */
        enableTrace?: boolean | undefined;
        /**
         * If true the server will request a certificate from clients that
         * connect and attempt to verify that certificate. Defaults to
         * false.
         */
        requestCert?: boolean | undefined;
        /**
         * An array of strings or a Buffer naming possible ALPN protocols.
         * (Protocols should be ordered by their priority.)
         */
        ALPNProtocols?: string[] | Uint8Array[] | Uint8Array | undefined;
        /**
         * SNICallback(servername, cb) <Function> A function that will be
         * called if the client supports SNI TLS extension. Two arguments
         * will be passed when called: servername and cb. SNICallback should
         * invoke cb(null, ctx), where ctx is a SecureContext instance.
         * (tls.createSecureContext(...) can be used to get a proper
         * SecureContext.) If SNICallback wasn't provided the default callback
         * with high-level API will be used (see below).
         */
        SNICallback?: ((servername: string, cb: (err: Error | null, ctx?: SecureContext) => void) => void) | undefined;
        /**
         * If true the server will reject any connection which is not
         * a