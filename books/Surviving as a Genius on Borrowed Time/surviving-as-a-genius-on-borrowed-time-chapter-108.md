<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Created by , GNU Texinfo 7.0.1 -->
  <head>
    <meta charset="utf-8">
    <title>
      Platform Specific Information
    </title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="style.min.css">
  </head>
  <body>
    <div class="container">
      <h1>
      Platform Specific Information
      </h1>


<div class="top-level-extent" id="SEC_Top">

<div class="element-contents" id="SEC_Contents">
<h2 class="contents-heading">Table of Contents</h2>

<div class="contents">

<ul class="toc-numbered-mark">
  <li><a id="toc-Unix_002dlike" href="#Unix_002dlike">1 Unix-like</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Advanced-linking-configuration" href="#Advanced-linking-configuration">1.1 Advanced linking configuration</a></li>
    <li><a id="toc-BSD" href="#BSD">1.2 BSD</a></li>
    <li><a id="toc-_0028Open_0029Solaris" href="#g_t_0028Open_0029Solaris">1.3 (Open)Solaris</a></li>
    <li><a id="toc-Darwin-_0028Mac-OS-X_002c-iPhone_0029" href="#Darwin-_0028Mac-OS-X_002c-iPhone_0029">1.4 Darwin (Mac OS X, iPhone)</a></li>
  </ul></li>
  <li><a id="toc-DOS" href="#DOS">2 DOS</a></li>
  <li><a id="toc-OS_002f2" href="#OS_002f2">3 OS/2</a></li>
  <li><a id="toc-Windows" href="#Windows">4 Windows</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Native-Windows-compilation-using-MinGW-or-MinGW_002dw64" href="#Native-Windows-compilation-using-MinGW-or-MinGW_002dw64">4.1 Native Windows compilation using MinGW or MinGW-w64</a>
    <ul class="toc-numbered-mark">
      <li><a id="toc-Native-Windows-compilation-using-MSYS2" href="#Native-Windows-compilation-using-MSYS2">4.1.1 Native Windows compilation using MSYS2</a></li>
    </ul></li>
    <li><a id="toc-Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows" href="#Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows">4.2 Microsoft Visual C++ or Intel C++ Compiler for Windows</a>
    <ul class="toc-numbered-mark">
      <li><a id="toc-Linking-to-FFmpeg-with-Microsoft-Visual-C_002b_002b" href="#Linking-to-FFmpeg-with-Microsoft-Visual-C_002b_002b">4.2.1 Linking to FFmpeg with Microsoft Visual C++</a></li>
    </ul></li>
    <li><a id="toc-Cross-compilation-for-Windows-with-Linux-1" href="#Cross-compilation-for-Windows-with-Linux-1">4.3 Cross compilation for Windows with Linux</a></li>
    <li><a id="toc-Compilation-under-Cygwin" href="#Compilation-under-Cygwin">4.4 Compilation under Cygwin</a></li>
    <li><a id="toc-Crosscompilation-for-Windows-under-Cygwin" href="#Crosscompilation-for-Windows-under-Cygwin">4.5 Crosscompilation for Windows under Cygwin</a></li>
  </ul></li>
</ul>
</div>
</div>

<ul class="mini-toc">
<li><a href="#Unix_002dlike" accesskey="1">Unix-like</a></li>
<li><a href="#DOS" accesskey="2">DOS</a></li>
<li><a href="#OS_002f2" accesskey="3">OS/2</a></li>
<li><a href="#Windows" accesskey="4">Windows</a></li>
</ul>
<div class="chapter-level-extent" id="Unix_002dlike">
<h2 class="chapter">1 Unix-like</h2>

<p>Some parts of FFmpeg cannot be built with version 2.15 of the GNU
assembler which is still provided by a few AMD64 distributions. To
make sure your compiler really uses the required version of gas
after a binutils upgrade, run:
</p>
<div class="example">
<pre class="example-preformatted">$(gcc -print-prog-name=as) --version
</pre></div>

