s._speed *= scaleFactor;
        }
    }
    // Getter and setter for precision
    get precision() {
        return globals.precision;
    }
    set precision(precision) {
        globals.precision = precision;
    }
}
const engine = /*#__PURE__*/ (() => {
    const engine = new Engine(now());
    if (isBrowser) {
        globalVersions.engine = engine;
        doc.addEventListener('visibilitychange', () => {
            if (!engine.pauseOnDocumentHidden)
                return;
            doc.hidden ? engine.pause() : engine.resume();
        });
    }
    return engine;
})();
const tickEngine = () => {
    if (engine._head) {
        engine.reqId = engineTickMethod(tickEngine);
        engine.update();
    }
    else {
        engine.reqId = 0;
    }
};
const killEngine = () => {
    engineCancelMethod(/** @type {NodeJS.Immediate & Number} */ (engine.reqId));
    engine.reqId = 0;
    return engine;
};


/**
 * @param  {DOMTarget} target
 * @param  {String} propName
 * @param  {Object} animationInlineStyles
 * @return {String}
 */
const parseInlineTransforms = (target, propName, animationInlineStyles) => {
    const inlineTransforms = target.style.transform;
    let inlinedStylesPropertyValue;
    if (inlineTransforms) {
        const cachedTransforms = target[transformsSymbol];
        let t;
        while (t = transformsExecRgx.exec(inlineTransforms)) {
            const inlinePropertyName = t[1];
            // const inlinePropertyValue = t[2];
            const inlinePropertyValue = t[2].slice(1, -1);
            cachedTransforms[inlinePropertyName] = inlinePropertyValue;
            if (inlinePropertyName === propName) {
                inlinedStylesPropertyValue = inlinePropertyValue;
                // Store the new parsed inline styles if animationInlineStyles is provided
                if (animationInlineStyles) {
                    animationInlineStyles[propName] = inlinePropertyValue;
                }
            }
        }
    }
    return inlineTransforms && !isUnd(inlinedStylesPropertyValue) ? inlinedStylesPropertyValue :
        stringStartsWith(propName, 'scale') ? '1' :
            stringStartsWith(propName, 'rotate') || stringStartsWith(propName, 'skew') ? '0deg' : '0px';
};


/**
 * @param  {DOMTargetsParam|TargetsParam} v
 * @return {NodeList|HTMLCollection}
 */
function getNodeList(v) {
    const n = isStr(v) ? globals.root.querySelectorAll(v) : v;
    if (n instanceof NodeList || n instanceof HTMLCollection)
        return n;
}
/**
 * @overload
 * @param  {DOMTargetsParam} targets
 * @return {DOMTargetsArray}
 *
 * @overload
 * @param  {JSTargetsParam} targets
 * @return {JSTargetsArray}
 *
 * @overload
 * @param  {TargetsParam} targets
 * @return {TargetsArray}
 *
 * @param  {DOMTargetsParam|JSTargetsParam|TargetsParam} targets
 */
function parseTargets(targets) {
    if (isNil(targets))
        return /** @type {TargetsArray} */ ([]);
    if (isArr(targets)) {
        const flattened = targets.flat(Infinity);
        /** @type {TargetsArray} */
        const parsed = [];
        for (let i = 0, l = flattened.length; i < l; i++) {
            const item = flattened[i];
            if (!isNil(item)) {
                const nodeList = getNodeList(item);
                if (nodeList) {
                    for (let j = 0, jl = nodeList.length; j < jl; j++) {
                        const subItem = nodeList[j];
                        if (!isNil(subItem)) {
                            let isDuplicate = false;
                            for (let k = 0, kl = parsed.length; k < kl; k++) {
                                if (parsed[k] === subItem) {
                                    isDuplicate = true;
                                    break;
                                }
                            }
                            if (!isDuplicate) {
                                parsed.push(subItem);
                            }
                        }
                    }
                }
                else {
                    let isDuplicate = false;
                    for (let j = 0, jl = parsed.length; j < jl; j++) {
                        if (parsed[j] === item) {
                            isDuplicate = true;
                            break;
                        }
                    }
                    if (!isDuplicate) {
                        parsed.push(item);
                    }
                }
            }
        }
        return parsed;
    }
    if (!isBrowser)
        return /** @type {JSTargetsArray} */ ([targets]);
    const nodeList = getNodeList(targets);
    if (nodeList)
        return /** @type {DOMTargetsArray} */ (Array.from(nodeList));
    return /** @type {TargetsArray} */ ([targets]);
}
/**
 * @overload
 * @param  {DOMTargetsParam} targets
 * @return {DOMTargetsArray}
 *
 * @overload
 * @param  {JSTargetsParam} targets
 * @return {JSTargetsArray}
 *
 * @overload
 * @param  {TargetsParam} targets
 * @return {TargetsArray}
 *
 * @param  {DOMTargetsParam|JSTargetsParam|TargetsParam} targets
 */
