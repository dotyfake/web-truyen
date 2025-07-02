ss="option">video_full_range_flag</samp></dt>
<dd><p>Set the video format in the stream (see H.265 section E.3.1 and
table E.2).
</p>
</dd>
<dt><samp class="option">colour_primaries</samp></dt>
<dt><samp class="option">transfer_characteristics</samp></dt>
<dt><samp class="option">matrix_coefficients</samp></dt>
<dd><p>Set the colour description in the stream (see H.265 section E.3.1
and tables E.3, E.4 and E.5).
</p>
</dd>
<dt><samp class="option">chroma_sample_loc_type</samp></dt>
<dd><p>Set the chroma sample location in the stream (see H.265 section
E.3.1 and figure E.1).
</p>
</dd>
<dt><samp class="option">tick_rate</samp></dt>
<dd><p>Set the tick rate in the VPS and VUI parameters (time_scale /
num_units_in_tick). Combined with <samp class="option">num_ticks_poc_diff_one</samp>, this can
set a constant framerate in the stream.  Note that it is likely to be
overridden by container parameters when the stream is in a container.
</p>
</dd>
<dt><samp class="option">num_ticks_poc_diff_one</samp></dt>
<dd><p>Set poc_proportional_to_timing_flag in VPS and VUI and use this value
to set num_ticks_poc_diff_one_minus1 (see H.265 sections 7.4.3.1 and
E.3.1).  Ignored if <samp class="option">tick_rate</samp> is not also set.
</p>
</dd>
<dt><samp class="option">crop_left</samp></dt>
<dt><samp class="option">crop_right</samp></dt>
<dt><samp class="option">crop_top</samp></dt>
<dt><samp class="option">crop_bottom</samp></dt>
<dd><p>Set the conformance window cropping offsets in the SPS.  These values
will replace the current ones if the stream is already cropped.
</p>
<p>These fields are set in pixels.  Note that some sizes may not be
representable if the chroma is subsampled (H.265 section 7.4.3.2.1).
</p>
</dd>
<dt><samp class="option">level</samp></dt>
<dd><p>Set the level in the VPS and SPS.  See H.265 section A.4 and tables
A.6 and A.7.
</p>
<p>The argument must be the name of a level (for example, &lsquo;<samp class="samp">5.1</samp>&rsquo;), a
<em class="emph">general_level_idc</em> value (for example, &lsquo;<samp class="samp">153</samp>&rsquo; for level 5.1),
or the special name &lsquo;<samp class="samp">auto</samp>&rsquo; indicating that the filter should
attempt to guess the level from the input stream properties.
</p>
</dd>
</dl>

</div>
<div class="section-level-extent" id="hevc_005fmp4toannexb">
<h3 class="section">2.15 hevc_mp4toannexb</h3>

<p>Convert an HEVC/H.265 bitstream from length prefixed mode to start code
prefixed mode (as defined in the Annex B of the ITU-T H.265
specification).
</p>
<p>This is required by some streaming formats, typically the MPEG-2
transport stream format (muxer <code class="code">mpegts</code>).
</p>
<p>For example to remux an MP4 file containing an HEVC stream to mpegts
format with <code class="command">ffmpeg</code>, you can use the command:
</p>
<div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT.mp4 -codec copy -bsf:v hevc_mp4toannexb OUTPUT.ts
</pre></div>

<p>Please note that this filter is auto-inserted for MPEG-TS (muxer
<code class="code">mpegts</code>) and raw HEVC/H.265 (muxer <code class="code">h265</code> or
<code class="code">hevc</code>) output formats.
</p>
</div>
<div class="section-level-extent" id="imxdump">
<h3 class="section">2.16 imxdump</h3>

