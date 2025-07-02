ormProperty}`]=parsedPropertyValue;cachedTransforms[individualTransformProperty]=parsedPropertyValue}else{keyframes[name]=parsedPropertyValue}addWAAPIAnimation(this,$el,name,keyframes,tweenParams)}}if(hasIndividualTransforms){let transforms=emptyString;for(let t in cachedTransforms){transforms+=`${transformsFragmentStrings[t]}var(--${t})) `}$el.style.transform=transforms}}));if(scroll){this.autoplay.link(this)}}forEach(callback){const cb=isStr(callback)?a=>a[callback]():callback;this.animations.forEach(cb);return this}get speed(){return this._speed}set speed(speed){this._speed=+speed;this.forEach((anim=>anim.playbackRate=speed))}get currentTime(){const controlAnimation=this.controlAnimation;const timeScale=globals.timeScale;return this.completed?this.duration:controlAnimation?+controlAnimation.currentTime*(timeScale===1?1:timeScale):0}set currentTime(time){const t=time*(globals.timeScale===1?1:K);this.forEach((anim=>{if(t>=this.duration)anim.play();anim.currentTime=t}))}get progress(){return this.currentTime/this.duration}set progress(progress){this.forEach((anim=>anim.currentTime=progress*this.duration||0))}resume(){if(!this.paused)return this;this.paused=false;return this.forEach("play")}pause(){if(this.paused)return this;this.paused=true;return this.forEach("pause")}alternate(){this.reversed=!this.reversed;this.forEach("reverse");if(this.paused)this.forEach("pause");return this}play(){if(this.reversed)this.alternate();return this.resume()}reverse(){if(!this.reversed)this.alternate();return this.resume()}seek(time,muteCallbacks=false){if(muteCallbacks)this.muteCallbacks=true;if(time<this.duration)this.completed=false;this.currentTime=time;this.muteCallbacks=false;if(this.paused)this.pause();return this}restart(){this.completed=false;return this.seek(0,true).resume()}commitStyles(){return this.forEach("commitStyles")}complete(){return this.seek(this.duration)}cancel(){this.forEach("cancel");return this.pause()}revert(){this.cancel();this.targets.forEach((($el,i)=>$el.setAttribute("style",this._inlineStyles[i])));return this}then(callback=noop){const then=this.then;const onResolve=()=>{this.then=null;callback(this);this.then=then;this._resolve=noop};return new Promise((r=>{this._resolve=()=>r(onResolve());if(this.completed)this._resolve();return this}))}}const waapi={animate:(targets,params)=>new WAAPIAnimation(targets,params),convertEase:easingToLinear};const sync=(callback=noop)=>new Timer({duration:1*globals.timeScale,onComplete:callback},null,0).resume();function getTargetValue(targetSelector,propName,unit){const targets=registerTargets(targetSelector);if(!targets.length)return;const[target]=targets;const tweenType=getTweenType(target,propName);const normalizePropName=sanitizePropertyName(propName,target,tweenType);let originalValue=getOriginalAnimatableValue(target,normalizePropName);if(isUnd(unit)){return originalValue}else{decomposeRawValue(originalValue,decomposedOriginalValue);if(decomposedOriginalValue.t===valueTypes.NUMBER||decomposedOriginalValue.t===valueTypes.UNIT){if(unit===false){return decomposedOriginalValue.n}else{const convertedValue=convertValueUnit(target,decomposedOriginalValue,unit,false);return`${round(convertedValue.n,globals.precision)}${convertedValue.u}`}}}}const setTargetValues=(targets,parameters)=>{if(isUnd(parameters))return;parameters.duration=minValue;parameters.composition=setValue(parameters.composition,compositionTypes.none);return new JSAnimation(targets,parameters,null,0,true).resume()};const removeTargetsFromAnimation=(targetsArray,animation,propertyName)=>{let tweensMatchesTargets=false;forEachChildren(animation,(tween=>{const tweenTarget=tween.target;if(targetsArray.includes(tweenTarget)){const tweenName=tween.property;const tweenType=tween._tweenType;const normalizePropName=sanitizePropertyName(propertyName,tweenTarget,tweenType);if(!normalizePropName||normalizePropName&&normalizePropName===tweenName){if(tween.parent._tail===tween&&tween._tweenType===tweenTypes.TRANSFORM&&tween._prev&&tween._prev._tweenType===tweenTypes.TRANSFORM){tween._prev._renderTransforms=1}removeChild(animation,tween);removeTweenSliblings(tween);tweensMatchesTargets=true}}}),true);return tweensMatchesTargets};const remove=(targets,renderable,propertyName)=>{const targetsArray=parseTargets(targets);const parent=renderable?renderable:engine;const waapiAnimation=renderable&&renderable.controlAnimation&&renderable;for(let i=0,l=targetsArray.length;i<l;i++){const $el=targetsArray[i];removeWAAPIAnimation($el,propertyName,waapiAnimation)}let removeMatches;if(parent._hasChildren){let iterationDuration=0;forEachChildren(parent,(child=>{if(!child._hasChildren){removeMatches=removeTargetsFromAnimation(targetsArray,child,propertyName);if(removeMatches&&!child._head){child.cancel();removeChild(parent,child)}else{const childTLOffset=child._offset+child._delay;const childDur=childTLOffset+child.duration;if(childDur>iterationDuration){iterationDuration=childDur}}}if(child._head){remove(targets,child,propertyName)}else{child._hasChildren=false}}),true);if(!isUnd(parent.iterationDuration)){parent.iterationDuration=iterationDuration}}else{removeMatches=removeTargetsFromAnimation(targetsArray,parent,propertyName)}if(removeMatches&&!parent._head){parent._hasChildren=false;if(parent.cancel)parent.cancel()}return targetsArray};const random=(min,max,decimalLength)=>{const m=10**(decimalLength||0);return floor((Math.random()*(max-min+1/m)+min)*m)/m};const randomPick=items=>items[random(0,items.length-1)];const shuffle=items=>{let m=items.length,t,i;while(m){i=random(0,--m);t=items[m];items[m]=items[i];items[i]=t}return items};const roundPad=(v,decimalLength)=>(+v).toFixed(decimalLength);const padStart=(v,totalLength,padString)=>`${v}`.padStart(totalLength,padString);const padEnd=(v,totalLength,padString)=>`${v}`.padEnd(totalLength,padString);const wrap=(v,min,max)=>((v-min)%(max-min)+(max-min))%(max-min)+min;const mapRange=(value,inLow,inHigh,outLow,outHigh)=>outLow+(value-inLow)/(inHigh-inLow)*(outHigh-outLow);const degToRad=degrees=>degrees*PI/180;const radToDeg=radians=>radians*180/PI;const lerp=(start,end,amount,renderable)=>{let dt=K/globals.defaults.frameRate;if(renderable!==false){const ticker=renderable||engine._hasChildren&&engine;if(ticker&&ticker.deltaTime){dt=ticker.deltaTime}}const t=1-Math.exp(-amount*dt*.1);return!amount?start:amount===1?end:(1-t)*start+t*end};const curry=(fn,last=0)=>(...args)=>last?v=>fn(...args,v):v=>fn(v,...args);const chain=fn=>(...args)=>{const result=fn(...args);return new Proxy(noop,{apply:(_,__,[v])=>result(v),get:(_,prop)=>chain(((...nextArgs)=>{const nextResult=utils[prop](...nextArgs);return v=>nextResult(result(v))}))})};const makeChainable=(fn,right=0)=>(...args)=>(args.length<fn.length?chain(curry(fn,right)):fn)(...args);const utils={$:registerTargets,get:getTargetValue,set:setTargetValues,remove:remove,cleanInlineStyles:cleanInlineStyles,random:random,randomPick:randomPick,shuffle:shuffle,lerp:lerp,sync:sync,clamp:makeChainable(clamp),round:makeChainable(round),snap:makeChainable(snap),wrap:makeChainable(wrap),interpolate:makeChainable(interpolate,1),mapRange:makeChainable(mapRange),roundPad:makeChainable(roundPad),padStart:makeChainable(padStart),padEnd:makeChainable(padEnd),degToRad:makeChainable(degToRad),radToDeg:makeChainable(radToDeg)};const getPrevChildOffset=(timeline,timePosition)=>{if(stringStartsWith(timePosition,"<")){const goToPrevAnimationOffset=timePosition[1]==="<";const prevAnimation=timeline._tail;const prevOffset=prevAnimation?prevAnimation._offset+prevAnimation._delay:0;return goToPrevAnimationOffset?prevOffset:prevOffset+prevAnimation.duration}};const parseTimelinePosition=(timeline,timePosition)=>{let tlDuration=timeline.iterationDuration;if(tlDuration===minValue)tlDuration=0;if(isUnd(timePosition))return tlDuration;if(isNum(+timePosition))return+timePosition;const timePosStr=timePosition;const tlLabels=timeline?timeline.labels:null;const hasLabels=!isNil(tlLabels);const prevOffset=getPrevChildOffset(timeline,timePosStr);const hasSibling=!isUnd(prevOffset);const matchedRelativeOperator=relativeValuesExecRgx.exec(timePosStr);if(matchedRelativeOperator){const fullOperator=matchedRelativeOperator[0];const split=timePosStr.split(fullOperator);const labelOffset=hasLabels&&split[0]?tlLabels[split[0]]:tlDuration;const parsedOffset=hasSibling?prevOffset:hasLabels?labelOffset:tlDuration;const parsedNumericalOffset=+split[1];return getRelativeValue(parsedOffset,parsedNumericalOffset,fullOperator[0])}else{return hasSibling?prevOffset:hasLabels?!isUnd(tlLabels[timePosStr])?tlLabels[timePosStr]:tlDuration:tlDuration}};function getTimelineTotalDuration(tl){return clampInfinity((tl.iterationDuration+tl._loopDelay)*tl.iterationCount-tl._loopDelay)||minValue}function addTlChild(childParams,tl,timePosition,targets,index,length){const isSetter=isNum(childParams.duration)&&childParams.duration<=minValue;const adjustedPosition=isSetter?timePosition-minValue:timePosition;tick(tl,adjustedPosition,1,1,tickModes.AUTO);const tlChild=targets?new JSAnimation(targets,childParams,tl,adjustedPosition,false,index,length):new Timer(childParams,tl,adjustedPosition);tlChild.init(1);addChild(tl,tlChild);forEachChildren(tl,(child=>{const childTLOffset=child._offset+child._delay;const childDur=childTLOffset+child.duration;if(childDur>tl.iterationDuration)tl.iterationDuration=childDur}));tl.duration=getTimelineTotalDuration(tl);return tl}class Timeline extends Timer{constructor(parameters={}){super(parameters,null,0);this.duration=0;this.labels={};const defaultsParams=parameters.defaults;const globalDefaults=globals.defaults;this.defaults=defaultsParams?mergeObjects(defaultsParams,globalDefaults):globalDefaults;this.onRender=parameters.onRender||globalDefaults.onRender;const tlPlaybackEase=setValue(parameters.playbackEase,globalDefaults.playbackEase);this._ease=tlPlaybackEase?parseEasings(tlPlaybackEase):null;this.iterationDuration=0}add(a1,a2,a3){const isAnim=isObj(a2);const isTimer=isObj(a1);if(isAnim||isTimer){this._hasChildren=true;if(isAnim){const childParams=a2;if(isFnc(a3)){const staggeredPosition=a3;const parsedTargetsArray=parseTargets(a1);const tlDuration=this.duration;const tlIterationDuration=this.iterationDuration;const id=childParams.id;let i=0;const parsedLength=parsedTargetsArray.length;parsedTargetsArray.forEach((target=>{const staggeredChildParams={...childParams};this.duration=tlDuration;this.iterationDuration=tlIterationDuration;if(!isUnd(id))staggeredChildParams.id=id+"-"+i;addTlChild(staggeredChildParams,this,staggeredPosition(target,i,parsedLength,this),target,i,parsedLength);i++}))}else{addTlChild(childParams,this,parseTimelinePosition(this,a3),a1)}}else{addTlChild(a1,this,parseTimelinePosition(this,a2))}return this.init(1)}}sync(synced,position){if(isUnd(synced)||synced&&isUnd(synced.pause))return this;synced.pause();const duration=+(synced.effect?synced.effect.getTiming().duration:synced.duration);return this.add(synced,{currentTime:[0,duration],duration:duration,ease:"linear"},position)}set(targets,parameters,position){if(isUnd(parameters))return this;parameters.duration=minValue;parameters.composition=compositionTypes.replace;return this.add(targets,parameters,position)}call(callback,position){if(isUnd(callback)||callback&&!isFnc(callback))return this;return this.add({duration:0,onComplete:()=>callback(this)},position)}label(labelName,position){if(isUnd(labelName)||labelName&&!isStr(labelName))return this;this.labels[labelName]=parseTimelinePosition(this,position);return this}remove(targets,propertyName){remove(targets,this,propertyName);return this}stretch(newDuration){const currentDuration=this.duration;if(currentDuration===normalizeTime(newDuration))return this;const timeScale=newDuration/currentDuration;const labels=this.labels;forEachChildren(this,(child=>child.stretch(child.duration*timeScale)));for(let labelName in labels)labels[labelName]*=timeScale;return super.stretch(newDuration)}refresh(){forEachChildren(this,(child=>{if(child.refresh)child.refresh()}));return this}revert(){super.revert();forEachChildren(this,(child=>child.revert),true);return cleanInlineStyles(this)}then(callback){return super.then(callback)}}const createTimeline=parameters=>new Timeline(parameters).init();class Animatable{constructor(targets,parameters){if(globals.scope)globals.scope.revertibles.push(this);const globalParams={};const properties={};this.targets=[];this.animations={};if(isUnd(targets)||isUnd(parameters))return;for(let propName in parameters){const paramValue=parameters[propName];if(isKey(propName)){properties[propName]=paramValue}else{globalParams[propName]=paramValue}}for(let propName in properties){const propValue=properties[propName];const isObjValue=isObj(propValue);let propParams={};let to="+=0";if(isObjValue){const unit=propValue.unit;if(isStr(unit))to+=unit}else{propParams.duration=propValue}propParams[propName]=isObjValue?mergeObjects({to:to},propValue):to;const animParams=mergeObjects(globalParams,propParams);animParams.composition=compositionTypes.replace;animParams.autoplay=false;const animation=this.animations[propName]=new JSAnimation(targets,animParams,null,0,false).init();if(!this.targets.length)this.targets.push(...animation.targets);this[propName]=(to,duration,ease)=>{const tween=animation._head;if(isUnd(to)&&tween){const numbers=tween._numbers;if(numbers&&numbers.length){return numbers}else{return tween._modifier(tween._number)}}else{forEachChildren(animation,(tween=>{if(isArr(to)){for(let i=0,l=to.length;i<l;i++){if(!isUnd(tween._numbers[i])){tween._fromNumbers[i]=tween._modifier(tween._numbers[i]);tween._toNumbers[i]=to[i]}}}else{tween._fromNumber=tween._modifier(tween._number);tween._toNumber=to}if(!isUnd(ease))tween._ease=parseEasings(ease);tween._currentTime=0}));if(!isUnd(duration))animation.stretch(duration);animation.reset(1).resume();return this}}}}revert(){for(let propName in this.animations){this[propName]=noop;this.animations[propName].revert()}this.animations={};this.targets.length=0;return this}}const createAnimatable=(targets,parameters)=>new Animatable(targets,parameters);class Spring{constructor(parameters={}){this.timeStep=.02;this.restThreshold=5e-4;this.restDuration=200;this.maxDuration=6e4;this.maxRestSteps=this.restDuration/this.timeStep/K;this.maxIterations=this.maxDuration/this.timeStep/K;this.m=clamp(setValue(parameters.mass,1),0,K);this.s=clamp(setValue(parameters.stiffness,100),1,K);this.d=clamp(setValue(parameters.damping,10),.1,K);this.v=clamp(setValue(parameters.velocity,0),-1e3,K);this.w0=0;this.zeta=0;this.wd=0;this.b=0;this.solverDuration=0;this.duration=0;this.compute();this.ease=t=>t===0||t===1?t:this.solve(t*this.solverDuration)}solve(time){const{zeta:zeta,w0:w0,wd:wd,b:b}=this;let t=time;if(zeta<1){t=exp(-t*zeta*w0)*(1*cos(wd*t)+b*sin(wd*t))}else{t=(1+b*t)*exp(-t*w0)}return 1-t}compute(){const{maxRestSteps:maxRestSteps,maxIterations:maxIterations,restThreshold:restThreshold,timeStep:timeStep,m:m,d:d,s:s,v:v}=this;const w0=this.w0=clamp(sqrt(s/m),minValue,K);const zeta=this.zeta=d/(2*sqrt(s*m));const wd=this.wd=zeta<1?w0*sqrt(1-zeta*zeta):0;this.b=zeta<1?(zeta*w0+-v)/wd:-v+w0;let solverTime=0;let restSteps=0;let iterations=0;while(restSteps<maxRestSteps&&iterations<maxIterations){if(abs(1-this.solve(solverTime))<restThreshold){restSteps++}else{restSteps=0}this.solverDuration=solverTime;solverTime+=timeStep;iterations++}this.duration=round(this.solverDuration*K,0)*globals.timeScale}get mass(){return this.m}set mass(v){this.m=clamp(setValue(v,1),0,K);this.compute()}get stiffness(){return this.s}set stiffness(v){this.s=clamp(setValue(v,100),1,K);this.compute()}get damping(){return this.d}set damping(v){this.d=clamp(setValue(v,10),.1,K);this.compute()}get velocity(){return this.v}set velocity(v){this.v=clamp(setValue(v,0),-1e3,K);this.compute()}}const createSpring=parameters=>new Spring(parameters);const preventDefault=e=>{if(e.cancelable)e.preventDefault()};class DOMProxy{constructor(el){this.el=el;this.zIndex=0;this.parentElement=null;this.classList={add:noop,remove:noop}}get x(){return this.el.x||0}set x(v){this.el.x=v}get y(){return this.el.y||0}set y(v){this.el.y=v}get width(){return this.el.width||0}set width(v){this.el.width=v}get height(){return this.el.height||0}set height(v){this.el.height=v}getBoundingClientRect(){return{top:this.y,right:this.x,bottom:this.y+this.# @mapbox/node-pre-gyp

#### @mapbox/node-pre-gyp makes it easy to publish and install Node.js C++ addons from binaries

[![Build Status](https://travis-ci.com/mapbox/node-pre-gyp.svg?branch=master)](https://travis-ci.com/mapbox/node-pre-gyp)
[![Build status](https://ci.appveyor.com/api/projects/status/3nxewb425y83c0gv)](https://ci.appveyor.com/project/Mapbox/node-pre-gyp)

`@mapbox/node-pre-gyp` stands between [npm](https://github.com/npm/npm) and [node-gyp](https://github.com/Tootallnate/node-gyp) and offers a cross-platform method of binary deployment.

### Special note on previous package

On Feb 9th, 2021 `@mapbox/node-pre-gyp@1.0.0` was [released](./CHANGELOG.md). Older, unscoped versions that are not part of the `@mapbox` org are deprecated and only `@mapbox/node-pre-gyp` will see updates going forward. To upgrade to the new package do:

```
npm uninstall node-pre-gyp --save
npm install @mapbox/node-pre-gyp --save
```

### Features

 - A command line tool called `node-pre-gyp` that can install your package's C++ module from a binary.
 - A variety of developer targeted commands for packaging, testing, and publishing binaries.
 - A JavaScript module that can dynamically require your installed binary: `require('@mapbox/node-pre-gyp').find`

For a hello world example of a module packaged with `node-pre-gyp` see <https://github.com/springmeyer/node-addon-example> and [the wiki ](https://github.com/mapbox/node-pre-gyp/wiki/Modules-using-node-pre-gyp) for real world examples.

## Credits

 - The module is modeled after [node-gyp](https://github.com/Tootallnate/node-gyp) by [@Tootallnate](https://github.com/Tootallnate)
 - Motivation for initial development came from [@ErisDS](https://github.com/ErisDS) and the [Ghost Project](https://github.com/TryGhost/Ghost).
 - Development is sponsored by [Mapbox](https://www.mapbox.com/)

## FAQ

See the [Frequently Ask Questions](https://github.com/mapbox/node-pre-gyp/wiki/FAQ).

## Depends

 - Node.js >= node v8.x

## Install

`node-pre-gyp` is designed to be installed as a local dependency of your Node.js C++ addon and accessed like:

    ./node_modules/.bin/node-pre-gyp --help

But you can also install it globally:

    npm install @mapbox/node-pre-gyp -g

## Usage

### Commands

View all possible commands:

    node-pre-gyp --help

- clean - Remove the entire folder containing the compiled .node module
- install - Install pre-built binary for module
- reinstall - Run "clean" and "install" at once
- build - Compile the module by dispatching to node-gyp or nw-gyp
- rebuild - Run "clean" and "build" at once
- package - Pack binary into tarball
- testpackage - Test that the staged package is valid
- publish - Publish pre-built binary
- unpublish - Unpublish pre-built binary
- info - Fetch info on published binaries

You can also chain commands:

    node-pre-gyp clean build unpublish publish info

### Options

Options include:

 - `-C/--directory`: run the command in this directory
 - `--build-from-source`: build from source instead of using pre-built binary
 - `--update-binary`: reinstall by replacing previously installed local binary with remote binary
 - `--runtime=node-webkit`: customize the runtime: `node`, `electron` and `node-webkit` are the valid options
 - `--fallback-to-build`: fallback to building from source if pre-built binary is not available
 - `--target=0.4.0`: Pass the target node or node-webkit version to compile against
 - `--target_arch=ia32`: Pass the target arch and override the host `arch`. Any value that is [supported by Node.js](https://nodejs.org/api/os.html#osarch) is valid.
 - `--target_platform=win32`: Pass the target platform and override the host `platform`. Valid values are `linux`, `darwin`, `win32`, `sunos`, `freebsd`, `openbsd`, and `aix`.

Both `--build-from-source` and `--fallback-to-build` can be passed alone or they can provide values. You can pass `--fallback-to-build=false` to override the option as declared in package.json. In addition to being able to pass `--build-from-source` you can also pass `--build-from-source=myapp` where `myapp` is the name of your module.

For example: `npm install --build-from-source=myapp`. This is useful if:

 - `myapp` is referenced in the package.json of a larger app and therefore `myapp` is being installed as a dependency with `npm install`.
 - The larger app also depends on other modules installed with `node-pre-gyp`
 - You only want to trigger a source compile for `myapp` and the other modules.

### Configuring

This is a guide to configuring your module to use node-pre-gyp.

#### 1) Add new entries to your `package.json`

 - Add `@mapbox/node-pre-gyp` to `dependencies`
 - Add `aws-sdk` as a `devDependency`
 - Add a custom `install` script
 - Declare a `binary` object

This looks like:

```js
    "dependencies"  : {
      "@mapbox/node-pre-gyp": "1.x"
    },
    "devDependencies": {
      "aws-sdk": "2.x"
    }
    "scripts": {
        "install": "node-pre-gyp install --fallback-to-build"
    },
    "binary": {
        "module_name": "your_module",
        "module_path": "./lib/binding/",
        "host": "https://your_module.s3-us-west-1.amazonaws.com"
    }
