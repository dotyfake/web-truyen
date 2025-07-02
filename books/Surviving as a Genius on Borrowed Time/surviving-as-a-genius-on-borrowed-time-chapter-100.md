ew segment if its
PTS satisfies the relation:
</p><div class="example">
<pre class="example-preformatted">PTS &gt;= start_time - time_delta
</pre></div>

<p>This option is useful when splitting video content, which is always
split at GOP boundaries, in case a key frame is found just before the
specified split time.
</p>
<p>In particular may be used in combination with the <samp class="file">ffmpeg</samp> option
<var class="var">force_key_frames</var>. The key frame times specified by
<var class="var">force_key_frames</var> may not be set accurately because of rounding
issues, with the consequence that a key frame time may result set just
before the specified time. For constant frame rate videos a value of
1/(2*<var class="var">frame_rate</var>) should address the worst case mismatch between
the specified time and the time set by <var class="var">force_key_frames</var>.
</p>
</dd>
<dt><samp class="option">segment_times <var class="var">times</var></samp></dt>
<dd><p>Specify a list of split points. <var class="var">times</var> contains a list of comma
separated duration specifications, in increasing order. See also
the <samp class="option">segment_time</samp> option.
</p>
</dd>
<dt><samp class="option">segment_frames <var class="var">frames</var></samp></dt>
<dd><p>Specify a list of split video frame numbers. <var class="var">frames</var> contains a
list of comma separated integer numbers, in increasing order.
</p>
<p>This option specifies to start a new segment whenever a reference
stream key frame is found and the sequential number (starting from 0)
of the frame is greater or equal to the next value in the list.
</p>
</dd>
<dt><samp class="option">segment_wrap <var class="var">limit</var></samp></dt>
<dd><p>Wrap around segment index once it reaches <var class="var">limit</var>.
</p>
</dd>
<dt><samp class="option">segment_start_number <var class="var">number</var></samp></dt>
<dd><p>Set the sequence number of the first segment. Defaults to <code class="code">0</code>.
</p>
</dd>
<dt><samp class="option">strftime <var class="var">1|0</var></samp></dt>
<dd><p>Use the <code class="code">strftime</code> function to define the name of the new
segments to write. If this is selected, the output segment name must
contain a <code class="code">strftime</code> function template. Default value is
<code class="code">0</code>.
</p>
</dd>
<dt><samp class="option">break_non_keyframes <var class="var">1|0</var></samp></dt>
<dd><p>If enabled, allow segments to start on frames other than keyframes. This
improves behavior on some players when the time between keyframes is
inconsistent, but may make things worse on others, and can cause some oddities
during seeking. Defaults to <code class="code">0</code>.
</p>
</dd>
<dt><samp class="option">reset_timestamps <var class="var">1|0</var></samp></dt>
<dd><p>Reset timestamps at the beginning of each segment, so that each segment
will start with near-zero timestamps. It is meant to ease the playback
of the generated segments. May not work with some combinations of
muxers/codecs. It is set to <code class="code">0</code> by default.
</p>
</dd>
<dt><samp class="option">initial_offset <var class="var">offset</var></samp></dt>
<dd><p>Specify timestamp offset to apply to the output packet timestamps. The
argument must be a time duration specification, and defaults to 0.
</p>
</dd>
<dt><samp class="option">write_empty_segments <var class="var">1|0</var></samp></dt>
<dd><p>If enabled, write an empty segment if there are no packets during the period a
segment would usually span. Otherwise, the segment will be filled with the next
packet written. Defaults to <code class="code">0</code>.
</p></dd>
</dl>

<p>Make sure to require a closed GOP when encoding and to set the GOP
size to fit your segment time constraint.
</p>
</div>
<div class="subsection-level-extent" id="Examples-10">
<h4 class="subsection">4.30.2 Examples</h4>

<ul class="itemize mark-bullet">
<li>Remux the content of file <samp class="file">in.mkv</samp> to a list of segments
<samp class="file">out-000.nut</samp>, <samp class="file">out-001.nut</samp>, etc., and write the list of
generated segments to <samp class="file">out.list</samp>:
<div class="example">
<pre class="example-preformatted">ffmpeg -i in.mkv -codec hevc -flags +cgop -g 60 -map 0 -f segment -segment_list out.list out%03d.nut
</pre></div>