<p>Modifies the bitstream to fit in MOV and to be usable by the Final Cut
Pro decoder. This filter only applies to the mpeg2video codec, and is
likely not needed for Final Cut Pro 7 and newer with the appropriate
<samp class="option">-tag:v</samp>.
</p>
<p>For example, to remux 30 MB/sec NTSC IMX to MOV:
</p>
<div class="example">
<pre class="example-preformatted">ffmpeg -i input.mxf -c copy -bsf:v imxdump -tag:v mx3n output.mov
</pre></div>

</div>
<div class="section-level-extent" id="mjpeg2jpeg">
<h3 class="section">2.17 mjpeg2jpeg</h3>

<p>Convert MJPEG/AVI1 packets to full JPEG/JFIF packets.
</p>
<p>MJPEG is a video codec wherein each video frame is essentially a
JPEG image. The individual frames can be extracted without loss,
e.g. by
</p>
<div class="example">
<pre class="example-preformatted">ffmpeg -i ../some_mjpeg.avi -c:v copy frames_%d.jpg
</pre></div>

<p>Unfortunately, these chunks are incomplete JPEG images, because
they lack the DHT segment required for decoding. Quoting from
<a class="url" href="http://www.digitalpreservation.gov/formats/fdd/fdd000063.shtml">http://www.digitalpreservation.gov/formats/fdd/fdd000063.shtml</a>:
</p>
<p>Avery Lee, writing in the rec.video.desktop newsgroup in 2001,
commented that &quot;MJPEG, or at least the MJPEG in AVIs having the
MJPG fourcc, is restricted JPEG with a fixed &ndash; and *omitted* &ndash;
Huffman table. The JPEG must be YCbCr colorspace, it must be 4:2:2,
and it must use basic Huffman encoding, not arithmetic or
progressive. . . . You can indeed extract the MJPEG frames and
decode them with a regular JPEG decoder, but you have to prepend
the DHT segment to them, or else the decoder won&rsquo;t have any idea
how to decompress the data. The exact table necessary is given in
the OpenDML spec.&quot;
</p>
<p>This bitstream filter patches the header of frames extracted from an MJPEG
stream (carrying the AVI1 header ID and lacking a DHT segment) to
produce fully qualified JPEG images.
</p>
<div class="example">
<pre class="example-preformatted">ffmpeg -i mjpeg-movie.avi -c:v copy -bsf:v mjpeg2jpeg frame_%d.jpg
exiftran -i -9 frame*.jpg
ffmpeg -i frame_%d.jpg -c:v copy rotated.avi
</pre></div>

</div>
<div class="section-level-extent" id="mjpegadump">
<h3 class="section">2.18 mjpegadump</h3>

<p>Add an MJPEG A header to the bitstream, to enable decoding by
Quicktime.
</p>
<a class="anchor" id="mov2textsub"></a></div>
<div class="section-level-extent" id="mov2textsub-1">
<h3 class="section">2.19 mov2textsub</h3>

<p>Extract a representable text file from MOV subtitles, stripping the
metadata header from each subtitle packet.
</p>
<p>See also the <a class="ref" href="#text2movsub">text2movsub</a> filter.
</p>
</div>
<div class="section-level-extent" id="mp3decomp">
<h3 class="section">2.20 mp3decomp</h3>

<p>Decompress non-standard compressed MP3 audio headers.
</p>
</div>
<div class="section-level-extent" id="mpeg2_005fmetadata">
<h3 class="section">2.21 mpeg2_metadata</h3>