function registerTargets(targets) {
    const parsedTargetsArray = parseTargets(targets);
    const parsedTargetsLength = parsedTargetsArray.length;
    if (parsedTargetsLength) {
        for (let i = 0; i < parsedTargetsLength; i++) {
            const target = parsedTargetsArray[i];
            if (!target[isRegisteredTargetSymbol]) {
                target[isRegisteredTargetSymbol] = true;
                const isSvgType = isSvg(target);
                const isDom = /** @type {DOMTarget} */ (target).nodeType || isSvgType;
                if (isDom) {
                    target[isDomSymbol] = true;
                    target[isSvgSymbol] = isSvgType;
                    target[transformsSymbol] = {};
                }
            }
        }
    }
    return parsedTargetsArray;
}


/**
 * @param  {TargetsParam} path
 * @return {SVGGeometryElement|undefined}
 */
const getPath = path => {
    const parsedTargets = parseTargets(path);
    const $parsedSvg = /** @type {SVGGeometryElement} */ (parsedTargets[0]);
    if (!$parsedSvg || !isSvg($parsedSvg))
        return;
    return $parsedSvg;
};
/**
 * @param  {TargetsParam} path2
 * @param  {Number} [precision]
 * @return {FunctionValue}
 */
const morphTo = (path2, precision = .33) => ($path1) => {
    const $path2 = /** @type {SVGGeometryElement} */ (getPath(path2));
    if (!$path2)
        return;
    const isPath = $path1.tagName === 'path';
    const separator = isPath ? ' ' : ',';
    const previousPoints = $path1[morphPointsSymbol];
    if (previousPoints)
        $path1.setAttribute(isPath ? 'd' : 'points', previousPoints);
    let v1 = '', v2 = '';
    if (!precision) {
        v1 = $path1.getAttribute(isPath ? 'd' : 'points');
        v2 = $path2.getAttribute(isPath ? 'd' : 'points');
    }
    else {
        const length1 = /** @type {SVGGeometryElement} */ ($path1).getTotalLength();
        const length2 = $path2.getTotalLength();
        const maxPoints = Math.max(Math.ceil(length1 * precision), Math.ceil(length2 * precision));
        for (let i = 0; i < maxPoints; i++) {
            const t = i / (maxPoints - 1);
            const pointOnPath1 = /** @type {SVGGeometryElement} */ ($path1).getPointAtLength(length1 * t);
            const pointOnPath2 = $path2.getPointAtLength(length2 * t);
            const prefix = isPath ? (i === 0 ? 'M' : 'L') : '';
            v1 += prefix + round(pointOnPath1.x, 3) + separator + pointOnPath1.y + ' ';
            v2 += prefix + round(pointOnPath2.x, 3) + separator + pointOnPath2.y + ' ';
        }
    }
    $path1[morphPointsSymbol] = v2;
    return [v1, v2];
};
/**
 * @param {SVGGeometryElement} [$el]
 * @return {Number}
 */
const getScaleFactor = $el => {
    let scaleFactor = 1;
    if ($el && $el.getCTM) {
        const ctm = $el.getCTM();
        if (ctm) {
            const scaleX = sqrt(ctm.a * ctm.a + ctm.b * ctm.b);
            const scaleY = sqrt(ctm.c * ctm.c + ctm.d * ctm.d);
            scaleFactor = (scaleX + scaleY) / 2;
        }
    }
    return scaleFactor;
};
/**
 * Creates a proxy that wraps an SVGGeometryElement and adds drawing functionality.
 * @param {SVGGeometryElement} $el - The SVG element to transform into a drawable
 * @param {number} start - Starting position (0-1)
 * @param {number} end - Ending position (0-1)
 * @return {DrawableSVGGeometry} - Returns a proxy that preserves the original element's type with additional 'draw' attribute functionality
 */