</li><li>Segment input and set output format options for the output segments:
<div class="example">
<pre class="example-preformatted">ffmpeg -i in.mkv -f segment -segment_time 10 -segment_format_options movflags=+faststart out%03d.mp4
</pre></div>

</li><li>Segment the input file according to the split points specified by the
<var class="var">segment_times</var> option:
<div class="example">
<pre class="example-preformatted">ffmpeg -i in.mkv -codec copy -map 0 -f segment -segment_list out.csv -segment_times 1,2,3,5,8,13,21 out%03d.nut
</pre></div>

</li><li>Use the <code class="command">ffmpeg</code> <samp class="option">force_key_frames</samp>
option to force key frames in the input at the specified location, together
with the segment option <samp class="option">segment_time_delta</samp> to account for
possible roundings operated when setting key frame times.
<div class="example">
<pre class="example-preformatted">ffmpeg -i in.mkv -force_key_frames 1,2,3,5,8,13,21 -codec:v mpeg4 -codec:a pcm_s16le -map 0 \
-f segment -segment_list out.csv -segment_times 1,2,3,5,8,13,21 -segment_time_delta 0.05 out%03d.nut
</pre></div>
<p>In order to force key frames on the input file, transcoding is
required.
</p>
</li><li>Segment the input file by splitting the input file according to the
frame numbers sequence specified with the <samp class="option">segment_frames</samp> option:
<div class="example">
<pre class="example-preformatted">ffmpeg -i in.mkv -codec copy -map 0 -f segment -segment_list out.csv -segment_frames 100,200,300,500,800 out%03d.nut
</pre></div>

</li><li>Convert the <samp class="file">in.mkv</samp> to TS segments using the <code class="code">libx264</code>
and <code class="code">aac</code> encoders:
<div class="example">
<pre class="example-preformatted">ffmpeg -i in.mkv -map 0 -codec:v libx264 -codec:a aac -f ssegment -segment_list out.list out%03d.ts
</pre></div>

</li><li>Segment the input file, and create an M3U8 live playlist (can be used
as live HLS source):
<div class="example">
<pre class="example-preformatted">ffmpeg -re -i in.mkv -codec copy -map 0 -f segment -segment_list playlist.m3u8 \
-segment_list_flags +live -segment_time 10 out%03d.mkv
</pre></div>
</li></ul>

</div>
</div>
<div class="section-level-extent" id="smoothstreaming">
<h3 class="section">4.31 smoothstreaming</h3>

<p>Smooth Streaming muxer generates a set of files (Manifest, chunks) suitable for serving with conventional web server.
</p>
<dl class="table">
<dt><samp class="option">window_size</samp></dt>
<dd><p>Specify the number of fragments kept in the manifest. Default 0 (keep all).
</p>
</dd>
<dt><samp class="option">extra_window_size</samp></dt>
<dd><p>Specify the number of fragments kept outside of the manifest before removing from disk. Default 5.
</p>
</dd>
<dt><samp class="option">lookahead_count</samp></dt>
<dd><p>Specify the number of lookahead fragments. Default 2.
</p>
</dd>
<dt><samp class="option">min_frag_duration</samp></dt>
<dd><p>Specify the minimum fragment duration (in microseconds). Default 5000000.
</p>
</dd>
<dt><samp class="option">remove_at_exit</samp></dt>
<dd><p>Specify whether to remove all fragments when finished. Default 0 (do not remove).
</p>
</dd>
</dl>

<a class="anchor" id="streamhash"></a></div>
<div class="section-level-extent" id="streamhash-1">
<h3 class="section">4.32 streamhash</h3>

