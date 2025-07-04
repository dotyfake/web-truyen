lipse, and the point at startAngle along this circle's circumference,
  * measured in radians clockwise from the ellipse's semi-major axis, acts as both the start point and the end point.
  */
  if (!counterclockwise && endAngle - startAngle >= twoPi)
    newEndAngle = startAngle + twoPi;
  else if (counterclockwise && startAngle - endAngle >= twoPi)
    newEndAngle = startAngle - twoPi;
  /*
  * Otherwise, the arc is the path along the circumference of this ellipse from the start point to the end point,
  * going anti-clockwise if the counterclockwise argument is true, and clockwise otherwise.
  * Since the points are on the ellipse, as opposed to being simply angles from zero,
  * the arc can never cover an angle greater than 2pi radians.
  */
  /* NOTE: When startAngle = 0, endAngle = 2Pi and counterclockwise = true, the spec does not indicate clearly.
  * We draw the entire circle, because some web sites use arc(x, y, r, 0, 2*Math.PI, true) to draw circle.
  * We preserve backward-compatibility.
  */
  else if (!counterclockwise && startAngle > endAngle)
    newEndAngle = startAngle + (twoPi - std::fmod(startAngle - endAngle, twoPi));
  else if (counterclockwise && startAngle < endAngle)
    newEndAngle = startAngle - (twoPi - std::fmod(endAngle - startAngle, twoPi));
  return newEndAngle;
}

/*
 * Adds an arc at x, y with the given radii and start/end angles.
 */

Napi::Value Context2d::Arc(const Napi::CallbackInfo& info) {
  double args[5];
  if(!checkArgs(info, args, 5))
    return;

  auto x = args[0];
  auto y = args[1];
  auto radius = args[2];
  auto startAngle = args[3];
  auto endAngle = args[4];

  if (radius < 0) {
    Napi::RangeError::New(env, "The radius provided is negative.").ThrowAsJavaScriptException();
    return env.Null();
  }

  bool counterclockwise = info[5].As<Napi::Boolean>().Value().FromMaybe(false);

  Context2d *context = info.This().Unwrap<Context2d>();
  cairo_t *ctx = context->context();

  canonicalizeAngle(startAngle, endAngle);
  endAngle = adjustEndAngle(startAngle, endAngle, counterclockwise);

  if (counterclockwise) {
    cairo_arc_negative(ctx, x, y, radius, startAngle, endAngle);
  } else {
    cairo_arc(ctx, x, y, radius, startAngle, endAngle);
  }
}

/*
 * Adds an arcTo point (x0,y0) to (x1,y1) with the given radius.
 *
 * Implementation influenced by WebKit.
 */