const createDrawableProxy = ($el, start, end) => {
    const pathLength = K;
    const computedStyles = getComputedStyle($el);
    const strokeLineCap = computedStyles.strokeLinecap;
    // @ts-ignore
    const $scalled = computedStyles.vectorEffect === 'non-scaling-stroke' ? $el : null;
    let currentCap = strokeLineCap;
    const proxy = new Proxy($el, {
        get(target, property) {
            const value = target[property];
            if (property === proxyTargetSymbol)
                return target;
            if (property === 'setAttribute') {
                return (...args) => {
                    if (args[0] === 'draw') {
                        const value = args[1];
                        const values = value.split(' ');
                        const v1 = +values[0];
                        const v2 = +values[1];
                        // TOTO: Benchmark if performing two slices is more performant than one split
                        // const spaceIndex = value.indexOf(' ');
                        // const v1 = round(+value.slice(0, spaceIndex), precision);
                        // const v2 = round(+value.slice(spaceIndex + 1), precision);
                        const scaleFactor = getScaleFactor($scalled);
                        const os = v1 * -1e3 * scaleFactor;
                        const d1 = (v2 * pathLength * scaleFactor) + os;
                        const d2 = (pathLength * scaleFactor +
                            ((v1 === 0 && v2 === 1) || (v1 === 1 && v2 === 0) ? 0 : 10 * scaleFactor) - d1);
                        if (strokeLineCap !== 'butt') {
                            const newCap = v1 === v2 ? 'butt' : strokeLineCap;
                            if (currentCap !== newCap) {
                                target.style.strokeLinecap = `${newCap}`;
                                currentCap = newCap;
                            }
                        }
                        target.setAttribute('stroke-dashoffset', `${os}`);
                        target.setAttribute('stroke-dasharray', `${d1} ${d2}`);
                    }
                    return Reflect.apply(value, target, args);
                };
            }
            if (isFnc(value)) {
                return (...args) => Reflect.apply(value, target, args);
            }
            else {
                return value;
            }
        }
    });
    if ($el.getAttribute('pathLength') !== `${pathLength}`) {
        $el.setAttribute('pathLength', `${pathLength}`);
        proxy.setAttribute('draw', `${start} ${end}`);
    }
    return /** @type {DrawableSVGGeometry} */ (proxy);
};
/**
 * Creates drawable proxies for multiple SVG elements.
 * @param {TargetsParam} selector - CSS selector, SVG element, or array of elements and selectors
 * @param {number} [start=0] - Starting position (0-1)
 * @param {number} [end=0] - Ending position (0-1)
 * @return {Array<DrawableSVGGeometry>} - Array of proxied elements with drawing functionality
 */
const createDrawable = (selector, start = 0, end = 0) => {
    const els = parseTargets(selector);
    return els.map($el => createDrawableProxy(
    /** @type {SVGGeometryElement} */ ($el), start, end));
};
// Motion path animation
/**
 * @param {SVGGeometryElement} $path
 * @param {Number} progress
 * @param {Number}lookup
 * @return {DOMPoint}
 */
const getPathPoint = ($path, progress, lookup = 0) => {
    return $path.getPointAtLength(progress + lookup >= 1 ? progress + lookup : 0);
};
/**
 * @param {SVGGeometryElement} $path
 * @param {String} pathProperty
 * @return {FunctionValue}
 */
const getPathProgess = ($path, pathProperty) => {
    return $el => {
        const totalLength = +($path.getTotalLength());
        const inSvg = $el[isSvgSymbol];
        const ctm = $path.getCTM();
        /** @type {TweenObjectValue} */
        return {
            from: 0,
            to: totalLength,
            /** @type {TweenModifier} */
            modifier: progress => {
                if (pathProperty === 'a') {
                    const p0 = getPathPoint($path, progress, -1);
                    const p1 = getPathPoint($path, progress, 1);
                    return atan2(p1.y - p0.y, p1.x - p0.x) * 180 / PI;
                }
                else {
                    const p = getPathPoint($path, progress, 0);
                    return pathProperty === 'x' ?
                        inSvg || !ctm ? p.x : p.x * ctm.a + p.y * ctm.c + ctm.e :
                        inSvg || !ctm ? p.y : p.x * ctm.b + p.y * ctm.d + ctm.f;
                }
            }
        };
    };
};
/**
 * @param {TargetsParam} path
 */
const createMotionPath = path => {
    const $path = getPath(path);
    if (!$path)
        return;
    return {
        translateX: getPathProgess($path, 'x'),
        translateY: getPathProgess($path, 'y'),
        rotate: getPathProgess($path, 'a'),
    };
};
// Check for valid SVG attribute
const cssReservedProperties = ['opacity', 'rotate', 'overflow', 'color'];
/**
 * @param  {Target} el
 * @param  {String} propertyName
 * @return {Boolean}
 */
