<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Created by , GNU Texinfo 7.0.1 -->
  <head>
    <meta charset="utf-8">
    <title>
      FFmpeg Bitstream Filters Documentation
    </title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="style.min.css">
  </head>
  <body>
    <div class="container">
      <h1>
      FFmpeg Bitstream Filters Documentation
      </h1>


<div class="top-level-extent" id="SEC_Top">

<div class="element-contents" id="SEC_Contents">
<h2 class="contents-heading">Table of Contents</h2>

<div class="contents">

<ul class="toc-numbered-mark">
  <li><a id="toc-Description" href="#Description">1 Description</a></li>
  <li><a id="toc-Bitstream-Filters" href="#Bitstream-Filters">2 Bitstream Filters</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-aac_005fadtstoasc" href="#aac_005fadtstoasc">2.1 aac_adtstoasc</a></li>
    <li><a id="toc-av1_005fmetadata" href="#av1_005fmetadata">2.2 av1_metadata</a></li>
    <li><a id="toc-chomp" href="#chomp">2.3 chomp</a></li>
    <li><a id="toc-dca_005fcore" href="#dca_005fcore">2.4 dca_core</a></li>
    <li><a id="toc-dump_005fextra" href="#dump_005fextra">2.5 dump_extra</a></li>
    <li><a id="toc-dv_005ferror_005fmarker" href="#dv_005ferror_005fmarker">2.6 dv_error_marker</a></li>
    <li><a id="toc-eac3_005fcore" href="#eac3_005fcore">2.7 eac3_core</a></li>
    <li><a id="toc-extract_005fextradata" href="#extract_005fextradata">2.8 extract_extradata</a></li>
    <li><a id="toc-filter_005funits" href="#filter_005funits">2.9 filter_units</a></li>
    <li><a id="toc-hapqa_005fextract" href="#hapqa_005fextract">2.10 hapqa_extract</a></li>
    <li><a id="toc-h264_005fmetadata" href="#h264_005fmetadata">2.11 h264_metadata</a></li>
    <li><a id="toc-h264_005fmp4toannexb" href="#h264_005fmp4toannexb">2.12 h264_mp4toannexb</a></li>
    <li><a id="toc-h264_005fredundant_005fpps" href="#h264_005fredundant_005fpps">2.13 h264_redundant_pps</a></li>
    <li><a id="toc-hevc_005fmetadata" href="#hevc_005fmetadata">2.14 hevc_metadata</a></li>
    <li><a id="toc-hevc_005fmp4toannexb" href="#hevc_005fmp4toannexb">2.15 hevc_mp4toannexb</a></li>
    <li><a id="toc-imxdump" href="#imxdump">2.16 imxdump</a></li>
    <li><a id="toc-mjpeg2jpeg" href="#mjpeg2jpeg">2.17 mjpeg2jpeg</a></li>
    <li><a id="toc-mjpegadump" href="#mjpegadump">2.18 mjpegadump</a></li>
    <li><a id="toc-mov2textsub-1" href="#mov2textsub-1">2.19 mov2textsub</a></li>
    <li><a id="toc-mp3decomp" href="#mp3decomp">2.20 mp3decomp</a></li>
    <li><a id="toc-mpeg2_005fmetadata" href="#mpeg2_005fmetadata">2.21 mpeg2_metadata</a></li>
    <li><a id="toc-mpeg4_005funpack_005fbframes" href="#mpeg4_005funpack_005fbframes">2.22 mpeg4_unpack_bframes</a></li>
    <li><a id="toc-noise" href="#noise">2.23 noise</a>
    <ul class="toc-numbered-mark">
      <li><a id="toc-Examples" href="#Examples">2.23.1 Examples</a></li>
    </ul></li>
    <li><a id="toc-null" href="#null">2.24 null</a></li>
    <li><a id="toc-pcm_005frechunk" href="#pcm_005frechunk">2.25 pcm_rechunk</a></li>
    <li><a id="toc-pgs_005fframe_005fmerge" href="#pgs_005fframe_005fmerge">2.26 pgs_frame_merge</a></li>
    <li><a id="toc-prores_005fmetadata" href="#prores_005fmetadata">2.27 prores_metadata</a></li>
    <li><a id="toc-remove_005fextra" href="#remove_005fextra">2.28 remove_extra</a></li>
    <li><a id="toc-setts" href="#setts">2.29 setts</a></li>
    <li><a id="toc-text2movsub-1" href="#text2movsub-1">2.30 text2movsub</a></li>
    <li><a id="toc-trace_005fheaders" href="#trace_005fheaders">2.31 trace_headers</a></li>
    <li><a id="toc-truehd_005fcore" href="#truehd_005fcore">2.32 truehd_core</a></li>
    <li><a id="toc-vp9_005fmetadata" href="#vp9_005fmetadata">2.33 vp9_metadata</a></li>
    <li><a id="toc-vp9_005fsuperframe" href="#vp9_005fsuperframe">2.34 vp9_superframe</a></li>
    <li><a id="toc-vp9_005fsuperframe_005fsplit" href="#vp9_005fsuperframe_005fsplit">2.35 vp9_superframe_split</a></li>
    <li><a id="toc-vp9_005fraw_005freorder" href="#vp9_005fraw_005freorder">2.36 vp9_raw_reorder</a></li>
  </ul></li>
  <li><a id="toc-See-Also" href="#See-Also">3 See Also</a></li>
  <li><a id="toc-Authors" href="#Authors">4 Authors</a></li>
