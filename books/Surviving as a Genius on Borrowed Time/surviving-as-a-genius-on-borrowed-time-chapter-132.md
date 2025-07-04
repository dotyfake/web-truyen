<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Created by , GNU Texinfo 7.0.1 -->
  <head>
    <meta charset="utf-8">
    <title>
      ffplay Documentation
    </title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="style.min.css">
  </head>
  <body>
    <div class="container">
      <h1>
      ffplay Documentation
      </h1>


<div class="top-level-extent" id="SEC_Top">

<div class="element-contents" id="SEC_Contents">
<h2 class="contents-heading">Table of Contents</h2>

<div class="contents">

<ul class="toc-numbered-mark">
  <li><a id="toc-Synopsis" href="#Synopsis">1 Synopsis</a></li>
  <li><a id="toc-Description" href="#Description">2 Description</a></li>
  <li><a id="toc-Options" href="#Options">3 Options</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Stream-specifiers-1" href="#Stream-specifiers-1">3.1 Stream specifiers</a></li>
    <li><a id="toc-Generic-options" href="#Generic-options">3.2 Generic options</a></li>
    <li><a id="toc-AVOptions" href="#AVOptions">3.3 AVOptions</a></li>
    <li><a id="toc-Main-options" href="#Main-options">3.4 Main options</a></li>
    <li><a id="toc-Advanced-options" href="#Advanced-options">3.5 Advanced options</a></li>
    <li><a id="toc-While-playing" href="#While-playing">3.6 While playing</a></li>
  </ul></li>
  <li><a id="toc-See-Also" href="#See-Also">4 See Also</a></li>
  <li><a id="toc-Authors" href="#Authors">5 Authors</a></li>
</ul>
</div>
</div>

<ul class="mini-toc">
<li><a href="#Synopsis" accesskey="1">Synopsis</a></li>
<li><a href="#Description" accesskey="2">Description</a></li>
<li><a href="#Options" accesskey="3">Options</a></li>
<li><a href="#See-Also" accesskey="4">See Also</a></li>
<li><a href="#Authors" accesskey="5">Authors</a></li>
</ul>
<div class="chapter-level-extent" id="Synopsis">
<h2 class="chapter">1 Synopsis</h2>

<p>ffplay [<var class="var">options</var>] [<samp class="file">input_url</samp>]
</p>
</div>
<div class="chapter-level-extent" id="Description">
<h2 class="chapter">2 Description</h2>

<p>FFplay is a very simple and portable media player using the FFmpeg
libraries and the SDL library. It is mostly used as a testbed for the
various FFmpeg APIs.
</p>
</div>
<div class="chapter-level-extent" id="Options">
<h2 class="chapter">3 Options</h2>

