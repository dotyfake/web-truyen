omp.operator === '<=')
  var oppositeDirectionsLessThan =
    cmp(this.semver, '<', comp.semver, options) &&
    ((this.operator === '>=' || this.operator === '>') &&
    (comp.operator === '<=' || comp.operator === '<'))
  var oppositeDirectionsGreaterThan =
    cmp(this.semver, '>', comp.semver, options) &&
    ((this.operator === '<=' || this.operator === '<') &&
    (comp.operator === '>=' || comp.operator === '>'))

  return sameDirectionIncreasing || sameDirectionDecreasing ||
    (sameSemVer && differentDirectionsInclusive) ||
    oppositeDirectionsLessThan || oppositeDirectionsGreaterThan
}

exports.Range = Range
function Range (range, options) {
  if (!options || typeof options !== 'object') {
    options = {
      loose: !!options,
      includePrerelease: false
    }
  }

  if (range instanceof Range) {
    if (range.loose === !!options.loose &&
        range.includePrerelease === !!options.includePrerelease) {
      return range
    } else {
      return new Range(range.raw, options)
    }
  }

  if (range instanceof Comparator) {
    return new Range(range.value, options)
  }

  if (!(this instanceof Range)) {
    return new Range(range, options)
  }

  this.options = options
  this.loose = !!options.loose
  this.includePrerelease = !!options.includePrerelease

  // First reduce all whitespace as much as possible so we do not have to rely
  // on potentially slow regexes like \s*. This is then stored and used for
  // future error messages as well.
  this.raw = range
    .trim()
    .split(/\s+/)
    .join(' ')

  // First, split based on boolean or ||
  this.set = this.raw.split('||').map(function (range) {
    return this.parseRange(range.trim())
  }, this).filter(function (c) {
    // throw out any that are not relevant for whatever reason
    return c.length
  })

  if (!this.set.length) {
    throw new TypeError('Invalid SemVer Range: ' + this.raw)
  }

  this.format()
}

Range.prototype.format = function () {
  this.range = this.set.map(function (comps) {
    return comps.join(' ').trim()
  }).join('||').trim()
  return this.range
}

Range.prototype.toString = function () {
  return this.range
}

Range.prototype.parseRange = function (range) {
  var loose = this.options.loose
  // `1.2.3 - 1.2.4` => `>=1.2.3 <=1.2.4`
  var hr = loose ? safeRe[t.HYPHENRANGELOOSE] : safeRe[t.HYPHENRANGE]
  range = range.replace(hr, hyphenReplace)
  debug('hyphen replace', range)
  // `> 1.2.3 < 1.2.5` => `>1.2.3 <1.2.5`
  range = range.replace(safeRe[t.COMPARATORTRIM], comparatorTrimReplace)
  debug('comparator trim', range, safeRe[t.COMPARATORTRIM])

  // `~ 1.2.3` => `~1.2.3`
  range = range.replace(safeRe[t.TILDETRIM], tildeTrimReplace)

  // `^ 1.2.3` => `^1.2.3`
  range = range.replace(safeRe[t.CARETTRIM], caretTrimReplace)

  // normalize spaces
  range = range.split(/\s+/).join(' ')

  // At this point, the range is completely trimmed and
  // ready to be split into comparators.

  var compRe = loose ? safeRe[t.COMPARATORLOOSE] : safeRe[t.COMPARATOR]
  var set = range.split(' ').map(function (comp) {
    return parseComparator(comp, this.options)
  }, this).join(' ').split(/\s+/)
  if (this.options.loose) {
    // in loose mode, throw out any that are not valid comparators
    set = set.filter(function (comp) {
      return !!comp.match(compRe)
    })
  }
  set = set.map(function (comp) {
    return new Comparator(comp, this.options)
  }, this)

  return set
}

Range.prototype.intersects = function (range, options) {
  if (!(range instanceof Range)) {
    throw new TypeError('a Range is required')
  }

  return this.set.some(function (thisComparators) {
    return (
      isSatisfiable(thisComparators, options) &&
      range.set.some(function (rangeComparators) {
        return (
          isSatisfiable(rangeComparators, options) &&
          thisComparators.every(function (thisComparator) {
            return rangeComparators.every(function (rangeComparator) {
              return thisComparator.intersects(rangeComparator, options)
            })
          })
        )
      })
    )
  })
}