</ul>
</div>
</div>

<ul class="mini-toc">
<li><a href="#Description" accesskey="1">Description</a></li>
<li><a href="#Bitstream-Filters" accesskey="2">Bitstream Filters</a></li>
<li><a href="#See-Also" accesskey="3">See Also</a></li>
<li><a href="#Authors" accesskey="4">Authors</a></li>
</ul>
<div class="chapter-level-extent" id="Description">
<h2 class="chapter">1 Description</h2>

<p>This document describes the bitstream filters provided by the
libavcodec library.
</p>
<p>A bitstream filter operates on the encoded stream data, and performs
bitstream level modifications without performing decoding.
</p>

</div>
<div class="chapter-level-extent" id="Bitstream-Filters">
<h2 class="chapter">2 Bitstream Filters</h2>

<p>When you configure your FFmpeg build, all the supported bitstream
filters are enabled by default. You can list all available ones using
the configure option <code class="code">--list-bsfs</code>.
</p>
<p>You can disable all the bitstream filters using the configure option
<code class="code">--disable-bsfs</code>, and selectively enable any bitstream filter using
the option <code class="code">--enable-bsf=BSF</code>, or you can disable a particular
bitstream filter using the option <code class="code">--disable-bsf=BSF</code>.
</p>
<p>The option <code class="code">-bsfs</code> of the ff* tools will display the list of
all the supported bitstream filters included in your build.
</p>
<p>The ff* tools have a -bsf option applied per stream, taking a
comma-separated list of filters, whose parameters follow the filter
name after a &rsquo;=&rsquo;.
</p>
<div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c:v copy -bsf:v filter1[=opt1=str1:opt2=str2][,filter2] OUTPUT
</pre></div>