<p>All the numerical options, if not specified otherwise, accept a string
representing a number as input, which may be followed by one of the SI
unit prefixes, for example: &rsquo;K&rsquo;, &rsquo;M&rsquo;, or &rsquo;G&rsquo;.
</p>
<p>If &rsquo;i&rsquo; is appended to the SI unit prefix, the complete prefix will be
interpreted as a unit prefix for binary multiples, which are based on
powers of 1024 instead of powers of 1000. Appending &rsquo;B&rsquo; to the SI unit
prefix multiplies the value by 8. This allows using, for example:
&rsquo;KB&rsquo;, &rsquo;MiB&rsquo;, &rsquo;G&rsquo; and &rsquo;B&rsquo; as number suffixes.
</p>
<p>Options which do not take arguments are boolean options, and set the
corresponding value to true. They can be set to false by prefixing
the option name with &quot;no&quot;. For example using &quot;-nofoo&quot;
will set the boolean option with name &quot;foo&quot; to false.
</p>
<a class="anchor" id="Stream-specifiers"></a><ul class="mini-toc">
<li><a href="#Stream-specifiers-1" accesskey="1">Stream specifiers</a></li>
<li><a href="#Generic-options" accesskey="2">Generic options</a></li>
<li><a href="#AVOptions" accesskey="3">AVOptions</a></li>
<li><a href="#Main-options" accesskey="4">Main options</a></li>
<li><a href="#Advanced-options" accesskey="5">Advanced options</a></li>
<li><a href="#While-playing" accesskey="6">While playing</a></li>
</ul>
<div class="section-level-extent" id="Stream-specifiers-1">
<h3 class="section">3.1 Stream specifiers</h3>
<p>Some options are applied per-stream, e.g. bitrate or codec. Stream specifiers
are used to precisely specify which stream(s) a given option belongs to.
</p>
<p>A stream specifier is a string generally appended to the option name and
separated from it by a colon. E.g. <code class="code">-codec:a:1 ac3</code> contains the
<code class="code">a:1</code> stream specifier, which matches the second audio stream. Therefore, it
would select the ac3 codec for the second audio stream.
</p>
<p>A stream specifier can match several streams, so that the option is applied to all
of them. E.g. the stream specifier in <code class="code">-b:a 128k</code> matches all audio
streams.
</p>
<p>An empty stream specifier matches all streams. For example, <code class="code">-codec copy</code>
or <code class="code">-codec: copy</code> would copy all the streams without reencoding.
</p>
<p>Possible forms of stream specifiers are:
</p><dl class="table">
<dt><samp class="option"><var class="var">stream_index</var></samp></dt>
<dd><p>Matches the stream with this index. E.g. <code class="code">-threads:1 4</code> would set the
thread count for the second stream to 4. If <var class="var">stream_index</var> is used as an
additional stream specifier (see below), then it selects stream number
<var class="var">stream_index</var> from the matching streams. Stream numbering is based on the
order of the streams as detected by libavformat except when a program ID is
also specified. In this case it is based on the ordering of the streams in the
program.
</p></dd>
<dt><samp class="option"><var class="var">stream_type</var>[:<var class="var">additional_stream_specifier</var>]</samp></dt>
<dd><p><var class="var">stream_type</var> is one of following: &rsquo;v&rsquo; or &rsquo;V&rsquo; for video, &rsquo;a&rsquo; for audio, &rsquo;s&rsquo;
for subtitle, &rsquo;d&rsquo; for data, and &rsquo;t&rsquo; for attachments. &rsquo;v&rsquo; matches all video
streams, &rsquo;V&rsquo; only matches video streams which are not attached pictures, video
thumbnails or cover arts. If <var class="var">additional_stream_specifier</var> is used, then
it matches streams which both have this type and match the
<var class="var">additional_stream_specifier</var>. Otherwise, it matches all streams of the
specified type.
</p></dd>
<dt><samp class="option">p:<var class="var">program_id</var>[:<var class="var">additional_stream_specifier</var>]</samp></dt>
<dd><p>Matches streams which are in the program with the id <var class="var">program_id</var>. If
<var class="var">additional_stream_specifier</var> is used, then it matches streams which both
are part of the program and match the <var class="var">additional_stream_specifier</var>.
</p>
</dd>
<dt><samp class="option">#<var class="var">stream_id</var> or i:<var class="var">stream_id</var></samp></dt>
<dd><p>Match the stream by stream id (e.g. PID in MPEG-TS container).
</p></dd>
<dt><samp class="option">m:<var class="var">key</var>[:<var class="var">value</var>]</samp></dt>
<dd><p>Matches streams with the metadata tag <var class="var">key</var> having the specified value. If
<var class="var">value</var> is not given, matches streams that contain the given tag with any
value.
</p></dd>
<dt><samp class="option">u</samp></dt>
<dd><p>Matches streams with usable configuration, the codec must be defined and the
essential information such as video dimension or audio sample rate must be present.
</p>
<p>Note that in <code class="command">ffmpeg</code>, matching by metadata will only work properly for
input files.
</p></dd>
</dl>

</div>
<div class="section-level-extent" id="Generic-options">
<h3 class="section">3.2 Generic options</h3>