Napi::Value Context2d::ArcTo(const Napi::CallbackInfo& info) {
  double args[5];
  if(!checkArgs(info, args, 5))
    return;

  Context2d *context = info.This().Unwrap<Context2d>();
  cairo_t *ctx = context->context();

  // Current path point
  double x, y;
  cairo_get_current_point(ctx, &x, &y);
  Point<float> p0(x, y);

  // Point (x0,y0)
  Point<float> p1(args[0], args[1]);

  // Point (x1,y1)
  Point<float> p2(args[2], args[3]);

  float radius = args[4];

  if ((p1.x == p0.x && p1.y == p0.y)
    || (p1.x == p2.x && p1.y == p2.y)
    || radius == 0.f) {
    cairo_line_to(ctx, p1.x, p1.y);
    return;
  }

  Point<float> p1p0((p0.x - p1.x),(p0.y - p1.y));
  Point<float> p1p2((p2.x - p1.x),(p2.y - p1.y));
  float p1p0_length = sqrtf(p1p0.x * p1p0.x + p1p0.y * p1p0.y);
  float p1p2_length = sqrtf(p1p2.x * p1p2.x + p1p2.y * p1p2.y);

  double cos_phi = (p1p0.x * p1p2.x + p1p0.y * p1p2.y) / (p1p0_length * p1p2_length);
  // all points on a line logic
  if (-1 == cos_phi) {
    cairo_line_to(ctx, p1.x, p1.y);
    return;
  }

  if (1 == cos_phi) {
    // add infinite far away point
    unsigned int max_length = 65535;
    double factor_max = max_length / p1p0_length;
    Point<float> ep((p0.x + factor_max * p1p0.x), (p0.y + factor_max * p1p0.y));
    cairo_line_to(ctx, ep.x, ep.y);
    return;
  }

  float tangent = radius / tan(acos(cos_phi) / 2);
  float factor_p1p0 = tangent / p1p0_length;
  Point<float> t_p1p0((p1.x + factor_p1p0 * p1p0.x), (p1.y + factor_p1p0 * p1p0.y));

  Point<float> orth_p1p0(p1p0.y, -p1p0.x);
  float orth_p1p0_length = sqrt(orth_p1p0.x * orth_p1p0.x + orth_p1p0.y * orth_p1p0.y);
  float factor_ra = radius / orth_p1p0_length;

  double cos_alpha = (orth_p1p0.x * p1p2.x + orth_p1p0.y * p1p2.y) / (orth_p1p0_length * p1p2_length);
  if (cos_alpha < 0.f)
      orth_p1p0 = Point<float>(-orth_p1p0.x, -orth_p1p0.y);

  Point<float> p((t_p1p0.x + factor_ra * orth_p1p0.x), (t_p1p0.y + factor_ra * orth_p1p0.y));

  orth_p1p0 = Point<float>(-orth_p1p0.x, -orth_p1p0.y);
  float sa = acos(orth_p1p0.x / orth_p1p0_length);
  if (orth_p1p0.y < 0.f)
      sa = 2 * M_PI - sa;

  bool anticlockwise = false;

  float factor_p1p2 = tangent / p1p2_length;
  Point<float> t_p1p2((p1.x + factor_p1p2 * p1p2.x), (p1.y + factor_p1p2 * p1p2.y));
  Point<float> orth_p1p2((t_p1p2.x - p.x),(t_p1p2.y - p.y));
  float orth_p1p2_length = sqrtf(orth_p1p2.x * orth_p1p2.x + orth_p1p2.y * orth_p1p2.y);
  float ea = acos(orth_p1p2.x / orth_p1p2_length);

  if (orth_p1p2.y < 0) ea = 2 * M_PI - ea;
  if ((sa > ea) && ((sa - ea) < M_PI)) anticlockwise = true;
  if ((sa < ea) && ((ea - sa) > M_PI)) anticlockwise = true;

  cairo_line_to(ctx, t_p1p0.x, t_p1p0.y);

  if (anticlockwise && M_PI * 2 != radius) {
    cairo_arc_negative(ctx
      , p.x
      , p.y
      , radius
      , sa
      , ea);
  } else {
    cairo_arc(ctx
      , p.x
      , p.y
      , radius
      , sa
      , ea);
  }
}

/*
 * Adds an ellipse to the path which is centered at (x, y) position with the
 * radii radiusX and radiusY starting at startAngle and ending at endAngle
 * going in the given direction by anticlockwise (defaulting to clockwise).
 */

Napi::Value Context2d::Ellipse(const Napi::CallbackInfo& info) {
  double args[7];
  if(!checkArgs(info, args, 7))
    return;

  double radiusX = args[2];
  double radiusY = args[3];

  if (radiusX == 0 || radiusY == 0) return;

  double x = args[0];
  double y = args[1];
  double rotation = args[4];
  double startAngle = args[5];
  double endAngle = args[6];
  bool anticlockwise = info[7].As<Napi::Boolean>().Value().FromMaybe(false);

  Context2d *context = info.This().Unwrap<Context2d>();
  cairo_t *ctx = context->context();

  // See https://www.cairographics.org/cookbook/ellipses/
  double xRatio = radiusX / radiusY;

  cairo_matrix_t save_matrix;
  cairo_get_matrix(ctx, &save_matrix);
  cairo_translate(ctx, x, y);
  cairo_rotate(ctx, rotation);
  cairo_scale(ctx, xRatio, 1.0);
  cairo_translate(ctx, -x, -y);
  if (anticlockwise && M_PI * 2 != args[4]) {
    cairo_arc_negative(ctx,
      x,
      y,
      radiusY,
      startAngle,
      endAngle);
  } else {
    cairo_arc(ctx,
      x,
      y,
      radiusY,
      startAngle,
      endAngle);
  }
  cairo_set_matrix(ctx, &save_matrix);
}