<p>Below is a description of the currently available bitstream filters,
with their parameters, if any.
</p>
<ul class="mini-toc">
<li><a href="#aac_005fadtstoasc" accesskey="1">aac_adtstoasc</a></li>
<li><a href="#av1_005fmetadata" accesskey="2">av1_metadata</a></li>
<li><a href="#chomp" accesskey="3">chomp</a></li>
<li><a href="#dca_005fcore" accesskey="4">dca_core</a></li>
<li><a href="#dump_005fextra" accesskey="5">dump_extra</a></li>
<li><a href="#dv_005ferror_005fmarker" accesskey="6">dv_error_marker</a></li>
<li><a href="#eac3_005fcore" accesskey="7">eac3_core</a></li>
<li><a href="#extract_005fextradata" accesskey="8">extract_extradata</a></li>
<li><a href="#filter_005funits" accesskey="9">filter_units</a></li>
<li><a href="#hapqa_005fextract">hapqa_extract</a></li>
<li><a href="#h264_005fmetadata">h264_metadata</a></li>
<li><a href="#h264_005fmp4toannexb">h264_mp4toannexb</a></li>
<li><a href="#h264_005fredundant_005fpps">h264_redundant_pps</a></li>
<li><a href="#hevc_005fmetadata">hevc_metadata</a></li>
<li><a href="#hevc_005fmp4toannexb">hevc_mp4toannexb</a></li>
<li><a href="#imxdump">imxdump</a></li>
<li><a href="#mjpeg2jpeg">mjpeg2jpeg</a></li>
<li><a href="#mjpegadump">mjpegadump</a></li>
<li><a href="#mov2textsub-1">mov2textsub</a></li>
<li><a href="#mp3decomp">mp3decomp</a></li>
<li><a href="#mpeg2_005fmetadata">mpeg2_metadata</a></li>
<li><a href="#mpeg4_005funpack_005fbframes">mpeg4_unpack_bframes</a></li>
<li><a href="#noise">noise</a></li>
<li><a href="#null">null</a></li>
<li><a href="#pcm_005frechunk">pcm_rechunk</a></li>
<li><a href="#pgs_005fframe_005fmerge">pgs_frame_merge</a></li>
<li><a href="#prores_005fmetadata">prores_metadata</a></li>
<li><a href="#remove_005fextra">remove_extra</a></li>
<li><a href="#setts">setts</a></li>
<li><a href="#text2movsub-1">text2movsub</a></li>
<li><a href="#trace_005fheaders">trace_headers</a></li>
<li><a href="#truehd_005fcore">truehd_core</a></li>
<li><a href="#vp9_005fmetadata">vp9_metadata</a></li>
<li><a href="#vp9_005fsuperframe">vp9_superframe</a></li>
<li><a href="#vp9_005fsuperframe_005fsplit">vp9_superframe_split</a></li>
<li><a href="#vp9_005fraw_005freorder">vp9_raw_reorder</a></li>
</ul>
<div class="section-level-extent" id="aac_005fadtstoasc">
<h3 class="section">2.1 aac_adtstoasc</h3>

<p>Convert MPEG-2/4 AAC ADTS to an MPEG-4 Audio Specific Configuration
bitstream.
</p>
<p>This filter creates an MPEG-4 AudioSpecificConfig from an MPEG-2/4
ADTS header and removes the ADTS header.
</p>
<p>This filter is required for example when copying an AAC stream from a
raw ADTS AAC or an MPEG-TS container to MP4A-LATM, to an FLV file, or
to MOV/MP4 files and related formats such as 3GP or M4A. Please note
that it is auto-inserted for MP4A-LATM and MOV/MP4 and related formats.
</p>
</div>
<div class="section-level-extent" id="av1_005fmetadata">
<h3 class="section">2.2 av1_metadata</h3>

<p>Modify metadata embedded in an AV1 stream.
</p>
<dl class="table">
<dt><samp class="option">td</samp></dt>
<dd><p>Insert or remove temporal delimiter OBUs in all temporal units of the
stream.
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">insert</samp>&rsquo;</dt>
<dd><p>Insert a TD at the beginning of every TU which does not already have one.
</p></dd>
<dt>&lsquo;<samp class="samp">remove</samp>&rsquo;</dt>
<dd><p>Remove the TD from the beginning of every TU which has one.
</p></dd>
</dl>

</dd>
<dt><samp class="option">color_primaries</samp></dt>
<dt><samp class="option">transfer_characteristics</samp></dt>
<dt><samp class="option">matrix_coefficients</samp></dt>
<dd><p>Set the color description fields in the stream (see AV1 section 6.4.2).
</p>
</dd>
<dt><samp class="option">color_range</samp></dt>
<dd><p>Set the color range in the stream (see AV1 section 6.4.2; note that
this cannot be set for streams using BT.709 primaries, sRGB transfer
characteristic and identity (RGB) matrix coefficients).
</p><dl class="table">
<dt>&lsquo;<samp class="samp">tv</samp>&rsquo;</dt>
<dd><p>Limited range.
</p></dd>
<dt>&lsquo;<samp class="samp">pc</samp>&rsquo;</dt>
<dd><p>Full range.
</p></dd>
</dl>