<p>These options are shared amongst the ff* tools.
</p>
<dl class="table">
<dt><samp class="option">-L</samp></dt>
<dd><p>Show license.
</p>
</dd>
<dt><samp class="option">-h, -?, -help, --help [<var class="var">arg</var>]</samp></dt>
<dd><p>Show help. An optional parameter may be specified to print help about a specific
item. If no argument is specified, only basic (non advanced) tool
options are shown.
</p>
<p>Possible values of <var class="var">arg</var> are:
</p><dl class="table">
<dt><samp class="option">long</samp></dt>
<dd><p>Print advanced tool options in addition to the basic tool options.
</p>
</dd>
<dt><samp class="option">full</samp></dt>
<dd><p>Print complete list of options, including shared and private options
for encoders, decoders, demuxers, muxers, filters, etc.
</p>
</dd>
<dt><samp class="option">decoder=<var class="var">decoder_name</var></samp></dt>
<dd><p>Print detailed information about the decoder named <var class="var">decoder_name</var>. Use the
<samp class="option">-decoders</samp> option to get a list of all decoders.
</p>
</dd>
<dt><samp class="option">encoder=<var class="var">encoder_name</var></samp></dt>
<dd><p>Print detailed information about the encoder named <var class="var">encoder_name</var>. Use the
<samp class="option">-encoders</samp> option to get a list of all encoders.
</p>
</dd>
<dt><samp class="option">demuxer=<var class="var">demuxer_name</var></samp></dt>
<dd><p>Print detailed information about the demuxer named <var class="var">demuxer_name</var>. Use the
<samp class="option">-formats</samp> option to get a list of all demuxers and muxers.
</p>
</dd>
<dt><samp class="option">muxer=<var class="var">muxer_name</var></samp></dt>
<dd><p>Print detailed information about the muxer named <var class="var">muxer_name</var>. Use the
<samp class="option">-formats</samp> option to get a list of all muxers and demuxers.
</p>
</dd>
<dt><samp class="option">filter=<var class="var">filter_name</var></samp></dt>
<dd><p>Print detailed information about the filter named <var class="var">filter_name</var>. Use the
<samp class="option">-filters</samp> option to get a list of all filters.
</p>
</dd>
<dt><samp class="option">bsf=<var class="var">bitstream_filter_name</var></samp></dt>
<dd><p>Print detailed information about the bitstream filter named <var class="var">bitstream_filter_name</var>.
Use the <samp class="option">-bsfs</samp> option to get a list of all bitstream filters.
</p>
</dd>
<dt><samp class="option">protocol=<var class="var">protocol_name</var></samp></dt>
<dd><p>Print detailed information about the protocol named <var class="var">protocol_name</var>.
Use the <samp class="option">-protocols</samp> option to get a list of all protocols.
</p></dd>
</dl>