// take a set of comparators and determine whether there
// exists a version which can satisfy it
function isSatisfiable (comparators, options) {
  var result = true
  var remainingComparators = comparators.slice()
  var testComparator = remainingComparators.pop()

  while (result && remainingComparators.length) {
    result = remainingComparators.every(function (otherComparator) {
      return testComparator.intersects(otherComparator, options)
    })

    testComparator = remainingComparators.pop()
  }

  return result
}

// Mostly just for testing and legacy API reasons
exports.toComparators = toComparators
function toComparators (range, options) {
  return new Range(range, options).set.map(function (comp) {
    return comp.map(function (c) {
      return c.value
    }).join(' ').trim().split(' ')
  })
}

// comprised of xranges, tildes, stars, and gtlt's at this point.
// already replaced the hyphen ranges
// turn into a set of JUST comparators.
function parseComparator (comp, options) {
  debug('comp', comp, options)
  comp = replaceCarets(comp, options)
  debug('caret', comp)
  comp = replaceTildes(comp, options)
  debug('tildes', comp)
  comp = replaceXRanges(comp, options)
  debug('xrange', comp)
  comp = replaceStars(comp, options)
  debug('stars', comp)
  return comp
}

function isX (id) {
  return !id || id.toLowerCase() === 'x' || id === '*'
}

// ~, ~> --> * (any, kinda silly)
// ~2, ~2.x, ~2.x.x, ~>2, ~>2.x ~>2.x.x --> >=2.0.0 <3.0.0
// ~2.0, ~2.0.x, ~>2.0, ~>2.0.x --> >=2.0.0 <2.1.0
// ~1.2, ~1.2.x, ~>1.2, ~>1.2.x --> >=1.2.0 <1.3.0
// ~1.2.3, ~>1.2.3 --> >=1.2.3 <1.3.0
// ~1.2.0, ~>1.2.0 --> >=1.2.0 <1.3.0
function replaceTildes (comp, options) {
  return comp.trim().split(/\s+/).map(function (comp) {
    return replaceTilde(comp, options)
  }).join(' ')
}

function replaceTilde (comp, options) {
  var r = options.loose ? safeRe[t.TILDELOOSE] : safeRe[t.TILDE]
  return comp.replace(r, function (_, M, m, p, pr) {
    debug('tilde', comp, _, M, m, p, pr)
    var ret

    if (isX(M)) {
      ret = ''
    } else if (isX(m)) {
      ret = '>=' + M + '.0.0 <' + (+M + 1) + '.0.0'
    } else if (isX(p)) {
      // ~1.2 == >=1.2.0 <1.3.0
      ret = '>=' + M + '.' + m + '.0 <' + M + '.' + (+m + 1) + '.0'
    } else if (pr) {
      debug('replaceTilde pr', pr)
      ret = '>=' + M + '.' + m + '.' + p + '-' + pr +
            ' <' + M + '.' + (+m + 1) + '.0'
    } else {
      // ~1.2.3 == >=1.2.3 <1.3.0
      ret = '>=' + M + '.' + m + '.' + p +
            ' <' + M + '.' + (+m + 1) + '.0'
    }

    debug('tilde return', ret)
    return ret
  })
}

// ^ --> * (any, kinda silly)
// ^2, ^2.x, ^2.x.x --> >=2.0.0 <3.0.0
// ^2.0, ^2.0.x --> >=2.0.0 <3.0.0
// ^1.2, ^1.2.x --> >=1.2.0 <2.0.0
// ^1.2.3 --> >=1.2.3 <2.0.0
// ^1.2.0 --> >=1.2.0 <2.0.0
function replaceCarets (comp, options) {
  return comp.trim().split(/\s+/).map(function (comp) {
    return replaceCaret(comp, options)
  }).join(' ')
}

