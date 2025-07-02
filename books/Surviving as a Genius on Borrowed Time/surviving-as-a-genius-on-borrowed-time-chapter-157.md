0000000000, will be range-checked as described below
         * console.log(myURL.port);
         * // Prints 1234
         * ```
         *
         * Numbers which contain a decimal point,
         * such as floating-point numbers or numbers in scientific notation,
         * are not an exception to this rule.
         * Leading numbers up to the decimal point will be set as the URL's port,
         * assuming they are valid:
         *
         * ```js
         * myURL.port = 4.567e21;
         * console.log(myURL.port);
         * // Prints 4 (because it is the leading number in the string '4.567e21')
         * ```
         */
        port: string;
        /**
         * Gets and sets the protocol portion of the URL.
         *
         * ```js
         * const myURL = new URL('https://example.org');
         * console.log(myURL.protocol);
         * // Prints https:
         *
         * myURL.protocol = 'ftp';
         * console.log(myURL.href);
         * // Prints ftp://example.org/
         * ```
         *
         * Invalid URL protocol values assigned to the `protocol` property are ignored.
         */
        protocol: string;
        /**
         * Gets and sets the serialized query portion of the URL.
         *
         * ```js
         * const myURL = new URL('https://example.org/abc?123');
         * console.log(myURL.search);
         * // Prints ?123
         *
         * myURL.search = 'abc=xyz';
         * console.log(myURL.href);
         * // Prints https://example.org/abc?abc=xyz
         * ```
         *
         * Any invalid URL characters appearing in the value assigned the `search`property will be `percent-encoded`. The selection of which
         * characters to percent-encode may vary somewhat from what the {@link parse} and {@link format} methods would produce.
         */
        search: string;
        /**
         * Gets the `URLSearchParams` object representing the query parameters of the
         * URL. This property is read-only but the `URLSearchParams` object it provides
         * can be used to mutate the URL instance; to replace the entirety of query
         * parameters of the URL, use the {@link search} setter. See `URLSearchParams` documentation for details.
         *
         * Use care when using `.searchParams` to modify the `URL` because,
         * per the WHATWG specification, the `URLSearchParams` object uses
         * different rules to determine which characters to percent-encode. For
         * instance, the `URL` object will not percent encode the ASCII tilde (`~`)
         * character, while `URLSearchParams` will always encode it:
         *
         * ```js
         * const myUrl = new URL('https://example.org/abc?foo=~bar');
         *
         * console.log(myUrl.search);  // prints ?foo=~bar
         *
         * // Modify the URL via searchParams...
         * myUrl.searchParams.sort();
         *
         * console.log(myUrl.search);  // prints ?foo=%7Ebar
         * ```
         */
        readonly searchParams: URLSearchParams;
        /**
         * Gets and sets the username portion of the URL.
         *
         * ```js
         * const myURL = new URL('https://abc:xyz@example.com');
         * console.log(myURL.username);
         * // Prints abc
         *
         * myURL.username = '123';
         * console.log(myURL.href);
         * // Prints https://123:xyz@example.com/
         * ```
         *
         * Any invalid URL characters appearing in the value assigned the `username` property will be `percent-encoded`. The selection of which
         * characters to percent-encode may vary somewhat from what the {@link parse} and {@link format} methods would produce.
         */
        username: string;
        /**
         * The `toString()` method on the `URL` object returns the serialized URL. The
         * value returned is equivalent to that of {@link href} and {@link toJSON}.
         */
        toString(): string;
        /**
         * The `toJSON()` method on the `URL` object returns the serialized URL. The
         * value returned is equivalent to that of {@link href} and {@link toString}.
         *
         * This method is automatically called when an `URL` object is serialized
         * with [`JSON.stringify()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify).
         *
         * ```js
         * const myURLs = [
         *   new URL('https://www.example.com'),
         *   new URL('https://test.example.org'),
         * ];
         * console.log(JSON.stringify(myURLs));
         * // Prints ["https://www.example.com/","https://test.example.org/"]
         * ```
         */
        toJSON(): string;
    }
    interface URLSearchParamsIterator<T> extends NodeJS.Iterator<T, NodeJS.BuiltinIteratorReturn, unknown> {
        [Symbol.iterator](): URLSearchParamsIterator<T>;
    }
    /**
     * The `URLSearchParams` API provides read and write access to the query of a `URL`. The `URLSearchParams` class can also be used standalone with one of the
     * four following constructors.
     * The `URLSearchParams` class is also available on the global object.
     *
     * The WHATWG `URLSearchParams` interface and the `querystring` module have
     * similar purpose, but the purpose of the `querystring` module is more
     * general, as it allows the customization of delimiter characters (`&#x26;` and `=`).
     * On the other hand, this API is designed purely for URL query strings.
     *
     * ```js
     * const myURL = new URL('https://example.org/?abc=123');
     * console.log(myURL.searchParams.get('abc'));
     * // Prints 123
     *
     * myURL.searchParams.append('abc', 'xyz');
     * console.log(myURL.href);
     * // Prints https://example.org/?abc=123&#x26;abc=xyz
     *
     * myURL.searchParams.delete('abc');
     * myURL.searchParams.set('a', 'b');
     * console.log(myURL.href);
     * // Prints https://example.org/?a=b
     *
     * const newSearchParams = new URLSearchParams(myURL.searchParams);
     * // The above is equivalent to
     * // const newSearchParams = new URLSearchParams(myURL.search);
     *
     * newSearchParams.append('a', 'c');
     * console.log(myURL.href);
     * // Prints https://example.org/?a=b
     * console.log(newSearchParams.toString());
     * // Prints a=b&#x26;a=c
     *
     * // newSearchParams.toString() is implicitly called
     * myURL.search = newSearchParams;
     * console.log(myURL.href);
     * // Prints https://example.org/?a=b&#x26;a=c
     * newSearchParams.delete('a');
     * console.log(myURL.href);
     * // Prints https://example.org/?a=b&#x26;a=c
     * ```
     * @since v7.5.0, v6.13.0
     */
    class URLSearchParams implements Iterable<[string, string]> {
        constructor(
            init?:
                | URLSearchParams
                | string
                | Record<string, string | readonly string[]>
                | Iterable<[string, string]>
                | ReadonlyArray<[string, string]>,
        );
        /**
         * Append a new name-value pair to the query string.
         */
        append(name: string, value: string): void;
        /**
         * If `value` is provided, removes all name-value pairs
         * where name is `name` and value is `value`.
         *
         * If `value` is not provided, removes all name-value pairs whose name is `name`.
         */
        delete(name: string, value?: string): void;
        /**
         * Returns an ES6 `Iterator` over each of the name-value pairs in the query.
         * Each item of the iterator is a JavaScript `Array`. The first item of the `Array` is the `name`, the second item of the `Array` is the `value`.
         *
         * Alias for `urlSearchParams[@@iterator]()`.
         */
        entries(): URLSearchParamsIterator<[string, string]>;
        /**
         * Iterates over each name-value pair in the query and invokes the given function.
         *
         * ```js
         * const myURL = new URL('https://example.org/?a=b&#x26;c=d');
         * myURL.searchParams.forEach((value, name, searchParams) => {
         *   console.log(name, value, myURL.searchParams === searchParams);
         * });
         * // Prints:
         * //   a b true
         * //   c d true
         * ```
         * @param fn Invoked for each name-value pair in the query
         * @param thisArg To be used as `this` value for when `fn` is called
         */
        forEach<TThis = this>(
            fn: (this: TThis, value: string, name: string, searchParams: URLSearchParams) => void,
            thisArg?: TThis,
        ): void;
        /**
         * Returns the value of the first name-value pair whose name is `name`. If there
         * are no such pairs, `null` is returned.
         * @return or `null` if there is no name-value pair with the given `name`.
         */
        get(name: string): string | null;
        /**
         * Returns the values of all name-value pairs whose name is `name`. If there are
         * no such pairs, an empty array is returned.
         */
        getAll(name: string): string[];
        /**
         * Checks if the `URLSearchParams` object contains key-value pair(s) based on `name` and an optional `value` argument.
         *
         * If `value` is provided, returns `true` when name-value pair with
         * same `name` and `value` exists.
         *
         * If `value` is not provided, returns `true` if there is at least one name-value
         * pair whose name is `name`.
         */
        has(name: string, value?: string): boolean;
        /**
         * Returns an ES6 `Iterator` over the names of each name-value pair.
         *
         * ```js
         * const params = new URLSearchParams('foo=bar&#x26;foo=baz');
         * for (const name of params.keys()) {
         *   console.log(name);
         * }
         * // Prints:
         * //   foo
         * //   foo
         * ```
         */
        keys(): URLSearchParamsIterator<string>;
        /**
         * Sets the value in the `URLSearchParams` object associated with `name` to`value`. If there are any pre-existing name-value pairs whose names are `name`,
         * set the first such pair's value to `value` and remove all others. If not,
         * append the name-value pair to the query string.
         *
         * ```js
         * const params = new URLSearchParams();
         * params.append('foo', 'bar');
         * params.append('foo', 'baz');
         * params.append('abc', 'def');
         * console.log(params.toString());
         * // Prints foo=bar&#x26;foo=baz&#x26;abc=def
         *
         * params.set('foo', 'def');
         * params.set('xyz', 'opq');
         * console.log(params.toString());
         * // Prints foo=def&#x26;abc=def&#x26;xyz=opq
         * ```
         */
        set(name: string, value: string): void;
        /**
         * The total number of parameter entries.
         * @since v18.16.0
         */
        readonly size: number;
        /**
         * Sort all existing name-value pairs in-place by their names. Sorting is done
         * with a [stable sorting algorithm](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability), so relative order between name-value pairs
         * with the same name is preserved.
         *
         * This method can be used, in particular, to increase cache hits.
         *
         * ```js
         * const params = new URLSearchParams('query[]=abc&#x26;type=search&#x26;query[]=123');
         * params.sort();
         * console.log(params.toString());
         * // Prints query%5B%5D=abc&#x26;query%5B%5D=123&#x26;type=search
         * ```
         * @since v7.7.0, v6.13.0
         */
        sort(): void;
        /**
         * Returns the search parameters serialized as a string, with characters
         * percent-encoded where necessary.
         */
        toString(): string;
        /**
         * Returns an ES6 `Iterator` over the values of each name-value pair.
         */
        values(): URLSearchParamsIterator<string>;
        [Symbol.iterator](): URLSearchParamsIterator<[string, string]>;
    }
    import { URL as _URL, URLSearchParams as _URLSearchParams } from "url";
    global {
        interface URLSearchParams extends _URLSearchParams {}
        interface URL extends _URL {}
        interface Global {
            URL: typeof _URL;
            URLSearchParams: typeof _URLSearchParams;
        }
        /**
         * `URL` class is a global reference for `import { URL } from 'node:url'`
         * https://nodejs.org/api/url.html#the-whatwg-url-api
         * @since v10.0.0
         */
        var URL: typeof globalThis extends {
            onmessage: any;
            URL: infer T;
        } ? T
            : typeof _URL;
        /**
         * `URLSearchParams` class is a global reference for `import { URLSearchParams } from 'node:url'`
         * https://nodejs.org/api/url.html#class-urlsearchparams
         * @since v10.0.0
         */
        var URLSearchParams: typeof globalThis extends {
            onmessage: any;
            URLSearchParams: infer T;
        } ? T
            : typeof _URLSearchParams;
    }
}
declare module "node:url" {
    export * from "url";
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      // @flow

import {
  serializeError,
} from 'serialize-error';
import {
  boolean,
} from 'boolean';
import Logger from '../Logger';
import type {
  AgentType,
  GetUrlProxyMethodType,
  IsProxyConfiguredMethodType,
  MustUrlUseProxyMethodType,
  ProtocolType,
} from '../types';

const log = Logger.child({
  namespace: 'Agent',
});

let requestId = 0;

class Agent {
  defaultPort: number;