</dd>
<dt><samp class="option">-version</samp></dt>
<dd><p>Show version.
</p>
</dd>
<dt><samp class="option">-buildconf</samp></dt>
<dd><p>Show the build configuration, one option per line.
</p>
</dd>
<dt><samp class="option">-formats</samp></dt>
<dd><p>Show available formats (including devices).
</p>
</dd>
<dt><samp class="option">-demuxers</samp></dt>
<dd><p>Show available demuxers.
</p>
</dd>
<dt><samp class="option">-muxers</samp></dt>
<dd><p>Show available muxers.
</p>
</dd>
<dt><samp class="option">-devices</samp></dt>
<dd><p>Show available devices.
</p>
</dd>
<dt><samp class="option">-codecs</samp></dt>
<dd><p>Show all codecs known to libavcodec.
</p>
<p>Note that the term &rsquo;codec&rsquo; is used throughout this documentation as a shortcut
for what is more correctly called a media bitstream format.
</p>
</dd>
<dt><samp class="option">-decoders</samp></dt>
<dd><p>Show available decoders.
</p>
</dd>
<dt><samp class="option">-encoders</samp></dt>
<dd><p>Show all available encoders.
</p>
</dd>
<dt><samp class="option">-bsfs</samp></dt>
<dd><p>Show available bitstream filters.
</p>
</dd>
<dt><samp class="option">-protocols</samp></dt>
<dd><p>Show available protocols.
</p>
</dd>
<dt><samp class="option">-filters</samp></dt>
<dd><p>Show available libavfilter filters.
</p>
</dd>
<dt><samp class="option">-pix_fmts</samp></dt>
<dd><p>Show available pixel formats.
</p>
</dd>
<dt><samp class="option">-sample_fmts</samp></dt>
<dd><p>Show available sample formats.
</p>
</dd>
<dt><samp class="option">-layouts</samp></dt>
<dd><p>Show channel names and standard channel layouts.
</p>
</dd>
<dt><samp class="option">-dispositions</samp></dt>
<dd><p>Show stream dispositions.
</p>
</dd>
<dt><samp class="option">-colors</samp></dt>
<dd><p>Show recognized color names.
</p>
</dd>
<dt><samp class="option">-sources <var class="var">device</var>[,<var class="var">opt1</var>=<var class="var">val1</var>[,<var class="var">opt2</var>=<var class="var">val2</var>]...]</samp></dt>
<dd><p>Show autodetected sources of the input device.
Some devices may provide system-dependent source names that cannot be autodetected.
The returned list cannot be assumed to be always complete.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -sources pulse,server=192.168.0.4
</pre></div>

</dd>
<dt><samp class="option">-sinks <var class="var">device</var>[,<var class="var">opt1</var>=<var class="var">val1</var>[,<var class="var">opt2</var>=<var class="var">val2</var>]...]</samp></dt>
<dd><p>Show autodetected sinks of the output device.
Some devices may provide system-dependent sink names that cannot be autodetected.
The returned list cannot be assumed to be always complete.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -sinks pulse,server=192.168.0.4
</pre></div>

</dd>
<dt><samp class="option">-loglevel [<var class="var">flags</var>+]<var class="var">loglevel</var> | -v [<var class="var">flags</var>+]<var class="var">loglevel</var></samp></dt>
<dd><p>Set logging level and flags used by the library.
</p>
<p>The optional <var class="var">flags</var> prefix can consist of the following values:
</p><dl class="table">
<dt>&lsquo;<samp class="samp">repeat</samp>&rsquo;</dt>
<dd><p>Indicates that repeated log output should not be compressed to the first line
and the &quot;Last message repeated n times&quot; line will be omitted.
</p></dd>
<dt>&lsquo;<samp class="samp">level</samp>&rsquo;</dt>
<dd><p>Indicates that log output should add a <code class="code">[level]</code> prefix to each message
line. This can be used as an alternative to log coloring, e.g. when dumping the
log to file.
</p></dd>
</dl>
<p>Flags can also be used alone by adding a &rsquo;+&rsquo;/&rsquo;-&rsquo; prefix to set/reset a single
flag without affecting other <var class="var">flags</var> or changing <var class="var">loglevel</var>. When
setting both <var class="var">flags</var> and <var class="var">loglevel</var>, a &rsquo;+&rsquo; separator is expected
between the last <var class="var">flags</var> value and before <var class="var">loglevel</var>.
</p>
<p><var class="var">loglevel</var> is a string or a number containing one of the following values:
</p><dl class="table">
<dt>&lsquo;<samp class="samp">quiet, -8</samp>&rsquo;</dt>
<dd><p>Show nothing at all; be silent.
</p></dd>
<dt>&lsquo;<samp class="samp">panic, 0</samp>&rsquo;</dt>
<dd><p>Only show fatal errors which could lead the process to crash, such as
an assertion failure. This is not currently used for anything.
</p></dd>
<dt>&lsquo;<samp class="samp">fatal, 8</samp>&rsquo;</dt>
<dd><p>Only show fatal errors. These are errors after which the process absolutely
cannot continue.
</p></dd>
<dt>&lsquo;<samp class="samp">error, 16</samp>&rsquo;</dt>
<dd><p>Show all errors, including ones which can be recovered from.
</p></dd>
<dt>&lsquo;<samp class="samp">warning, 24</samp>&rsquo;</dt>
<dd><p>Show all warnings and errors. Any message related to possibly
incorrect or unexpected events will be shown.
</p></dd>
<dt>&lsquo;<samp class="samp">info, 32</samp>&rsquo;</dt>
<dd><p>Show informative messages during processing. This is in addition to
warnings and errors. This is the default value.
</p></dd>
<dt>&lsquo;<samp class="samp">verbose, 40</samp>&rsquo;</dt>
<dd><p>Same as <code class="code">info</code>, except more verbose.
</p></dd>
<dt>&lsquo;<samp class="samp">debug, 48</samp>&rsquo;</dt>
<dd><p>Show everything, including debugging information.
</p></dd>
<dt>&lsquo;<samp class="samp">trace, 56</samp>&rsquo;</dt>
</dl>