</dd>
<dt><samp class="option">chroma_sample_position</samp></dt>
<dd><p>Set the chroma sample location in the stream (see AV1 section 6.4.2).
This can only be set for 4:2:0 streams.
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">vertical</samp>&rsquo;</dt>
<dd><p>Left position (matching the default in MPEG-2 and H.264).
</p></dd>
<dt>&lsquo;<samp class="samp">colocated</samp>&rsquo;</dt>
<dd><p>Top-left position.
</p></dd>
</dl>

</dd>
<dt><samp class="option">tick_rate</samp></dt>
<dd><p>Set the tick rate (<em class="emph">time_scale / num_units_in_display_tick</em>) in
the timing info in the sequence header.
</p></dd>
<dt><samp class="option">num_ticks_per_picture</samp></dt>
<dd><p>Set the number of ticks in each picture, to indicate that the stream
has a fixed framerate.  Ignored if <samp class="option">tick_rate</samp> is not also set.
</p>
</dd>
<dt><samp class="option">delete_padding</samp></dt>
<dd><p>Deletes Padding OBUs.
</p>
</dd>
</dl>

</div>
<div class="section-level-extent" id="chomp">
<h3 class="section">2.3 chomp</h3>

<p>Remove zero padding at the end of a packet.
</p>
</div>
<div class="section-level-extent" id="dca_005fcore">
<h3 class="section">2.4 dca_core</h3>

<p>Extract the core from a DCA/DTS stream, dropping extensions such as
DTS-HD.
</p>
</div>
<div class="section-level-extent" id="dump_005fextra">
<h3 class="section">2.5 dump_extra</h3>

<p>Add extradata to the beginning of the filtered packets except when
said packets already exactly begin with the extradata that is intended
to be added.
</p>
<dl class="table">
<dt><samp class="option">freq</samp></dt>
<dd><p>The additional argument specifies which packets should be filtered.
It accepts the values:
</p><dl class="table">
<dt>&lsquo;<samp class="samp">k</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">keyframe</samp>&rsquo;</dt>
<dd><p>add extradata to all key packets
</p>
</dd>
<dt>&lsquo;<samp class="samp">e</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">all</samp>&rsquo;</dt>
<dd><p>add extradata to all packets
</p></dd>
</dl>
</dd>
</dl>

<p>If not specified it is assumed &lsquo;<samp class="samp">k</samp>&rsquo;.
</p>
<p>For example the following <code class="command">ffmpeg</code> command forces a global
header (thus disabling individual packet headers) in the H.264 packets
generated by the <code class="code">libx264</code> encoder, but corrects them by adding
the header stored in extradata to the key packets:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -map 0 -flags:v +global_header -c:v libx264 -bsf:v dump_extra out.ts
</pre></div>

</div>
<div class="section-level-extent" id="dv_005ferror_005fmarker">
<h3 class="section">2.6 dv_error_marker</h3>

<p>Blocks in DV which are marked as damaged are replaced by blocks of the specified color.
</p>
<dl class="table">
<dt><samp class="option">color</samp></dt>
<dd><p>The color to replace damaged blocks by
</p></dd>
<dt><samp class="option">sta</samp></dt>
<dd><p>A 16 bit mask which specifies which of the 16 possible error status values are
to be replaced by colored blocks. 0xFFFE is the default which replaces all non 0
error status values.
</p><dl class="table">
<dt>&lsquo;<samp class="samp">ok</samp>&rsquo;</dt>
<dd><p>No error, no concealment
</p></dd>
<dt>&lsquo;<samp class="samp">err</samp>&rsquo;</dt>
<dd><p>Error, No concealment
</p></dd>
<dt>&lsquo;<samp class="samp">res</samp>&rsquo;</dt>
<dd><p>Reserved
</p></dd>
<dt>&lsquo;<samp class="samp">notok</samp>&rsquo;</dt>
<dd><p>Error or concealment
</p></dd>
<dt>&lsquo;<samp class="samp">notres</samp>&rsquo;</dt>
<dd><p>Not reserved
</p></dd>
<dt>&lsquo;<samp class="samp">Aa, Ba, Ca, Ab, Bb, Cb, A, B, C, a, b, erri, erru</samp>&rsquo;</dt>
<dd><p>The specific error status code
</p></dd>
</dl>
<p>see page 44-46 or section 5.5 of
<a class="url" href="http://web.archive.org/web/20060927044735/http://www.smpte.org/smpte_store/standards/pdf/s314m.pdf">http://web.archive.org/web/20060927044735/http://www.smpte.org/smpte_store/standards/pdf/s314m.pdf</a>
</p>
</dd>
</dl>