#undef CHECK_RECEIVER
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       // Copyright (c) 2010 LearnBoost <tj@learnboost.com>

#pragma once

#include "cairo.h"
#include "Canvas.h"
#include "color.h"
#include "napi.h"
#include "uv.h"
#include <pango/pangocairo.h>
#include <stack>

/*
 * State struct.
 *
 * Used in conjunction with Save() / Restore() since
 * cairo's gstate maintains only a single source pattern at a time.
 */

struct canvas_state_t {
  rgba_t fill = { 0, 0, 0, 1 };
  rgba_t stroke = { 0, 0, 0, 1 };
  rgba_t shadow = { 0, 0, 0, 0 };
  double shadowOffsetX = 0.;
  double shadowOffsetY = 0.;
  cairo_pattern_t* fillPattern = nullptr;
  cairo_pattern_t* strokePattern = nullptr;
  cairo_pattern_t* fillGradient = nullptr;
  cairo_pattern_t* strokeGradient = nullptr;
  PangoFontDescription* fontDescription = nullptr;
  std::string font = "10px sans-serif";
  cairo_filter_t patternQuality = CAIRO_FILTER_GOOD;
  float globalAlpha = 1.f;
  int shadowBlur = 0;
  text_align_t textAlignment = TEXT_ALIGNMENT_LEFT; // TODO default is supposed to be START
  text_baseline_t textBaseline = TEXT_BASELINE_ALPHABETIC;
  canvas_draw_mode_t textDrawingMode = TEXT_DRAW_PATHS;
  bool imageSmoothingEnabled = true;

  canvas_state_t() {
    fontDescription = pango_font_description_from_string("sans");
    pango_font_description_set_absolute_size(fontDescription, 10 * PANGO_SCALE);
  }

  canvas_state_t(const canvas_state_t& other) {
    fill = other.fill;
    stroke = other.stroke;
    patternQuality = other.patternQuality;
    fillPattern = other.fillPattern;
    strokePattern = other.strokePattern;
    fillGradient = other.fillGradient;
    strokeGradient = other.strokeGradient;
    globalAlpha = other.globalAlpha;
    textAlignment = other.textAlignment;
    textBaseline = other.textBaseline;
    shadow = other.shadow;
    shadowBlur = other.shadowBlur;
    shadowOffsetX = other.shadowOffsetX;
    shadowOffsetY = other.shadowOffsetY;
    textDrawingMode = other.textDrawingMode;
    fontDescription = pango_font_description_copy(other.fontDescription);
    font = other.font;
    imageSmoothingEnabled = other.imageSmoothingEnabled;
  }

  ~canvas_state_t() {
    pango_font_description_free(fontDescription);
  }
};

/*
 * Equivalent to a PangoRectangle but holds floats instead of ints
 * (software pixels are stored here instead of pango units)
 *
 * Should be compatible with PANGO_ASCENT, PANGO_LBEARING, etc.
 */

typedef struct {
  float x;
  float y;
  float width;
  float height;
} float_rectangle;