<p>Modify metadata embedded in an MPEG-2 stream.
</p>
<dl class="table">
<dt><samp class="option">display_aspect_ratio</samp></dt>
<dd><p>Set the display aspect ratio in the stream.
</p>
<p>The following fixed values are supported:
</p><dl class="table">
<dt><samp class="option">4/3</samp></dt>
<dt><samp class="option">16/9</samp></dt>
<dt><samp class="option">221/100</samp></dt>
</dl>
<p>Any other value will result in square pixels being signalled instead
(see H.262 section 6.3.3 and table 6-3).
</p>
</dd>
<dt><samp class="option">frame_rate</samp></dt>
<dd><p>Set the frame rate in the stream.  This is constructed from a table
of known values combined with a small multiplier and divisor - if
the supplied value is not exactly representable, the nearest
representable value will be used instead (see H.262 section 6.3.3
and table 6-4).
</p>
</dd>
<dt><samp class="option">video_format</samp></dt>
<dd><p>Set the video format in the stream (see H.262 section 6.3.6 and
table 6-6).
</p>
</dd>
<dt><samp class="option">colour_primaries</samp></dt>
<dt><samp class="option">transfer_characteristics</samp></dt>
<dt><samp class="option">matrix_coefficients</samp></dt>
<dd><p>Set the colour description in the stream (see H.262 section 6.3.6
and tables 6-7, 6-8 and 6-9).
</p>
</dd>
</dl>

</div>
<div class="section-level-extent" id="mpeg4_005funpack_005fbframes">
<h3 class="section">2.22 mpeg4_unpack_bframes</h3>

<p>Unpack DivX-style packed B-frames.
</p>
<p>DivX-style packed B-frames are not valid MPEG-4 and were only a
workaround for the broken Video for Windows subsystem.
They use more space, can cause minor AV sync issues, require more
CPU power to decode (unless the player has some decoded picture queue
to compensate the 2,0,2,0 frame per packet style) and cause
trouble if copied into a standard container like mp4 or mpeg-ps/ts,
because MPEG-4 decoders may not be able to decode them, since they are
not valid MPEG-4.
</p>
<p>For example to fix an AVI file containing an MPEG-4 stream with
DivX-style packed B-frames using <code class="command">ffmpeg</code>, you can use the command:
</p>
<div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT.avi -codec copy -bsf:v mpeg4_unpack_bframes OUTPUT.avi
</pre></div>

</div>
<div class="section-level-extent" id="noise">
<h3 class="section">2.23 noise</h3>

<p>Damages the contents of packets or simply drops them without damaging the
container. Can be used for fuzzing or testing error resilience/concealment.
</p>
<p>Parameters:
</p><dl class="table">
<dt><samp class="option">amount</samp></dt>
<dd><p>Accepts an expression whose evaluation per-packet determines how often bytes in that
packet will be modified. A value below 0 will result in a variable frequency.
Default is 0 which results in no modification. However, if neither amount nor drop is specified,
amount will be set to <var class="var">-1</var>. See below for accepted variables.
</p></dd>
<dt><samp class="option">drop</samp></dt>
<dd><p>Accepts an expression evaluated per-packet whose value determines whether that packet is dropped.
Evaluation to a positive value results in the packet being dropped. Evaluation to a negative
value results in a variable chance of it being dropped, roughly inverse in proportion to the magnitude
of the value. Default is 0 which results in no drops. See below for accepted variables.
</p></dd>
<dt><samp class="option">dropamount</samp></dt>
<dd><p>Accepts a non-negative integer, which assigns a variable chance of it being dropped, roughly inverse
in proportion to the value. Default is 0 which results in no drops. This option is kept for backwards
compatibility and is equivalent to setting drop to a negative value with the same magnitude
i.e. <code class="code">dropamount=4</code> is the same as <code class="code">drop=-4</code>. Ignored if drop is also specified.
</p></dd>
</dl>