<p>If not, then you should install a different compiler that has no
hard-coded path to gas. In the worst case pass <code class="code">--disable-asm</code>
to configure.
</p>
<ul class="mini-toc">
<li><a href="#Advanced-linking-configuration" accesskey="1">Advanced linking configuration</a></li>
<li><a href="#BSD" accesskey="2">BSD</a></li>
<li><a href="#g_t_0028Open_0029Solaris" accesskey="3">(Open)Solaris</a></li>
<li><a href="#Darwin-_0028Mac-OS-X_002c-iPhone_0029" accesskey="4">Darwin (Mac OS X, iPhone)</a></li>
</ul>
<div class="section-level-extent" id="Advanced-linking-configuration">
<h3 class="section">1.1 Advanced linking configuration</h3>

<p>If you compiled FFmpeg libraries statically and you want to use them to
build your own shared library, you may need to force PIC support (with
<code class="code">--enable-pic</code> during FFmpeg configure) and add the following option
to your project LDFLAGS:
</p>
<div class="example">
<pre class="example-preformatted">-Wl,-Bsymbolic
</pre></div>

<p>If your target platform requires position independent binaries, you should
pass the correct linking flag (e.g. <code class="code">-pie</code>) to <code class="code">--extra-ldexeflags</code>.
</p>
</div>
<div class="section-level-extent" id="BSD">
<h3 class="section">1.2 BSD</h3>

<p>BSD make will not build FFmpeg, you need to install and use GNU Make
(<code class="command">gmake</code>).
</p>
</div>
<div class="section-level-extent" id="g_t_0028Open_0029Solaris">
<h3 class="section">1.3 (Open)Solaris</h3>

<p>GNU Make is required to build FFmpeg, so you have to invoke (<code class="command">gmake</code>),
standard Solaris Make will not work. When building with a non-c99 front-end
(gcc, generic suncc) add either <code class="code">--extra-libs=/usr/lib/values-xpg6.o</code>
or <code class="code">--extra-libs=/usr/lib/64/values-xpg6.o</code> to the configure options
since the libc is not c99-compliant by default. The probes performed by
configure may raise an exception leading to the death of configure itself
due to a bug in the system shell. Simply invoke a different shell such as
bash directly to work around this:
</p>
<div class="example">
<pre class="example-preformatted">bash ./configure
</pre></div>

<a class="anchor" id="Darwin"></a></div>
<div class="section-level-extent" id="Darwin-_0028Mac-OS-X_002c-iPhone_0029">
<h3 class="section">1.4 Darwin (Mac OS X, iPhone)</h3>

<p>The toolchain provided with Xcode is sufficient to build the basic
unaccelerated code.
</p>
<p>Mac OS X on PowerPC or ARM (iPhone) requires a preprocessor from
<a class="url" href="https://github.com/FFmpeg/gas-preprocessor">https://github.com/FFmpeg/gas-preprocessor</a> or
<a class="url" href="https://github.com/yuvi/gas-preprocessor">https://github.com/yuvi/gas-preprocessor</a>(currently outdated) to build the optimized
assembly functions. Put the Perl script somewhere
in your PATH, FFmpeg&rsquo;s configure will pick it up automatically.
</p>
<p>Mac OS X on amd64 and x86 requires <code class="command">nasm</code> to build most of the
optimized assembly functions. <a class="uref" href="http://www.finkproject.org/">Fink</a>,
<a class="uref" href="https://wiki.gentoo.org/wiki/Project:Prefix">Gentoo Prefix</a>,
<a class="uref" href="https://mxcl.github.com/homebrew/">Homebrew</a>
or <a class="uref" href="http://www.macports.org">MacPorts</a> can easily provide it.
</p>

</div>
</div>
<div class="chapter-level-extent" id="DOS">
<h2 class="chapter">2 DOS</h2>