<p>Per stream hash testing format.
</p>
<p>This muxer computes and prints a cryptographic hash of all the input frames,
on a per-stream basis. This can be used for equality checks without having
to do a complete binary comparison.
</p>
<p>By default audio frames are converted to signed 16-bit raw audio and
video frames to raw video before computing the hash, but the output
of explicit conversions to other codecs can also be used. Timestamps
are ignored. It uses the SHA-256 cryptographic hash function by default,
but supports several other algorithms.
</p>
<p>The output of the muxer consists of one line per stream of the form:
<var class="var">streamindex</var>,<var class="var">streamtype</var>,<var class="var">algo</var>=<var class="var">hash</var>, where
<var class="var">streamindex</var> is the index of the mapped stream, <var class="var">streamtype</var> is a
single character indicating the type of stream, <var class="var">algo</var> is a short string
representing the hash function used, and <var class="var">hash</var> is a hexadecimal number
representing the computed hash.
</p>
<dl class="table">
<dt><samp class="option">hash <var class="var">algorithm</var></samp></dt>
<dd><p>Use the cryptographic hash function specified by the string <var class="var">algorithm</var>.
Supported values include <code class="code">MD5</code>, <code class="code">murmur3</code>, <code class="code">RIPEMD128</code>,
<code class="code">RIPEMD160</code>, <code class="code">RIPEMD256</code>, <code class="code">RIPEMD320</code>, <code class="code">SHA160</code>,
<code class="code">SHA224</code>, <code class="code">SHA256</code> (default), <code class="code">SHA512/224</code>, <code class="code">SHA512/256</code>,
<code class="code">SHA384</code>, <code class="code">SHA512</code>, <code class="code">CRC32</code> and <code class="code">adler32</code>.
</p>
</dd>
</dl>

<ul class="mini-toc">
<li><a href="#Examples-11" accesskey="1">Examples</a></li>
</ul>
<div class="subsection-level-extent" id="Examples-11">
<h4 class="subsection">4.32.1 Examples</h4>

<p>To compute the SHA-256 hash of the input converted to raw audio and
video, and store it in the file <samp class="file">out.sha256</samp>:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -f streamhash out.sha256
</pre></div>

<p>To print an MD5 hash to stdout use the command:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i INPUT -f streamhash -hash md5 -
</pre></div>

<p>See also the <a class="ref" href="#hash">hash</a> and <a class="ref" href="#framehash">framehash</a> muxers.
</p>
<a class="anchor" id="tee"></a></div>
</div>
<div class="section-level-extent" id="tee-1">
<h3 class="section">4.33 tee</h3>

<p>The tee muxer can be used to write the same data to several outputs, such as files or streams.
It can be used, for example, to stream a video over a network and save it to disk at the same time.
</p>
<p>It is different from specifying several outputs to the <code class="command">ffmpeg</code>
command-line tool. With the tee muxer, the audio and video data will be encoded only once.
With conventional multiple outputs, multiple encoding operations in parallel are initiated,
which can be a very expensive process. The tee muxer is not useful when using the libavformat API
directly because it is then possible to feed the same packets to several muxers directly.
</p>
<p>Since the tee muxer does not represent any particular output format, ffmpeg cannot auto-select
output streams. So all streams intended for output must be specified using <code class="code">-map</code>. See
the examples below.
</p>
<p>Some encoders may need different options depending on the output format;
the auto-detection of this can not work with the tee muxer, so they need to be explicitly specified.
The main example is the <samp class="option">global_header</samp> flag.
</p>
<p>The slave outputs are specified in the file name given to the muxer,
separated by &rsquo;|&rsquo;. If any of the slave name contains the &rsquo;|&rsquo; separator,
leading or trailing spaces or any special character, those must be
escaped (see <a data-manual="ffmpeg-utils" href="ffmpeg-utils.html#quoting_005fand_005fescaping">(ffmpeg-utils)the &quot;Quoting and escaping&quot;
section in the ffmpeg-utils(1) manual</a>).
</p>
<ul class="mini-toc">
<li><a href="#Options-17" accesskey="1">Options</a></li>
<li><a href="#Examples-12" accesskey="2">Examples</a></li>
</ul>
<div class="subsection-level-extent" id="Options-17">
<h4 class="subsection">4.33.1 Options</h4>

<dl class="table">
<dt><samp class="option">use_fifo <var class="var">bool</var></samp></dt>
<dd><p>If set to 1, slave outputs will be processed in separate threads using the <a class="ref" href="#fifo">fifo</a>
muxer. This allows to compensate for different speed/latency/reliability of
outputs and setup transparent recovery. By default this feature is turned off.
</p>
</dd>
<dt><samp class="option">fifo_options</samp></dt>
<dd><p>Options to pass to fifo pseudo-muxer instances. See <a class="ref" href="#fifo">fifo</a>.
</p>
</dd>
</dl>