<p>Both <code class="code">amount</code> and <code class="code">drop</code> accept expressions containing the following variables:
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">n</samp>&rsquo;</dt>
<dd><p>The index of the packet, starting from zero.
</p></dd>
<dt>&lsquo;<samp class="samp">tb</samp>&rsquo;</dt>
<dd><p>The timebase for packet timestamps.
</p></dd>
<dt>&lsquo;<samp class="samp">pts</samp>&rsquo;</dt>
<dd><p>Packet presentation timestamp.
</p></dd>
<dt>&lsquo;<samp class="samp">dts</samp>&rsquo;</dt>
<dd><p>Packet decoding timestamp.
</p></dd>
<dt>&lsquo;<samp class="samp">nopts</samp>&rsquo;</dt>
<dd><p>Constant representing AV_NOPTS_VALUE.
</p></dd>
<dt>&lsquo;<samp class="samp">startpts</samp>&rsquo;</dt>
<dd><p>First non-AV_NOPTS_VALUE PTS seen in the stream.
</p></dd>
<dt>&lsquo;<samp class="samp">startdts</samp>&rsquo;</dt>
<dd><p>First non-AV_NOPTS_VALUE DTS seen in the stream.
</p></dd>
<dt>&lsquo;<samp class="samp">duration</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">d</samp>&rsquo;</dt>
<dd><p>Packet duration, in timebase units.
</p></dd>
<dt>&lsquo;<samp class="samp">pos</samp>&rsquo;</dt>
<dd><p>Packet position in input; may be -1 when unknown or not set.
</p></dd>
<dt>&lsquo;<samp class="samp">size</samp>&rsquo;</dt>
<dd><p>Packet size, in bytes.
</p></dd>
<dt>&lsquo;<samp class="samp">key</samp>&rsquo;</dt>
<dd><p>Whether packet is marked as a keyframe.
</p></dd>
<dt>&lsquo;<samp class="samp">state</samp>&rsquo;</dt>
<dd><p>A pseudo random integer, primarily derived from the content of packet payload.
</p></dd>
</dl>

<ul class="mini-toc">
<li><a href="#Examples" accesskey="1">Examples</a></li>
</ul>
<div class="subsection-level-extent" id="Examples">
<h4 class="subsection">2.23.1 Examples</h4>
<p>Apply modification to every byte but don&rsquo;t drop any packets.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c copy -bsf noise=1 output.mkv
</pre></div>

<p>Drop every video packet not marked as a keyframe after timestamp 30s but do not
modify any of the remaining packets.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c copy -bsf:v noise=drop='gt(t\,30)*not(key)' output.mkv
</pre></div>

<p>Drop one second of audio every 10 seconds and add some random noise to the rest.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c copy -bsf:a noise=amount=-1:drop='between(mod(t\,10)\,9\,10)' output.mkv
</pre></div>

</div>
</div>
<div class="section-level-extent" id="null">
<h3 class="section">2.24 null</h3>
<p>This bitstream filter passes the packets through unchanged.
</p>
</div>
<div class="section-level-extent" id="pcm_005frechunk">
<h3 class="section">2.25 pcm_rechunk</h3>

<p>Repacketize PCM audio to a fixed number of samples per packet or a fixed packet
rate per second. This is similar to the <a data-manual="ffmpeg-filters" href="ffmpeg-filters.html#asetnsamples">(ffmpeg-filters)asetnsamples audio
filter</a> but works on audio packets instead of audio frames.
</p>
<dl class="table">
<dt><samp class="option">nb_out_samples, n</samp></dt>
<dd><p>Set the number of samples per each output audio packet. The number is intended
as the number of samples <em class="emph">per each channel</em>. Default value is 1024.
</p>
</dd>
<dt><samp class="option">pad, p</samp></dt>
<dd><p>If set to 1, the filter will pad the last audio packet with silence, so that it
will contain the same number of samples (or roughly the same number of samples,
see <samp class="option">frame_rate</samp>) as the previous ones. Default value is 1.
</p>
</dd>
<dt><samp class="option">frame_rate, r</samp></dt>
<dd><p>This option makes the filter output a fixed number of packets per second instead
of a fixed number of samples per packet. If the audio sample rate is not
divisible by the frame rate then the number of samples will not be constant but
will vary slightly so that each packet will start as close to the frame
boundary as possible. Using this option has precedence over <samp class="option">nb_out_samples</samp>.
</p></dd>
</dl>

<p>You can generate the well known 1602-1601-1602-1601-1602 pattern of 48kHz audio
for NTSC frame rate using the <samp class="option">frame_rate</samp> option.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -f lavfi -i sine=r=48000:d=1 -c pcm_s16le -bsf pcm_rechunk=r=30000/1001 -f framecrc -
</pre></div>