function replaceCaret (comp, options) {
  debug('caret', comp, options)
  var r = options.loose ? safeRe[t.CARETLOOSE] : safeRe[t.CARET]
  return comp.replace(r, function (_, M, m, p, pr) {
    debug('caret', comp, _, M, m, p, pr)
    var ret

    if (isX(M)) {
      ret = ''
    } else if (isX(m)) {
      ret = '>=' + M + '.0.0 <' + (+M + 1) + '.0.0'
    } else if (isX(p)) {
      if (M === '0') {
        ret = '>=' + M + '.' + m + '.0 <' + M + '.' + (+m + 1) + '.0'
      } else {
        ret = '>=' + M + '.' + m + '.0 <' + (+M + 1) + '.0.0'
      }
    } else if (pr) {
      debug('replaceCaret pr', pr)
      if (M === '0') {
        if (m === '0') {
          ret = '>=' + M + '.' + m + '.' + p + '-' + pr +
                ' <' + M + '.' + m + '.' + (+p + 1)
        } else {
          ret = '>=' + M + '.' + m + '.' + p + '-' + pr +
                ' <' + M + '.' + (+m + 1) + '.0'
        }
      } else {
        ret = '>=' + M + '.' + m + '.' + p + '-' + pr +
              ' <' + (+M + 1) + '.0.0'
      }
    } else {
      debug('no pr')
      if (M === '0') {
        if (m === '0') {
          ret = '>=' + M + '.' + m + '.' + p +
                ' <' + M + '.' + m + '.' + (+p + 1)
        } else {
          ret = '>=' + M + '.' + m + '.' + p +
                ' <' + M + '.' + (+m + 1) + '.0'
        }
      } else {
        ret = '>=' + M + '.' + m + '.' + p +
              ' <' + (+M + 1) + '.0.0'
      }
    }

    debug('caret return', ret)
    return ret
  })
}

function replaceXRanges (comp, options) {
  debug('replaceXRanges', comp, options)
  return comp.split(/\s+/).map(function (comp) {
    return replaceXRange(comp, options)
  }).join(' ')
}

function replaceXRange (comp, options) {
  comp = comp.trim()
  var r = options.loose ? safeRe[t.XRANGELOOSE] : safeRe[t.XRANGE]
  return comp.replace(r, function (ret, gtlt, M, m, p, pr) {
    debug('xRange', comp, ret, gtlt, M, m, p, pr)
    var xM = isX(M)
    var xm = xM || isX(m)
    var xp = xm || isX(p)
    var anyX = xp

    if (gtlt === '=' && anyX) {
      gtlt = ''
    }

    // if we're including prereleases in the match, then we need
    // to fix this to -0, the lowest possible prerelease value
    pr = options.includePrerelease ? '-0' : ''

    if (xM) {
      if (gtlt === '>' || gtlt === '<') {
        // nothing is allowed
        ret = '<0.0.0-0'
      } else {
        // nothing is forbidden
        ret = '*'
      }
    } else if (gtlt && anyX) {
      // we know patch is an x, because we have any x at all.
      // replace X with 0
      if (xm) {
        m = 0
      }
      p = 0

      if (gtlt === '>') {
        // >1 => >=2.0.0
        // >1.2 => >=1.3.0
        // >1.2.3 => >= 1.2.4
        gtlt = '>='
        if (xm) {
          M = +M + 1
          m = 0
          p = 0
        } else {
          m = +m + 1
          p = 0
        }
      } else if (gtlt === '<=') {
        // <=0.7.x is actually <0.8.0, since any 0.7.x should
        // pass.  Similarly, <=7.x is actually <8.0.0, etc.
        gtlt = '<'
        if (xm) {
          M = +M + 1
        } else {
          m = +m + 1
        }
      }

      ret = gtlt + M + '.' + m + '.' + p + pr
    } else if (xm) {
      ret = '>=' + M + '.0.0' + pr + ' <' + (+M + 1) + '.0.0' + pr
    } else if (xp) {
      ret = '>=' + M + '.' + m + '.0' + pr +
        ' <' + M + '.' + (+m + 1) + '.0' + pr
    }

    debug('xRange return', ret)

    return ret
  })
}