<p>Using a cross-compiler is preferred for various reasons.
<a class="url" href="http://www.delorie.com/howto/djgpp/linux-x-djgpp.html">http://www.delorie.com/howto/djgpp/linux-x-djgpp.html</a>
</p>

</div>
<div class="chapter-level-extent" id="OS_002f2">
<h2 class="chapter">3 OS/2</h2>

<p>For information about compiling FFmpeg on OS/2 see
<a class="url" href="http://www.edm2.com/index.php/FFmpeg">http://www.edm2.com/index.php/FFmpeg</a>.
</p>

</div>
<div class="chapter-level-extent" id="Windows">
<h2 class="chapter">4 Windows</h2>

<ul class="mini-toc">
<li><a href="#Native-Windows-compilation-using-MinGW-or-MinGW_002dw64" accesskey="1">Native Windows compilation using MinGW or MinGW-w64</a></li>
<li><a href="#Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows" accesskey="2">Microsoft Visual C++ or Intel C++ Compiler for Windows</a></li>
<li><a href="#Cross-compilation-for-Windows-with-Linux-1" accesskey="3">Cross compilation for Windows with Linux</a></li>
<li><a href="#Compilation-under-Cygwin" accesskey="4">Compilation under Cygwin</a></li>
<li><a href="#Crosscompilation-for-Windows-under-Cygwin" accesskey="5">Crosscompilation for Windows under Cygwin</a></li>
</ul>
<div class="section-level-extent" id="Native-Windows-compilation-using-MinGW-or-MinGW_002dw64">
<h3 class="section">4.1 Native Windows compilation using MinGW or MinGW-w64</h3>

<p>FFmpeg can be built to run natively on Windows using the MinGW-w64
toolchain. Install the latest versions of MSYS2 and MinGW-w64 from
<a class="url" href="http://msys2.github.io/">http://msys2.github.io/</a> and/or <a class="url" href="http://mingw-w64.sourceforge.net/">http://mingw-w64.sourceforge.net/</a>.
You can find detailed installation instructions in the download section and
the FAQ.
</p>
<p>Notes:
</p>
<ul class="itemize mark-bullet">
<li>Building for the MSYS environment is discouraged, MSYS2 provides a full
MinGW-w64 environment through <samp class="file">mingw64_shell.bat</samp> or
<samp class="file">mingw32_shell.bat</samp> that should be used instead of the environment
provided by <samp class="file">msys2_shell.bat</samp>.

</li><li>Building using MSYS2 can be sped up by disabling implicit rules in the
Makefile by calling <code class="code">make -r</code> instead of plain <code class="code">make</code>. This
speed up is close to non-existent for normal one-off builds and is only
noticeable when running make for a second time (for example during
<code class="code">make install</code>).

</li><li>In order to compile FFplay, you must have the MinGW development library
of <a class="uref" href="http://www.libsdl.org/">SDL</a> and <code class="code">pkg-config</code> installed.

</li><li>By using <code class="code">./configure --enable-shared</code> when configuring FFmpeg,
you can build the FFmpeg libraries (e.g. libavutil, libavcodec,
libavformat) as DLLs.

</li></ul>

<ul class="mini-toc">
<li><a href="#Native-Windows-compilation-using-MSYS2" accesskey="1">Native Windows compilation using MSYS2</a></li>
</ul>
<div class="subsection-level-extent" id="Native-Windows-compilation-using-MSYS2">
<h4 class="subsection">4.1.1 Native Windows compilation using MSYS2</h4>

<p>The MSYS2 MinGW-w64 environment provides ready to use toolchains and dependencies
through <code class="command">pacman</code>.
</p>
<p>Make sure to use <samp class="file">mingw64_shell.bat</samp> or <samp class="file">mingw32_shell.bat</samp> to have
the correct MinGW-w64 environment. The default install provides shortcuts to
them under <code class="command">MinGW-w64 Win64 Shell</code> and <code class="command">MinGW-w64 Win32 Shell</code>.
</p>
<div class="example">
<pre class="example-preformatted"># normal msys2 packages
pacman -S make pkgconf diffutils