<p>For example to enable repeated log output, add the <code class="code">level</code> prefix, and set
<var class="var">loglevel</var> to <code class="code">verbose</code>:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -loglevel repeat+level+verbose -i input output
</pre></div>
<p>Another example that enables repeated log output without affecting current
state of <code class="code">level</code> prefix flag or <var class="var">loglevel</var>:
</p><div class="example">
<pre class="example-preformatted">ffmpeg [...] -loglevel +repeat
</pre></div>

<p>By default the program logs to stderr. If coloring is supported by the
terminal, colors are used to mark errors and warnings. Log coloring
can be disabled setting the environment variable
<code class="env">AV_LOG_FORCE_NOCOLOR</code>, or can be forced setting
the environment variable <code class="env">AV_LOG_FORCE_COLOR</code>.
</p>
</dd>
<dt><samp class="option">-report</samp></dt>
<dd><p>Dump full command line and log output to a file named
<code class="code"><var class="var">program</var>-<var class="var">YYYYMMDD</var>-<var class="var">HHMMSS</var>.log</code> in the current
directory.
This file can be useful for bug reports.
It also implies <code class="code">-loglevel debug</code>.
</p>
<p>Setting the environment variable <code class="env">FFREPORT</code> to any value has the
same effect. If the value is a &rsquo;:&rsquo;-separated key=value sequence, these
options will affect the report; option values must be escaped if they
contain special characters or the options delimiter &rsquo;:&rsquo; (see the
&ldquo;Quoting and escaping&rdquo; section in the ffmpeg-utils manual).
</p>
<p>The following options are recognized:
</p><dl class="table">
<dt><samp class="option">file</samp></dt>
<dd><p>set the file name to use for the report; <code class="code">%p</code> is expanded to the name
of the program, <code class="code">%t</code> is expanded to a timestamp, <code class="code">%%</code> is expanded
to a plain <code class="code">%</code>
</p></dd>
<dt><samp class="option">level</samp></dt>
<dd><p>set the log verbosity level using a numerical value (see <code class="code">-loglevel</code>).
</p></dd>
</dl>

<p>For example, to output a report to a file named <samp class="file">ffreport.log</samp>
using a log level of <code class="code">32</code> (alias for log level <code class="code">info</code>):
</p>
<div class="example">
<pre class="example-preformatted">FFREPORT=file=ffreport.log:level=32 ffmpeg -i input output
</pre></div>