// Because * is AND-ed with everything else in the comparator,
// and '' means "any version", just remove the *s entirely.
function replaceStars (comp, options) {
  debug('replaceStars', comp, options)
  // Looseness is ignored here.  star is always as loose as it gets!
  return comp.trim().replace(safeRe[t.STAR], '')
}

// This function is passed to string.replace(re[t.HYPHENRANGE])
// M, m, patch, prerelease, build
// 1.2 - 3.4.5 => >=1.2.0 <=3.4.5
// 1.2.3 - 3.4 => >=1.2.0 <3.5.0 Any 3.4.x will do
// 1.2 - 3.4 => >=1.2.0 <3.5.0
function hyphenReplace ($0,
  from, fM, fm, fp, fpr, fb,
  to, tM, tm, tp, tpr, tb) {
  if (isX(fM)) {
    from = ''
  } else if (isX(fm)) {
    from = '>=' + fM + '.0.0'
  } else if (isX(fp)) {
    from = '>=' + fM + '.' + fm + '.0'
  } else {
    from = '>=' + from
  }

  if (isX(tM)) {
    to = ''
  } else if (isX(tm)) {
    to = '<' + (+tM + 1) + '.0.0'
  } else if (isX(tp)) {
    to = '<' + tM + '.' + (+tm + 1) + '.0'
  } else if (tpr) {
    to = '<=' + tM + '.' + tm + '.' + tp + '-' + tpr
  } else {
    to = '<=' + to
  }

  return (from + ' ' + to).trim()
}

// if ANY of the sets match ALL of its comparators, then pass
Range.prototype.test = function (version) {
  if (!version) {
    return false
  }

  if (typeof version === 'string') {
    try {
      version = new SemVer(version, this.options)
    } catch (er) {
      return false
    }
  }

  for (var i = 0; i < this.set.length; i++) {
    if (testSet(this.set[i], version, this.options)) {
      return true
    }
  }
  return false
}

function testSet (set, version, options) {
  for (var i = 0; i < set.length; i++) {
    if (!set[i].test(version)) {
      return false
    }
  }

  if (version.prerelease.length && !options.includePrerelease) {
    // Find the set of versions that are allowed to have prereleases
    // For example, ^1.2.3-pr.1 desugars to >=1.2.3-pr.1 <2.0.0
    // That should allow `1.2.3-pr.2` to pass.
    // However, `1.2.4-alpha.notready` should NOT be allowed,
    // even though it's within the range set by the comparators.
    for (i = 0; i < set.length; i++) {
      debug(set[i].semver)
      if (set[i].semver === ANY) {
        continue
      }

      if (set[i].semver.prerelease.length > 0) {
        var allowed = set[i].semver
        if (allowed.major === version.major &&
            allowed.minor === version.minor &&
            allowed.patch === version.patch) {
          return true
        }
      }
    }

    // Version has a -pre, but it's not one of the ones we like.
    return false
  }

  return true
}

exports.satisfies = satisfies
function satisfies (version, range, options) {
  try {
    range = new Range(range, options)
  } catch (er) {
    return false
  }
  return range.test(version)
}

exports.maxSatisfying = maxSatisfying
function maxSatisfying (versions, range, options) {
  var max = null
  var maxSV = null
  try {
    var rangeObj = new Range(range, options)
  } catch (er) {
    return null
  }
  versions.forEach(function (v) {
    if (rangeObj.test(v)) {
      // satisfies(v, range, options)
      if (!max || maxSV.compare(v) === -1) {
        // compare(max, v, true)
        max = v
        maxSV = new SemVer(max, options)
      }
    }
  })
  return max
}

exports.minSatisfying = minSatisfying
function minSatisfying (versions, range, options) {
  var min = null
  var minSV = null
  try {
    var rangeObj = new Range(range, options)
  } catch (er) {
    return null
  }
  versions.forEach(function (v) {
    if (rangeObj.test(v)) {
      // satisfies(v, range, options)
      if (!min || minSV.compare(v) === 1) {
        // compare(min, v, true)
        min = v
        minSV = new SemVer(min, options)
      }
    }
  })
  return min
}