class Context2d : public Napi::ObjectWrap<Context2d> {
  public:
    std::stack<canvas_state_t> states;
    canvas_state_t *state;
    Context2d(Canvas *canvas);
    static Napi::FunctionReference _DOMMatrix;
    static Napi::FunctionReference _parseFont;
    static Napi::FunctionReference constructor;
    static void Initialize(Napi::Env& env, Napi::Object& target);
    static Napi::Value New(const Napi::CallbackInfo& info);
    static Napi::Value SaveExternalModules(const Napi::CallbackInfo& info);
    static Napi::Value DrawImage(const Napi::CallbackInfo& info);
    static Napi::Value PutImageData(const Napi::CallbackInfo& info);
    static Napi::Value Save(const Napi::CallbackInfo& info);
    static Napi::Value Restore(const Napi::CallbackInfo& info);
    static Napi::Value Rotate(const Napi::CallbackInfo& info);
    static Napi::Value Translate(const Napi::CallbackInfo& info);
    static Napi::Value Scale(const Napi::CallbackInfo& info);
    static Napi::Value Transform(const Napi::CallbackInfo& info);
    static Napi::Value GetTransform(const Napi::CallbackInfo& info);
    static Napi::Value ResetTransform(const Napi::CallbackInfo& info);
    static Napi::Value SetTransform(const Napi::CallbackInfo& info);
    static Napi::Value IsPointInPath(const Napi::CallbackInfo& info);
    static Napi::Value BeginPath(const Napi::CallbackInfo& info);
    static Napi::Value ClosePath(const Napi::CallbackInfo& info);
    static Napi::Value AddPage(const Napi::CallbackInfo& info);
    static Napi::Value Clip(const Napi::CallbackInfo& info);
    static Napi::Value Fill(const Napi::CallbackInfo& info);
    static Napi::Value Stroke(const Napi::CallbackInfo& info);
    static Napi::Value FillText(const Napi::CallbackInfo& info);
    static Napi::Value StrokeText(const Napi::CallbackInfo& info);
    static Napi::Value SetFont(const Napi::CallbackInfo& info);
    static Napi::Value SetFillColor(const Napi::CallbackInfo& info);
    static Napi::Value SetStrokeColor(const Napi::CallbackInfo& info);
    static Napi::Value SetStrokePattern(const Napi::CallbackInfo& info);
    static Napi::Value SetTextAlignment(const Napi::CallbackInfo& info);
    static Napi::Value SetLineDash(const Napi::CallbackInfo& info);
    static Napi::Value GetLineDash(const Napi::CallbackInfo& info);
    static Napi::Value MeasureText(const Napi::CallbackInfo& info);
    static Napi::Value BezierCurveTo(const Napi::CallbackInfo& info);
    static Napi::Value QuadraticCurveTo(const Napi::CallbackInfo& info);
    static Napi::Value LineTo(const Napi::CallbackInfo& info);
    static Napi::Value MoveTo(const Napi::CallbackInfo& info);
    static Napi::Value FillRect(const Napi::CallbackInfo& info);
    static Napi::Value StrokeRect(const Napi::CallbackInfo& info);
    static Napi::Value ClearRect(const Napi::CallbackInfo& info);
    static Napi::Value Rect(const Napi::CallbackInfo& info);
    static Napi::Value RoundRect(const Napi::CallbackInfo& info);
    static Napi::Value Arc(const Napi::CallbackInfo& info);
    static Napi::Value ArcTo(const Napi::CallbackInfo& info);
    static Napi::Value Ellipse(const Napi::CallbackInfo& info);
    static Napi::Value GetImageData(const Napi::CallbackInfo& info);
    static Napi::Value CreateImageData(const Napi::CallbackInfo& info);
    static Napi::Value GetStrokeColor(const Napi::CallbackInfo& info);
    static Napi::Value CreatePattern(const Napi::CallbackInfo& info);
    static Napi::Value CreateLinearGradient(const Napi::CallbackInfo& info);
    static Napi::Value CreateRadialGradient(const Napi::CallbackInfo& info);
    Napi::Value GetFormat(const Napi::CallbackInfo& info);
    Napi::Value GetPatternQuality(const Napi::CallbackInfo& info);
    Napi::Value GetImageSmoothingEnabled(const Napi::CallbackInfo& info);
    Napi::Value GetGlobalCompositeOperation(const Napi::CallbackInfo& info);
    Napi::Value GetGlobalAlpha(const Napi::CallbackInfo& info);
    Napi::Value GetShadowColor(const Napi::CallbackInfo& info);
    Napi::Value GetMiterLimit(const Napi::CallbackInfo& info);
    Napi::Value GetLineCap(const Napi::CallbackInfo& info);
    Napi::Value GetLineJoin(const Napi::CallbackInfo& info);
    Napi::Value GetLineWidth(const Napi::CallbackInfo& info);
    Napi::Value GetLineDashOffset(const Napi::CallbackInfo& info);
    Napi::Value GetShadowOffsetX(const Napi::CallbackInfo& info);
    Napi::Value GetShadowOffsetY(const Napi::CallbackInfo& info);
    Napi::Value GetShadowBlur(const Napi::CallbackInfo& info);
    Napi::Value GetAntiAlias(const Napi::CallbackInfo& info);
    Napi::Value GetTextDrawingMode(const Napi::CallbackInfo& info);
    Napi::Value GetQuality(const Napi::CallbackInfo& info);
    Napi::Value GetCurrentTransform(const Napi::CallbackInfo& info);
    Napi::Value GetFillStyle(const Napi::CallbackInfo& info);
    Napi::Value GetStrokeStyle(const Napi::CallbackInfo& info);
    Napi::Value GetFont(const Napi::CallbackInfo& info);
    Napi::Value GetTextBaseline(const Napi::CallbackInfo& info);
    Napi::Value GetTextAlign(const Napi::CallbackInfo& info);
    void SetPatternQuality(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetImageSmoothingEnabled(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetGlobalCompositeOperation(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetGlobalAlpha(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetShadowColor(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetMiterLimit(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetLineCap(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetLineJoin(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetLineWidth(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetLineDashOffset(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetShadowOffsetX(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetShadowOffsetY(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetShadowBlur(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetAntiAlias(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetTextDrawingMode(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetQuality(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetCurrentTransform(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetFillStyle(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetStrokeStyle(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetFont(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetTextBaseline(const Napi::CallbackInfo& info, const Napi::Value& value);
    void SetTextAlign(const Napi::CallbackInfo& info, const Napi::Value& value);
    inline void setContext(cairo_t *ctx) { _context = ctx; }
    inline cairo_t *context(){ return _context; }
    inline Canvas *canvas(){ return _canvas; }
    inline bool hasShadow();
    void inline setSourceRGBA(rgba_t color);
    void inline setSourceRGBA(cairo_t *ctx, rgba_t color);
    void setTextPath(double x, double y);
    void blur(cairo_surface_t *surface, int radius);
    void shadow(void (fn)(cairo_t *cr));
    void shadowStart();
    void shadowApply();
    void savePath();
    void restorePath();
    void saveState();
    void restoreState();
    void inline setFillRule(Napi::Value value);
    void fill(bool preserve = false);
    void stroke(bool preserve = false);
    void save();
    void restore();
    void setFontFromState();
    void resetState();
    inline PangoLayout *layout(){ return _layout; }

  private:
    ~Context2d();
    void _resetPersistentHandles();
    Napi::Value _getFillColor();
    Napi::Value _getStrokeColor();
    void _setFillColor(Napi::Value arg);
    void _setFillPattern(Napi::Value arg);
    void _setStrokeColor(Napi::Value arg);
    void _setStrokePattern(Napi::Value arg);
    Napi::Persistent<v8::Value> _fillStyle;
    Napi::Persistent<v8::Value> _strokeStyle;
    Canvas *_canvas;
    cairo_t *_context;
    cairo_path_t *_path;
    PangoLayout *_layout;
};
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      // TypeScript Version: 3.0

import { Readable } from 'stream'

export interface PngConfig {
	/** Specifies the ZLIB compression level. Defaults to 6. */
	compressionLevel?: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
	/**
	 * Any bitwise combination of `PNG_FILTER_NONE`, `PNG_FILTER_SUB`,
	 * `PNG_FILTER_UP`, `PNG_FILTER_AVG` and `PNG_FILTER_PATETH`; or one of
	 * `PNG_ALL_FILTERS` or `PNG_NO_FILTERS` (all are properties of the canvas
	 * instance). These specify which filters *may* be used by libpng. During
	 * encoding, libpng will select the best filter from this list of allowed
	 * filters. Defaults to `canvas.PNG_ALL_FILTERS`.
	 */
	filters?: number
	/**
	 * _For creating indexed PNGs._ The palette of colors. Entries should be in
	 * RGBA order.
	 */
	palette?: Uint8ClampedArray
	/**
	 * _For creating indexed PNGs._ The index of the background color. Defaults
	 * to 0.
	 */
	backgroundIndex?: number
	/** pixels per inch */
	resolution?: number
}

export interface JpegConfig {
	/** Specifies the quality, between 0 and 1. Defaults to 0.75. */
	quality?: number
	/** Enables progressive encoding. Defaults to `false`. */
	progressive?: boolean
	/** Enables 2x2 chroma subsampling. Defaults to `true`. */
	chromaSubsampling?: boolean
}

export interface PdfConfig {
	title?: string
	author?: string
	subject?: string
	keywords?: string
	creator?: string
	creationDate?: Date
	modDate?: Date
}

export interface NodeCanvasRenderingContext2DSettings {
	alpha?: boolean
	pixelFormat?: 'RGBA32' | 'RGB24' | 'A8' | 'RGB16_565' | 'A1' | 'RGB30'
}

export class Canvas {
	width: number
	height: number

	/** _Non standard._ The type of the canvas. */
	readonly type: 'image'|'pdf'|'svg'

	/** _Non standard._ Getter. The stride used by the canvas. */
	readonly stride: number;

	/** Constant used in PNG encoding methods. */
	readonly PNG_NO_FILTERS: number
	/** Constant used in PNG encoding methods. */
	readonly PNG_ALL_FILTERS: number
	/** Constant used in PNG encoding methods. */
	readonly PNG_FILTER_NONE: number
	/** Constant used in PNG encoding methods. */
	readonly PNG_FILTER_SUB: number
	/** Constant used in PNG encoding methods. */
	readonly PNG_FILTER_UP: number
	/** Constant used in PNG encoding methods. */
	readonly PNG_FILTER_AVG: number
	/** Constant used in PNG encoding methods. */
	readonly PNG_FILTER_PAETH: number

	constructor(width: number, height: number, type?: 'image'|'pdf'|'svg')

	getContext(contextId: '2d', contextAttributes?: NodeCanvasRenderingContext2DSettings): CanvasRenderingContext2D

	/**
	 * For image canvases, encodes the canvas as a PNG. For PDF canvases,
	 * encodes the canvas as a PDF. For SVG canvases, encodes the canvas as an
	 * SVG.
	 */
	toBuffer(cb: (err: Error|null, result: Buffer) => void): void
	toBuffer(cb: (err: Error|null, result: Buffer) => void, mimeType: 'image/png', config?: PngConfig): void
	toBuffer(cb: (err: Error|null, result: Buffer) => void, mimeType: 'image/jpeg', config?: JpegConfig): void

	/**
	 * For image canvases, encodes the canvas as a PNG. For PDF canvases,
	 * encodes the canvas as a PDF. For SVG canvases, encodes the canvas as an
	 * SVG.
	 */
	toBuffer(): Buffer
	toBuffer(mimeType: 'image/png', config?: PngConfig): Buffer
	toBuffer(mimeType: 'image/jpeg', config?: JpegConfig): Buffer
	toBuffer(mimeType: 'application/pdf', config?: PdfConfig): Buffer

	/**
	 * Returns the unencoded pixel data, top-to-bottom. On little-endian (most)
	 * systems, the array will be ordered BGRA; on big-endian systems, it will
	 * be ARGB.
	 */
	toBuffer(mimeType: 'raw'): Buffer

	createPNGStream(config?: PngConfig): PNGStream
	createJPEGStream(config?: JpegConfig): JPEGStream
	createPDFStream(config?: PdfConfig): PDFStream

	/** Defaults to PNG image. */
	toDataURL(): string
	toDataURL(mimeType: 'image/png'): string
	toDataURL(mimeType: 'image/jpeg', quality?: number): string
	/** _Non-standard._ Defaults to PNG image. */
	toDataURL(cb: (err: Error|null, result: string) => void): void
	/** _Non-standard._ */
	toDataURL(mimeType: 'image/png', cb: (err: Error|null, result: string) => void): void
	/** _Non-standard._ */
	toDataURL(mimeType: 'image/jpeg', cb: (err: Error|null, result: string) => void): void
	/** _Non-standard._ */
	toDataURL(mimeType: 'image/jpeg', config: J