</div>
<div class="section-level-extent" id="pgs_005fframe_005fmerge">
<h3 class="section">2.26 pgs_frame_merge</h3>

<p>Merge a sequence of PGS Subtitle segments ending with an &quot;end of display set&quot;
segment into a single packet.
</p>
<p>This is required by some containers that support PGS subtitles
(muxer <code class="code">matroska</code>).
</p>
</div>
<div class="section-level-extent" id="prores_005fmetadata">
<h3 class="section">2.27 prores_metadata</h3>

<p>Modify color property metadata embedded in prores stream.
</p>
<dl class="table">
<dt><samp class="option">color_primaries</samp></dt>
<dd><p>Set the color primaries.
Available values are:
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">auto</samp>&rsquo;</dt>
<dd><p>Keep the same color primaries property (default).
</p>
</dd>
<dt>&lsquo;<samp class="samp">unknown</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt709</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt470bg</samp>&rsquo;</dt>
<dd><p>BT601 625
</p>
</dd>
<dt>&lsquo;<samp class="samp">smpte170m</samp>&rsquo;</dt>
<dd><p>BT601 525
</p>
</dd>
<dt>&lsquo;<samp class="samp">bt2020</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">smpte431</samp>&rsquo;</dt>
<dd><p>DCI P3
</p>
</dd>
<dt>&lsquo;<samp class="samp">smpte432</samp>&rsquo;</dt>
<dd><p>P3 D65
</p>
</dd>
</dl>

</dd>
<dt><samp class="option">transfer_characteristics</samp></dt>
<dd><p>Set the color transfer.
Available values are:
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">auto</samp>&rsquo;</dt>
<dd><p>Keep the same transfer characteristics property (default).
</p>
</dd>
<dt>&lsquo;<samp class="samp">unknown</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt709</samp>&rsquo;</dt>
<dd><p>BT 601, BT 709, BT 2020
</p></dd>
<dt>&lsquo;<samp class="samp">smpte2084</samp>&rsquo;</dt>
<dd><p>SMPTE ST 2084
</p></dd>
<dt>&lsquo;<samp class="samp">arib-std-b67</samp>&rsquo;</dt>
<dd><p>ARIB STD-B67
</p></dd>
</dl>


</dd>
<dt><samp class="option">matrix_coefficients</samp></dt>
<dd><p>Set the matrix coefficient.
Available values are:
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">auto</samp>&rsquo;</dt>
<dd><p>Keep the same colorspace property (default).
</p>
</dd>
<dt>&lsquo;<samp class="samp">unknown</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt709</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">smpte170m</samp>&rsquo;</dt>
<dd><p>BT 601
</p>
</dd>
<dt>&lsquo;<samp class="samp">bt2020nc</samp>&rsquo;</dt>
</dl>
</dd>
</dl>

<p>Set Rec709 colorspace for each frame of the file
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c copy -bsf:v prores_metadata=color_primaries=bt709:color_trc=bt709:colorspace=bt709 output.mov
</pre></div>

<p>Set Hybrid Log-Gamma parameters for each frame of the file
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -c copy -bsf:v prores_metadata=color_primaries=bt2020:color_trc=arib-std-b67:colorspace=bt2020nc output.mov
</pre></div>

</div>
<div class="section-level-extent" id="remove_005fextra">
<h3 class="section">2.28 remove_extra</h3>

<p>Remove extradata from packets.
</p>
<p>It accepts the following parameter:
</p><dl class="table">
<dt><samp class="option">freq</samp></dt>
<dd><p>Set which frame types to remove extradata from.
</p>
<dl class="table">
<dt>&lsquo;<samp class="samp">k</samp>&rsquo;</dt>
<dd><p>Remove extradata from non-keyframes only.
</p>
</dd>
<dt>&lsquo;<samp class="samp">keyframe</samp>&rsquo;</dt>
<dd><p>Remove extradata from keyframes only.
</p>
</dd>
<dt>&lsquo;<samp class="samp">e, all</samp>&rsquo;</dt>
<dd><p>Remove extradata from all frames.
</p>
</dd>
</dl>
</dd>
</dl>