exports.minVersion = minVersion
function minVersion (range, loose) {
  range = new Range(range, loose)

  var minver = new SemVer('0.0.0')
  if (range.test(minver)) {
    return minver
  }

  minver = new SemVer('0.0.0-0')
  if (range.test(minver)) {
    return minver
  }

  minver = null
  for (var i = 0; i < range.set.length; ++i) {
    var comparators = range.set[i]

    comparators.forEach(function (comparator) {
      // Clone to avoid manipulating the comparator's semver object.
      var compver = new SemVer(comparator.semver.version)
      switch (comparator.operator) {
        case '>':
          if (compver.prerelease.length === 0) {
            compver.patch++
          } else {
            compver.prerelease.push(0)
          }
          compver.raw = compver.format()
          /* fallthrough */
        case '':
        case '>=':
          if (!minver || gt(minver, compver)) {
            minver = compver
          }
          break
        case '<':
        case '<=':
          /* Ignore maximum versions */
          break
        /* istanbul ignore next */
        default:
          throw new Error('Unexpected operation: ' + comparator.operator)
      }
    })
  }

  if (minver && range.test(minver)) {
    return minver
  }

  return null
}

exports.validRange = validRange
function validRange (range, options) {
  try {
    // Return '*' instead of '' so that truthiness works.
    // This will throw if it's invalid anyway
    return new Range(range, options).range || '*'
  } catch (er) {
    return null
  }
}

// Determine if version is less than all the versions possible in the range
exports.ltr = ltr
function ltr (version, range, options) {
  return outside(version, range, '<', options)
}

// Determine if version is greater than all the versions possible in the range.
exports.gtr = gtr
function gtr (version, range, options) {
  return outside(version, range, '>', options)
}