const isValidSVGAttribute = (el, propertyName) => {
    // Return early and use CSS opacity animation instead (already better default values (opacity: 1 instead of 0)) and rotate should be considered a transform
    if (cssReservedProperties.includes(propertyName))
        return false;
    if (el.getAttribute(propertyName) || propertyName in el) {
        if (propertyName === 'scale') { // Scale
            const elParentNode = /** @type {SVGGeometryElement} */ ( /** @type {DOMTarget} */(el).parentNode);
            // Only consider scale as a valid SVG attribute on filter element
            return elParentNode && elParentNode.tagName === 'filter';
        }
        return true;
    }
};
const svg = {
    morphTo,
    createMotionPath,
    createDrawable,
};


/**
 * RGB / RGBA Color value string -> RGBA values array
 * @param  {String} rgbValue
 * @return {ColorArray}
 */
const rgbToRgba = rgbValue => {
    const rgba = rgbExecRgx.exec(rgbValue) || rgbaExecRgx.exec(rgbValue);
    const a = !isUnd(rgba[4]) ? +rgba[4] : 1;
    return [
        +rgba[1],
        +rgba[2],
        +rgba[3],
        a
    ];
};
/**
 * HEX3 / HEX3A / HEX6 / HEX6A Color value string -> RGBA values array
 * @param  {String} hexValue
 * @return {ColorArray}
 */
const hexToRgba = hexValue => {
    const hexLength = hexValue.length;
    const isShort = hexLength === 4 || hexLength === 5;
    return [
        +('0x' + hexValue[1] + hexValue[isShort ? 1 : 2]),
        +('0x' + hexValue[isShort ? 2 : 3] + hexValue[isShort ? 2 : 4]),
        +('0x' + hexValue[isShort ? 3 : 5] + hexValue[isShort ? 3 : 6]),
        ((hexLength === 5 || hexLength === 9) ? +(+('0x' + hexValue[isShort ? 4 : 7] + hexValue[isShort ? 4 : 8]) / 255).toFixed(3) : 1)
    ];
};
/**
 * @param  {Number} p
 * @param  {Number} q
 * @param  {Number} t
 * @return {Number}
 */
const hue2rgb = (p, q, t) => {
    if (t < 0)
        t += 1;
    if (t > 1)
        t -= 1;
    return t < 1 / 6 ? p + (q - p) * 6 * t :
        t < 1 / 2 ? q :
            t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 :
                p;
};
/**
 * HSL / HSLA Color value string -> RGBA values array
 * @param  {String} hslValue
 * @return {ColorArray}
 */