</div>
<div class="section-level-extent" id="eac3_005fcore">
<h3 class="section">2.7 eac3_core</h3>

<p>Extract the core from a E-AC-3 stream, dropping extra channels.
</p>
</div>
<div class="section-level-extent" id="extract_005fextradata">
<h3 class="section">2.8 extract_extradata</h3>

<p>Extract the in-band extradata.
</p>
<p>Certain codecs allow the long-term headers (e.g. MPEG-2 sequence headers,
or H.264/HEVC (VPS/)SPS/PPS) to be transmitted either &quot;in-band&quot; (i.e. as a part
of the bitstream containing the coded frames) or &quot;out of band&quot; (e.g. on the
container level). This latter form is called &quot;extradata&quot; in FFmpeg terminology.
</p>
<p>This bitstream filter detects the in-band headers and makes them available as
extradata.
</p>
<dl class="table">
<dt><samp class="option">remove</samp></dt>
<dd><p>When this option is enabled, the long-term headers are removed from the
bitstream after extraction.
</p></dd>
</dl>

</div>
<div class="section-level-extent" id="filter_005funits">
<h3 class="section">2.9 filter_units</h3>

<p>Remove units with types in or not in a given set from the stream.
</p>
<dl class="table">
<dt><samp class="option">pass_types</samp></dt>
<dd><p>List of unit types or ranges of unit types to pass through while removing
all others.  This is specified as a &rsquo;|&rsquo;-separated list of unit type values
or ranges of values with &rsquo;-&rsquo;.
</p>
</dd>
<dt><samp class="option">remove_types</samp></dt>
<dd><p>Identical to <samp class="option">pass_types</samp>, except the units in the given set
removed and all others passed through.
</p></dd>
</dl>

<p>Extradata is unchanged by this transformation, but note that if the stream
contains inline parameter sets then the output may be unusable if they are
removed.
</p>
<p>For example, to remove all non-VCL NAL units from an H.264 stream:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=pass_types=1-5' OUTPUT
</pre></div>

<p>To remove all AUDs, SEI and filler from an H.265 stream:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=remove_types=35|38-40' OUTPUT
</pre></div>

</div>
<div class="section-level-extent" id="hapqa_005fextract">
<h3 class="section">2.10 hapqa_extract</h3>

<p>Extract Rgb or Alpha part of an HAPQA file, without recompression, in order to create an HAPQ or an HAPAlphaOnly file.
</p>
<dl class="table">
<dt><samp class="option">texture</samp></dt>
<dd><p>Specifies the texture to keep.
</p>
<dl class="table">
<dt><samp class="option">color</samp></dt>
<dt><samp class="option">alpha</samp></dt>
</dl>

</dd>
</dl>

<p>Convert HAPQA to HAPQ
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i hapqa_inputfile.mov -c copy -bsf:v hapqa_extract=texture=color -tag:v HapY -metadata:s:v:0 encoder=&quot;HAPQ&quot; hapq_file.mov
</pre></div>

<p>Convert HAPQA to HAPAlphaOnly
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i hapqa_inputfile.mov -c copy -bsf:v hapqa_extract=texture=alpha -tag:v HapA -metadata:s:v:0 encoder=&quot;HAPAlpha Only&quot; hapalphaonly_file.mov
</pre></div>

</div>
<div class="section-level-extent" id="h264_005fmetadata">
<h3 class="section">2.11 h264_metadata</h3>

<p>Modify metadata embedded in an H.264 stream.
</p>
<dl class="table">
<dt><samp class="option">aud</samp></dt>
<dd><p>Insert or remove AUD NAL units in all access units of the stream.
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">pass</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">insert</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">remove</samp>&rsquo;</dt>
</dl>