</div>
<div class="section-level-extent" id="setts">
<h3 class="section">2.29 setts</h3>
<p>Set PTS and DTS in packets.
</p>
<p>It accepts the following parameters:
</p><dl class="table">
<dt><samp class="option">ts</samp></dt>
<dt><samp class="option">pts</samp></dt>
<dt><samp class="option">dts</samp></dt>
<dd><p>Set expressions for PTS, DTS or both.
</p></dd>
<dt><samp class="option">duration</samp></dt>
<dd><p>Set expression for duration.
</p></dd>
<dt><samp class="option">time_base</samp></dt>
<dd><p>Set output time base.
</p></dd>
</dl>

<p>The expressions are evaluated through the eval API and can contain the following
constants:
</p>
<dl class="table">
<dt><samp class="option">N</samp></dt>
<dd><p>The count of the input packet. Starting from 0.
</p>
</dd>
<dt><samp class="option">TS</samp></dt>
<dd><p>The demux timestamp in input in case of <code class="code">ts</code> or <code class="code">dts</code> option or presentation
timestamp in case of <code class="code">pts</code> option.
</p>
</dd>
<dt><samp class="option">POS</samp></dt>
<dd><p>The original position in the file of the packet, or undefined if undefined
for the current packet
</p>
</dd>
<dt><samp class="option">DTS</samp></dt>
<dd><p>The demux timestamp in input.
</p>
</dd>
<dt><samp class="option">PTS</samp></dt>
<dd><p>The presentation timestamp in input.
</p>
</dd>
<dt><samp class="option">DURATION</samp></dt>
<dd><p>The duration in input.
</p>
</dd>
<dt><samp class="option">STARTDTS</samp></dt>
<dd><p>The DTS of the first packet.
</p>
</dd>
<dt><samp class="option">STARTPTS</samp></dt>
<dd><p>The PTS of the first packet.
</p>
</dd>
<dt><samp class="option">PREV_INDTS</samp></dt>
<dd><p>The previous input DTS.
</p>
</dd>
<dt><samp class="option">PREV_INPTS</samp></dt>
<dd><p>The previous input PTS.
</p>
</dd>
<dt><samp class="option">PREV_INDURATION</samp></dt>
<dd><p>The previous input duration.
</p>
</dd>
<dt><samp class="option">PREV_OUTDTS</samp></dt>
<dd><p>The previous output DTS.
</p>
</dd>
<dt><samp class="option">PREV_OUTPTS</samp></dt>
<dd><p>The previous output PTS.
</p>
</dd>
<dt><samp class="option">PREV_OUTDURATION</samp></dt>
<dd><p>The previous output duration.
</p>
</dd>
<dt><samp class="option">NEXT_DTS</samp></dt>
<dd><p>The next input DTS.
</p>
</dd>
<dt><samp class="option">NEXT_PTS</samp></dt>
<dd><p>The next input PTS.
</p>
</dd>
<dt><samp class="option">NEXT_DURATION</samp></dt>
<dd><p>The next input duration.
</p>
</dd>
<dt><samp class="option">TB</samp></dt>
<dd><p>The timebase of stream packet belongs.
</p>
</dd>
<dt><samp class="option">TB_OUT</samp></dt>
<dd><p>The output timebase.
</p>
</dd>
<dt><samp class="option">SR</samp></dt>
<dd><p>The sample rate of stream packet belongs.
</p>
</dd>
<dt><samp class="option">NOPTS</samp></dt>
<dd><p>The AV_NOPTS_VALUE constant.
</p></dd>
</dl>

<a class="anchor" id="text2movsub"></a></div>
<div class="section-level-extent" id="text2movsub-1">
<h3 class="section">2.30 text2movsub</h3>