const hslToRgba = hslValue => {
    const hsla = hslExecRgx.exec(hslValue) || hslaExecRgx.exec(hslValue);
    const h = +hsla[1] / 360;
    const s = +hsla[2] / 100;
    const l = +hsla[3] / 100;
    const a = !isUnd(hsla[4]) ? +hsla[4] : 1;
    let r, g, b;
    if (s === 0) {
        r = g = b = l;
    }
    else {
        const q = l < .5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        r = round(hue2rgb(p, q, h + 1 / 3) * 255, 0);
        g = round(hue2rgb(p, q, h) * 255, 0);
        b = round(hue2rgb(p, q, h - 1 / 3) * 255, 0);
    }
    ret{
  "version": 3,
  "sources": ["../../react/cjs/react-jsx-runtime.development.js", "../../react/jsx-runtime.js"],
  "sourcesContent": ["/**\n * @license React\n * react-jsx-runtime.development.js\n *\n * Copyright (c) Meta Platforms, Inc. and affiliates.\n *\n * This source code is licensed under the MIT license found in the\n * LICENSE file in the root directory of this source tree.\n */\n\n\"use strict\";\n\"production\" !== process.env.NODE_ENV &&\n  (function () {\n    function getComponentNameFromType(type) {\n      if (null == type) return null;\n      if (\"function\" === typeof type)\n        return type.$$typeof === REACT_CLIENT_REFERENCE\n          ? null\n          : type.displayName || type.name || null;\n      if (\"string\" === typeof type) return type;\n      switch (type) {\n        case REACT_FRAGMENT_TYPE:\n          return \"Fragment\";\n        case REACT_PROFILER_TYPE:\n          return \"Profiler\";\n        case REACT_STRICT_MODE_TYPE:\n          return \"StrictMode\";\n        case REACT_SUSPENSE_TYPE:\n          return \"Suspense\";\n        case REACT_SUSPENSE_LIST_TYPE:\n          return \"SuspenseList\";\n        case REACT_ACTIVITY_TYPE:\n          return \"Activity\";\n      }\n      if (\"object\" === typeof type)\n        switch (\n          (\"number\" === typeof type.tag &&\n            console.error(\n              \"Received an unexpected object in getComponentNameFromType(). This is likely a bug in React. Please file an issue.\"\n            ),\n          type.$$typeof)\n        ) {\n          case REACT_PORTAL_TYPE:\n            return \"Portal\";\n          case REACT_CONTEXT_TYPE:\n            return (type.displayName || \"Context\") + \".Provider\";\n          case REACT_CONSUMER_TYPE:\n            return (type._context.displayName || \"Context\") + \".Consumer\";\n          case REACT_FORWARD_REF_TYPE:\n            var innerType = type.render;\n            type = type.displayName;\n            type ||\n              ((type = innerType.displayName || innerType.name || \"\"),\n              (type = \"\" !== type ? \"ForwardRef(\" + type + \")\" : \"ForwardRef\"));\n            return type;\n          case REACT_MEMO_TYPE:\n            return (\n              (innerType = type.displayName || null),\n              null !== innerType\n                ? innerType\n                : getComponentNameFromType(type.type) || \"Memo\"\n            );\n          case REACT_LAZY_TYPE:\n            innerType = type._payload;\n            type = type._init;\n            try {\n              return getComponentNameFromType(type(innerType));\n            } catch (x) {}\n        }\n      return null;\n    }\n    function testStringCoercion(value) {\n      return \"\" + value;\n    }\n    function checkKeyStringCoercion(value) {\n      try {\n        testStringCoercion(value);\n        var JSCompiler_inline_result = !1;\n      } catch (e) {\n        JSCompiler_inline_result = !0;\n      }\n      if (JSCompiler_inline_result) {\n        JSCompiler_inline_result = console;\n        var JSCompiler_temp_const = JSCompiler_inline_result.error;\n        var JSCompiler_inline_result$jscomp$0 =\n          (\"function\" === typeof Symbol &&\n            Symbol.toStringTag &&\n            value[Symbol.toStringTag]) ||\n          value.constructor.name ||\n          \"Object\";\n        JSCompiler_temp_const.call(\n          JSCompiler_inline_result,\n          \"The provided key is an unsupported type %s. This value must be coerced to a string before using it here.\",\n          JSCompiler_inline_result$jscomp$0\n        );\n        return testStringCoercion(value);\n      }\n    }\n    function getTaskName(type) {\n      if (type === REACT_FRAGMENT_TYPE) return \"<>\";\n      if (\n        \"object\" === typeof type &&\n        null !== type &&\n        type.$$typeof === REACT_LAZY_TYPE\n      )\n        return \"<...>\";\n      try {\n        var name = getComponentNameFromType(type);\n        return name ? \"<\" + name + \">\" : \"<...>\";\n      } catch (x) {\n        return \"<...>\";\n      }\n    }\n    function getOwner() {\n      var dispatcher = ReactSharedInternals.A;\n      return null === dispatcher ? null : dispatcher.getOwner();\n    }\n    function UnknownOwner() {\n      return Error(\"react-stack-top-frame\");\n    }\n    function hasValidKey(config) {\n      if (hasOwnProperty.call(config, \"key\")) {\n        var getter = Object.getOwnPropertyDescriptor(config, \"key\").get;\n        if (getter && getter.isReactWarning) return !1;\n      }\n      return void 0 !== config.key;\n    }\n    function defineKeyPropWarningGetter(props, displayName) {\n      function warnAboutAccessingKey() {\n        specialPropKeyWarningShown ||\n          ((specialPropKeyWarningShown = !0),\n          console.error(\n            \"%s: `key` is not a prop. Trying to access it will result in `undefined` being returned. If you need to access the same value within the child component, you should pass it as a different prop. (https://react.dev/link/special-props)\",\n            displayName\n          ));\n      }\n      warnAboutAccessingKey.isReactWarning = !0;\n      Object.defineProperty(props, \"key\", {\n        get: warnAboutAccessingKey,\n        configurable: !0\n      });\n    }\n    function elementRefGetterWithDeprecationWarning() {\n      var componentName = getComponentNameFromType(this.type);\n      didWarnAboutElementRef[componentName] ||\n        ((didWarnAboutElementRef[componentName] = !0),\n        console.error(\n          \"Accessing element.ref was removed in React 19. ref is now a regular prop. It will be removed from the JSX Element type in a future release.\"\n        ));\n      componentName = this.props.ref;\n      return void 0 !== componentName ? componentName : null;\n    }\n    function ReactElement(\n      type,\n      key,\n      self,\n      source,\n      owner,\n      props,\n      debugStack,\n      debugTask\n    ) {\n      self = props.ref;\n      type = {\n        $$typeof: REACT_ELEMENT_TYPE,\n        type: type,\n        key: key,\n        props: props,\n        _owner: owner\n      };\n      null !== (void 0 !== self ? self : null)\n        ? Object.defineProperty(type, \"ref\", {\n            enumerable: !1,\n            get: elementRefGetterWithDeprecationWarning\n          })\n        : Object.defineProperty(type, \"ref\", { enumerable: !1, value: null });\n      type._store = {};\n      Object.defineProperty(type._store, \"validated\", {\n        configurable: !1,\n        enumerable: !1,\n        writable: !0,\n        value: 0\n      });\n      Object.defineProperty(type, \"_debugInfo\", {\n        configurable: !1,\n        enumerable: !1,\n        writable: !0,\n        value: null\n      });\n      Object.defineProperty(type, \"_debugStack\", {\n        configurable: !1,\n        enumerable: !1,\n        writable: !0,\n        value: debugStack\n      });\n      Object.defineProperty(type, \"_debugTask\", {\n        configurable: !1,\n        enumerable: !1,\n        writable: !0,\n        value: debugTask\n      });\n      Object.freeze && (Object.freeze(type.props), Object.freeze(type));\n      return type;\n    }\n    function jsxDEVImpl(\n      type,\n      config,\n      maybeKey,\n      isStaticChildren,\n      source,\n      self,\n      debugStack,\n      debugTask\n    ) {\n      var children = config.children;\n      if (void 0 !== children)\n        if (isStaticChildren)\n          if (isArrayImpl(children)) {\n            for (\n              isStaticChildren = 0;\n              isStaticChildren < children.length;\n              isStaticChildren++\n            )\n              validateChildKeys(children[isStaticChildren]);\n            Object.freeze && Object.freeze(children);\n          } else\n            console.error(\n              \"React.jsx: Static children should always be an array. You are likely explicitly calling React.jsxs or React.jsxDEV. Use the Babel transform instead.\"\n            );\n        else validateChildKeys(children);\n      if (hasOwnProperty.call(config, \"key\")) {\n        children = getComponentNameFromType(type);\n        var keys = Object.keys(config).filter(function (k) {\n          return \"key\" !== k;\n        });\n        isStaticChildren =\n          0 < keys.length\n            ? \"{key: someKey, \" + keys.join(\": ..., \") + \": ...}\"\n            : \"{key: someKey}\";\n        didWarnAboutKeySpread[children + isStaticChildren] ||\n          ((keys =\n            0 < keys.length ? \"{\" + keys.join(\": ..., \") + \": ...}\" : \"{}\"),\n          console.error(\n            'A props object containing a \"key\" prop is being spread into JSX:\\n  let props = %s;\\n  <%s {...props} />\\nReact keys must be passed directly to JSX without using spread:\\n  let props = %s;\\n  <%s key={someKey} {...props} />',\n            isStaticChildren,\n            children,\n            keys,\n            children\n          ),\n          (didWarnAboutKeySpread[children + isStaticChildren] = !0));\n      }\n      children = null;\n      void 0 !== maybeKey &&\n        (checkKeyStringCoercion(maybeKey), (children = \"\" + maybeKey));\n      hasValidKey(config) &&\n        (checkKeyStringCoercion(config.key), (children = \"\" + config.key));\n      if (\"key\" in config) {\n        maybeKey = {};\n        for (var propName in config)\n          \"key\" !== propName && (maybeKey[propName] = config[propName]);\n      } else maybeKey = config;\n      children &&\n        defineKeyPropWarningGetter(\n          maybeKey,\n          \"function\" === typeof type\n            ? type.displayName || type.name || \"Unknown\"\n            : type\n        );\n      return ReactElement(\n        type,\n        children,\n        self,\n        source,\n        getOwner(),\n        maybeKey,\n        debugStack,\n        debugTask\n      );\n    }\n    function validateChildKeys(node) {\n      \"object\" === typeof node &&\n        null !== node &&\n        node.$$typeof === REACT_ELEMENT_TYPE &&\n        node._store &&\n        (node._store.validated = 1);\n    }\n    var React = require(\"react\"),\n      REACT_ELEMENT_TYPE = Symbol.for(\"react.transitional.element\"),\n      REACT_PORTAL_TYPE = Symbol.for(\"react.portal\"),\n      REACT_FRAGMENT_TYPE = Symbol.for(\"react.fragment\"),\n      REACT_STRICT_MODE_TYPE = Symbol.for(\"react.strict_mode\"),\n      REACT_PROFILER_TYPE = Symbol.for(\"react.profiler\");\n    Symbol.for(\"react.provider\");\n    var REACT_CONSUMER_TYPE = Symbol.for(\"react.consumer\"),\n      REACT_CONTEXT_TYPE = Symbol.for(\"react.context\"),\n      REACT_FORWARD_REF_TYPE = Symbol.for(\"react.forward_ref\"),\n      REACT_SUSPENSE_TYPE = Symbol.for(\"react.suspense\"),\n      REACT_SUSPENSE_LIST_TYPE = Symbol.for(\"react.suspense_list\"),\n      REACT_MEMO_TYPE = Symbol.for(\"react.memo\"),\n      REACT_LAZY_TYPE = Symbol.for(\"react.lazy\"),\n      REACT_ACTIVITY_TYPE = Symbol.for(\"react.activity\"),\n      REACT_CLIENT_REFERENCE = Symbol.for(\"react.client.reference\"),\n      ReactSharedInternals =\n        React.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,\n      hasOwnProperty = Object.prototype.hasOwnProperty,\n      isArrayImpl = Array.isArray,\n      createTask = console.createTask\n        ? console.createTask\n        : function () {\n            return null;\n          };\n    React = {\n      \"react-stack-bottom-frame\": function (callStackForError) {\n        return callStackForError();\n      }\n    };\n    var specialPropKeyWarningShown;\n    var didWarnAboutElementRef = {};\n    var unknownOwnerDebugStack = React[\"react-stack-bottom-frame\"].bind(\n      React,\n      UnknownOwner\n    )();\n    var unknownOwnerDebugTask = createTask(getTaskName(UnknownOwner));\n    var didWarnAboutKeySpread = {};\n    exports.Fragment = REACT_FRAGMENT_TYPE;\n    exports.jsx = function (type, config, maybeKey, source, self) {\n      var trackActualOwner =\n        1e4 > ReactSharedInternals.recentlyCreatedOwnerStacks++;\n      return jsxDEVImpl(\n        type,\n        config,\n        maybeKey,\n        !1,\n        source,\n        self,\n        trackActualOwner\n          ? Error(\"react-stack-top-frame\")\n          : unknownOwnerDebugStack,\n        trackActualOwner ? createTask(getTaskName(type)) : unknownOwnerDebugTask\n      );\n    };\n    exports.jsxs = function (type, config, maybeKey, source, self) {\n      var trackActualOwner =\n        1e4 > ReactSharedInternals.recentlyCreatedOwnerStacks++;\n      return jsxDEVImpl(\n        type,\n        config,\n        maybeKey,\n        !0,\n        source,\n        self,\n        trackActualOwner\n          ? Error(\"react-stack-top-frame\")\n          : unknownOwnerDebugStack,\n        trackActualOwner ? createTask(getTaskName(type)) : unknownOwnerDebugTask\n      );\n    };\n  })();\n", "'use strict';\n\nif (process.env.NODE_ENV === 'production') {\n  module.exports = require('./cjs/react-jsx-runtime.production.js');\n} else {\n  module.exports = require('./cjs/react-jsx-runtime.development.js');\n}\n"],
  "mappings": "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",
  "names": []
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       te->GetCurrentContext(), &src)
          .FromMaybe(v8::Local<v8::Script>()));
}