exports.outside = outside
function outside (version, range, hilo, options) {
  version = new SemVer(version, options)
  range = new Range(range, options)

  var gtfn, ltefn, ltfn, comp, ecomp
  switch (hilo) {
    case '>':
      gtfn = gt
      ltefn ._offset:0);let N=NaN,Y=NaN,X=0,O=0;for(let t=0;t<l;t++){const e=h[t],r=o||t,d=a||l;let u=NaN,m=NaN;for(let t in p)if(U(t)){const o=Mt(e,t),a=ye(t,e,o);let h=p[t];const l=F(h);if(n&&!l&&(Ee[0]=h,Ee[1]=h,h=Ee),l){const t=h.length,e=!P(h[0]);2===t&&e?(Ce.to=h,$e[0]=Ce,Be=$e):t>2&&e?(Be=[],h.forEach(((t,e)=>{e?1===e?(Ee[1]=t,Be.push(Ee)):Be.push(t):Ee[0]=t}))):Be=h}else $e[0]=h,Be=$e;let f=null,g=null,_=NaN,y=0,v=0;for(let t=Be.length;v<t;v++){const n=Be[v];P(n)?De=n:(Ce.to=n,De=Ce),ke.func=null;const h=Xt(De.to,e,r,d,ke);let l;P(h)&&!M(h.to)?(De=h,l=h.to):l=h;const u=Xt(De.from,e,r,d),p=De.ease,m=!M(p)&&!M(p.ease),b=m?p.ease:p||k,x=m?p.duration:Xt(Yt(De.duration,t>1?Xt($,e,r,d)/t:$),e,r,d),S=Xt(Yt(De.delay,v?0:E),e,r,d),T=Xt(Yt(De.composition,D),e,r,d),w=R(T)?T:i[T],B=De.modifier||C,N=!M(u),Y=!M(l),z=F(l),I=z||N&&Y,W=g?y+S:S,V=A+W;O||!N&&!z||(O=1);let U=g;if(w!==i.none){f||(f=qt(e,a));let t=f._head;for(;t&&!t._isOverridden&&t._absoluteStartTime<=V;)if(U=t,t=t._nextRep,t&&t._absoluteStartTime>=V)for(;t;)jt(t),t=t._nextRep}if(I?(Wt(z?Xt(l[0],e,r,d):u,Te),Wt(z?Xt(l[1],e,r,d,ke):l,we),0===Te.t&&(U?1===U._valueType&&(Te.t=1,Te.u=U._unit):(Wt(zt(e,a,o,L),Ut),1===Ut.t&&(Te.t=1,Te.u=Ut.u)))):(Y?Wt(l,we):g?Vt(g,we):Wt(s&&U&&U.parent.parent===s?U._value:zt(e,a,o,L),we),N?Wt(u,Te):g?Vt(g,Te):Wt(s&&U&&U.parent.parent===s?U._value:zt(e,a,o,L),Te)),Te.o&&(Te.n=It(U?U._toNumber:Wt(zt(e,a,o,L),Ut).n,Te.n,Te.o)),we.o&&(we.n=It(Te.n,we.n,we.o)),Te.t!==we.t)if(3===Te.t||3===we.t){const t=3===Te.t?Te:we,e=3===Te.t?we:Te;e.t=3,e.s=pt(t.s),e.d=t.d.map((()=>e.n))}else if(1===Te.t||1===we.t){const t=1===Te.t?Te:we,e=1===Te.t?we:Te;e.t=1,e.u=t.u}else if(2===Te.t||2===we.t){const t=2===Te.t?Te:we,e=2===Te.t?we:Te;e.t=2,e.s=t.s,e.d=[0,0,0,1]}if(Te.u!==we.u){let t=we.u?Te:we;t=xe(e,t,we.u?we.u:Te.u,!1)}if(we.d&&Te.d&&we.d.length!==Te.d.length){const t=Te.d.length>we.d.length?Te:we,e=t===Te?we:Te;e.d=t.d.map(((t,s)=>M(e.d[s])?0:e.d[s])),e.s=pt(t.s)}const H=ht(+x||c,12),q={parent:this,id:Le++,property:a,target:e,_value:null,_func:ke.func,_ease:ge(b),_fromNumbers:pt(Te.d),_toNumbers:pt(we.d),_strings:pt(we.s),_fromNumber:Te.n,_toNumber:we.n,_numbers:pt(Te.d),_number:Te.n,_unit:we.u,_modifier:B,_currentTime:0,_startTime:W,_delay:+S,_updateDuration:H,_changeDuration:H,_absoluteStartTime:V,_tweenType:o,_valueType:we.t,_composition:w,_isOverlapped:0,_isOverridden:0,_renderTransforms:0,_prevRep:null,_nextRep:null,_prevAdd:null,_nextAdd:null,_prev:null,_next:null};w!==i.none&&Gt(q,f),isNaN(_)&&(_=q._startTime),y=ht(W+H,12),g=q,X++,_t(this,q)}(isNaN(Y)||_<Y)&&(Y=_),(isNaN(N)||y>N)&&(N=y),3===o&&(u=X-v,m=X)}if(!isNaN(u)){let t=0;ft(this,(e=>{t>=u&&t<m&&(e._renderTransforms=1,e._composition===i.blend&&ft(xt.animation,(t=>{t.id===e.id&&(t._renderTransforms=1)}))),t++}))}}l||console.warn("No target found. Make sure the element you're trying to animate is accessible before creating your animation."),Y?(ft(this,(t=>{t._startTime-t._delay||(t._delay-=Y),t._startTime-=Y})),N-=Y):Y=0,N||(N=c,this.iterationCount=0),this.targets=h,this.duration=N===c?c:dt((N+this._loopDelay)*this.iterationCount-this._loopDelay)||c,this.onRender=b||x.onRender,this._ease=T,this._delay=Y,this.iterationDuration=N,this._inlineStyles=L,!this._autoplay&&O&&this.onRender(this)}stretch(t){const e=this.duration;if(e===ut(t))return this;const s=t/e;return ft(this,(t=>{t._updateDuration=ut(t._updateDuration*s),t._changeDuration=ut(t._changeDuration*s),t._currentTime*=s,t._startTime*=s,t._absoluteStartTime*=s})),super.stretch(t)}refresh(){return ft(this,(t=>{const e=zt(t.target,t.property,t._tweenType);Wt(e,Ut),t._fromNumbers=pt(Ut.d),t._fromNumber=Ut.n,t._func&&(Wt(t._func(),we),t._toNumbers=pt(we.d),t._strings=pt(we.s),t._toNumber=we.n)})),this}revert(){return super.revert(),Se(this)}then(t){return super.then(t)}}const Ne=(t,e=100)=>{const s=[];for(let i=0;i<=e;i++)s.push(t(i/e));return`linear(${s.join(", ")})`},Fe={in:"ease-in",out:"ease-out",inOut:"ease-in-out"},Pe=(()=>{const t={};for(let e in ue)t[e]=t=>ue[e](ce(t));return t})(),Re=t=>{let e=Fe[t];if(e)return e;if(e="linear",Y(t)){if(A(t,"linear")||A(t,"cubic-")||A(t,"steps")||A(t,"ease"))e=t;else if(A(t,"cubicB"))e=L(t);else{const s=pe(t,Pe,Fe);X(s)&&(e=s===se?"linear":Ne(s))}Fe[t]=e}else if(X(t)){const s=Ne(t);s&&(e=s)}else t.ease&&(e=Ne(t.ease));return e},Ye=["x","y","z"],Xe=["perspective","width","height","margin","padding","top","right","bottom","left","borderWidth","fontSize","borderRadius",...Ye],Me=[...Ye,...f.filter((t=>["X","Y","Z"].some((e=>t.endsWith(e)))))];let Oe=t&&(M(CSS)||!Object.hasOwnProperty.call(CSS,"registerProperty"));const ze={_head:null,_tail:null},Ie=(t,e,s)=>{let i=ze._head;for(;i;){const r=i._next,n=i.$el===t,o=!e||i.property===e,a=!s||i.parent===s;if(n&&o&&a){const t=i.animation;try{t.commitStyles()}catch{}t.cancel(),gt(ze,i);const e=i.parent;e&&(e._completed++,e.animations.length===e._completed&&(e.completed=!0,e.muteCallbacks||(e.paused=!0,e.onComplete(e),e._resolve(e))))}i=r}},We=(t,e,s,i,r)=>{const n=e.animate(i,r),o=r.delay+ +r.duration*r.iterations;n.playbackRate=t._speed,t.paused&&n.pause(),t.duration<o&&(t.duration=o,t.controlAnimation=n),t.animations.push(n),Ie(e,s),_t(ze,{parent:t,animation:n,$el:e,property:s,_next:null,_prev:null});const a=()=>{Ie(e,s,t)};return n.onremove=a,n.onfinish=a,n},Ve=(t,e,s,i,r)=>{let n=Xt(e,s,i,r);return R(n)?Xe.includes(t)||A(t,"translate")?`${n}px`:A(t,"rotate")||A(t,"skew")?`${n}deg`:`${n}`:n},Ue=(t,e,s,i,r,n)=>{let o="0";const a=M(i)?getComputedStyle(t)[e]:Ve(e,i,t,r,n);return o=M(s)?F(i)?i.map((s=>Ve(e,s,t,r,n))):a:[Ve(e,s,t,r,n),a],o};class He{constructor(t,e){B.scope&&B.scope.revertibles.push(this),Oe||(f.forEach((t=>{const e=A(t,"skew"),s=A(t,"scale"),i=A(t,"rotate"),r=A(t,"translate"),n=i||e,o=n?"<angle>":s?"<number>":r?"<length-percentage>":"*";try{CSS.registerProperty({name:"--"+t,syntax:o,inherits:!1,initialValue:r?"0px":n?"0deg":s?"1":"0"})}catch{}})),Oe=!0);const s=Dt(t),i=s.length;i||console.warn("No target found. Make sure the element you're trying to animate is accessible before creating your animation.");const r=Yt(e.ease,Re(B.defaults.ease)),n=r.ease&&r,o=Yt(e.autoplay,B.defaults.autoplay),h=!(!o||!o.link)&&o,l=e.alternate&&!0===e.alternate,c=e.reversed&&!0===e.reversed,d=Yt(e.loop,B.defaults.loop),y=!0===d||d===1/0?1/0:R(d)?d+1:1,v=l?c?"alternate-reverse":"alternate":c?"reverse":"normal",b=Re(r),x=1===B.timeScale?1:u;this.targets=s,this.animations=[],this.controlAnimation=null,this.onComplete=e.onComplete||_,this.duration=0,this.muteCallbacks=!1,this.completed=!1,this.paused=!o||!1!==h,this.reversed=c,this.autoplay=o,this._speed=Yt(e.playbackRate,B.defaults.playbackRate),this._resolve=_,this._completed=0,this._inlineStyles=s.map((t=>t.getAttribute("style"))),s.forEach(((t,s)=>{const o=t[a],h=Me.some((t=>e.hasOwnProperty(t))),l=(n?n.duration:Xt(Yt(e.duration,B.defaults.duration),t,s,i))*x,c=Xt(Yt(e.delay,B.defaults.delay),t,s,i)*x,d=Yt(e.composition,"replace");for(let n in e){if(!U(n))continue;const a={},u={iterations:y,direction:v,fill:"forwards",easing:b,duration:l,delay:c,composite:d},p=e[n],g=!!h&&(f.includes(n)?n:m.get(n));let _;if(P(p)){const e=p,h=Yt(e.ease,r),m=h.ease&&h,f=e.to,y=e.from;if(u.duration=(m?m.duration:Xt(Yt(e.duration,l),t,s,i))*x,u.delay=Xt(Yt(e.delay,c),t,s,i)*x,u.composite=Yt(e.composition,d),u.easing=Re(h),_=Ue(t,n,y,f,s,i),g?(a[`--${g}`]=_,o[g]=_):a[n]=Ue(t,n,y,f,s,i),We(this,t,n,a,u),!M(y))if(g){const e=`--${g}`;t.style.setProperty(e,a[e][0])}else t.style[n]=a[n][0]}else _=F(p)?p.map((e=>Ve(n,e,t,s,i))):Ve(n,p,t,s,i),g?(a[`--${g}`]=_,o[g]=_):a[n]=_,We(this,t,n,a,u)}if(h){let e=p;for(let t in o)e+=`${g[t]}var(--${t})) `;t.style.transform=e}})),h&&this.autoplay.link(this)}forEach(t){const e=Y(t)?e=>e[t]():t;return this.animations.forEach(e),this}get speed(){return this._speed}set speed(t){this._speed=+t,this.forEach((e=>e.playbackRate=t))}get currentTime(){const t=this.controlAnimation,e=B.timeScale;return this.completed?this.duration:t?+t.currentTime*(1===e?1:e):0}set currentTime(t){const e=t*(1===B.timeScale?1:u);this.forEach((t=>{e>=this.duration&&t.play(),t.currentTime=e}))}get progress(){return this.currentTime/this.duration}set progress(t){this.forEach((e=>e.currentTime=t*this.duration||0))}resume(){return this.paused?(this.paused=!1,this.forEach("play")):this}pause(){return this.paused?this:(this.paused=!0,this.forEach("pause"))}alternate(){return this.reversed=!this.reversed,this.forEach("reverse"),this.paused&&this.forEach("pause"),this}play(){return this.reversed&&this.alternate(),this.resume()}reverse(){return this.reversed||this.alternate(),this.resume()}seek(t,e=!1){return e&&(this.muteCallbacks=!0),t<this.duration&&(this.completed=!1),this.currentTime=t,this.muteCallbacks=!1,this.paused&&this.pause(),this}restart(){return this.completed=!1,this.seek(0,!0).resume()}commitStyles(){return this.forEach("commitStyles")}complete(){return this.seek(this.duration)}cancel(){return this.forEach("cancel"),this.pause()}revert(){return this.cancel(),this.targets.forEach(((t,e)=>t.setAttribute("style",this._inlineStyles[e]))),this}then(t=_){const e=this.then,s=()=>{this.then=null,t(this),this.then=e,this._resolve=_};return new Promise((t=>(this._resolve=()=>t(s()),this.comple