// @flow

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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      // @flow

import net from 'net';
import type {
  ConnectionCallbackType,
  ConnectionConfigurationType,
} from '../types';
import Agent from './Agent';

class HttpProxyAgent extends Agent {
  // @see https://github.com/sindresorhus/eslint-plugin-unicorn/issues/169#issuecomment-486980290
  // eslint-disable-next-line unicorn/prevent-abbreviations
  constructor (...args: *) {
    super(...args);

    this.protocol = 'http:';
    this.defaultPort = 80;
  }

  createConnection (configuration: ConnectionConfigurationType, callback: ConnectionCallbackType) {
    const socket = net.connect(
      configuration.proxy.port,
      configuration.proxy.hostname,
    );

    callback(null, socket);
  }
}

export default HttpProxyAgent;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   // @flow

import net from 'net';
import tls from 'tls';
import type {
  ConnectionCallbackType,
  ConnectionConfigurationType,
} from '../types';
import Agent from './Agent';

class HttpsProxyAgent extends Agent {
  // eslint-disable-next-line unicorn/prevent-abbreviations
  constructor (...args: *) {
    super(...args);

    this.protocol = 'https:';
    this.defaultPort = 443;
  }

  createConnection (configuration: ConnectionConfigurationType, callback: ConnectionCallbackType) {
    const socket = net.connect(
      configuration.proxy.port,
      configuration.proxy.hostname,
    );

    socket.on('error', (error) => {
      callback(error);
    });

    socket.once('data', () => {
      const secureSocket = tls.connect({
        ...configuration.tls,
        socket,
      });

      callback(null, secureSocket);
    });

    let connectMessage = '';

    connectMessage += 'CONNECT ' + configuration.host + ':' + configuration.port + ' HTTP/1.1\r\n';
    connectMessage += 'Host: ' + configuration.host + ':' + configuration.port + '\r\n';

    if (configuration.proxy.authorization) {
      connectMessage += 'Proxy-Authorization: Basic ' + Buffer.from(configuration.proxy.authorization).toString('base64') + '\r\n';
    }

    connectMessage += '\r\n';

    socket.write(connectMessage);
  }
}

export default HttpsProxyAgent;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              // @flow

import http from 'http';
import https from 'https';
import {
  boolean as parseBoolean,
} from 'boolean';
import semver from 'semver';
import Logger from '../Logger';
import {
  HttpProxyAgent,
  HttpsProxyAgent,
} from '../classes';
import {
  UnexpectedStateError,
} from '../errors';
import {
  bindHttpMethod,
  isUrlMatchingNoProxy,
  parseProxyUrl,
} from '../utilities';
import type {
  ProxyAgentConfigurationInputType,
  ProxyAgentConfigurationType,
} from '../types';
import createProxyController from './createProxyController';

const httpGet = http.get;
const httpRequest = http.request;
const httpsGet = https.get;
const httpsRequest = https.request;

const log = Logger.child({
  namespace: 'createGlobalProxyAgent',
});

const defaultConfigurationInput = {
  environmentVariableNamespace: undefined,
  forceGlobalAgent: undefined,
  socketConnectionTimeout: 60000,
};

const omitUndefined = (subject) => {
  const keys = Object.keys(subject);

  const result = {};

  for (const key of keys) {
    const value = subject[key];

    if (value !== undefined) {
      result[key] = value;
    }
  }

  return result;
};

const createConfiguration = (configurationInput: ProxyAgentConfigurationInputType): ProxyAgentConfigurationType => {
  // eslint-disable-next-line no-process-env
  const environment = process.env;

  const defaultConfiguration = {
    environmentVariableNamespace: typeof environment.GLOBAL_AGENT_ENVIRONMENT_VARIABLE_NAMESPACE === 'string' ? environment.GLOBAL_AGENT_ENVIRONMENT_VARIABLE_NAMESPACE : 'GLOBAL_AGENT_',
    forceGlobalAgent: typeof environment.GLOBAL_AGENT_FORCE_GLOBAL_AGENT === 'string' ? parseBoolean(environment.GLOBAL_AGENT_FORCE_GLOBAL_AGENT) : true,
    socketConnectionTimeout: typeof environment.GLOBAL_AGENT_SOCKET_CONNECTION_TIMEOUT === 'string' ? Number.parseInt(environment.GLOBAL_AGENT_SOCKET_CONNECTION_TIMEOUT, 10) : defaultConfigurationInput.socketConnectionTimeout,
  };

  // $FlowFixMe
  return {
    ...defaultConfiguration,
    ...omitUndefined(configurationInput),
  };
};