<p>Convert text subtitles to MOV subtitles (as used by the <code class="code">mov_text</code>
codec) with metadata headers.
</p>
<p>See also the <a class="ref" href="#mov2textsub">mov2textsub</a> filter.
</p>
</div>
<div class="section-level-extent" id="trace_005fheaders">
<h3 class="section">2.31 trace_headers</h3>

<p>Log trace output containing all syntax elements in the coded stream
headers (everything above the level of individual coded blocks).
This can be useful for debugging low-level stream issues.
</p>
<p>Supports AV1, H.264, H.265, (M)JPEG, MPEG-2 and VP9, but depending
on the build only a subset of these may be available.
</p>
</div>
<div class="section-level-extent" id="truehd_005fcore">
<h3 class="section">2.32 truehd_core</h3>

<p>Extract the core from a TrueHD stream, dropping ATMOS data.
</p>
</div>
<div class="section-level-extent" id="vp9_005fmetadata">
<h3 class="section">2.33 vp9_metadata</h3>

<p>Modify metadata embedded in a VP9 stream.
</p>
<dl class="table">
<dt><samp class="option">color_space</samp></dt>
<dd><p>Set the color space value in the frame header.  Note that any frame
set to RGB will be implicitly set to PC range and that RGB is
incompatible with profiles 0 and 2.
</p><dl class="table">
<dt>&lsquo;<samp class="samp">unknown</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt601</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt709</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">smpte170</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">smpte240</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bt2020</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">rgb</samp>&rsquo;</dt>
</dl>

</dd>
<dt><samp class="option">color_range</samp></dt>
<dd><p>Set the color range value in the frame header.  Note that any value
imposed by the color space will take precedence over this value.
</p><dl class="table">
<dt>&lsquo;<samp class="samp">tv</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">pc</samp>&rsquo;</dt>
</dl>
</dd>
</dl>

</div>
<div class="section-level-extent" id="vp9_005fsuperframe">
<h3 class="section">2.34 vp9_superframe</h3>

<p>Merge VP9 invisible (alt-ref) frames back into VP9 superframes. This
fixes merging of split/segmented VP9 streams where the alt-ref frame
was split from its visible counterpart.
</p>
</div>
<div class="section-level-extent" id="vp9_005fsuperframe_005fsplit">
<h3 class="section">2.35 vp9_superframe_split</h3>

<p>Split VP9 superframes into single frames.
</p>
</div>
<div class="section-level-extent" id="vp9_005fraw_005freorder">
<h3 class="section">2.36 vp9_raw_reorder</h3>

<p>Given a VP9 stream with correct timestamps but possibly out of order,
insert additional show-existing-frame packets to correct the ordering.
</p>

</div>
</div>
<div class="chapter-level-extent" id="See-Also">
<h2 class="chapter">3 See Also</h2>

<p><a class="url" href="ffmpeg.html">ffmpeg</a>, <a class="url" href="ffplay.html">ffplay</a>, <a class="url" href="ffprobe.html">ffprobe</a>,
<a class="url" href="libavcodec.html">libavcodec</a>
</p>

</div>
<div class="chapter-level-extent" id="Authors">
<h2 class="chapter">4 Authors</h2>

<p>The FFmpeg developers.
</p>
<p>For details about the authorship, see the Git history of the project
(https://git.ffmpeg.org/ffmpeg), e.g. by typing the command
<code class="command">git log</code> in the FFmpeg source directory, or browsing the
online repository at <a class="url" href="https://git.ffmpeg.org/ffmpeg">https://git.ffmpeg.org/ffmpeg</a>.
</p>
<p>Maintainers for the specific components are listed in the file
<samp class="file">MAINTAINERS</samp> in the source code tree.
</p>

</div>
</div>
      <p style="font-size: small;">
        This document was generated using <a class="uref" href="https://www.gnu.org/software/texinfo/"><em class="emph">makeinfo</em></a>.
      </p>
    </div>
  </body>
</html>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 