Factory<v8::Script>::return_t
Factory<v8::Script>::New( v8::Local<v8::String> source
                        , v8::ScriptOrigin const& origin) {
  v8::Isolate *isolate = v8::Isolate::GetCurrent();
  v8::EscapableHandleScope scope(isolate);
  v8::ScriptCompiler::Source src(source, origin);
  return scope.Escape(
      v8::ScriptCompiler::Compile(isolate->GetCurrentContext(), &src)
          .FromMaybe(v8::Local<v8::Script>()));
}
#else
Factory<v8::Script>::return_t
Factory<v8::Script>::New( v8::Local<v8::String> source) {
  v8::ScriptCompiler::Source src(source);
  return v8::ScriptCompiler::Compile(v8::Isolate::GetCurrent(), &src);
}

Factory<v8::Script>::return_t
Factory<v8::Script>::New( v8::Local<v8::String> source
                        , v8::ScriptOrigin const& origin) {
  v8::ScriptCompiler::Source src(source, origin);
  return v8::ScriptCompiler::Compile(v8::Isolate::GetCurrent(), &src);
}
#endif

//=== Signature ================================================================

Factory<v8::Signature>::return_t
Factory<v8::Signature>::New(Factory<v8::Signature>::FTH receiver) {
  return v8::Signature::New(v8::Isolate::GetCurrent(), receiver);
}