  protocol: ProtocolType;

  fallbackAgent: AgentType;

  isProxyConfigured: IsProxyConfiguredMethodType;

  mustUrlUseProxy: MustUrlUseProxyMethodType;

  getUrlProxy: GetUrlProxyMethodType;

  socketConnectionTimeout: number;

  constructor (
    isProxyConfigured: IsProxyConfiguredMethodType,
    mustUrlUseProxy: MustUrlUseProxyMethodType,
    getUrlProxy: GetUrlProxyMethodType,
    fallbackAgent: AgentType,
    socketConnectionTimeout: number,
  ) {
    this.fallbackAgent = fallbackAgent;
    this.isProxyConfigured = isProxyConfigured;
    this.mustUrlUseProxy = mustUrlUseProxy;
    this.getUrlProxy = getUrlProxy;
    this.socketConnectionTimeout = socketConnectionTimeout;
  }

  addRequest (request: *, configuration: *) {
    let requestUrl;

    // It is possible that addRequest was constructed for a proxied request already, e.g.
    // "request" package does this when it detects that a proxy should be used
    // https://github.com/request/request/blob/212570b6971a732b8dd9f3c73354bcdda158a737/request.js#L402
    // https://gist.github.com/gajus/e2074cd3b747864ffeaabbd530d30218
    if (request.path.startsWith('http://') || request.path.startsWith('https://')) {
      requestUrl = request.path;
    } else {
      requestUrl = this.protocol + '//' + (configuration.hostname || configuration.host) + (configuration.port === 80 || configuration.port === 443 ? '' : ':' + configuration.port) + request.path;
    }

    if (!this.isProxyConfigured()) {
      log.trace({
        destination: requestUrl,
      }, 'not proxying request; GLOBAL_AGENT.HTTP_PROXY is not configured');

      // $FlowFixMe It appears that Flow is missing the method description.
      this.fallbackAgent.addRequest(request, configuration);

      return;
    }

    if (!this.mustUrlUseProxy(requestUrl)) {
      log.trace({
        destination: requestUrl,
      }, 'not proxying request; url matches GLOBAL_AGENT.NO_PROXY');

      // $FlowFixMe It appears that Flow is missing the method description.
      this.fallbackAgent.addRequest(request, configuration);

      return;
    }

    const currentRequestId = requestId++;

    const proxy = this.getUrlProxy(requestUrl);

    if (this.protocol === 'http:') {
      request.path = requestUrl;

      if (proxy.authorization) {
        request.setHeader('proxy-authorization', 'Basic ' + Buffer.from(proxy.authorization).toString('base64'));
      }
    }

    log.trace({
      destination: requestUrl,
      proxy: 'http://' + proxy.hostname + ':' + proxy.port,
      requestId: currentRequestId,
    }, 'proxying request');

    request.on('error', (error) => {
      log.error({
        error: serializeError(error),
      }, 'request error');
    });

    request.once('response', (response) => {
      log.trace({
        headers: response.headers,
        requestId: currentRequestId,
        statusCode: response.statusCode,
      }, 'proxying response');
    });

    request.shouldKeepAlive = false;

    const connectionConfiguration = {
      host: configuration.hostname || configuration.host,
      port: configuration.port || 80,
      proxy,
      tls: {},
    };

    // add optional tls options for https requests.
    // @see https://nodejs.org/docs/latest-v12.x/api/https.html#https_https_request_url_options_callback :
    // > The following additional options from tls.connect()
    // >   - https://nodejs.org/docs/latest-v12.x/api/tls.html#tls_tls_connect_options_callback -
    // > are also accepted:
    // >   ca, cert, ciphers, clientCertEngine, crl, dhparam, ecdhCurve, honorCipherOrder,
    // >   key, passphrase, pfx, rejectUnauthorized, secureOptions, secureProtocol, servername, sessionIdContext.
    if (this.protocol === 'https:') {
      connectionConfiguration.tls = {
        ca: configuration.ca,
        cert: configuration.cert,
        ciphers: configuration.ciphers,
        clientCertEngine: configuration.clientCertEngine,
        crl: configuration.crl,
        dhparam: configuration.dhparam,
        ecdhCurve: configuration.ecdhCurve,
        honorCipherOrder: configuration.honorCipherOrder,
        key: configuration.key,
        passphrase: configuration.passphrase,
        pfx: configuration.pfx,
        rejectUnauthorized: configuration.rejectUnauthorized,
        secureOptions: configuration.secureOptions,
        secureProtocol: configuration.secureProtocol,
        servername: configuration.servername || connectionConfiguration.host,
        sessionIdContext: configuration.sessionIdContext,
      };

      // This is not ideal because there is no way to override this setting using `tls` configuration if `NODE_TLS_REJECT_UNAUTHORIZED=0`.
      // However, popular HTTP clients (such as https://github.com/sindresorhus/got) come with pre-configured value for `rejectUnauthorized`,
      // which makes it impossible to override that value globally and respect `rejectUnauthorized` for specific requests only.
      //
      // eslint-disable-next-line no-process-env
      if (typeof process.env.NODE_TLS_REJECT_UNAUTHORIZED === 'string' && boolean(process.env.NODE_TLS_REJECT_UNAUTHORIZED) === false) {
        connectionConfiguration.tls.rejectUnauthorized = false;
      }
    }

    // $FlowFixMe It appears that Flow is missing the method description.
    this.createConnection(connectionConfiguration, (error, socket) => {
      log.trace({
        target: connectionConfiguration,
      }, 'connecting');

      // @see https://github.com/nodejs/node/issues/5757#issuecomment-305969057
      if (socket) {
        socket.setTimeout(this.socketConnectionTimeout, () => {
          socket.destroy();
        });

        socket.once('connect', () => {
          log.trace({
            target: connectionConfiguration,
          }, 'connected');

          socket.setTimeout(0);
        });

        socket.once('secureConnect', () => {
          log.trace({
            target: connectionConfiguration,
          }, 'connected (secure)');

          socket.setTimeout(0);
        });
      }

      if (error) {
        request.emit('error', error);
      } else {
        log.debug('created socket');

        socket.on('error', (socketError) => {
          log.error({
            error: serializeError(socketError),
          }, 'socket error');
        });

        request.onSocket(socket);
      }
    });
  }
}

export default Agent;
                                                                                                                                                                                                                                                                                                                                         