```

For a full example see [node-addon-examples's package.json](https://github.com/springmeyer/node-addon-example/blob/master/package.json).

Let's break this down:

 - Dependencies need to list `node-pre-gyp`
 - Your devDependencies should list `aws-sdk` so that you can run `node-pre-gyp publish` locally or a CI system. We recommend using `devDependencies` only since `aws-sdk` is large and not needed for `node-pre-gyp install` since it only uses http to fetch binaries
 - Your `scripts` section should override the `install` target with `"install": "node-pre-gyp install --fallback-to-build"`. This allows node-pre-gyp to be used instead of the default npm behavior of always source compiling with `node-gyp` directly.
 - Your package.json should contain a `binary` section describing key properties you provide to allow node-pre-gyp to package optimally. They are detailed below.

Note: in the past we recommended putting `@mapbox/node-pre-gyp` in the `bundledDependencies`, but we no longer recommend this. In the past there were npm bugs (with node versions 0.10.x) that could lead to node-pre-gyp not being available at the right time during install (unless we bundled). This should no longer be the case. Also, for a time we recommended using `"preinstall": "npm install @mapbox/node-pre-gyp"` as an alternative method to avoid needing to bundle. But this did not behave predictably across all npm versions - see https://github.com/mapbox/node-pre-gyp/issues/260 for the details. So we do not recommend using `preinstall` to install `@mapbox/node-pre-gyp`. More history on this at https://github.com/strongloop/fsevents/issues/157#issuecomment-265545908.

##### The `binary` object has three required properties

###### module_name

The name of your native node module. This value must:

 - Match the name passed to [the NODE_MODULE macro](http://nodejs.org/api/addons.html#addons_hello_world)
 - Must be a valid C variable name (e.g. it cannot contain `-`)
 - Should not include the `.node` extension.

###### module_path

The location your native module is placed after a build. This should be an empty directory without other Javascript files. This entire directory will be packaged in the binary tarball. When installing from a remote package this directory will be overwritten with the contents of the tarball.

Note: This property supports variables based on [Versioning](#versioning).

###### host

A url to the remote location where you've published tarball binaries (must be `https` not `http`).

It is highly recommended that you use Amazon S3. The reasons are:

  - Various node-pre-gyp commands like `publish` and `info` only work with an S3 host.
  - S3 is a very solid hosting platform for distributing large files.
  - We provide detail documentation for using [S3 hosting](#s3-hosting) with node-pre-gyp.

Why then not require S3? Because while some applications using node-pre-gyp need to distribute binaries as large as 20-30 MB, others might have very small binaries and might wish to store them in a GitHub repo. This is not recommended, but if an author really wants to host in a non-S3 location then it should be possible.

It should also be mentioned that there is an optional and entirely separate npm module called [node-pre-gyp-github](https://github.com/bchr02/node-pre-gyp-github) which is intended to complement node-pre-gyp and be installed along with it. It provides the ability to store and publish your binaries within your repositories GitHub Releases if you would rather not use S3 directly. Installation and usage instructions can be found [here](https://github.com/bchr02/node-pre-gyp-github), but the basic premise is that instead of using the ```node-pre-gyp publish``` command you would use ```node-pre-gyp-github publish```.

##### The `binary` object other optional S3 properties

If you are not using a standard s3 path like `bucket_name.s3(.-)region.amazonaws.com`, you might get an error on `publish` because node-pre-gyp extracts the region and bucket from the `host` url. For example, you may have an on-premises s3-compatible storage  server, or may have configured a specific dns redirecting to an s3  endpoint. In these cases, you can explicitly set the `region` and `bucket` properties to tell node-pre-gyp to use these values instead of guessing from the `host` property. The following values can be used in the `binary` section:

###### host

The url to the remote server root location (must be `https` not `http`).

###### bucket

The bucket name where your tarball binaries should be located.

###### region

Your S3 server region.

###### s3ForcePathStyle

Set `s3ForcePathStyle` to true if the endpoint url should not be prefixed with the bucket name. If false (default), the server endpoint would be  constructed as `bucket_name.your_server.com`.

##### The `binary` object has optional properties

###### remote_path

It **is recommended** that you customize this property. This is an extra path to use for publishing and finding remote tarballs. The default value for `remote_path` is `""` meaning that if you do not provide it then all packages will be published at the base of the `host`. It is recommended to provide a value like `./{name}/v{version}` to help organize remote packages in the case that you choose to publish multiple node addons to the same `host`.

Note: This property supports variables based on [Versioning](#versioning).

###### package_name

It is **not recommended** to override this property unless you are also overriding the `remote_path`. This is the versioned name of the remote tarball containing the binary `.node` module and any supporting files you've placed inside the `module_path` directory. Unless you specify `package_name` in your `package.json` then it defaults to `{module_name}-v{version}-{node_abi}-{platform}-{arch}.tar.gz` which allows your binary to work across node versions, platforms, and architectures. If you are using `remote_path` that is also versioned by `./{module_name}/v{version}` then you could remove these variables from the `package_name` and just use: `{node_abi}-{platform}-{arch}.tar.gz`. Then your remote tarball will be looked up at, for example, `https://example.com/your-module/v0.1.0/node-v11-linux-x64.tar.gz`.

Avoiding the version of your module in the `package_name` and instead only embedding in a directory name can be useful when you want to make a quick tag of your 