<p>Errors in parsing the environment variable are not fatal, and will not
appear in the report.
</p>
</dd>
<dt><samp class="option">-hide_banner</samp></dt>
<dd><p>Suppress printing banner.
</p>
<p>All FFmpeg tools will normally show a copyright notice, build options
and library versions. This option can be used to suppress printing
this information.
</p>
</dd>
<dt><samp class="option">-cpuflags flags (<em class="emph">global</em>)</samp></dt>
<dd><p>Allows setting and clearing cpu flags. This option is intended
for testing. Do not use it unless you know what you&rsquo;re doing.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -cpuflags -sse+mmx ...
ffmpeg -cpuflags mmx ...
ffmpeg -cpuflags 0 ...
</pre></div>
<p>Possible flags for this option are:
</p><dl class="table">
<dt>&lsquo;<samp class="samp">x86</samp>&rsquo;</dt>
<dd><dl class="table">
<dt>&lsquo;<samp class="samp">mmx</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">mmxext</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse2</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse2slow</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse3</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse3slow</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">ssse3</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">atom</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse4.1</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">sse4.2</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">avx</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">avx2</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">xop</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">fma3</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">fma4</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">3dnow</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">3dnowext</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bmi1</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">bmi2</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">cmov</samp>&rsquo;</dt>
</dl>
</dd>
<dt>&lsquo;<samp class="samp">ARM</samp>&rsquo;</dt>
<dd><dl class="table">
<dt>&lsquo;<samp class="samp">armv5te</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">armv6</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">armv6t2</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">vfp</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">vfpv3</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">neon</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">setend</samp>&rsquo;</dt>
</dl>
</dd>
<dt>&lsquo;<samp class="samp">AArch64</samp>&rsquo;</dt>
<dd><dl class="table">
<dt>&lsquo;<samp class="samp">armv8</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">vfp</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">neon</samp>&rsquo;</dt>
</dl>
</dd>
<dt>&lsquo;<samp class="samp">PowerPC</samp>&rsquo;</dt>
<dd><dl class="table">
<dt>&lsquo;<samp class="samp">altivec</samp>&rsquo;</dt>
</dl>
</dd>
<dt>&lsquo;<samp class="samp">Specific Processors</samp>&rsquo;</dt>
<dd><dl class="table">
<dt>&lsquo;<samp class="samp">pentium2</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">pentium3</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">pentium4</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">k6</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">k62</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">athlon</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">athlonxp</samp>&rsquo;</dt>
<dt>&lsquo;<samp class="samp">k8</samp>&rsquo;</dt>
</dl>
</dd>
</dl>

</dd>
<dt><samp class="option">-cpucount <var class="var">count</var> (<em class="emph">global</em>)</samp></dt>
<dd><p>Override detection of CPU count. This option is intended
for testing. Do not use it unless you know what you&rsquo;re doing.
</p><div class="example">
<pre class="example-preformatted">ffmpeg -cpucount 2
</pre></div>

</dd>
<dt><samp class="option">-max_alloc <var class="var">bytes</var></samp></dt>
<dd><p>Set the maximum size limit for allocating a block on the heap by ffmpeg&rsquo;s
family of malloc functions. Exercise <strong class="strong">extreme caution</strong> when using
this option. Don&rsquo;t use if you do not understand the full consequence of doing so.
Default is INT_MAX.
</p></dd>
</dl>

</div>
<div class="section-level-extent" id="AVOptions">
<h3 class="section">3.3 AVOptions</h3>

<p>These options are provided directly by the libavformat, libavdevice and
libavcodec libraries. To see the list of available AVOptions, use the
<samp class="option">-help</samp> option. They are separated into two categories:
</p><dl class="table">
<dt><samp class="option">generic</samp></dt>
<dd><p>These options can be set for any container, codec or device. Generic options
are listed under AVFormatContext options for containers/devices and under
AVCodecContext options for codecs.
</p></dd>
<dt><samp class="option">private</samp></dt>
<dd><p>These options are specific to the given container, device or codec. Private
options are listed under their corresponding containers/devices/codecs.
</p></dd>
</dl>

<p>For example to write an ID3v2.3 header instead of a default ID3v2.4 to
an MP3 file, use the <samp class="option">id3v2_version</samp> private option of the MP3
muxer:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i input.flac -id3v2_version 3 out.mp3
</pre></div>

<p>All codec AVOptions are per-stream, and thus a stream specifier
should be attached to them:
</p><div class="example">
<pre class="example-preformatted">ffmpeg -i multichannel.mxf -map 0:v:0 -map 0:a:0 -map 0:a:0 -c:a:0 ac3 -b:a:0 640k -ac:a:1 2 -c:a:1 aac -b:2 128k out.mp4
</pre></div>