<p>Muxer options can be specified for each slave by prepending them as a list of
<var class="var">key</var>=<var class="var">value</var> pairs separated by &rsquo;:&rsquo;, between square brackets. If
the options values contain a special character or the &rsquo;:&rsquo; separator, they
must be escaped; note that this is a second level escaping.
</p>
<p>The following special options are also recognized:
</p><dl class="table">
<dt><samp class="option">f</samp></dt>
<dd><p>Specify the format name. Required if it cannot be guessed from the
output URL.
</p>
</dd>
<dt><samp class="option">bsfs[/<var class="var">spec</var>]</samp></dt>
<dd><p>Specify a list of bitstream filters to apply to the specified
output.
</p>
<p>It is possible to specify to which streams a given bitstream filter
applies, by appending a stream specifier to the option separated by
<code class="code">/</code>. <var class="var">spec</var> must be a stream specifier (see <a class="ref" href="#Format-stream-specifiers">Format stream specifiers</a>).
</p>
<p>If the stream specifier is not specified, the bitstream filters will be
applied to all streams in the output. This will cause that output operation
to fail if the output contains streams to which the bitstream filter cannot
be applied e.g. <code class="code">h264_mp4toannexb</code> being applied to an output containing an audio stream.
</p>
<p>Options for a bitstream filter must be specified in the form of <code class="code">opt=value</code>.
</p>
<p>Several bitstream filters can be specified, separated by &quot;,&quot;.
</p>
</dd>
<dt><samp class="option">use_fifo <var class="var">bool</var></samp></dt>
<dd><p>This allows to override tee muxer use_fifo option for individual slave muxer.
</p>
</dd>
<dt><samp class="option">fifo_options</samp></dt>
<dd><p>This allows to override tee muxer fifo_options for individual slave muxer.
See <a class="ref" href="#fifo">fifo</a>.
</p>
</dd>
<dt><samp class="option">select</samp></dt>
<dd><p>Select the streams that should be mapped to the slave output,
specified by a stream specifier. If not specified, this defaults to
all the mapped streams. This will cause that output operation to fail
if the output format does not accept all mapped streams.
</p>
<p>You may use multiple stream specifiers separated by commas (<code class="code">,</code>) e.g.: <code class="code">a:0,v</code>
</p>
</dd>
<dt><samp class="option">onfail</samp></dt>
<dd><p>Specify behaviour on output failure. This can be set to either <code class="code">abort</code> (which is
default) or <code class="code">ignore</code>. <code class="code">abort</code> will cause whole process to fail in case of failure
on this slave output. <code class="code">ignore</code> will ignore failure on this output, so other outputs
will continue without being affected.
</p></dd>
</dl>

</div>
<div class="subsection-level-extent" id="Examples-12">
<h4 class="subsection">4.33.2 Examples</h4>

<ul class="itemize mark-bullet">
<li>Encode something and both archive it in a WebM file and stream it
as MPEG-TS over UDP:
<div class="example">
<pre class="example-preformatted">ffmpeg -i ... -c:v libx264 -c:a mp2 -f tee -map 0:v -map 0:a
  &quot;archive-20121107.mkv|[f=mpegts]udp://10.0.1.255:1234/&quot;
</pre></div>

</li><li>As above, but continue streaming even if output to local file fails
(for example local drive fills up):
<div class="example">
<pre class="example-preformatted">ffmpeg -i ... -c:v libx264 -c:a mp2 -f tee -map 0:v -map 0:a
  &quot;[onfail=ignore]archive-20121107.mkv|[f=mpegts]udp://10.0.1.255:1234/&quot;
</pre></div>

</li><li>Use <code class="command">ffmpeg</code> to encode the input, and send the output
to three different destinations. The <code class="code">dump_extra</code> bitstream
filter is used to add extradata information to all the output video
keyframes packets, as requested by the MPEG-TS format. The select
option is applied to <samp class="file">out.aac</samp> in order to make it contain only
audio packets.
<div class="example">
<pre class="example-preformatted">ffmpeg -i ... -map 0 -flags +global_header -c:v libx264 -c:a aac
       -f tee &quot;[bsfs/v=dump_extra=freq=keyframe]out.ts|[movflags=+faststart]out.mp4|[select=a]out.aac&quot;
</pre></div>