//=== String ===================================================================

Factory<v8::String>::return_t
Factory<v8::String>::New() {
  return v8::String::Empty(v8::Isolate::GetCurrent());
}

#if defined(V8_MAJOR_VERSION) && (V8_MAJOR_VERSION > 4 ||                      \
  (V8_MAJOR_VERSION == 4 && defined(V8_MINOR_VERSION) && V8_MINOR_VERSION >= 3))
Factory<v8::String>::return_t
Factory<v8::String>::New(const char * value, int length) {
  return v8::String::NewFromUtf8(
      v8::Isolate::GetCurrent(), value, v8::NewStringType::kNormal, length);
}

Factory<v8::String>::return_t
Factory<v8::String>::New(std::string const& value) {
  assert(value.size() <= INT_MAX && "string too long");
  return v8::String::NewFromUtf8(v8::Isolate::GetCurrent(),
      value.data(), v8::NewStringType::kNormal, static_cast<int>(value.size()));
}

Factory<v8::String>::return_t
Factory<v8::String>::New(const uint16_t * value, int length) {
  return v8::String::NewFromTwoByte(v8::Isolate::GetCurrent(), value,
        v8::NewStringType::kNormal, length);
}

Factory<v8::String>::return_t
Factory<v8::String>::New(v8::String::ExternalStringResource * value) {
  return v8::String::NewExternalTwoByte(v8::Isolate::GetCurrent(), value);
}