# mingw-w64 packages and toolchains
pacman -S mingw-w64-x86_64-nasm mingw-w64-x86_64-gcc mingw-w64-x86_64-SDL2
</pre></div>

<p>To target 32 bits replace <code class="code">x86_64</code> with <code class="code">i686</code> in the command above.
</p>
</div>
</div>
<div class="section-level-extent" id="Microsoft-Visual-C_002b_002b-or-Intel-C_002b_002b-Compiler-for-Windows">
<h3 class="section">4.2 Microsoft Visual C++ or Intel C++ Compiler for Windows</h3>

<p>FFmpeg can be built with MSVC 2013 or later.
</p>
<p>You will need the following prerequisites:
</p>
<ul class="itemize mark-bullet">
<li><a class="uref" href="http://msys2.github.io/">MSYS2</a>
</li><li><a class="uref" href="http://www.nasm.us/">NASM</a>
(Also available via MSYS2&rsquo;s package manager.)
</li></ul>

<p>To set up a proper environment in MSYS2, you need to run <code class="code">msys_shell.bat</code> from
the Visual Studio or Intel Compiler command prompt.
</p>
<p>Place <code class="code">yasm.exe</code> somewhere in your <code class="code">PATH</code>.
</p>
<p>Next, make sure any other headers and libs you want to use, such as zlib, are
located in a spot that the compiler can see. Do so by modifying the <code class="code">LIB</code>
and <code class="code">INCLUDE</code> environment variables to include the <strong class="strong">Windows-style</strong>
paths to these directories. Alternatively, you can try to use the
<code class="code">--extra-cflags</code>/<code class="code">--extra-ldflags</code> configure options.
</p>
<p>Finally, run:
</p>
<div class="example">
<pre class="example-preformatted">For MSVC:
./configure --toolchain=msvc

For ICL:
./configure --toolchain=icl

make
make install
</pre></div>

<p>If you wish to compile shared libraries, add <code class="code">--enable-shared</code> to your
configure options. Note that due to the way MSVC and ICL handle DLL imports and
exports, you cannot compile static and shared libraries at the same time, and
enabling shared libraries will automatically disable the static ones.
</p>
<p>Notes:
</p>
<ul class="itemize mark-bullet">
<li>If you wish to build with zlib support, you will have to grab a compatible
zlib binary from somewhere, with an MSVC import lib, or if you wish to link
statically, you can follow the instructions below to build a compatible
<code class="code">zlib.lib</code> with MSVC. Regardless of which method you use, you must still
follow step 3, or compilation will fail.
<ol class="enumerate">
<li> Grab the <a class="uref" href="http://zlib.net/">zlib sources</a>.
</li><li> Edit <code class="code">win32/Makefile.msc</code> so that it uses -MT instead of -MD, since
this is how FFmpeg is built as well.
</li><li> Edit <code class="code">zconf.h</code> and remove its inclusion of <code class="code">unistd.h</code>. This gets
erroneously included when building FFmpeg.
</li><li> Run <code class="code">nmake -f win32/Makefile.msc</code>.
</li><li> Move <code class="code">zlib.lib</code>, <code class="code">zconf.h</code>, and <code class="code">zlib.h</code> to somewhere MSVC
can see.
</li></ol>

</li><li>FFmpeg has been tested with the following on i686 and x86_64:
<ul class="itemize mark-bullet">
<li>Visual Studio 2013 Pro and Express
</li><li>Intel Composer XE 2013
</li><li>Intel Composer XE 2013 SP1
</li></ul>
<p>Anything else is not officially supported.
</p>
</li></ul>

