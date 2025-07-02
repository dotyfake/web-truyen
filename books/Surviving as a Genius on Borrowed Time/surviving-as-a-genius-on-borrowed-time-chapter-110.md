 }
    else {
        forEachChildren(timer, (/** @type {Tween} tween*/ tween) => {
            if (tween._composition !== compositionTypes.none) {
                composeTween(tween, getTweenSiblings(tween.target, tween.property));
            }
        });
    }
    timer._cancelled = 0;
    return timer;
};
let timerId = 0;
/**
 * Base class used to create Timers, Animations and Timelines
 */
class Timer extends Clock {
    /**
     * @param {TimerParams} [parameters]
     * @param {Timeline} [parent]
     * @param {Number} [parentPosition]
     */
    constructor(parameters = {}, parent = null, parentPosition = 0) {
        super(0);
        const { id, delay, duration, reversed, alternate, loop, loopDelay, autoplay, frameRate, playbackRate, onComplete, onLoop, onPause, onBegin, onBeforeUpdate, onUpdate, } = parameters;
        if (globals.scope)
            globals.scope.revertibles.push(this);
        const timerInitTime = parent ? 0 : engine._elapsedTime;
        const timerDefaults = parent ? parent.defaults : globals.defaults;
        const timerDelay = /** @type {Number} */ (isFnc(delay) || isUnd(delay) ? timerDefaults.delay : +delay);
        const timerDuration = isFnc(duration) || isUnd(duration) ? Infinity : +duration;
        const timerLoop = setValue(loop, timerDefaults.loop);
        const timerLoopDelay = setValue(loopDelay, timerDefaults.loopDelay);
        const timerIterationCount = timerLoop === true ||
            timerLoop === Infinity ||
            /** @type {Number} */ (timerLoop) < 0 ? Infinity :
            /** @type {Number} */ (timerLoop) + 1;
        let offsetPosition = 0;
        if (parent) {
            offsetPosition = parentPosition;
        }
        else {
            let startTime = now();
            // Make sure to tick the engine once if suspended to avoid big gaps with the following offsetPosition calculation
            if (engine.paused) {
                engine.requestTick(startTime);
                startTime = engine._elapsedTime;
            }
            offsetPosition = startTime - engine._startTime;
        }
        // Timer's parameters
        this.id = !isUnd(id) ? id : ++timerId;
        /** @type {Timeline} */
        this.parent = parent;
        // Total duration of the timer
        this.duration = clampInfinity(((timerDuration + timerLoopDelay) * timerIterationCount) - timerLoopDelay) || minValue;
        /** @type {Boolean} */
        this.backwards = false;
        /** @type {Boolean} */
        this.paused = true;
        /** @type {Boolean} */
        this.began = false;
        /** @type {Boolean} */
        this.completed = false;
        /** @type {Callback<this>} */
        this.onBegin = onBegin || timerDefaults.onBegin;
        /** @type {Callback<this>} */
        this.onBeforeUpdate = onBeforeUpdate || timerDefaults.onBeforeUpdate;
        /** @type {Callback<this>} */
        this.onUpdate = onUpdate || timerDefaults.onUpdate;
        /** @type {Callback<this>} */
        this.onLoop = onLoop || timerDefaults.onLoop;
        /** @type {Callback<this>} */
        this.onPause = onPause || timerDefaults.onPause;
        /** @type {Callback<this>} */
        this.onComplete = onComplete || timerDefaults.onComplete;
        /** @type {Number} */
        this.iterationDuration = timerDuration; // Duration of one loop
        /** @type {Number} */
        this.iterationCount = timerIterationCount; // Number of loops
        /** @type {Boolean|ScrollObserver} */
        this._autoplay = parent ? false : setValue(autoplay, timerDefaults.autoplay);
        /** @type {Number} */
        this._offset = offsetPosition;
        /** @type {Number} */
        this._delay = timerDelay;
        /** @type {Number} */
        this._loopDelay = timerLoopDelay;
        /** @type {Number} */
        this._iterationTime = 0;
        /** @type {Number} */
        this._currentIteration = 0; // Current loop index
        /** @type {Function} */
        this._resolve = noop; // Used by .then()
        /** @type {Boolean} */
        this._running = false;
        /** @type {Number} */
        this._reversed = +setValue(reversed, timerDefaults.reversed);
        /** @type {Number} */
        this._reverse = this._reversed;
        /** @type {Number} */
        this._cancelled = 0;
        /** @type {Boolean} */
        this._alternate = setValue(alternate, timerDefaults.alternate);
        /** @type {Renderable} */
        this._prev = null;
        /** @type {Renderable} */
        this._next = null;
        // Clock's parameters
        /** @type {Number} */
        this._elapsedTime = timerInitTime;
        /** @type {Number} */
        this._startTime = timerInitTime;
        /** @type {Number} */
        this._lastTime = timerInitTime;
        /** @type {Number} */
        this._fps = setValue(frameRate, timerDefaults.frameRate);
        /** @type {Number} */
        this._speed = setValue(playbackRate, timerDefaults.playbackRate);
    }
    get cancelled() {
        return !!this._cancelled;
    }
    /** @param {Boolean} cancelled  */
    set cancelled(cancelled) {
        cancelled ? this.cancel() : this.reset(1).play();
    }
    get currentTime() {
        return clamp(round(this._currentTime, globals.precision), -this._delay, this.duration);
    }
    /** @param {Number} time  */
    set currentTime(time) {
        const paused = this.paused;
        // Pausing the timer is necessary to avoid time jumps on a running instance
        this.pause().seek(+time);
        if (!paused)
            this.resume();
    }
    get iterationCurrentTime() {
        return round(this._iterationTime, globals.precision);
    }
    /** @param {Number} time  */
    set iterationCurrentTime(time) {
        this.currentTime = (this.iterationDuration * this._currentIteration) + time;
    }
    get progress() {
        return clamp(round(this._currentTime / this.duration, 5), 0, 1);
    }
    /** @param {Number} progress  */
    set progress(progress) {
        this.currentTime = this.duration * progress;
    }
    get iterationProgress() {
        return clamp(round(this._iterationTime / this.iterationDuration, 5), 0, 1);
    }
    /** @param {Number} progress  */
    set iterationProgress(progress) {
        const iterationDuration = this.iterationDuration;
        this.currentTime = (iterationDuration * this._currentIteration) + (iterationDuration * progress);
    }
    get currentIteration() {
        return this._currentIteration;
    }
    /** @param {Number} iterationCount  */
    set currentIteration(iterationCount) {
        this.currentTime = (this.iterationDuration * clamp(+iterationCount, 0, this.iterationCount - 1));
    }
    get reversed() {
        return !!this._reversed;
    }
    /** @param {Boolean} reverse  */
    set reversed(reverse) {
        reverse ? this.reverse() : this.play();
    }
    get speed() {
        return super.speed;
    }
    /** @param {Number} playbackRate  */
    set speed(playbackRate) {
        super.speed = playbackRate;
        this.resetTime();
    }
    /**
     * @param  {Number} internalRender
     * @return {this}
     */
    reset(internalRender = 0) {
        // If cancelled, revive the timer before rendering in order to have propertly composed tweens siblings
        reviveTimer(this);
        if (this._reversed && !this._reverse)
            this.reversed = false;
        // Rendering before updating the completed flag to prevent skips and to make sure the properties are not overridden
        // Setting the iterationTime at the end to force the rendering to happend backwards, otherwise calling .reset() on Timelines might not render children in the right order
        // NOTE: This is only required for Timelines and might be better to move to the Timeline class?
        this._iterationTime = this.iterationDuration;
        // Set tickMode to tickModes.FORCE to force rendering
        tick(this, 0, 1, internalRender, tickModes.FORCE);
        // Reset timer properties after revive / render to make sure the props are not updated again
        resetTimerProperties(this);
        // Also reset children properties
        if (this._hasChildren) {
            forEachChildren(this, resetTimerProperties);
        }
        return this;
    }
    /**
     * @param  {Number} internalRender
     * @return {this}
     */
    init(internalRender = 0) {
        this.fps = this._fps;
        this.speed = this._speed;
        // Manually calling .init() on timelines should render all children intial state
        // Forces all children to render once then render to 0 when reseted
        if (!internalRender && this._hasChildren) {
            tick(this, this.duration, 1, internalRender, tickModes.FORCE);
        }
        this.reset(internalRender);
        // Make sure to set autoplay to false to child timers so it doesn't attempt to autoplay / link
        const autoplay = this._autoplay;
        if (autoplay === true) {
            this.resume();
        }
        else if (autoplay && !isUnd(/** @type {ScrollObserver} */ (autoplay).linked)) {
            /** @type {ScrollObserver} */ (autoplay).link(this);
        }
        return this;
    }
    /** @return {this} */
    resetTime() {
        const timeScale = 1 / (this._speed * engine._speed);
        this._startTime = now() - (this._currentTime + this._delay) * timeScale;
        return this;
    }
    /** @return {this} */
    pause() {
        if (this.paused)
            return this;
        this.paused = true;
        this.onPause(this);
        return this;
    }
    /** @return {this} */
    resume() {
        if (!this.paused)
            return this;
        this.paused = false;
        // We can safely imediatly render a timer that has no duration and no children
        if (this.duration <= minValue && !this._hasChildren) {
            tick(this, minValue, 0, 0, tickModes.FORCE);
        }
        else {
            if (!this._running) {
                addChild(engine, this);
                engine._hasChildren = true;
                this._running = true;
            }
            this.resetTime();
            // Forces the timer to advance by at least one frame when the next tick occurs
            this._startTime -= 12;
            engine.wake();
        }
        return this;
    }
    /** @return {this} */
    restart() {
        return this.reset(0).resume();
    }
    /**
     * @param  {Number} time
     * @param  {Boolean|Number} [muteCallbacks]
     * @param  {Boolean|Number} [internalRender]
     * @return {this}
     */
    seek(time, muteCallbacks = 0, internalRender = 0) {
        // Recompose the tween siblings in case the timer has been cancelled
        reviveTimer(this);
        // If you seek a completed animation, otherwise the next play will starts at 0
        this.completed = false;
        const isPaused = this.paused;
        this.paused = true;
        // timer, time, muteCallbacks, internalRender, tickMode
        tick(this, time + this._delay, ~~muteCallbacks, ~~internalRender, tickModes.AUTO);
        return isPaused ? this : this.resume();
    }
    /** @return {this} */
    alternate() {
        const reversed = this._reversed;
        const count = this.iterationCount;
        const duration = this.iterationDuration;
        // Calculate the maximum iterations possible given the iteration duration
        const iterations = count === Infinity ? floor(maxValue / duration) : count;
        this._reversed = +(this._alternate && !(iterations % 2) ? reversed : !reversed);
        if (count === Infinity) {
            // Handle infinite loops to loop on themself
            this.iterationProgress = this._reversed ? 1 - this.iterationProgress : this.iterationProgress;
        }
        else {
            this.seek((duration * iterations) - this._currentTime);
        }
        this.resetTime();
        return this;
    }
    /** @return {this} */
    play() {
        if (this._reversed)
            this.alternate();
        return this.resume();
    }
    /** @return {this} */
    reverse() {
        if (!this._reversed)
            this.alternate();
        return this.resume();
    }
    // TODO: Move all the animation / tweens / children related code to Animation / Timeline
    /** @return {this} */
    cancel() {
        if (this._hasChildren) {
            forEachChildren(this, (/** @type {Renderable} */ child) => child.cancel(), true);
        }
        else {
            forEachChildren(this, removeTweenSliblings);
        }
        this._cancelled = 1;
        // Pausing the timer removes it from the engine
        return this.pause();
    }
    /**
     * @param  {Number} newDuration
     * @return {this}
     */
    stretch(newDuration) {
        const currentDuration = this.duration;
        const normlizedDuration = normalizeTime(newDuration);
        if (currentDuration === normlizedDuration)
            return this;
        const timeScale = newDuration / currentDuration;
        const isSetter = newDuration <= minValue;
        this.duration = isSetter ? minValue : normlizedDuration;
        this.iterationDuration = isSetter ? minValue : normalizeTime(this.iterationDuration * timeScale);
        this._offset *= timeScale;
        this._delay *= timeScale;
        this._loopDelay *= timeScale;
        return this;
    }
    /**
      * Cancels the timer by seeking it back to 0 and reverting the attached scroller if necessary
      * @return {this}
      */
    revert() {
        tick(this, 0, 1, 0, tickModes.AUTO);
        const ap = /** @type {ScrollObserver} */ (this._autoplay);
        if (ap && ap.linked && ap.linked === this)
            ap.revert();
        return this.cancel();
    }
    /**
      * Imediatly completes the timer, cancels it and triggers the onComplete callback
      * @return {this}
      */
    complete() {
        return this.seek(this.duration).cancel();
    }
    /**
     * @param  {Callback<this>} [callback]
     * @return {Promise}
     */
    then(callback = noop) {
        const then = this.then;
        const onResolve = () => {
            // this.then = null prevents infinite recursion if returned by an async function
            // https://github.com/juliangarnierorg/anime-beta/issues/26
            this.then = null;
            callback(this);
            this.then = then;
            this._resolve = noop;
        };
        return new Promise(r => {
            this._resolve = () => r(onResolve());
            // Make sure to resolve imediatly if the timer has already completed
            if (this.completed)
                this._resolve();
            return this;
        });
    }
}
/**
 * @param {TimerParams} [parameters]
 * @return {Timer}
 */