Factory<v8::String>::return_t
Factory<v8::String>::New(ExternalOneByteStringResource * value) {
  return v8::String::NewExternalOneByte(v8::Isolate::GetCurrent(), value);
}
#else
Factory<v8::String>::return_t
Factory<v8::String>::New(const char * value, int length) {
  return v8::String::NewFromUtf8(v8::Isolate::GetCurrent(), value,
                                 v8::String::kNormalString, length);
}

Factory<v8::String>::return_t
Factory<v8::String>::New(
    std::string const& value) /* NOLINT(build/include_what_you_use) */ {
  assert(value.size() <= INT_MAX && "string too long");
  return v8::String::NewFromUtf8(v8::Isolate::GetCurrent(), value.data(),
                                 v8::String::kNormalString,
                                 static_cast<int>(value.size()));
}

Factory<v8::String>::return_t
Factory<v8::String>::New(const uint16_t * value, int length) {
  return v8::String::NewFromTwoByte(v8::Isolate::GetCurrent(), value,
                                    v8::String::kNormalString, length);
}

Factory<v8::String>::return_t
Factory<v8::String>::New(v8::String::ExternalStringResource * value) {
  return v8::String::NewExternal(v8::Isolate::GetCurrent(), value);
}

Factory<v8::String>::return_t
Factory<v8::String>::New(ExternalOneByteStringResource * value) {
  return v8::String::NewExternal(v8::Isolate::GetCurrent(), value);
}
#endif

//=== String Object ============================================================

// See https://github.com/nodejs/nan/pull/811#discussion_r224594980.
// Disable the warning as there is no way around it.
// TODO(bnoordhuis) Use isolate-based version in Node.js v12.
Factory<v8::StringObject>::return_t
Factory<v8::StringObject>::New(v8::Local<v8::String> value) {
// V8 > 7.0
#if V8_MAJOR_VERSION > 7 || (V8_MAJOR_VERSION == 7 && V8_MINOR_VERSION > 0)
  return v8::StringObject::New(v8::Isolate::GetCurrent(), value)
      .As<v8::StringObject>();
#else
#ifdef _MSC_VER
#pragma warning(push)
#pragma warning(disable : 4996)
#endif
#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#endif
  return v8::StringObject::New(value).As<v8::StringObject>();
#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif
#ifdef _MSC_VER
#pragma warning(pop)
#endif
#endif
}

//=== Unbound Script ===========================================================

#if defined(V8_MAJOR_VERSION) && (V8_MAJOR_VERSION > 4 ||                      \
  (V8_MAJOR_VERSION == 4 && defined(V8_MINOR_VERSION) && V8_MINOR_VERSION >= 3))
Factory<v8::UnboundScript>::re