<p>In the above example, a multichannel audio stream is mapped twice for output.
The first instance is encoded with codec ac3 and bitrate 640k.
The second instance is downmixed to 2 channels and encoded with codec aac. A bitrate of 128k is specified for it using
absolute index of the output stream.
</p>
<p>Note: the <samp class="option">-nooption</samp> syntax cannot be used for boolean
AVOptions, use <samp class="option">-option 0</samp>/<samp class="option">-option 1</samp>.
</p>
<p>Note: the old undocumented way of specifying per-stream AVOptions by
prepending v/a/s to the options name is now obsolete and will be
removed soon.
</p>
</div>
<div class="section-level-extent" id="Main-options">
<h3 class="section">3.4 Main options</h3>

<dl class="table">
<dt><samp class="option">-x <var class="var">width</var></samp></dt>
<dd><p>Force displayed width.
</p></dd>
<dt><samp class="option">-y <var class="var">height</var></samp></dt>
<dd><p>Force displayed height.
</p></dd>
<dt><samp class="option">-fs</samp></dt>
<dd><p>Start in fullscreen mode.
</p></dd>
<dt><samp class="option">-an</samp></dt>
<dd><p>Disable audio.
</p></dd>
<dt><samp class="option">-vn</samp></dt>
<dd><p>Disable video.
</p></dd>
<dt><samp class="option">-sn</samp></dt>
<dd><p>Disable subtitles.
</p></dd>
<dt><samp class="option">-ss <var class="var">pos</var></samp></dt>
<dd><p>Seek to <var class="var">pos</var>. Note that in most formats it is not possible to seek
exactly, so <code class="command">ffplay</code> will seek to the nearest seek point to
<var class="var">pos</var>.
</p>
<p><var class="var">pos</var> must be a time duration specification,
see <a data-manual="ffmpeg-utils" href="ffmpeg-utils.html#time-duration-syntax">(ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual</a>.
</p></dd>
<dt><samp class="option">-t <var class="var">duration</var></samp></dt>
<dd><p>Play <var class="var">duration</var> seconds of audio/video.
</p>
<p><var class="var">duration</var> must be a time duration specification,
see <a data-manual="ffmpeg-utils" href="ffmpeg-utils.html#time-duration-syntax">(ffmpeg-utils)the Time duration section in the ffmpeg-utils(1) manual</a>.
</p></dd>
<dt><samp class="option">-bytes</samp></dt>
<dd><p>Seek by bytes.
</p></dd>
<dt><samp class="option">-seek_interval</samp></dt>
<dd><p>Set custom interval, in seconds, for seeking using left/right keys. Default is 10 seconds.
</p></dd>
<dt><samp class="option">-nodisp</samp></dt>
<dd><p>Disable graphical display.
</p></dd>
<dt><samp class="option">-noborder</samp></dt>
<dd><p>Borderless window.
</p></dd>
<dt><samp class="option">-alwaysontop</samp></dt>
<dd><p>Window always on top. Available on: X11 with SDL &gt;= 2.0.5, Windows SDL &gt;= 2.0.6.
</p></dd>
<dt><samp class="option">-volume</samp></dt>
<dd><p>Set the startup volume. 0 means silence, 100 means no volume reduction or
amplification. Negative values are treated as 0, values above 100 are treated
as 100.
</p></dd>
<dt><samp class="option">-f <var class="var">fmt</var></samp></dt>
<dd><p>Force format.
</p></dd>
<dt><samp class="option">-window_title <var class="var">title</var></samp></dt>
<dd><p>Set window title (default is the input filename).
</p></dd>
<dt><samp class="option">-left <var class="var">title</var></samp></dt>
<dd><p>Set the x position for the left of the window (default is a centered window).
</p></dd>
<dt><samp class="option">-top <var clas