<p>Default is pass.
</p>
</dd>
<dt><samp class="option">sample_aspect_ratio</samp></dt>
<dd><p>Set the sample aspect ratio of the stream in the VUI parameters.
See H.264 table E-1.
</p>
</dd>
<dt><samp class="option">overscan_appropriate_flag</samp></dt>
<dd><p>Set whether the stream is suitable for display using overscan
or not (see H.264 section E.2.1).
</p>
</dd>
<dt><samp class="option">video_format</samp></dt>
<dt><samp class="option">video_full_range_flag</samp></dt>
<dd><p>Set the video format in the stream (see H.264 section E.2.1 and
table E-2).
</p>
</dd>
<dt><samp class="option">colour_primaries</samp></dt>
<dt><samp class="option">transfer_characteristics</samp></dt>
<dt><samp class="option">matrix_coefficients</samp></dt>
<dd><p>Set the colour description in the stream (see H.264 section E.2.1
and tables E-3, E-4 and E-5).
</p>
</dd>
<dt><samp class="option">chroma_sample_loc_type</samp></dt>
<dd><p>Set the chroma sample location in the stream (see H.264 section
E.2.1 and figure E-1).
</p>
</dd>
<dt><samp class="option">tick_rate</samp></dt>
<dd><p>Set the tick rate (time_scale / num_units_in_tick) in the VUI
parameters.  This is the smallest time unit representable in the
stream, and in many cases represents the field rate of the stream
(double the frame rate).
</p></dd>
<dt><samp class="option">fixed_frame_rate_flag</samp></dt>
<dd><p>Set whether the stream has fixed framerate - typically this indicates
that the framerate is exactly half the tick rate, but the exact
meaning is dependent on interlacing and the picture structure (see
H.264 section E.2.1 and table E-6).
</p></dd>
<dt><samp class="option">zero_new_constraint_set_flags</samp></dt>
<dd><p>Zero constraint_set4_flag and constraint_set5_flag in the SPS. These
bits were reserved in a previous version of the H.264 spec, and thus
some hardware decoders require these to be zero. The result of zeroing
this is still a valid bitstream.
</p>
</dd>
<dt><samp class="option">crop_left</samp></dt>
<dt><samp class="option">crop_right</samp></dt>
<dt><samp class="option">crop_top</samp></dt>
<dt><samp class="option">crop_bottom</samp></dt>
<dd><p>Set the frame cropping offsets in the SPS.  These values will replace
the current ones if the stream is already cropped.
</p>
<p>These fields are set in pixels.  Note that some sizes may not be
representable if the chroma is subsampled or the stream is interlaced
(see H.264 section 7.4.2.1.1).
</p>
</dd>
<dt><samp class="option">sei_user_data</samp></dt>
<dd><p>Insert a string as SEI unregistered user data.  The argument must
be of the form <em class="emph">UUID+string</em>, where the UUID is as hex digits
possibly separated by hyphens, and the string can be anything.
</p>
<p>For example, &lsquo;<samp class="samp">086f3693-b7b3-4f2c-9653-21492feee5b8+hello</samp>&rsquo; will
insert the string &ldquo;hello&rdquo; associated with the given UUID.
</p>
</dd>
<dt><samp class="option">delete_filler</samp></dt>
<dd><p>Deletes both filler NAL units and filler SEI messages.
</p>
</dd>
<dt><samp class="option">display_orientation</samp></dt>
<dd><p>Insert, extract or remove Display orientation SEI messages.
See H.264 section D.1.27 and D.2.27 for syntax and semantics.
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">pass</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">insert</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">remove</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">extract</samp>&rsquo;</dt>
</dl>

<p>Default is pass.
</p>
<p>Insert mode works in conjunction with <code class="code">rotate</code> and <code class="code">flip</code> options.
Any pre-existing Display orientation messages will be removed in insert or remove mode.
Extract mode attaches the display matrix to the packet as side data.
</p>
</dd>
<dt><samp class="option">rotate</samp></dt>
<dd><p>Set rotation in display orientation SEI (anticlockwise angle in degrees).
Range is -360 to +360. Default is NaN.
</p>
</dd>
<d