</li><li>As above, but select only stream <code class="code">a:1</code> for the audio output. Note
that a second level escaping must be performed, as &quot;:&quot; is a special
character used to separate options.
<div class="example">
<pre class="example-preformatted">ffmpeg -i ... -map 0 -flags +global_header -c:v libx264 -c:a aac
       -f tee &quot;[bsfs/v=dump_extra=freq=keyframe]out.ts|[movflags=+faststart]out.mp4|[select=\'a:1\']out.aac&quot;
</pre></div>
</li></ul>

</div>
</div>
<div class="section-level-extent" id="webm_005fchunk">
<h3 class="section">4.34 webm_chunk</h3>

<p>WebM Live Chunk Muxer.
</p>
<p>This muxer writes out WebM headers and chunks as separate files which can be
consumed by clients that support WebM Live streams via DASH.
</p>
<ul class="mini-toc">
<li><a href="#Options-18" accesskey="1">Options</a></li>
<li><a href="#Example-2" accesskey="2">Example</a></li>
</ul>
<div class="subsection-level-extent" id="Options-18">
<h4 class="subsection">4.34.1 Options</h4>

<p>This muxer supports the following options:
</p>
<dl class="table">
<dt><samp class="option">chunk_start_index</samp></dt>
<dd><p>Index of the first chunk (defaults to 0).
</p>
</dd>
<dt><samp class="option">header</samp></dt>
<dd><p>Filename of the header where the initialization data will be written.
</p>
</dd>
<dt><samp class="option">audio_chunk_duration</samp></dt>
<dd><p>Duration of each audio chunk in milliseconds (defaults to 5000).
</p></dd>
</dl>

</div>
<div class="subsection-level-extent" id="Example-2">
<h4 class="subsection">4.34.2 Example</h4>
<div class="example">
<pre class="example-preformatted">ffmpeg -f v4l2 -i /dev/video0 \
       -f alsa -i hw:0 \
       -map 0:0 \
       -c:v libvpx-vp9 \
       -s 640x360 -keyint_min 30 -g 30 \
       -f webm_chunk \
       -header webm_live_video_360.hdr \
       -chunk_start_index 1 \
       webm_live_video_360_%d.chk \
       -map 1:0 \
       -c:a libvorbis \
       -b:a 128k \
       -f webm_chunk \
       -header webm_live_audio_128.hdr \
       -chunk_start_index 1 \
       -audio_chunk_duration 1000 \
       webm_live_audio_128_%d.chk
</pre></div>

</div>
</div>
<div class="section-level-extent" id="webm_005fdash_005fmanifest">
<h3 class="section">4.35 webm_dash_manifest</h3>

<p>WebM DASH Manifest muxer.
</p>
<p>This muxer implements the WebM DASH Manifest specification to generate the DASH
manifest XML. It also supports manifest generation for DASH live streams.
</p>
<p>For more information see:
</p>
<ul class="itemize mark-bullet">
<li>WebM DASH Specification: <a class="url" href="https://sites.google.com/a/webmproject.org/wiki/adaptive-streaming/webm-dash-specification">https://sites.google.com/a/webmproject.org/wiki/adaptive-streaming/webm-dash-specification</a>
</li><li>ISO DASH Specification: <a class="url" href="http://standards.iso.org/ittf/PubliclyAvailableStandards/c065274_ISO_IEC_23009-1_2014.zip">http://standards.iso.org/ittf/PubliclyAvailableStandards/c065274_ISO_IEC_23009-1_2014.zip</a>
</li></ul>

<ul class="mini-toc">
<li><a href="#Options-19" accesskey="1">Options</a></li>
<li><a href="#Example-3" accesskey="2">Example</a></li>
</ul>
<div class="subsection-level-extent" id="Options-19">
<h4 class="subsection">4.35.1 Options</h4>

<p>This muxer supports the following options:
</p>
<dl class="table">
<dt><samp class="option">adaptation_sets</samp></dt>
<dd><p>This option has the following syntax: &quot;id=x,streams=a,b,c id=y,streams=d,e&quot; where x and y are the
unique identifiers of the adaptation sets and a,b,c,d and e are the indices of the corresponding
audio and video streams. Any number of adaptation sets can be added using this option.
</p>
</dd>
<dt><samp class="option">live</samp></dt>
<dd><p>Set this to 1 to create a live stream DASH Manifest. Default: 0.
</p>
</dd>
<dt><samp class="option">chunk_start_index</samp></dt>
<dd><p>Start index of the first chunk. This will go in the &lsquo;<samp class="samp">startNumber</samp>&rsquo; attribute
of the &lsquo;<samp class="samp">SegmentTemplate</samp>&rsquo; element in the manifest. Default: 0.
</p>
</dd>
<dt><samp class="option">chunk_duration_ms</samp></dt>
<dd><p>Duration of each chunk in milliseconds. This will go in the &lsquo;<samp class="samp">duration</samp>&rsquo;
attribute of the &lsquo;<samp class="samp">SegmentTemplate</samp>&rsquo; element in the manifest. Default: 1000.
</p>
</dd>
<dt><samp class="option">utc_timing_url</samp></dt>
<dd><p>URL of the page that will return the UTC timestamp in ISO format. This will go
in the &lsquo;<samp class="samp">value</samp>&rsquo; attribute of the &lsquo;<samp class="samp">UTCTiming</samp>&rsquo; element in the manifest.
Default: None.
</p>
</dd>
<dt><samp class="option">time_shift_buffer_depth</samp></dt>
<dd><p>Smallest time (in seconds) shifting buffer for which any Representation is
guaranteed to be available. This will go in the &lsquo;<samp class="samp">timeShiftBufferDepth</samp>&rsquo;
attribute of the &lsquo;<samp class="samp">MPD</samp>&rsquo; element. Default: 60.
</p>
</dd>
<dt><samp class="option">minimum_update_period</samp></dt>
<dd><p>Minimum update period (in seconds) of the manifest. This will go in the
&lsquo;<samp class="samp">minimumUpdatePeriod</samp>&rsquo; attribute of the &lsquo;<samp class="samp">MPD</samp>&rsquo; element. Default: 0.
</p>
</dd>
</dl>

</div>
<div class="subsection-level-extent" id="Example-3">
<h4 class="subsection">4.35.2 Example</h4>
<div class="example">
<pre class="example-preformatted">ffmpeg -f webm_dash_manifest -i video1.webm \
       -f webm_dash_manifest -i video2.webm \
       -f webm_dash_manifest -i audio1.webm \
       -f webm_dash_manifest -i audio2.webm \
       -map 0 -map 1 -map 2 -map 3 \
       -c copy \
       -f webm_dash_manifest \
       -adaptation_sets &quot;id=0,streams=0,1 id=1,streams=2,3&quot; \
       manifest.xml
</pre></div>

</div>
</div>
</div>
<div class="chapter-level-extent" id="Metadata-1">
<h2 class="chapter">5 Metadata</h2>

<p>FFmpeg is able to dump metadata from media files into a simple UTF-8-encoded
INI-like text file and then load it back using the metadata muxer/demuxer.
</p>
<p>The file format is as follows:
</p><ol class="enumerate">
<li> A file consists of a header and a number of metadata tags divided into sections,
each on its own line.

</li><li> The header is a &lsquo;<samp class="samp">;FFMETADATA</samp>&rsquo; string, followed by a version number (now 1).

</li><li> Metadata tags are of the form &lsquo;<samp class="samp">key=value</samp>&rsquo;

</li><li> Immediately after header follows global metadata

</li><li> After global metadata there may be sections with per-stream/per-chapter
metadata.

</li><li> A section starts with the section name in uppercase (i.e. STREAM or CHAPTER) in
brackets (&lsquo;<samp class="samp">[</samp>&rsquo;, &lsquo;<samp class="samp">]</samp>&rsquo;) and ends with next section or end of file.

</li><li> At the beginning of a chapter section there may be an optional timebase to be
used for start/end values. It must be in form
&lsquo;<samp class="samp">TIMEBASE=<var class="var">num</var>/<var class="var">den</var></samp>&rsquo;, where <var class="var">num</var> and <var class="var">den</var> are
integers. If the timebase is missing then start/end times are assumed to
be in nanoseconds.

<p>Next a chapter section must contain chapter start and end times in form
&lsquo;<samp class="samp">START=<var class="var">num</var></samp>&rsquo;, &lsquo;<samp class="samp">END=<var class="var">num</var></samp>&rsquo;, where <var class="var">num</var> is a positive
integer.
</p>
</li><li> Empty lines and lines starting with &lsquo;<samp class="samp">;</samp>&rsquo; or &lsquo;<samp class="samp">#</samp>&r