const createTimer = parameters => new Timer(parameters, null, 0).init();


/** @type {EasingFunction} */
const none = t => t;
// Cubic Bezier solver adapted from https://github.com/gre/bezier-ease © Gaëtan Renaudeau
/**
 * @param  {Number} aT
 * @param  {Number} aA1
 * @param  {Number} aA2
 * @return {Number}
 */
const calcBezier = (aT, aA1, aA2) => (((1 - 3 * aA2 + 3 * aA1) * aT + (3 * aA2 - 6 * aA1)) * aT + (3 * aA1)) * aT;
/**
 * @param  {Number} aX
 * @param  {Number} mX1
 * @param  {Number} mX2
 * @return {Number}
 */
const binarySubdivide = (aX, mX1, mX2) => {
    let aA = 0, aB = 1, currentX, currentT, i = 0;
    do {
        currentT = aA + (aB - aA) / 2;
        currentX = calcBezier(currentT, mX1, mX2) - aX;
        if (currentX > 0) {
            aB = currentT;
        }
        else {
            aA = currentT;
        }
    } while (abs(currentX) > .0000001 && ++i < 100);
    return currentT;
};
/**
 * @param  {Number} [mX1]
 * @param  {Number} [mY1]
 * @param  {Number} [mX2]
 * @param  {Number} [mY2]
 * @return {EasingFunction}
 */