<ul class="mini-toc">
<li><a href="#Linking-to-FFmpeg-with-Microsoft-Visual-C_002b_002b" accesskey="1">Linking to FFmpeg with Microsoft Visual C++</a></li>
</ul>
<div class="subsection-level-extent" id="Linking-to-FFmpeg-with-Microsoft-Visual-C_002b_002b">
<h4 class="subsection">4.2.1 Linking to FFmpeg with Microsoft Visual C++</h4>

<p>If you plan to link with MSVC-built static libraries, you will need
to make sure you have <code class="code">Runtime Library</code> set to
<code class="code">Multi-threaded (/MT)</code> in your project&rsquo;s settings.
</p>
<p>You will need to define <code class="code">inline</code> to something MSVC understands:
</p><div class="example">
<pre class="example-preformatted">#define inline __inline
</pre></div>

<p>Also note, that as stated in <strong class="strong">Microsoft Visual C++</strong>, you will need
an MSVC-compatible <a class="uref" href="http://code.google.com/p/msinttypes/">inttypes.h</a>.
</p>
<p>If you plan on using import libraries created by dlltool, you must
set <code class="code">References</code> to <code class="code">No (/OPT:NOREF)</code> under the linker optimization
settings, otherwise the resulting binaries will fail during runtime.
This is not required when using import libraries generated by <code class="code">lib.exe</code>.
This issue is reported upstream at
<a class="url" href="http://sourceware.org/bugzilla/show_bug.cgi?id=12633">http://sourceware.org/bugzilla/show_bug.cgi?id=12633</a>.
</p>
<p>To create import libraries that work with the <code class="code">/OPT:REF</code> option
(which is enabled by default in Release mode), follow these steps:
</p>
<ol class="enumerate">
<li> Open the <em class="emph">Visual Studio Command Prompt</em>.