export default (configurationInput: ProxyAgentConfigurationInputType = defaultConfigurationInput) => {
  const configuration = createConfiguration(configurationInput);

  const proxyController = createProxyController();

  // eslint-disable-next-line no-process-env
  proxyController.HTTP_PROXY = process.env[configuration.environmentVariableNamespace + 'HTTP_PROXY'] || null;

  // eslint-disable-next-line no-process-env
  proxyController.HTTPS_PROXY = process.env[configuration.environmentVariableNamespace + 'HTTPS_PROXY'] || null;

  // eslint-disable-next-line no-process-env
  proxyController.NO_PROXY = process.env[configuration.environmentVariableNamespace + 'NO_PROXY'] || null;

  log.info({
    configuration,
    state: proxyController,
  }, 'global agent has been initialized');

  const mustUrlUseProxy = (getProxy) => {
    return (url) => {
      if (!getProxy()) {
        return false;
      }

      if (!proxyController.NO_PROXY) {
        return true;
      }

      return !isUrlMatchingNoProxy(url, proxyController.NO_PROXY);
    };
  };

  const getUrlProxy = (getProxy) => {
    return () => {
      const proxy = getProxy();

      if (!proxy) {
        throw new UnexpectedStateError('HTTP(S) proxy must be configured.');
      }

      return parseProxyUrl(proxy);
    };
  };

  const getHttpProxy = () => {
    return proxyController.HTTP_PROXY;
  };

  const BoundHttpProxyAgent = class extends HttpProxyAgent {
    constructor () {
      super(
        () => {
          return getHttpProxy();
        },
        mustUrlUseProxy(getHttpProxy),
        getUrlProxy(getHttpProxy),
        http.globalAgent,
        configuration.socketConnectionTimeout,
      );
    }
  };

  const httpAgent = new BoundHttpProxyAgent();

  const getHttpsProxy = () => {
    return proxyController.HTTPS_PROXY || proxyController.HTTP_PROXY;
  };

  const BoundHttpsProxyAgent = class extends HttpsProxyAgent {
    constructor () {
      super(
        () => {
          return getHttpsProxy();
        },
        mustUrlUseProxy(getHttpsProxy),
        getUrlProxy(getHttpsProxy),
        https.globalAgent,
        configuration.socketConnectionTimeout,
      );
    }
  };

  const httpsAgent = new BoundHttpsProxyAgent();

  // Overriding globalAgent was added in v11.7.
  // @see https://nodejs.org/uk/blog/release/v11.7.0/
  if (semver.gte(process.version, 'v11.7.0')) {
    // @see https://github.com/facebook/flow/issues/7670
    // $FlowFixMe
    http.globalAgent = httpAgent;

    // $FlowFixMe
    https.globalAgent = httpsAgent;
  }

  // The reason this logic is used in addition to overriding http(s).globalAgent
  // is because there is no guarantee that we set http(s).globalAgent variable
  // before an instance of http(s).Agent has been already constructed by someone,
  // e.g. Stripe SDK creates instances of http(s).Agent at the top-level.
  // @see https://github.com/gajus/global-agent/pull/13
  //
  // We still want to override http(s).globalAgent when possible to enable logic
  // in `bindHttpMethod`.
  if (semver.gte(process.version, 'v10.0.0')) {
    // $FlowFixMe
    http.get = bindHttpMethod(httpGet, httpAgent, configuration.forceGlobalAgent);

    // $FlowFixMe
    http.request = bindHttpMethod(httpRequest, httpAgent, configuration.forceGlobalAgent);

    // $FlowFixMe
    https.get = bindHttpMethod(httpsGet, httpsAgent, configuration.forceGlobalAgent);

    // $FlowFixMe
    https.request = bindHttpMethod(httpsRequest, httpsAgent, configuration.forceGlobalAgent);
  } else {
    log.warn('attempt to initialize global-agent in unsupported Node.js version was ignored');
  }

  return proxyController;
};
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             // @flow

import Logger from '../Logger';

type ProxyControllerType = {|
  HTTP_PROXY: string | null,
  HTTPS_PROXY: string | null,
  NO_PROXY: string | null,
|};

const log = Logger.child({
  namespace: 'createProxyController',
});

const KNOWN_PROPERTY_NAMES = [
  'HTTP_PROXY',
  'HTTPS_PROXY',
  'NO_PROXY',
];

export default (): ProxyControllerType => {
  // eslint-disable-next-line fp/no-proxy
  return new Proxy({
    HTTP_PROXY: null,
    HTTPS_PROXY: null,
    NO_PROXY: null,
  }, {
    set: (subject, name, value) => {
      if (!KNOWN_PROPERTY_NAMES.includes(name)) {
        throw new Error('Cannot set an unmapped property "' + name + '".');
      }

      subject[name] = value;

      log.info({
        change: {
          name,
          value,
        },
        newConfiguration: subject,
      }, 'configuration changed');

      return true;
    },
  });
};
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              INDX( 	 � b           (   p  �       �                    ہ    ` P     ց    ��"1���f�%1������i�����i��                        c l a s s e s ׁ    h T     ց    ��!1���`��7�����i���YZc��0      +              	 e r r o r s . j s     ��    h T     ց    ��&1����j(1������i�����i��                       	 f a c t o r i e s     ؁    h R     ց    �!1���Q���7�����i����Zc��h       d                i n d e x . j s       ف    h T     