const cubicBezier = (mX1 = 0.5, mY1 = 0.0, mX2 = 0.5, mY2 = 1.0) => (mX1 === mY1 && mX2 === mY2) ? none :
    t => t === 0 || t === 1 ? t :
        calcBezier(binarySubdivide(t, mX1, mX2), mY1, mY2);
/**
 * Steps ease implementation https://developer.mozilla.org/fr/docs/Web/CSS/transition-timing-function
 * Only covers 'end' and 'start' jumpterms
 * @param  {Number} steps
 * @param  {Boolean} [fromStart]
 * @return {EasingFunction}
 */
const steps = (steps = 10, fromStart) => {
    const roundMethod = fromStart ? ceil : floor;
    return t => roundMethod(clamp("use strict";

module.exports = function () {
  // https://mths.be/emoji
  return /\uD83C\uDFF4\uDB40\uDC67\uDB40\uDC62(?:\uDB40\uDC65\uDB40\uDC6E\uDB40\uDC67|\uDB40\uDC73\uDB40\uDC63\uDB40\uDC74|\uDB40\uDC77\uDB40\uDC6C\uDB40\uDC73)\uDB40\uDC7F|\uD83D\uDC68(?:\uD83C\uDFFC\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68\uD83C\uDFFB|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFF\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFB-\uDFFE])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFE\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFB-\uDFFD])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFD\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFB\uDFFC])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\u200D(?:\u2764\uFE0F\u200D(?:\uD83D\uDC8B\u200D)?\uD83D\uDC68|(?:\uD83D[\uDC68\uDC69])\u200D(?:\uD83D\uDC66\u200D\uD83D\uDC66|\uD83D\uDC67\u200D(?:\uD83D[\uDC66\uDC67]))|\uD83D\uDC66\u200D\uD83D\uDC66|\uD83D\uDC67\u200D(?:\uD83D[\uDC66\uDC67])|(?:\uD83D[\uDC68\uDC69])\u200D(?:\uD83D[\uDC66\uDC67])|[\u2695\u2696\u2708]\uFE0F|\uD83D[\uDC66\uDC67]|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|(?:\uD83C\uDFFB\u200D[\u2695\u2696\u2708]|\uD83C\uDFFF\u200D[\u2695\u2696\u2708]|\uD83C\uDFFE\u200D[\u2695\u2696\u2708]|\uD83C\uDFFD\u200D[\u2695\u2696\u2708]|\uD83C\uDFFC\u200D[\u2695\u2696\u2708])\uFE0F|\uD83C\uDFFB\u200D(?:\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C[\uDFFB-\uDFFF])|(?:\uD83E\uDDD1\uD83C\uDFFB\u200D\uD83E\uDD1D\u200D\uD83E\uDDD1|\uD83D\uDC69\uD83C\uDFFC\u200D\uD83E\uDD1D\u200D\uD83D\uDC69)\uD83C\uDFFB|\uD83E\uDDD1(?:\uD83C\uDFFF\u200D\uD83E\uDD1D\u200D\uD83E\uDDD1(?:\uD83C[\uDFFB-\uDFFF])|\u200D\uD83E\uDD1D\u200D\uD83E\uDDD1)|(?:\uD83E\uDDD1\uD83C\uDFFE\u200D\uD83E\uDD1D\u200D\uD83E\uDDD1|\uD83D\uDC69\uD83C\uDFFF\u200D\uD83E\uDD1D\u200D(?:\uD83D[\uDC68\uDC69]))(?:\uD83C[\uDFFB-\uDFFE])|(?:\uD83E\uDDD1\uD83C\uDFFC\u200D\uD83E\uDD1D\u200D\uD83E\uDDD1|\uD83D\uDC69\uD83C\uDFFD\u200D\uD83E\uDD1D\u200D\uD83D\uDC69)(?:\uD83C[\uDFFB\uDFFC])|\uD83D\uDC69(?:\uD83C\uDFFE\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFB-\uDFFD\uDFFF])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFC\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFB\uDFFD-\uDFFF])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFB\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFC-\uDFFF])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFD\u200D(?:\uD83E\uDD1D\u200D\uD83D\uDC68(?:\uD83C[\uDFFB\uDFFC\uDFFE\uDFFF])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\u200D(?:\u2764\uFE0F\u200D(?:\uD83D\uDC8B\u200D(?:\uD83D[\uDC68\uDC69])|\uD83D[\uDC68\uDC69])|\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD])|\uD83C\uDFFF\u200D(?:\uD83C[\uDF3E\uDF73\uDF93\uDFA4\uDFA8\uDFEB\uDFED]|\uD83D[\uDCBB\uDCBC\uDD27\uDD2C\uDE80\uDE92]|\uD83E[\uDDAF-\uDDB3\uDDBC\uDDBD]))|\uD83D\uDC69\u200D\uD83D\uDC69\u200D(?:\uD83D\uDC66\u200D\uD83D\uDC66|\uD83D\uDC67\u200D(?:\uD83D[\uDC66\uDC67]))|(?:\uD83E\uDDD1\uD83C\uDFFD\u200D\uD83E\uDD1D\u200D\uD83E\uDDD1|\uD83D\uDC69\uD83C\uDFFE\u200D\uD83E\uDD1D\u200D\uD83D\uDC69)(?:\uD83C[\uDFFB-\uDFFD])|\uD83D\uDC69\u200D\uD83D\uDC66\u200D\uD83D\uDC66|\uD83D\uDC69\u200D\uD83D\uDC69\u200D(?:\uD83D[\uDC66\uDC67])|(?:\uD83D\uDC41\uFE0F\u200D\uD83D\uDDE8|\uD83D\uDC69(?:\uD83C\uDFFF\u200D[\u2695\u2696\u2708]|\uD83C\uDFFE\u200D[\u2695\u2696\u2708]|\uD83C\uDFFC\u200D[\u2695\u2696\u2708]|\uD83C\uDFFB\u200D[\u2695\u2696\u2708]|\uD83C\uDFFD\u200D[\u2695\u2696\u2708]|\u200D[\u2695\u2696\u2708])|(?:(?:\u26F9|\uD83C[\uDFCB\uDFCC]|\uD83D\uDD75)\uFE0F|\uD83D\uDC6F|\uD83E[\uDD3C\uDDDE\uDDDF])\u200D[\u2640\u2642]|(?:\u26F9|\uD83C[\uDFCB\uDFCC]|\uD83D\uDD75)(?:\uD83C[\uDFFB-\uDFFF])\u200D[\u2640\u2642]|(?:\uD83C[\uDFC3\uDFC4\uDFCA]|\uD83D[\uDC6E\uDC71\uDC73\uDC77\uDC81\uDC82\uDC86\uDC87\uDE45-\uDE47\uDE4B\uDE4D\uDE4E\uDEA3\uDEB4-\uDEB6]|\uD83E[\uDD26\uDD37-\uDD39\uDD3D\uDD3E\uDDB8\uDDB9\uDDCD-\uDDCF\uDDD6-\uDDDD])(?:(?:\uD83C[\uDFFB-\uDFFF])\u200D[\u2640\u2642]|\u200D[\u2640\u2642])|\uD83C\uDFF4\u200D\u2620)\uFE0F|\uD83D\uDC69\u200D\uD83D\uDC67\u200D(?:\uD83D[\uDC66\uDC67])|\uD83C\uDFF3\uFE0F\u200D\uD83C\uDF08|\uD83D\uDC15\u200D\uD83E\uDDBA|\uD83D\uDC69\u200D\uD83D\uDC66|\uD83D\uDC69\u200D\uD83D\uDC67|\uD83C\uDDFD\uD83C\uDDF0|\uD83C\uDDF4\uD83C\uDDF2|\uD83C\uDDF6\uD83C\uDDE6|[#\*0-9]\uFE0F\u20E3|\uD83C\uDDE7(?:\uD83C[\uDDE6\uDDE7\uDDE9-\uDDEF\uDDF1-\uDDF4\uDDF6-\uDDF9\uDDFB\uDDFC\uDDFE\uDDFF])|\uD83C\uDDF9(?:\uD83C[\uDDE6\uDDE8\uDDE9\uDDEB-\uDDED\uDDEF-\uDDF4\uDDF7\uDDF9\uDDFB\uDDFC\uDDFF])|\uD83C\uDDEA(?:\uD83C[\uDDE6\uDDE8\uDDEA\uDDEC\uDDED\uDDF7-\uDDFA])|\uD83E\uDDD1(?:\uD83C[\uDFFB-\uDFFF])|\uD83C\uDDF7(?:\uD83C[\uDDEA\uDDF4\uDDF8\uDDFA\uDDFC])|\uD83D\uDC69(?:\uD83C[\uDFFB-\uDFFF])|\uD83C\uDDF2(?:\uD83C[\uDDE6\uDDE8-\uDDED\uDDF0-\uDDFF])|\uD83C\uDDE6(?:\uD83C[\uDDE8-\uDDEC\uDDEE\uDDF1\uDDF2\uDDF4\uDDF6-\uDDFA\uDDFC\uDDFD\uDDFF])|\uD83C\uDDF0(?:\uD83C[\uDDEA\uDDEC-\uDDEE\uDDF2\uDDF3\uDDF5\uDDF7\uDDFC\uDDFE\uDDFF])|\uD83C\uDDED(?:\uD83C[\uDDF0\uDDF2\uDDF3\uDDF7\uDDF9\uDDFA])|\uD83C\uDDE9(?:\uD83C[\uDDEA\uDDEC\uDDEF\uDDF0\uDDF2\uDDF4\uDDFF])|\uD83C\uDDFE(?:\uD83C[\uDDEA\uDDF9])|\uD83C\uDDEC(?:\uD83C[\uDDE6\uDDE7\uDDE9-\uDDEE\uDDF1-\uDDF3\uDDF5-\uDDFA\uDDFC\uDDFE])|\uD83C\uDDF8(?:\uD83C[\uDDE6-\uDDEA\uDDEC-\uDDF4\uDDF7-\uDDF9\uDDFB\uDDFD-\uDDFF])|\uD83C\uDDEB(?:\uD83C[\uDDEE-\uDDF0\uDDF2\uDDF4\uDDF7])|\uD83C\uDDF5(?:\uD83C[\uDDE6\uDDEA-\uDDED\uDDF0-\uDDF3\uDDF7-\uDDF9\uDDFC\uDDFE])|\uD83C\uDDFB(?:\uD83C[\uDDE6\uDDE8\uDDEA\uDDEC\uDDEE\uDDF3\uDDFA])|\uD83C\uDDF3(?:\uD83C[\uDDE6\uDDE8\uDDEA-\uDDEC\uDDEE\uDDF1\uDDF4\uDDF5\uDDF7\uDDFA\uDDFF])|\uD83C\uDDE8(?:\uD83C[\uDDE6\uDDE8\uDDE9\uDDEB-\uDDEE\uDDF0-\uDDF5\uDDF7\uDDFA-\uDDFF])|\uD83C\uDDF1(?:\uD83C[\uDDE6-\uDDE8\uDDEE\uDDF0\uDDF7-\uDDFB\uDDFE])|\uD83C\uDDFF(?:\uD83C[\uDDE6\uDDF2\uDDFC])|\uD83C\uDDFC(?:\uD83C[\uDDEB\uDDF8])|\uD83C\uDDFA(?:\uD83C[\uDDE6\uDDEC\uDDF2\uDDF3\uDDF8\uDDFE\uDDFF])|\uD83C\uDDEE(?:\uD83C[\uDDE8-\uDDEA\uDDF1-\uDDF4\uDDF6-\uDDF9])|\uD83C\uDDEF(?:\uD83C[\uDDEA\uDDF2\uDDF4\uDDF5])|(?:\uD83C[\uDFC3\uDFC4\uDFCA]|\uD83D[\uDC6E\uDC71\uDC73\uDC77\uDC81\uDC82\uDC86\uDC87\uDE45-\uDE47\uDE4B\uDE4D\uDE4E\uDEA3\uDEB4-\uDEB6]|\uD83E[\uDD26\uDD37-\uDD39\uDD3D\uDD3E\uDDB8\uDDB9\uDDCD-\uDDCF\uDDD6-\uDDDD])(?:\uD83C[\uDFFB-\uDFFF])|(?:\u26F9|\uD83C[\uDFCB\uDFCC]|\uD83D\uDD75)(?:\uD83C[\uDFFB-\uDFFF])|(?:[\u261D\u270A-\u270D]|\uD83C[\uDF85\uDFC2\uDFC7]|\uD83D[\uDC42\uDC43\uDC46-\uDC50\uDC66\uDC67\uDC6B-\uDC6D\uDC70\uDC72\uDC74-\uDC76\uDC78\uDC7C\uDC83\uDC85\uDCAA\uDD74\uDD7A\uDD90\uDD95\uDD96\uDE4C\uDE4F\uDEC0\uDECC]|\uD83E[\uDD0F\uDD18-\uDD1C\uDD1E\uDD1F\uDD30-\uDD36\uDDB5\uDDB6\uDDBB\uDDD2-\uDDD5])(?:\uD83C[\uDFFB-\uDFFF])|(?:[\u231A\u231B\u23E9-\u23EC\u23F0\u23F3\u25FD\u25FE\u2614\u2615\u2648-\u2653\u267F\u2693\u26A1\u26AA\u26AB\u26BD\u26BE\u26C4\u26C5\u26CE\u26D4\u26EA\u26F2\u26F3\u26F5\u26FA\u26FD\u2705\u270A\u270B\u2728\u274C\u274E\u2753-\u2755\u2757\u2795-\u2797\u27B0\u27BF\u2B1B\u2B1C\u2B50\u2B55]|\uD83C[\uDC04\uDCCF\uDD8E\uDD91-\uDD9A\uDDE6-\uDDFF\uDE01\uDE1A\uDE2F\uDE32-\uDE36\uDE38-\uDE3A\uDE50\uDE51\uDF00-\uDF20\uDF2D-\uDF35\uDF37-\uDF7C\uDF7E-\uDF93\uDFA0-\uDFCA\uDFCF-\uDFD3\uDFE0-\uDFF0\uDFF4\uDFF8-\uDFFF]|\uD83D[\uDC00-\uDC3E\uDC40\uDC42-\uDCFC\uDCFF-\uDD3D\uDD4B-\uDD4E\uDD50-\uDD67\uDD7A\uDD95\uDD96\uDDA4\uDDFB-\uDE4F\uDE80-\uDEC5\uDECC\uDED0-\uDED2\uDED5\uDEEB\uDEEC\uDEF4-\uDEFA\uDFE0-\uDFEB]|\uD83E[\uDD0D-\uDD3A\uDD3C-\uDD45\uDD47-\uDD71\uDD73-\uDD76\uDD7A-\uDDA2\uDDA5-\uDDAA\uDDAE-\uDDCA\uDDCD-\uDDFF\uDE70-\uDE73\uDE78-\uDE7A\uDE80-\uDE82\uDE90-\uDE95])|(?:[#\*0-9\xA9\xAE\u203C\u2049\u2122\u2139\u2194-\u2199\u21A9\u21AA\u231A\u231B\u2328\u23CF\u23E9-\u23F3\u23F8-\u23FA\u24C2\u25AA\u25AB\u25B6\u25C0\u25FB-\u25FE\u2600-\u2604\u260E\u2611\u2614\u2615\u2618\u261D\u2620\u2622\u2623\u2626\u262A\u262E\u262F\u2638-\u263A\u2640\u2642\u2648-\u2653\u265F\u2660\u2663\u2665\u2666\u2668\u267B\u267E\u267F\u2692-\u2697\u2699\u269B\u269C\u26A0\u26A1\u26AA\u26AB\u26B0\u26B1\u26BD\u26BE\u26C4\u26C5\u26C8\u26CE\u26CF\u26D1\u26D3\u26D4\u26E9\u26EA\u26F0-\u26F5\u26F7-\u26FA\u26FD\u2702\u2705\u2708-\u270D\u270F\u2712\u2714\u2716\u271D\u2721\u2728\u2733\u2734\u2744\u2747\u274C\u274E\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27A1\u27B0\u27BF\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55\u3030\u303D\u3297\u3299]|\uD83C[\uDC04\uDCCF\uDD70\uDD71\uDD7E\uDD7F\uDD8E\uDD91-\uDD9A\uDDE6-\uDDFF\uDE01\uDE02\uDE1A\uDE2F\uDE32-\uDE3A\uDE50\uDE51\uDF00-\uDF21\uDF24-\uDF93\uDF96\uDF97\uDF99-\uDF9B\uDF9E-\uDFF0\uDFF3-\uDFF5\uDFF7-\uDFFF]|\uD83D[\uDC00-\uDCFD\uDCFF-\uDD3D\uDD49-\uDD4E\uDD50-\uDD67\uDD6F\uDD70\uDD73-\uDD7A\uDD87\uDD8A-\uDD8D\uDD90\uDD95\uDD96\uDDA4\uDDA5\uDDA8\uDDB1\uDDB2\uDDBC\uDDC2-\