<p>Alternatively, in a normal command line prompt, call <samp class="file">vcvars32.bat</samp>
which sets up the environment variables for the Visual C++ tools
(the standard location for this file is something like
<samp class="file">C:\Program Files (x86_\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat</samp>).
</p>
</li><li> Enter the <samp class="file">bin</samp> directory where the created LIB and DLL files
are stored.

</li><li> Generate new import libraries with <code class="command">lib.exe</code>:

<div class="example">
<pre class="example-preformatted">lib /machine:i386 /def:..\lib\foo-version.def  /out:foo.lib
</pre></div>

<p>Replace <code class="code">foo-version</code> and <code class="code">foo</code> with the respective library names.
</p>
</li></ol>

<a class="anchor" id="Cross-compilation-for-Windows-with-Linux"></a></div>
</div>
<div class="section-level-extent" id="Cross-compilation-for-Windows-with-Linux-1">
<h3 class="section">4.3 Cross compilation for Windows with Linux</h3>

<p>You must use the MinGW cross compilation tools available at
<a class="url" href="http://www.mingw.org/">http://www.mingw.org/</a>.
</p>
<p>Then configure FFmpeg with the following options:
</p><div class="example">
<pre class="example-preformatted">./configure --target-os=mingw32 --cross-prefix=i386-mingw32msvc-
</pre></div>
<p>(you can change the cross-prefix according to the prefix chosen for the
MinGW tools).
</p>
<p>Then you can easily test FFmpeg with <a class="uref" href="http://www.winehq.com/">Wine</a>.
</p>
</div>
<div class="section-level-extent" id="Compilation-under-Cygwin">
<h3 class="section">4.4 Compilation under Cygwin</h3>

<p>Please use Cygwin 1.7.x as the obsolete 1.5.x Cygwin versions lack
llrint() in its C library.
</p>
<p>Install your Cygwin with all the &quot;Base&quot; packages, plus the
following &quot;Devel&quot; ones:
</p><div class="example">
<pre class="example-preformatted">binutils, gcc4-core, make, git, mingw-runtime, texinfo
</pre></div>

<p>In order to run FATE you will also need the following &quot;Utils&quot; packages:
</p><div class="example">
<pre class="example-preformatted">diffutils
</pre></div>

<p>If you want to build FFmpeg with additional libraries, download Cygwin
&quot;Devel&quot; packages for Ogg and Vorbis from any Cygwin packages repository:
</p><div class="example">
<pre class="example-preformatted">libogg-devel, libvorbis-devel
</pre></div>

<p>These library packages are only available from
<a class="uref" href="http://sourceware.org/cygwinports/">Cygwin Ports</a>:
</p>
<div class="example">
<pre class="example-preformatted">yasm, libSDL-devel, libgsm-devel, libmp3lame-devel,
speex-devel, libtheora-devel, libxvidcore-devel
</pre></div>

<p>The recommendation for x264 is to build it from source, as it evolves too
quickly for Cygwin Ports to be up to date.
</p>
</div>
<div class="section-level-extent" id="Crosscompilation-for-Windows-under-Cygwin">
<h3 class="section">4.5 Crosscompilation for Windows under Cygwin</h3>

<p>With Cygwin you can create Windows binaries that do not need the cygwin1.dll.
</p>
<p>Just install your Cygwin as explained before, plus these additional
&quot;Devel&quot; packages:
</p><div class="example">
<pre class="example-preformatted">gcc-mingw-core, mingw-runtime, mingw-zlib
</pre></div>

<p>and add some special flags to your configure invocation.
</p>
<p>For a static build run
</p><div class="example">
<pre class="example-preformatted">./configure --target-os=mingw32 --extra-cflags=-mno-cygwin --extra-libs=-mno-cygwin
</pre></div>

<p>and for a build with shared libraries
</p><div class="example">
<pre class="example-preformatted">./configure --target-os=mingw32 --enable-shared --disable-static --extra-cflags=-mno-cygwin --extra-libs=-mno-cygwin
</pre></div>

</div>
</div>
</div>
      <p style="font-size: small;">
        This document was generated using <a class="uref" href="https://www.gnu.org/software/texinfo/"><em class="emph">makeinfo</em></a>.
      </p>
    </div>
  </body>
</html>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 INDX( 	 ��a          (   �  �         �g                 ��    h X     ��    �������.tQ��ko���ko��� �      $�               f f p l a y . h t m l ��    x b     ��    M:�����,uQ��ko���ko��� p      `b               f f p r o b e - a l l . h t m l       ��    p Z     ��    ������.tQ��ko���ko��� �      ��               f f p r o b e . h t m l       ��    p Z     ��    �������,uQ��&Io���&Io��� �     F�              g e n e r a l . h t m l      ��    p ^     ��    �������,uQ��&Io���&Io��� p      ?d               g i t - h o w t o . h t m l   ��    p `     ��    t�����,uQ��&Io���&Io���       Y               l i b a v c o d e c . h t m l ��    x b     ��    7������,uQ���po����po���       �
               l i b a v d e v i c e . h t m l       ��    x b     ��    Ar�����,uQ���po����po���       "               l i b a v f i l t e r . h t m l       ��    x b     ��    5������,uQ���po�� �po���       @               l i b a v f o r m a t . h t m l       ��    p ^     ��    �������,uQ��Зo���Зo���       3               l i b a v u t i l . h t m l   ��    x f     ��    �J�����,uQ��Зo���Зo���       �               l i b s w r e s a m p l e . h t m l   ��    p `     ��    �������,uQ���o���Зo���       3               l i b s w s c a l e . h t m l ��    � l     ��    mI�����,uQ���o����o��� �      �p               m a i l i n  - l i s t - f a q . h t m l     ��    h R     ��    ƾ�����,uQ���o����o��� 0      �(               n u t . h t m l       ��    p \     ��    ������,uQ���o����o��� P      �M               p l a t f o r m . h t m l      �    p \     ��    �������S|Q���o����o���        �               s t y l e . m i n . c s s     �    p \     ��    ������ ):F���o����o��� 0     �#              U V N B a n h M i . T T F                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        